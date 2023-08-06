#
# Copyright The NOMAD Authors.
#
# This file is part of NOMAD.
# See https://nomad-lab.eu for further info.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
import numpy as np
import logging
import xarray
import json
import re

from nomad.units import ureg
from nomad.parsing.parser import FairdiParser
from nomad.parsing.file_parser import FileParser

from .metainfo import m_env
from nomad.datamodel.metainfo.common_dft import Run, Method, System, Workflow,\
    SingleConfigurationCalculation, EnergyContribution, StressTensorContribution,\
    AtomStressContribution, XCFunctionals
from fhivibesparser.metainfo.fhi_vibes import x_fhi_vibes_section_attributes,\
    x_fhi_vibes_section_metadata, x_fhi_vibes_section_atoms, x_fhi_vibes_section_MD,\
    x_fhi_vibes_section_calculator, x_fhi_vibes_section_calculator_parameters,\
    x_fhi_vibes_section_vibes, x_fhi_vibes_section_relaxation,\
    x_fhi_vibes_section_relaxation_kwargs, x_fhi_vibes_section_settings,\
    x_fhi_vibes_section_phonopy


class XarrayParser(FileParser):
    def __init__(self):
        super().__init__()
        self.re_index = re.compile(r'(.+?)\[(\d+)\]')
        self._raw_metadata = dict()

    @property
    def dataset(self):
        if self._file_handler is None:
            try:
                self._file_handler = xarray.open_dataset(self.mainfile)
                self._raw_metadata = json.loads(self._file_handler.attrs.get('raw_metadata', '{}'))
            except Exception:
                self.logger.error('Error reading trajectory file.')
                pass

        return self._file_handler

    def parse(self, key):
        key = key.strip('/')
        val = self.dataset
        for section in key.split('/'):
            indexed = re.match(self.re_index, section)
            if indexed:
                section = indexed.group(1)
                index = indexed.group(2)
            if section == 'raw_metadata':
                val = self._raw_metadata
            elif section == 'attrs':
                val = self.dataset.attrs
            else:
                val = val.get(section)
            try:
                val = val[int(index)] if indexed else val
            except Exception:
                val = None
            if val is None:
                break
        if isinstance(val, xarray.DataArray):
            val = np.array(val, dtype=val.dtype)

        self._results[key] = val


class FHIVibesParser(FairdiParser):
    def __init__(self):
        super().__init__(
            name='parsers/fhi-vibes', code_name='FHI-vibes',
            code_homepage='https://vibes.fhi-berlin.mpg.de/',
            mainfile_name_re=(r'^.*\.(nc)$'), mainfile_mime_re=r'(application/x-hdf)',
            mainfile_binary_header_re=br'^\x89HDF')

        self.parser = XarrayParser()
        self._metainfo_env = m_env

        self._units = {
            'volume': ureg.angstrom ** 3, 'displacements': ureg.angstrom, 'velocities': ureg.angstrom / ureg.fs,
            'momenta': ureg.eV * ureg.fs / ureg.angstrom, 'force_constants': ureg.eV / ureg.angstrom ** 2,
            'forces_harmonic': ureg.eV / ureg.angstrom, 'forces': ureg.eV / ureg.angstrom, 'stress': ureg.eV / ureg.angstrom ** 3,
            'energy_potential_harmonic': ureg.eV, 'sigma_per_sample': None,
            'pressure': ureg.eV / ureg.angstrom ** 3, 'temperature': ureg.K, 'pressure_kinetic': ureg.eV / ureg.angstrom ** 3,
            'pressure_potential': ureg.eV / ureg.angstrom ** 3, 'aims_uuid': None, 'energy': ureg.eV,
            'heat_flux': ureg.amu / ureg.fs ** 3, 'heat_flux_harmonic': ureg.amu / ureg.fs ** 3,
            'heat_flux_0_harmonic': ureg.amu / ureg.fs ** 3, 'mass': ureg.amu, 'length': ureg.angstrom, 'time': ureg.fs}

    @property
    def n_frames(self):
        if self.calculation_type == 'phonon':
            return 1
        return len(self.parser.get('positions'))

    def parse_configurations(self):

        def parse_system(n_frame):
            sec_system = sec_run.m_create(System)
            sec_system.atom_labels = self.parser.get('attrs').get('symbols')
            sec_system.atom_positions = self.parser.get('positions', unit=self._units.get('length'))[n_frame]
            sec_system.lattice_vectors = self.parser.get('cell', unit=self._units.get('length'))[n_frame]
            sec_system.configuration_periodic_dimensions = self.parser.get('attrs/raw_metadata/atoms/pbc')
            velocities = self.parser.get('velocities', unit=self._units.get('velocities'))
            if velocities is not None:
                sec_system.atom_velocities = velocities[n_frame]
            return sec_system

        def parse_scc(n_frame):
            sec_scc = sec_run.m_create(SingleConfigurationCalculation)

            if self.calculation_type == 'molecular_dynamics':
                sec_scc.time_step = n_frame
                # TODO metainfo should be in common
                sec_scc.x_fhi_vibes_MD_time = n_frame * timestep

            for key in ['kinetic', 'potential']:
                val = self.parser.get('energy_%s' % key, unit=self._units.get('energy'))
                if val is not None:
                    sec_energy = sec_scc.m_create(EnergyContribution)
                    sec_energy.energy_contribution_kind = key
                    sec_energy.energy_contribution_value = val[n_frame]

                val = self.parser.get('stress_%s' % key, unit=self._units.get('stress'))
                if val is not None:
                    sec_stress = sec_scc.m_create(StressTensorContribution)
                    sec_stress.stress_tensor_contribution_kind = key
                    sec_stress.stress_tensor_contribution_value = val[n_frame]

                val = self.parser.get('stresses_%s' % key, unit=self._units.get('stress'))
                if val is not None:
                    sec_atom_stress = sec_scc.m_create(AtomStressContribution)
                    sec_atom_stress.atom_stress_contribution_kind = key
                    sec_atom_stress.atom_stress_contribution_value = val[n_frame]

            calculation_quantities = [
                'volume', 'displacements', 'momenta', 'forces_harmonic',
                'forces', 'stress', 'energy_potential_harmonic', 'sigma_per_sample',
                'pressure', 'temperature', 'pressure_kinetic', 'pressure_potential', 'aims_uuid',
                'heat_flux', 'heat_flux_harmonic', 'heat_flux_0_harmonic']
            for key in calculation_quantities:
                val = self.parser.get(key, unit=self._units.get(key, None))
                if val is None:
                    continue

                # TODO figure out what shape of output fc
                if key.startswith('force_constants'):
                    continue
                if key.startswith('forces'):
                    key = 'atom_%s' % key
                elif key == 'stress':
                    key = 'stress_tensor'

                if key in ['temperature', 'pressure', 'atom_forces', 'stress_tensor']:
                    setattr(sec_scc, key, val[n_frame])
                else:
                    setattr(sec_scc, 'x_fhi_vibes_%s' % key, val[n_frame])

            return sec_scc

        sec_atrr = self.archive.section_run[-1].section_method[-1].x_fhi_vibes_section_attributes[-1]
        timestep = sec_atrr.x_fhi_vibes_attributes_timestep
        for n_frame in range(self.n_frames):
            if self.calculation_type == 'single_point':
                sec_run = self.archive.section_run[n_frame]
                # we can only do this for single point where we have separate section_runs
                # for each frame
                sec_run.raw_id = self.parser.get('aims_uuid')[n_frame]
            else:
                # TODO aims_uuid is in x_fhi_vibes_aims_uuid, this should be changed
                sec_run = self.archive.section_run[-1]

            sec_system = parse_system(n_frame)
            sec_scc = parse_scc(n_frame)
            sec_scc.single_configuration_calculation_to_system_ref = sec_system
            sec_scc.single_configuration_to_calculation_method_ref = sec_run.section_method[-1]

        # force constants
        for key in ['force_constants', 'force_constants_remapped']:
            val = self.parser.get(key, unit=self._units.get('force_constants'))
            if val is not None:
                setattr(sec_scc, 'x_fhi_vibes_%s' % key, val)

    def parse_method(self, n_run):
        def parse_xc_functional():
            # TODO This is a temporary fix to circumvent the normalization tests failure
            # due to missing xc functional information but this should be fetched directly
            # from the underlying calculation
            xc_type_map = {'PW': 'C'}
            calculator_parameters = self.parser.get(
                'attrs/raw_metadata/calculator/calculator_parameters', {})
            xc_functional = calculator_parameters.get('xc', '').upper()
            xc_functional_info = re.match(r'(\w+)\S+?((?:LDA|GGA|MGGA|HYB_GGA|HYB_MGGA))', xc_functional)
            if xc_functional_info:
                xc_name = xc_functional_info.group(1)
                xc_type = xc_type_map.get(xc_name, None)
                if xc_type is None:
                    self.logger.error('Cannot resolve XC functional.')
                    return
                sec_xc_functional = sec_method.m_create(XCFunctionals)
                sec_xc_functional.XC_functional_name = '%s_%s_%s' % (
                    xc_functional_info.group(2), xc_type, xc_functional_info.group(1))

        def parse_atoms(section, atoms):
            for key, val in atoms.items():
                # why is the formatting of symbols and masses different for atoms?
                if key in ['symbols', 'masses']:
                    if isinstance(val[0], list):
                        val_flattened = []
                        for val_i in val:
                            val_flattened.extend([val_i[1]] * val_i[0])
                        val = val_flattened
                    if key == 'masses':
                        val = val * self._units.get('mass')
                elif key in ['positions', 'cell']:
                    val = val * self._units.get('length')
                elif key == 'velocities':
                    val = val * self._units.get('length') / self._units.get('time')
                setattr(section, 'x_fhi_vibes_atoms_%s' % key, val)

        def parse_metadata():
            metadata = self.parser.get('attrs/raw_metadata')
            sec_metadata = sec_attrs.m_create(x_fhi_vibes_section_metadata)
            for key, val in metadata.items():
                if key == 'MD':
                    sec_md = sec_metadata.m_create(x_fhi_vibes_section_MD)
                    for md_key in val.keys():
                        setattr(
                            sec_md, 'x_fhi_vibes_MD_%s' % md_key.replace('-', '_'),
                            val[md_key])
                elif key == 'relaxation':
                    sec_relaxation = sec_metadata.m_create(x_fhi_vibes_section_relaxation)
                    for relaxation_key in val.keys():
                        if relaxation_key == 'kwargs':
                            sec_kwargs = sec_relaxation.m_create(x_fhi_vibes_section_relaxation_kwargs)
                            for kwargs_key in val['kwargs']:
                                setattr(
                                    sec_kwargs, 'x_fhi_vibes_relaxation_kwargs_%s' % kwargs_key,
                                    val['kwargs'][kwargs_key])
                        else:
                            setattr(
                                sec_relaxation, 'x_fhi_vibes_relaxation_%s' % relaxation_key.replace('-', '_'),
                                val[relaxation_key])
                elif key == 'Phonopy':
                    sec_phonopy = sec_metadata.m_create(x_fhi_vibes_section_phonopy)
                    for phonopy_key in val.keys():
                        if phonopy_key == 'primitive':
                            sec_primitive = sec_phonopy.m_create(x_fhi_vibes_section_atoms)
                            parse_atoms(sec_primitive, val['primitive'])
                        else:
                            setattr(sec_phonopy, 'x_fhi_vibes_phonopy_%s' % phonopy_key, val[phonopy_key])
                elif key == 'calculator':
                    sec_calculator = sec_metadata.m_create(x_fhi_vibes_section_calculator)
                    sec_calculator.x_fhi_vibes_calculator = metadata['calculator']['calculator']
                    sec_calculator_parameters = sec_calculator.m_create(x_fhi_vibes_section_calculator_parameters)
                    for calc_key in val['calculator_parameters'].keys():
                        if calc_key == 'use_pimd_wrapper':
                            val['calculator_parameters'][calc_key] = str(val['calculator_parameters'][calc_key])
                        setattr(
                            sec_calculator_parameters, 'x_fhi_vibes_calculator_parameters_%s' % calc_key,
                            val['calculator_parameters'][calc_key])
                elif key in ['atoms', 'primitive', 'supercell']:
                    sec_atoms = sec_metadata.m_create(x_fhi_vibes_section_atoms)
                    sec_atoms.x_fhi_vibes_atoms_kind = key
                    parse_atoms(sec_atoms, val)
                elif key == 'vibes':
                    sec_vibes = sec_metadata.m_create(x_fhi_vibes_section_vibes)
                    for vibes_key in val.keys():
                        setattr(sec_vibes, 'x_fhi_vibes_%s' % vibes_key, val[vibes_key])
                elif key == 'settings':
                    sec_settings = sec_metadata.m_create(x_fhi_vibes_section_settings)
                    for settings_key in val.keys():
                        setattr(sec_settings, 'x_fhi_vibes_settings_%s' % settings_key, val[settings_key])
                else:
                    setattr(sec_metadata, key, val)

        sec_method = self.archive.section_run[n_run].m_create(Method)

        parse_xc_functional()

        sec_attrs = sec_method.m_create(x_fhi_vibes_section_attributes)

        time_units = {'ns': ureg.ns, 'fs': ureg.fs, 'ps': ureg.ps}
        attrs = self.parser.get('attrs')
        for key, val in attrs.items():
            if key == 'raw_metadata':
                parse_metadata()
            elif key.startswith('atoms_'):
                sec_atoms = sec_attrs.m_create(x_fhi_vibes_section_atoms)
                sec_atoms.x_fhi_vibes_atoms_kind = key
                atoms = json.loads(val)
                sec_atoms.x_fhi_vibes_atoms_natoms = len(atoms['positions'])
                parse_atoms(sec_atoms, atoms)
                setattr(sec_attrs, 'x_fhi_vibes_attributes_number_of_%s' % key, len(atoms['positions']))
            else:
                if key == 'masses':
                    val = val * self._units.get('mass')
                elif key == 'timestep':
                    val = val * time_units.get(attrs.get('time_unit').lower(), self._units.get('time'))
                setattr(sec_attrs, 'x_fhi_vibes_attributes_%s' % key, val)

        # we need this information for force constants
        n_atoms_supercell = sec_attrs.x_fhi_vibes_attributes_number_of_atoms_supercell
        if n_atoms_supercell:
            sec_attrs.x_fhi_vibes_attributes_force_constants_remapped_size = n_atoms_supercell * 3

    def init_parser(self):
        self.parser.mainfile = self.filepath
        self.parser.logger = self.logger

    def parse(self, filepath, archive, logger):
        self.filepath = os.path.abspath(filepath)
        self.archive = archive
        self.logger = logger if logger is not None else logging.getLogger(__name__)
        self.maindir = os.path.dirname(self.filepath)

        self.init_parser()

        metadata = self.parser.get('attrs/raw_metadata')

        if 'MD' in metadata:
            self.calculation_type = 'molecular_dynamics'
        elif 'relaxation' in metadata:
            self.calculation_type = 'geometry_optimization'
        elif 'Phonopy' in metadata:
            self.calculation_type = 'phonon'
        else:
            # the single point workflow in vibes means multiple separate calculations on
            # on same material (stoichiometry, number of atoms) but may differ on
            # on structure (lattice, positions). This means we need to create separate
            # section runs
            self.calculation_type = 'single_point'

        if self.calculation_type == 'single_point':
            for _ in range(self.n_frames):
                self.archive.m_create(Run)
        else:
            self.archive.m_create(Run)

        for n_run, sec_run in enumerate(self.archive.section_run):
            sec_run.program_name = 'FHI-vibes'
            sec_run.program_version = metadata['vibes']['version']

            if metadata['calculator']['calculator'].lower() == 'aims':
                sec_run.program_basis_set_type = 'numeric AOs'

            self.parse_method(n_run)

        # TODO For single_point, we can only have workflow for one vibes single point frame
        # as workflow is not repeating in metainfo.
        # To resolve this, we can redefine single_point workflow to be consistent with
        # the idea of vibes single point but I do not like it.
        sec_workflow = self.archive.m_create(Workflow)
        sec_workflow.workflow_type = self.calculation_type
        sec_workflow.calculator = metadata['calculator']['calculator']

        self.parse_configurations()
