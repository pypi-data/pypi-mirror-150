
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

import sys
import os
import click

from .cli import cli


@cli.group(help='Commands related to the nomad source code.')
def dev():
    pass


@dev.command(help='Runs tests and linting of the nomad python source code. Useful before committing code.')
@click.option('--skip-tests', help='Do no tests, just do code checks.', is_flag=True)
@click.option('-x', '--exitfirst', help='Stop testing after first failed test case.', is_flag=True)
def qa(skip_tests: bool, exitfirst: bool):
    os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
    ret_code = 0

    if not skip_tests:
        click.echo('Run tests ...')
        ret_code += os.system('python -m pytest -sv%s tests' % ('x' if exitfirst else ''))
    click.echo('Run code style checks ...')
    ret_code += os.system('python -m pycodestyle --ignore=E501,E701,E731 nomad tests')
    click.echo('Run linter ...')
    ret_code += os.system('python -m pylint --load-plugins=pylint_mongoengine,nomad.metainfo.pylint_plugin nomad tests')
    click.echo('Run static type checks ...')
    ret_code += os.system('python -m mypy --ignore-missing-imports --follow-imports=silent --no-strict-optional nomad tests')

    sys.exit(ret_code)


@dev.command(help='Runs tests and linting of the nomad gui source code. Useful before committing code.')
@click.option('--skip-tests', help='Do no tests, just do code checks.', is_flag=True)
def gui_qa(skip_tests: bool):
    os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../gui')))
    ret_code = 0

    if not skip_tests:
        click.echo('Run gui testing ...')
        ret_code += os.system('yarn run test')
    click.echo('Run gui code linting ...')
    ret_code += os.system('yarn run lint')

    sys.exit(ret_code)


@dev.command(help='Generates a JSON with all metainfo.')
def metainfo():
    import json
    export = _all_metainfo_packages()
    metainfo_data = export.m_to_dict(with_meta=True)
    print(json.dumps(metainfo_data, indent=2))


def _all_metainfo_packages():
    from nomad.metainfo import Package, Environment
    from nomad.datamodel import EntryArchive

    # TODO similar to before, due to lazyloading, we need to explicily access parsers
    # to actually import all parsers and indirectly all metainfo packages
    from nomad.parsing.parsers import import_all_parsers
    import_all_parsers()

    # Create the ES mapping to populate ES annoations with search keys.
    from nomad.search import entry_type
    entry_type.create_mapping(EntryArchive.m_def)

    # TODO we call __init_metainfo__() for all packages where this has been forgotten
    # by the package author. Ideally this would not be necessary and we fix the
    # actual package definitions.
    for module_key in list(sys.modules):
        pkg: Package = getattr(sys.modules[module_key], 'm_package', None)
        if pkg is not None and isinstance(pkg, Package):
            if (pkg.name not in Package.registry):
                pkg.__init_metainfo__()

    export = Environment()
    for package in Package.registry.values():
        export.m_add_sub_section(Environment.packages, package)
    return export


@dev.command(help='Generates a JSON with all search quantities.')
def search_quantities():
    _all_metainfo_packages()
    import json

    # Currently only quantities with "entry_type" are included.
    from nomad.metainfo.elasticsearch_extension import entry_type, Elasticsearch
    from nomad.datamodel import EntryArchive

    def to_dict(search_quantity, section=False):
        if section:
            keys = ["name", "description", "nested"]
            metadict = search_quantity.sub_section.m_to_dict(with_meta=True)
            metadict["name"] = search_quantity.m_to_dict(with_meta=True)["name"]
            es_annotations = search_quantity.m_get_annotations(Elasticsearch, as_list=True)
            nested = any([x.nested for x in es_annotations])
            metadict["nested"] = nested
        else:
            keys = ["name", "description", "type", "unit"]
            metadict = search_quantity.definition.m_to_dict(with_meta=True)
        result = {}
        for key in keys:
            val = metadict.get(key)
            if val is not None:
                result[key] = val
        return result

    export = {}

    # Add quantities
    for search_quantity in entry_type.quantities.values():
        isSuggestion = search_quantity.annotation.suggestion
        if not isSuggestion:
            export[search_quantity.qualified_name] = to_dict(search_quantity)

    # Add suggestion flag
    for suggestion in entry_type.suggestions.keys():
        export[suggestion]["suggestion"] = True

    # Add section definitions
    def get_sections(m_def, prefix=None):
        for sub_section_def in m_def.all_sub_sections.values():
            name = sub_section_def.name
            full_name = f"{prefix}.{name}" if prefix else name
            export[full_name] = to_dict(sub_section_def, True)
            get_sections(sub_section_def.sub_section, full_name)
    get_sections(EntryArchive.results.sub_section, "results")

    print(json.dumps(export, indent=2))


@dev.command(help='Generates a JSON file that compiles all the parser metadata from each parser project.')
def parser_metadata():
    import json
    import yaml
    import os
    import os.path
    from glob import glob

    parsers_metadata = {}
    parsers_path = './dependencies/parsers'
    for parser_metadata_file in sorted(glob(f'{parsers_path}/**/metadata.yaml', recursive=True)):
        with open(parser_metadata_file) as f:
            parser_metadata = yaml.load(f, Loader=yaml.FullLoader)
        parsers_metadata[os.path.basename(os.path.dirname(parser_metadata_file))] = parser_metadata

    parsers_metadata = {
        key: parsers_metadata[key]
        for _, key in sorted([(key.lower(), key) for key in parsers_metadata], key=lambda x: x[0])}

    print(json.dumps(parsers_metadata, indent=2))


@dev.command(help='Generate toolkit tutorial metadata from anaytics submodules.')
def toolkit_metadata():
    import requests
    import re
    import json
    modules = requests.get(
        'https://gitlab.mpcdf.mpg.de/api/v4/projects/3161/repository/files/.gitmodules/raw?ref=master').text

    tutorials = []
    lines = modules.split('\n')
    for line in lines:
        match = re.match(r'\s*url = (.*)$', line)
        if match:
            url = match.group(1).replace('.git', '') + '/-/raw/master/metainfo.json'
            response = requests.get(url)
            if response.status_code != 200:
                print('Could not get metadata for %s' % match.group(1), file=sys.stderr)
                continue
            try:
                tutorials.append(response.json())
            except Exception:
                print('Could not get metadata for %s. Project is probably not public.' % match.group(1), file=sys.stderr)

    print(json.dumps(dict(tutorials=tutorials), indent=2))


@dev.command(help=(
    'Updates parser`s README files by combining a general template with  '
    'a parser`s metadata YAML file.'))
@click.option('--parser', help='Only updated the README of the given parsers subdirctory.')
def update_parser_readmes(parser):
    from glob import glob
    import re
    import yaml

    os.chdir(os.path.join(os.path.dirname(__file__), '../..'))

    # filenames
    local_fn = 'README.md'
    generic_fn = './README.parsers.md'
    parser_path = './dependencies/parsers/'

    # Open general template
    with open(generic_fn, 'r') as generic:  # read only
        generic_contents = generic.read()

    # Replace the comment at the top of the gereral template
    generic_contents = re.sub(
        rf'\*\*\*Note:\*\* This is a general README file for NOMAD parsers, '
        rf'consult the README of specific parser projects for more detailed '
        rf'information!\*\n\n', '', generic_contents)

    def open_metadata(path):
        # read local yaml metadata file
        with open(path, 'r') as metadata_f:
            try:
                metadata = yaml.load(metadata_f, Loader=yaml.FullLoader)
            except Exception as e:
                print(f'Error reading metadata.yaml: {e}')
                metadata = None
        return metadata

    def replace(metadata, contents, path):
        # replace placelder in contents with metadata values
        for key in metadata.keys():
            replace = metadata.get(key)
            if replace is None:
                continue
            print(f'\tReplacing {key} with {replace}')
            contents = re.sub(rf'\${key}\$', replace, contents)

        # save file
        with open(path, 'w') as f:
            f.write(contents.strip())
            f.write('\n')

    for local_readme in sorted(glob(f'{parser_path}/*/{local_fn}')):
        parser_dir = os.path.dirname(local_readme)
        project_name = os.path.basename(parser_dir)
        print(f'Working on {parser_dir}')

        contents = generic_contents
        # if metadata file under the parser directory exists, it is a single parser project
        single = os.path.isfile(os.path.join(parser_dir, 'metadata.yaml'))

        if single:
            metadata = open_metadata(os.path.join(parser_dir, 'metadata.yaml'))
            # git path is given by nomad-parser-codename
            metadata['gitPath'] = f'nomad-parser-{project_name}'
            parser_header, parser_specs = '', ''
        else:
            # replace header for the single parser with that for a group of parsers
            parser_header_re = r'(\nThis is a NOMAD parser[\s\S]+?Archive format\.\n)'
            parser_header = re.search(parser_header_re, contents).group(1)
            group_header = 'This is a collection of the NOMAD parsers for the following $codeName$ codes:\n\n$parserList$'
            contents = re.sub(parser_header_re, group_header, contents)
            # remove individual parser specs
            parser_specs_re = r'(For \$codeLabel\$ please provide[\s\S]+?\$tableOfFiles\$)\n\n'
            parser_specs = re.search(parser_specs_re, contents).group(1)
            contents = re.sub(parser_specs_re, '', contents)
            metadata = dict(
                gitPath=f'{project_name}-parsers',
                parserGitUrl=f'https://github.com/nomad-coe/{project_name}-parsers.git',
                parserSpecific='')
        if metadata.get('codeName', '').strip() == '':
            metadata['codeName'] = project_name
        if 'preamble' not in metadata:
            metadata['preamble'] = ''

        # if this is a group of parser, find all individdual parsers and write the
        # parser specs
        parser_list = ''
        for index, local_metadata in enumerate(sorted(glob(f'{parser_dir}/*/*/metadata.yaml'))):
            metadata_parser = open_metadata(local_metadata)
            # contents is simply the parser header and specs
            contents_parser = f'{parser_header}\n{parser_specs}'
            replace(metadata_parser, contents_parser, os.path.join(os.path.dirname(local_metadata), local_fn))
            # add the codename to the list of parsers for the group header
            codelabel = metadata_parser.get('codeLabel', os.path.basename(os.path.dirname(local_metadata)))
            codeurl = metadata_parser.get('codeUrl', '')
            parser_list = rf'{parser_list}{index + 1}. [{codelabel}]({codeurl})\n'
        metadata['parserList'] = parser_list.strip()

        # Find & Replace Parser`s metadata on its README file
        replace(metadata, contents, local_readme)


@dev.command(help='Adds a few pieces of data to NOMAD.')
@click.option('--username', '-u', type=str, help='The main author username.')
def example_data(username: str):
    from nomad import infrastructure, utils
    from tests.utils import ExampleData

    infrastructure.setup()

    main_author = infrastructure.keycloak.get_user(username=username)
    if main_author is None:
        print(f'The user {username} does not exist.')
        sys.exit(1)

    data = ExampleData(main_author=main_author)

    # one upload with two entries published with embargo, one shared
    upload_id = utils.create_uuid()
    data.create_upload(upload_id=upload_id, published=True, embargo_length=0)
    data.create_entry(
        entry_id=utils.create_uuid(),
        upload_id=upload_id,
        mainfile='test_content/test_embargo_entry/mainfile.json')

    data.save(with_files=True, with_es=True, with_mongo=True)

    return data


@dev.command(help='Creates a Javascript source file containing the required unit conversion factors.')
@click.pass_context
def units(ctx):
    import re
    import json
    from nomad.units import ureg

    # Mapping from unit name to dimension
    unit_map = {
        # Time
        "second": {
            "dimension": "time",
            "label": "Second",
            "abbreviation": "s",
        },
        "atomic_unit_of_time": {
            "dimension": "time",
            "label": "Atomic unit of time",
            "abbreviation": "a_u_time",
        },
        # Length
        "meter": {
            "dimension": "length",
            "label": "Meter",
            "abbreviation": "m",
        },
        "bohr": {
            "dimension": "length",
            "label": "Bohr",
            "abbreviation": "bohr",
        },
        "angstrom": {
            "dimension": "length",
            "label": "Ångstrom",
            "abbreviation": "Å",
        },
        # Mass
        "kilogram": {
            "dimension": "mass",
            "label": "Kilogram",
            "abbreviation": "kg",
        },
        "electron_mass": {
            "dimension": "mass",
            "label": "Electron mass",
            "abbreviation": "mₑ",
        },
        "unified_atomic_mass_unit": {
            "dimension": "mass",
            "label": "Unified atomic mass unit",
            "abbreviation": "u",
        },
        # Current
        "ampere": {
            "dimension": "current",
            "label": "Ampere",
            "abbreviation": "A",
        },
        "atomic_unit_of_current": {
            "dimension": "current",
            "label": "Atomic unit of current",
            "abbreviation": "a_u_current",
        },
        # Substance
        "mole": {
            "dimension": "substance",
            "label": "Mole",
            "abbreviation": "mole",
        },
        # Luminosity
        "candela": {
            "dimension": "luminosity",
            "label": "Candela",
            "abbreviation": "cd",
        },
        # Temperature
        "kelvin": {
            "dimension": "temperature",
            "label": "Kelvin",
            "abbreviation": "K",
        },
        "celsius": {
            "dimension": "temperature",
            "label": "Celsius",
            "abbreviation": "°C",
        },
        "fahrenheit": {
            "dimension": "temperature",
            "label": "Fahrenheit",
            "abbreviation": "°F",
        },
        "atomic_unit_of_temperature": {
            "dimension": "temperature",
            "label": "Atomic unit of temperature",
            "abbreviation": "a_u_temperature",
        },
        # Force
        "newton": {
            "dimension": "force",
            "label": "Newton",
            "abbreviation": "N",
        },
        "atomic_unit_of_force": {
            "dimension": "force",
            "label": "Atomic unit of force",
            "abbreviation": "a_u_force",
        },
        # Pressure
        "pascal": {
            "dimension": "pressure",
            "label": "Pascal",
            "abbreviation": "Pa"
        },
        "gigapascal": {
            "dimension": "pressure",
            "label": "Gigapascal",
            "abbreviation": "GPa"
        },
        "atomic_unit_of_pressure": {
            "dimension": "pressure",
            "label": "Atomic unit of pressure",
            "abbreviation": "a_u_pressure"
        },
        # Energy
        "joule": {
            "dimension": "energy",
            "label": "Joule",
            "abbreviation": "J",
        },
        "electron_volt": {
            "dimension": "energy",
            "label": "Electron volt",
            "abbreviation": "eV",
        },
        "hartree": {
            "dimension": "energy",
            "label": "Hartree",
            "abbreviation": "Ha",
        },
        # Power
        "watt": {
            "dimension": "power",
            "label": "Watt",
            "abbreviation": "W",
        },
        # Frequency
        "hertz": {
            "dimension": "frequency",
            "label": "Hertz",
            "abbreviation": "Hz",
        },
        # Electric potential
        "volt": {
            "dimension": "electric_potential",
            "label": "Volt",
            "abbreviation": "V",
        },
        # Capacitance
        "farad": {
            "dimension": "capacitance",
            "label": "Farad",
            "abbreviation": "F",
        },
        # Charge
        "coulomb": {
            "dimension": "charge",
            "label": "Coulomb",
            "abbreviation": "C",
        },
        "elementary_charge": {
            "dimension": "charge",
            "label": "Elementary charge",
            "abbreviation": "e",
        },
        # Magnetic field
        "tesla": {
            "dimension": "magnetic_field",
            "label": "Tesla",
            "abbreviation": "T",
        },
        # Magnetic flux
        "weber": {
            "dimension": "magnetic_flux",
            "label": "Weber",
            "abbreviation": "Wb",
        },
        # Magnetic dipole
        "bohr_magneton": {
            "dimension": "magnetic_dipole",
            "label": "Bohr magneton",
            "abbreviation": "Bm",
        },
        # Inductance
        "henry": {
            "dimension": "inductance",
            "label": "Henry",
            "abbreviation": "H",
        },
        # angle
        "radian": {
            "dimension": "angle",
            "label": "Radian",
            "abbreviation": "rad",
        },
        "degree": {
            "dimension": "angle",
            "label": "Degree",
            "abbreviation": "°",
        },
        # dimensionless
        "dimensionless": {
            "dimension": "dimensionless",
            "label": "Dimensionless",
            "abbreviation": "",
        },
    }

    # Units that are supported
    unit_table = {
        # Base units
        "time": {
            "units": [
                "second",
                "atomic_unit_of_time",
            ],
            "multipliers": {},
        },
        "length": {
            "units": [
                "meter",
                "bohr",
                "angstrom",
            ],
            "multipliers": {},
        },
        "mass": {
            "units": [
                "kilogram",
                "electron_mass",
                "unified_atomic_mass_unit",
            ],
            "multipliers": {},
        },
        "current": {
            "units": [
                "ampere",
                "atomic_unit_of_current",
            ],
            "multipliers": {},
        },
        "substance": {
            "units": [
                "mole",
            ],
            "multipliers": {},
        },
        "luminosity": {
            "units": [
                "candela",
            ],
            "multipliers": {},
        },
        "temperature": {
            "units": [
                "kelvin",
                "celsius",
                "fahrenheit",
                "atomic_unit_of_temperature",
            ],
            "multipliers": {},
            "constants": {},
        },
        # Derived units
        "force": {
            "units": [
                "newton",
                "atomic_unit_of_force",
            ],
            "multipliers": {},
        },
        "pressure": {
            "units": [
                "pascal",
                "gigapascal",
                "atomic_unit_of_pressure",
            ],
            "multipliers": {},
        },
        "energy": {
            "units": [
                "joule",
                "electron_volt",
                "hartree",
            ],
            "multipliers": {},
        },
        "power": {
            "units": [
                "watt",
            ],
            "multipliers": {},
        },
        "frequency": {
            "units": [
                "hertz",
            ],
            "multipliers": {},
        },
        "electric_potential": {
            "units": [
                "volt",
            ],
            "multipliers": {},
        },
        "capacitance": {
            "units": [
                "farad",
            ],
            "multipliers": {},
        },
        "charge": {
            "units": [
                "coulomb",
                "elementary_charge",
            ],
            "multipliers": {},
        },
        "magnetic_field": {
            "units": [
                "tesla",
            ],
            "multipliers": {},
        },
        "magnetic_flux": {
            "units": [
                "weber",
            ],
            "multipliers": {},
        },
        "magnetic_dipole": {
            "units": [
                "bohr_magneton",
            ],
            "multipliers": {},
        },
        "inductance": {
            "dimension": "inductance",
            "units": [
                "henry",
            ],
            "multipliers": {},
        },
        "angle": {
            "dimension": "angle",
            "units": [
                "radian",
                "degree",
            ],
            "multipliers": {},
        },
        "dimensionless": {
            "dimension": "dimensionless",
            "units": [
                "dimensionless",
            ],
            "multipliers": {},
        },
    }

    # Unit systems
    unit_systems = {
        "SI": {
            "label": "SI",
            "description": "International System of Units (SI)",
            "units": {
                "time": "second",
                "length": "meter",
                "mass": "kilogram",
                "current": "ampere",
                "substance": "mole",
                "luminosity": "candela",
                "temperature": "kelvin",
                "force": "newton",
                "pressure": "pascal",
                "energy": "joule",
                "power": "watt",
                "frequency": "hertz",
                "electric_potential": "volt",
                "charge": "coulomb",
                "angle": "radian",
            },
        },
        "AU": {
            "label": "Atomic units",
            "description": "Hartree atomic units",
            "units": {
                "time": "atomic_unit_of_time",
                "length": "bohr",
                "mass": "electron_mass",
                "current": "atomic_unit_of_current",
                "temperature": "atomic_unit_of_temperature",
                "force": "atomic_unit_of_force",
                "energy": "hartree",
                "pressure": "atomic_unit_of_pressure",
                "angle": "radian",
            }
        }
    }

    # Precompute conversion factors and possible shifts
    for value in unit_table.values():
        units = value["units"]
        for i_unit in units:
            for j_unit in units:
                # Create dictionaries if not present
                multipliers = value["multipliers"]
                if i_unit not in multipliers:
                    multipliers[i_unit] = {}
                if j_unit not in multipliers[i_unit]:
                    multipliers[i_unit][j_unit] = {}

                # Check if there is a constant shift: y = ax + b -> y(0) = b.
                # Uses delta units for temperatures since only they are
                # multiplicative.
                y_0 = 0 * getattr(ureg, "delta_" + i_unit, getattr(ureg, i_unit))
                b = y_0.to(getattr(ureg, j_unit)).magnitude

                # Solving the multiplication factor with:
                # y(1) = a + b -> a = y(1) - b
                # Uses delta units for temperatures since only they are
                # multiplicative. Causes minor numerical accuracy issues in the
                # factor due to floating point precision
                y_1 = 1 * getattr(ureg, "delta_" + i_unit, getattr(ureg, i_unit))
                a = y_1.to(getattr(ureg, "delta_" + j_unit, getattr(ureg, j_unit))).magnitude
                multipliers[i_unit][j_unit] = a

                # Create dictionaries if not present
                if b != 0:
                    constants = value["constants"]
                    if i_unit not in constants:
                        constants[i_unit] = {}
                    if j_unit not in constants[i_unit]:
                        constants[i_unit][j_unit] = {}
                    constants[i_unit][j_unit] = b

    # Check that all defined units are present in the conversion table
    for unit, info in unit_map.items():
        dimension = info["dimension"]
        unit_list = unit_table[dimension]["units"]
        assert unit in unit_list, "Could not find '{}' in the unit table under the dimension '{}'.".format(unit, dimension)

    # Check unit system correctness
    for system in unit_systems.values():
        for dimension, unit in system["units"].items():
            info = unit_map[unit]
            assert dimension == info["dimension"]

    # Go through the metainfo and check that all units are defined
    all_metainfo = _all_metainfo_packages()
    units = set()
    packages = all_metainfo.m_to_dict(with_meta=True)['packages']
    for package in packages:
        sections = package.get("section_definitions", [])
        for section in sections:
            quantities = section.get("quantities", [])
            for quantity in quantities:
                unit = quantity.get("unit")
                if unit is not None:
                    parts = unit.split()
                    for part in parts:
                        is_operator = part in {"/", "**", "*"}
                        is_number = True
                        try:
                            int(part)
                        except Exception:
                            is_number = False
                        if not is_operator and not is_number:
                            units.add(part)
    for unit in units:
        if unit == 'byte':
            continue

        assert unit in unit_map, "The unit '{}' is not defined in the unit definitions.".format(unit)

    # Print unit conversion table and unit systems as a Javascript source file
    output = """/*
 * Copyright The NOMAD Authors.
 *
 * This file is part of NOMAD. See https://nomad-lab.eu for further info.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
// Generated by NOMAD CLI. Do not edit manually.
"""
    output += "export const unitMap = "
    json_string = json.dumps(unit_map, indent=2)
    json_string = re.sub(r'(?<!: )"(\S*?)":', '\\1:', json_string)
    json_string = json_string.replace("\"", "'")
    output += json_string
    output += "\nexport const conversionMap = "
    json_string = json.dumps(unit_table, indent=2)
    json_string = re.sub(r'(?<!: )"(\S*?)":', '\\1:', json_string)
    json_string = json_string.replace("\"", "'")
    output += json_string
    output += "\nexport const unitSystems = "
    json_string = json.dumps(unit_systems, indent=2)
    json_string = re.sub(r'(?<!: )"(\S*?)":', '\\1:', json_string)
    json_string = json_string.replace("\"", "'")
    output += json_string
    print(output)
