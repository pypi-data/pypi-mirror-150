#
# Copyright The NOMAD Authors.
#
# This file is part of NOMAD. See https://nomad-lab.eu for further info.
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

'''
This module describes all configurable parameters for the nomad python code. The
configuration is used for all executed python code including API, worker, CLI, and other
scripts. To use the configuration in your own scripts or new modules, simply import
this module.

All parameters are structured into objects for two reasons. First, to have
categories. Second, to allow runtime manipulation that is not effected
by python import logic. The categories are choosen along infrastructure components:
``mongo``, ``elastic``, etc.

This module also provides utilities to read the configuration from environment variables
and .yaml files. This is done automatically on import. The precedence is env over .yaml
over defaults.

.. autoclass:: nomad.config.NomadConfig
.. autofunction:: nomad.config.load_config
'''

import logging
import os
import os.path
import yaml
import warnings
from typing import Dict, Any

try:
    from nomad import gitinfo
except ImportError:
    git_root = os.path.join(os.path.dirname(__file__), '..')
    cwd = os.getcwd()
    os.chdir(git_root)
    os.system('./gitinfo.sh')
    os.chdir(cwd)

    from nomad import gitinfo


warnings.filterwarnings('ignore', message='numpy.dtype size changed')
warnings.filterwarnings('ignore', message='numpy.ufunc size changed')


class NomadConfig(dict):
    '''
    A class for configuration categories. It is a dict subclass that uses attributes as
    key/value pairs.
    '''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __getattr__(self, name):
        if name in self:
            return self[name]
        else:
            raise AttributeError("No such attribute: " + name)

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        if name in self:
            del self[name]
        else:
            raise AttributeError("No such attribute: " + name)

    def customize(self, custom_settings: Dict[str, Any]) -> 'NomadConfig':
        '''
        Returns a new NomadConfig object, created by taking a copy of the current config and
        updating it with the settings defined in `custom_settings`. The `custom_settings` dict
        must not contain any new keys (keys not defined in this NomadConfig). If it does,
        an exception will be raised.
        '''
        rv = NomadConfig(**self)
        if custom_settings:
            for k, v in custom_settings.items():
                assert k in rv, f'Invalid setting: {k}'
                rv[k] = v
        return rv


CELERY_WORKER_ROUTING = 'worker'
CELERY_QUEUE_ROUTING = 'queue'

rabbitmq = NomadConfig(
    host='localhost',
    user='rabbitmq',
    password='rabbitmq'
)


def rabbitmq_url():
    return 'pyamqp://%s:%s@%s//' % (rabbitmq.user, rabbitmq.password, rabbitmq.host)


celery = NomadConfig(
    max_memory=64e6,  # 64 GB
    timeout=1800,  # 1/2 h
    acks_late=False,
    routing=CELERY_QUEUE_ROUTING,
    priorities={
        'Upload.process_upload': 5,
        'Upload.delete_upload': 9,
        'Upload.publish_upload': 10
    }
)

fs = NomadConfig(
    tmp='.volumes/fs/tmp',
    staging='.volumes/fs/staging',
    public='.volumes/fs/public',
    local_tmp='/tmp',
    prefix_size=2,
    archive_version_suffix='v1',
    working_directory=os.getcwd()
)

elastic = NomadConfig(
    host='localhost',
    port=9200,
    timeout=60,
    bulk_timeout=600,
    bulk_size=1000,
    entries_per_material_cap=1000,
    entries_index='nomad_entries_v1',
    materials_index='nomad_materials_v1',
)

keycloak = NomadConfig(
    public_server_url=None,
    server_url='https://nomad-lab.eu/fairdi/keycloak/auth/',
    realm_name='fairdi_nomad_prod',
    username='admin',
    password='password',
    client_id='nomad_public',
    client_secret=None,
    oasis=False)

mongo = NomadConfig(
    host='localhost',
    port=27017,
    db_name='nomad_v1'
)

logstash = NomadConfig(
    enabled=False,
    host='localhost',
    tcp_port='5000',
    level=logging.DEBUG
)

services = NomadConfig(
    api_host='localhost',
    api_port=8000,
    api_base_path='/fairdi/nomad/latest',
    api_secret='defaultApiSecret',
    api_chaos=0,
    admin_user_id='00000000-0000-0000-0000-000000000000',
    not_processed_value='not processed',
    unavailable_value='unavailable',
    https=False,
    https_upload=False,
    upload_limit=10,
    force_raw_file_decoding=False,
    download_scan_size=500,
    download_scan_timeout=u'30m'
)

oasis = NomadConfig(
    central_nomad_api_url='https://nomad-lab.eu/prod/v1/api',
    central_nomad_deployment_id='nomad-lab.eu/prod/v1',
    allowed_users=None  # a list of usernames or user account emails
)

tests = NomadConfig(
    default_timeout=30
)


def api_url(ssl: bool = True, api: str = 'api'):
    '''
    Returns the url of the current running nomad API. This is for server-side use.
    This is not the NOMAD url to use as a client, use `nomad.config.client.url` instead.
    '''
    protocol = 'https' if services.https and ssl else 'http'
    host_and_port = services.api_host.strip('/')
    if services.api_port not in [80, 443]:
        host_and_port += ':' + str(services.api_port)
    base_path = services.api_base_path.strip('/')
    return f'{protocol}://{host_and_port}/{base_path}/{api}'


def gui_url(page: str = None):
    base = api_url(True)[:-3]
    if base.endswith('/'):
        base = base[:-1]

    if page is not None:
        return '%s/gui/%s' % (base, page)

    return '%s/gui' % base


def _check_config():
    """Used to check that the current configuration is valid. Should only be
    called once after the final config is loaded.

    Raises:
        AssertionError: if there is a contradiction or invalid values in the
            config file settings.
    """
    # The AFLOW symmetry information is checked once on import
    proto_symmetry_tolerance = normalize.prototype_symmetry_tolerance
    symmetry_tolerance = normalize.symmetry_tolerance
    if proto_symmetry_tolerance != symmetry_tolerance:
        raise AssertionError(
            "The AFLOW prototype information is outdated due to changed tolerance "
            "for symmetry detection. Please update the AFLOW prototype information "
            "by running the CLI command 'nomad admin ops prototype-update "
            "--matches-only'."
        )

    if normalize.springer_db_path and not os.path.exists(normalize.springer_db_path):
        normalize.springer_db_path = None

    if keycloak.public_server_url is None:
        keycloak.public_server_url = keycloak.server_url


mail = NomadConfig(
    enabled=False,
    with_login=False,
    host='',
    port=8995,
    user='',
    password='',
    from_address='support@nomad-lab.eu',
    cc_address='support@nomad-lab.eu'
)

normalize = NomadConfig(
    # The system size limit for running the dimensionality analysis. For very
    # large systems the dimensionality analysis will get too expensive.
    system_classification_with_clusters_threshold=64,
    # Symmetry tolerance controls the precision used by spglib in order to find
    # symmetries. The atoms are allowed to move 1/2*symmetry_tolerance from
    # their symmetry positions in order for spglib to still detect symmetries.
    # The unit is angstroms. The value of 0.1 is used e.g. by Materials Project
    # according to
    # https://pymatgen.org/pymatgen.symmetry.analyzer.html#pymatgen.symmetry.analyzer.SpacegroupAnalyzer
    symmetry_tolerance=0.1,
    # The symmetry tolerance used in aflow prototype matching. Should only be
    # changed before re-running the prototype detection.
    prototype_symmetry_tolerance=0.1,
    # Maximum number of atoms in the single cell of a 2D material for it to be
    # considered valid.
    max_2d_single_cell_size=7,
    # The distance tolerance between atoms for grouping them into the same
    # cluster. Used in detecting system type.
    cluster_threshold=2.5,
    # Defines the "bin size" for rounding cell angles for the material hash
    angle_rounding=float(10.0),  # unit: degree
    # The threshold for a system to be considered "flat". Used e.g. when
    # determining if a 2D structure is purely 2-dimensional to allow extra rigid
    # transformations that are improper in 3D but proper in 2D.
    flat_dim_threshold=0.1,
    # The threshold for point equality in k-space. Unit: 1/m.
    k_space_precision=150e6,
    # The energy threshold for how much a band can be on top or below the fermi
    # level in order to still detect a gap. Unit: Joule.
    band_structure_energy_tolerance=8.01088e-21,  # 0.05 eV
    springer_db_path=os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'normalizing/data/springer.msg'
    )
)

paths = NomadConfig(
    similarity="",
)

client = NomadConfig(
    user='leonard.hofstadter@nomad-fairdi.tests.de',
    password='password',
    url='http://nomad-lab.eu/prod/v1/api'
)

datacite = NomadConfig(
    mds_host='https://mds.datacite.org',
    enabled=False,
    prefix='10.17172',
    user='*',
    password='*'
)

meta = NomadConfig(
    version='1.0.8',
    commit=gitinfo.commit,
    deployment='devel',
    label=None,
    default_domain='dft',
    service='unknown nomad service',
    name='novel materials discovery (NOMAD)',
    description='A FAIR data sharing platform for materials science data',
    homepage='https://nomad-lab.eu',
    source_url='https://gitlab.mpcdf.mpg.de/nomad-lab/nomad-FAIR',
    maintainer_email='markus.scheidgen@physik.hu-berlin.de',
    deployment_id='nomad-lab.eu/prod/v1',
    beta=None
)

gitlab = NomadConfig(
    private_token='not set'
)

reprocess = NomadConfig(
    # Configures standard behaviour when reprocessing.
    # Note, the settings only matter for published uploads and entries. For uploads in
    # staging, we always reparse, add newfound entries, and delete unmatched entries.
    rematch_published=True,
    reprocess_existing_entries=True,
    use_original_parser=False,
    add_matched_entries_to_published=True,
    delete_unmatched_published_entries=False,
    index_invidiual_entries=False
)

process = NomadConfig(
    index_materials=True,
    reuse_parser=True,
    metadata_file_name='nomad',
    metadata_file_extensions=('json', 'yaml', 'yml')
)

bundle_import = NomadConfig(
    # Basic settings
    allow_bundles_from_oasis=True,  # If oasis admins can "push" bundles to this NOMAD deployment
    allow_unpublished_bundles_from_oasis=False,  # If oasis admins can "push" bundles of unpublished uploads
    required_nomad_version='1.0.0',  # Minimum  nomad version of bundles required for import

    default_settings=NomadConfig(
        # Default settings for the import_bundle process.
        # Note, admins, and only admins, can override these settings when importing a bundle.
        # This means that if oasis admins pushes bundles to this NOMAD deployment, these
        # default settings will be applied.
        include_raw_files=True,
        include_archive_files=False,
        include_datasets=True,
        include_bundle_info=True,  # Keeps the bundle_info.json file (not necessary but nice to have)
        keep_original_timestamps=False,  # If all time stamps (create time, publish time etc) should be imported from the bundle
        set_from_oasis=True,  # If the from_oasis flag and oasis_deployment_id should be set
        delete_upload_on_fail=False,  # If False, it is just removed from the ES index on failure
        delete_bundle_when_done=True,  # Deletes the source bundle when done (regardless of success)
        also_delete_bundle_parent_folder=True,  # Also deletes the parent folder, if it is empty.
        trigger_processing=True,  # If the upload should be processed when the import is done.

        # When importing with trigger_processing=True, the settings below control the
        # initial processing behaviour (see the config for `reprocess` for more info).
        rematch_published=True,
        reprocess_existing_entries=True,
        use_original_parser=False,
        add_matched_entries_to_published=True,
        delete_unmatched_published_entries=False
    )
)

archive = NomadConfig(
    block_size=256 * 1024,
    read_buffer_size=256 * 1024,  # GPFS needs at least 256K to achieve decent performance
    max_process_number=20,  # maximum number of processes can be assigned to process archive query
    min_entires_per_process=20  # minimum number of entries per process
)

auxfile_cutoff = 100
parser_matching_size = 150 * 80  # 150 lines of 80 ASCII characters per line
console_log_level = logging.WARNING
max_upload_size = 32 * (1024 ** 3)
raw_file_strip_cutoff = 1000
max_entry_download = 500000
encyclopedia_base = "https://nomad-lab.eu/prod/rae/encyclopedia/#"
aitoolkit_enabled = False
use_empty_parsers = False


def normalize_loglevel(value, default_level=logging.INFO):
    plain_value = value
    if plain_value is None:
        return default_level
    else:
        try:
            return int(plain_value)
        except ValueError:
            return getattr(logging, plain_value)


_transformations = {
    'console_log_level': normalize_loglevel,
    'logstash_level': normalize_loglevel
}


# use std python logger, since logging is not configured while loading configuration
logger = logging.getLogger(__name__)


def _apply(key, value, raise_error: bool = True) -> None:
    '''
    Changes the config according to given key and value. The first part of a key
    (with ``_`` as a separator) is interpreted as a group of settings. E.g. ``fs_staging``
    leading to ``config.fs.staging``.
    '''
    full_key = key
    try:
        group_key, config_key = full_key.split('_', 1)
    except Exception:
        if raise_error:
            logger.error(f'config key does not exist: {full_key}')
        return

    current = globals()

    if group_key not in current:
        if key not in current:
            if raise_error:
                logger.error(f'config key does not exist: {full_key}')
            return
    else:
        current = current[group_key]
        if not isinstance(current, NomadConfig):
            if raise_error:
                logger.error(f'config key does not exist: {full_key}')
            return

        if config_key not in current:
            if raise_error:
                logger.error(f'config key does not exist: {full_key}')
            return

        key = config_key

    try:
        current_value = current[key]
        if current_value is not None and not isinstance(value, type(current_value)):
            value = _transformations.get(full_key, type(current_value))(value)

        current[key] = value
        logger.info(f'set config setting {full_key}={value}')
    except Exception as e:
        logger.error(f'cannot set config setting {full_key}={value}: {e}')


def _apply_env_variables():
    kwargs = {
        key[len('NOMAD_'):].lower(): value
        for key, value in os.environ.items()
        if key.startswith('NOMAD_') and key != 'NOMAD_CONFIG'}

    for key, value in kwargs.items():
        _apply(key, value, raise_error=False)


def _apply_nomad_yaml():
    config_file = os.environ.get('NOMAD_CONFIG', 'nomad.yaml')

    if not os.path.exists(config_file):
        return

    with open(config_file, 'r') as stream:
        try:
            config_data = yaml.load(stream, Loader=getattr(yaml, 'FullLoader'))
        except yaml.YAMLError as e:
            logger.error(f'cannot read nomad config: {e}')
            return

    if not config_data:
        return

    for key, value in config_data.items():
        if isinstance(value, dict):
            group_key = key
            for key, value in value.items():
                _apply(f'{group_key}_{key}', value)
        else:
            _apply(key, value)


def load_config():
    '''
    Loads the configuration from nomad.yaml and environment.
    '''
    _apply_nomad_yaml()
    _apply_env_variables()
    _check_config()


load_config()
