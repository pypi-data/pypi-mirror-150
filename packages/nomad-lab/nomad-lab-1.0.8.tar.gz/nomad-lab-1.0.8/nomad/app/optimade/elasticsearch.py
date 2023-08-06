from typing import Optional, Tuple, List, Union, Dict, Set, Any
from elasticsearch_dsl import Q
from fastapi import HTTPException
from pydantic import create_model
from datetime import datetime
import numpy as np

from optimade.filterparser import LarkParser
from optimade.server.entry_collections import EntryCollection
from optimade.server.query_params import EntryListingQueryParams, SingleEntryQueryParams
from optimade.server.exceptions import BadRequest
from optimade.server.mappers import StructureMapper
from optimade.models import StructureResource, StructureResourceAttributes
from optimade.models.utils import OptimadeField, SupportLevel
from optimade.server.schemas import ENTRY_INFO_SCHEMAS

from nomad.units import ureg
from nomad.search import search
from nomad.app.v1.models import MetadataPagination, MetadataRequired
from nomad import datamodel, files, utils, metainfo, config
from nomad.normalizing.optimade import (
    optimade_chemical_formula_reduced, optimade_chemical_formula_anonymous,
    optimade_chemical_formula_hill)

from .filterparser import _get_transformer as get_transformer
from .common import provider_specific_fields


logger = utils.get_logger(__name__)
float64 = np.dtype('float64')
int64 = np.dtype('int64')
int32 = np.dtype(np.int32)


class StructureResourceAttributesByAlias(StructureResourceAttributes):
    nmd_entry_page_url: Optional[str] = OptimadeField(
        None,
        alias='_nmd_entry_page_url',
        description='The url for the NOMAD gui entry page for this structure.',
        support=SupportLevel.OPTIONAL)

    nmd_raw_file_download_url: Optional[str] = OptimadeField(
        None,
        alias='_nmd_raw_file_download_url',
        description='The url to download all entry raw files as .zip file.',
        support=SupportLevel.OPTIONAL)

    nmd_archive_url: Optional[str] = OptimadeField(
        None,
        alias='_nmd_archive_url',
        description='The url to the NOMAD archive json of this structure.',
        support=SupportLevel.OPTIONAL)

    def dict(self, *args, **kwargs):
        kwargs['by_alias'] = True
        return super().dict(*args, **kwargs)


def create_nomad_structure_resource_attributes_cls():
    fields: Dict[str, Tuple[type, OptimadeField]] = {}

    for name, search_quantity in provider_specific_fields().items():
        quantity = search_quantity.definition

        pydantic_type: type
        if not quantity.is_scalar:
            pydantic_type = list
        elif quantity.type == int32:
            pydantic_type = int
        elif quantity.type in [str, int, float, bool]:
            if quantity.type == float64:
                pydantic_type = float
            elif quantity.type == int64:
                pydantic_type = int
            else:
                pydantic_type = quantity.type
        elif quantity.type == metainfo.Datetime:
            pydantic_type = datetime
        elif isinstance(quantity.type, metainfo.MEnum):
            pydantic_type = str
        elif isinstance(quantity.type, metainfo.Reference):
            continue
        else:
            raise NotImplementedError('Search quantity type not support in optimade API')

        field = Optional[pydantic_type], OptimadeField(
            None,
            alias=f'_nmd_{name}',
            sortable=False,
            description=quantity.description if quantity.description else 'Not available. Will be added soon.',
            support=SupportLevel.OPTIONAL,
            queryable=SupportLevel.OPTIONAL)

        fields[f'nmd_{name}'] = field

    return create_model(
        'NomadStructureResourceAttributes',
        __base__=StructureResourceAttributesByAlias,
        **fields)


NomadStructureResourceAttributes = create_nomad_structure_resource_attributes_cls()


class NomadStructureResource(StructureResource):
    attributes: NomadStructureResourceAttributes  # type: ignore


ENTRY_INFO_SCHEMAS['structures'] = NomadStructureResource.schema


class StructureCollection(EntryCollection):

    def __init__(self):
        super().__init__(
            resource_cls=NomadStructureResource,
            resource_mapper=StructureMapper,
            transformer=get_transformer(without_prefix=False))

        self.parser = LarkParser(version=(1, 0, 0), variant="default")

        # check aliases do not clash with mongo operators
        self._check_aliases(self.resource_mapper.all_aliases())
        self._check_aliases(self.resource_mapper.all_length_aliases())

    def _base_search_query(self) -> Q:
        return Q('exists', field='optimade.elements') & Q('term', processed=True)

    def __len__(self) -> int:
        # TODO cache
        return search(
            owner='public',
            query=self._base_search_query(),
            pagination=MetadataPagination(page_size=0)).pagination.total

    def count(self, **kwargs) -> int:
        # This seams solely mongodb specific
        raise NotImplementedError()

    def find(
            self,
            params: Union[EntryListingQueryParams, SingleEntryQueryParams]) \
            -> Tuple[List[StructureResource], int, bool, set]:

        criteria = self.handle_query_params(params)
        single_entry = isinstance(params, SingleEntryQueryParams)
        response_fields = criteria.pop("fields")

        results, data_returned, more_data_available = self._run_db_query(
            criteria, single_entry=isinstance(params, SingleEntryQueryParams)
        )

        results = self._es_to_optimade_results(results, response_fields=response_fields)

        if single_entry:
            results = results[0] if results else None

            if data_returned > 1:
                raise HTTPException(
                    status_code=404,
                    detail=f'Instead of a single entry, {data_returned} entries were found')

        exclude_fields = self.all_fields - response_fields

        return (
            results,
            data_returned,
            more_data_available,
            exclude_fields,
        )

    def _check_aliases(self, aliases):
        pass

    def _es_to_optimade_result(
            self, es_result: dict,
            response_fields: Set[str],
            upload_files_cache: Dict[str, files.UploadFiles]) -> StructureResource:

        entry_id, upload_id = es_result['entry_id'], es_result['upload_id']
        upload_files = upload_files_cache.get(upload_id)

        if upload_files is None:
            upload_files = files.UploadFiles.get(upload_id)
            if upload_files is None:
                logger.error('missing upload', upload_id=upload_id)
                return None

            upload_files_cache[upload_id] = upload_files

        try:
            archive_reader = upload_files.read_archive(entry_id)
        except KeyError:
            logger.error('missing archive entry', upload_id=upload_id, entry_id=entry_id)
            return None

        entry_archive_reader = archive_reader[entry_id]
        archive = datamodel.EntryArchive(
            metadata=datamodel.EntryMetadata.m_from_dict(
                entry_archive_reader['metadata'].to_dict())
        )

        # Lazy load results if only if results provider specfic field is requested
        def get_results():
            if not archive.results:
                archive.results = datamodel.Results.m_from_dict(
                    entry_archive_reader['results'].to_dict())
            return archive.results

        attrs = archive.metadata.optimade.m_to_dict()

        attrs['immutable_id'] = entry_id
        attrs['last_modified'] = archive.metadata.upload_create_time

        # TODO this should be removed, once all data is reprocessed with the right normalization
        attrs['chemical_formula_reduced'] = optimade_chemical_formula_reduced(
            attrs['chemical_formula_reduced'])
        attrs['chemical_formula_anonymous'] = optimade_chemical_formula_anonymous(
            attrs['chemical_formula_reduced'])
        attrs['chemical_formula_hill'] = optimade_chemical_formula_hill(
            attrs['chemical_formula_hill'])
        attrs['chemical_formula_descriptive'] = attrs['chemical_formula_hill']
        dimension_types = attrs['dimension_types']
        if isinstance(dimension_types, int):
            attrs['dimension_types'] = [1] * dimension_types + [0] * (3 - dimension_types)
            attrs['nperiodic_dimensions'] = dimension_types
        elif isinstance(dimension_types, list):
            attrs['nperiodic_dimensions'] = sum(dimension_types)

        if response_fields is not None:
            for request_field in response_fields:
                if not request_field.startswith('_nmd_'):
                    continue

                if request_field == '_nmd_archive_url':
                    attrs[request_field] = config.api_url() + f'/archive/{upload_id}/{entry_id}'
                    continue

                if request_field == '_nmd_entry_page_url':
                    attrs[request_field] = config.gui_url(f'entry/id/{upload_id}/{entry_id}')
                    continue

                if request_field == '_nmd_raw_file_download_url':
                    attrs[request_field] = config.api_url() + f'/raw/calc/{upload_id}/{entry_id}'
                    continue

                search_quantity = provider_specific_fields().get(request_field[5:])
                if search_quantity is None:
                    # if unknown properties where provided, we will ignore them as per
                    # optimade spec
                    continue

                try:
                    path = search_quantity.qualified_name.split('.')
                    if path[0] == 'results':
                        get_results()
                    section = archive
                    for segment in path:
                        value = getattr(section, segment)
                        section = value

                    # Empty values are not stored and only the magnitude of
                    # Quantities is stored.
                    if value is not None:
                        if isinstance(value, ureg.Quantity):
                            value = value.magnitude
                        attrs[request_field] = value
                except Exception:
                    # TODO there a few things that can go wrong. Most notable the search
                    # quantity might have a path with repeated sections. This won't be
                    # handled right now.
                    pass

        return self.resource_cls(
            type='structures',
            id=entry_id,
            attributes=attrs,
            relationships=None)

    def _es_to_optimade_results(self, es_results: List[dict], response_fields: Set[str]):
        upload_files_cache: Dict[str, files.UploadFiles] = {}
        optimade_results = []
        try:
            for es_result in es_results:
                optimade_result = self._es_to_optimade_result(
                    es_result, response_fields, upload_files_cache)
                if optimade_result is not None:
                    optimade_results.append(optimade_result)
        finally:
            for upload_files in upload_files_cache.values():
                upload_files.close()

        return optimade_results

    def _run_db_query(self, criteria: Dict[str, Any], single_entry=False):

        sort, order = criteria.get('sort', (('chemical_formula_reduced', 1),))[0]
        sort_quantity = datamodel.OptimadeEntry.m_def.all_quantities.get(sort, None)
        if sort_quantity is None:
            raise BadRequest(detail='Unable to sort on field %s' % sort)
        sort_quantity_a_optimade = sort_quantity.m_get_annotations('optimade')
        if not sort_quantity_a_optimade.sortable:
            raise BadRequest(detail='Unable to sort on field %s' % sort)

        search_query = self._base_search_query()

        filter = criteria.get('filter')
        if filter:
            search_query &= filter

        es_response = search(
            owner='public',
            query=search_query,
            required=MetadataRequired(include=['entry_id', 'upload_id']),
            pagination=MetadataPagination(
                page_size=criteria['limit'],
                page_offset=criteria.get('skip', 0),
                order='asc' if order == 1 else 'desc',
                order_by=f'optimade.{sort}'
            ))

        results = es_response.data

        data_returned = es_response.pagination.total
        more_data_available = data_returned >= criteria.get('skip', 0) + criteria['limit']

        return results, data_returned, more_data_available

    def insert(self, *args, **kwargs):
        # This is used to insert test records during OPT tests. This should never be necessary
        # on our implementation. We just need to implement it, because its marked as
        # @abstractmethod.
        raise NotImplementedError()
