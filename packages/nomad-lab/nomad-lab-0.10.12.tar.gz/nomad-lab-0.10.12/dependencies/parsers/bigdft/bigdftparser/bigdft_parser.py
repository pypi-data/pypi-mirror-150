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
import logging
import numpy as np
from ase.data import chemical_symbols
import yaml
try:
    from yaml import CLoader
except Exception:
    pass

from nomad.units import ureg
from nomad.parsing import FairdiParser
from nomad.datamodel.metainfo.common_dft import Run, Method, System, XCFunctionals,\
    SingleConfigurationCalculation, ScfIteration


class BigDFTParser(FairdiParser):
    def __init__(self):
        super().__init__(
            name='parsers/bigdft', code_name='BigDFT', code_homepage='http://bigdft.org/',
            mainfile_contents_re=(
                # r'__________________________________ A fast and precise DFT wavelet code\s*'
                # r'\|     \|     \|     \|     \|     \|\s*'
                # r'\|     \|     \|     \|     \|     \|      BBBB         i       gggggg\s*'
                # r'\|_____\|_____\|_____\|_____\|_____\|     B    B               g\s*'
                # r'\|     \|  :  \|  :  \|     \|     \|    B     B        i     g\s*'
                # r'\|     \|-0\+--\|-0\+--\|     \|     \|    B    B         i     g        g\s*'
                r'\|_____\|__:__\|__:__\|_____\|_____\|___ BBBBB          i     g         g\s*'
                # r'\|  :  \|     \|     \|  :  \|     \|    B    B         i     g         g\s*'
                # r'\|--\+0-\|     \|     \|-0\+--\|     \|    B     B     iiii     g         g\s*'
                # r'\|__:__\|_____\|_____\|__:__\|_____\|    B     B        i      g        g\s*'
                # r'\|     \|  :  \|  :  \|     \|     \|    B BBBB        i        g      g\s*'
                # r'\|     \|-0\+--\|-0\+--\|     \|     \|    B        iiiii          gggggg\s*'
                # r'\|_____\|__:__\|__:__\|_____\|_____\|__BBBBB\s*'
                # r'\|     \|     \|     \|  :  \|     \|                           TTTTTTTTT\s*'
                # r'\|     \|     \|     \|--\+0-\|     \|  DDDDDD          FFFFF        T\s*'
                # r'\|_____\|_____\|_____\|__:__\|_____\| D      D        F        TTTT T\s*'
                # r'\|     \|     \|     \|  :  \|     \|D        D      F        T     T\s*'
                # r'\|     \|     \|     \|--\+0-\|     \|D         D     FFFF     T     T\s*'
                # r'\|_____\|_____\|_____\|__:__\|_____\|D___      D     F         T    T\s*'
                # r'\|     \|     \|  :  \|     \|     \|D         D     F          TTTTT\s*'
                # r'\|     \|     \|--\+0-\|     \|     \| D        D     F         T    T\s*'
                # r'\|_____\|_____\|__:__\|_____\|_____\|          D     F        T     T\s*'
                # r'\|     \|     \|     \|     \|     \|         D               T    T\s*'
                # r'\|     \|     \|     \|     \|     \|   DDDDDD       F         TTTT\s*'
                # r'\|_____\|_____\|_____\|_____\|_____\|______                    www\.bigdft\.org'
            ))
        self.yaml_dict = dict()

        # TODO complete mapping
        self.xc_mapping = {
            1: ['LDA_XC_TETER93'],
            11: ['GGA_C_PBE", "GGA_X_PBE'],
            12: ['GGA_X_PBE'],
            15: ['GGA_C_PBE", "GGA_X_RPBE'],
            16: ['GGA_XC_HCTH_93'],
            17: ['GGA_XC_HCTH_120'],
            26: ['GGA_XC_HCTH_147'],
            27: ['GGA_XC_HCTH_407'],
            100: ['HF_X'],
            # libxc
            "001": "LDA_X",
            "002": "LDA_C_WIGNER",
            "003": "LDA_C_RPA",
            "004": "LDA_C_HL",
            "005": "LDA_C_GL",
            "006": "LDA_C_XALPHA",
            "007": "LDA_C_VWN",
            "008": "LDA_C_VWN_RPA",
            "009": "LDA_C_PZ",
            "010": "LDA_C_PZ_MOD",
            "011": "LDA_C_OB_PZ",
            "012": "LDA_C_PW",
            "013": "LDA_C_PW_MOD",
            "014": "LDA_C_OB_PW",
            "015": "LDA_C_2D_AMGB",
            "016": "LDA_C_2D_PRM",
            "017": "LDA_C_vBH",
            "018": "LDA_C_1D_CSC",
            "019": "LDA_X_2D",
            "020": "LDA_XC_TETER93",
            "021": "LDA_X_1D",
            "101": "GGA_X_PBE",
            "102": "GGA_X_PBE_R",
            "103": "GGA_X_B86",
            "104": "GGA_X_B86_R",
            "105": "GGA_X_B86_MGC",
            "106": "GGA_X_B88",
            "107": "GGA_X_G96",
            "108": "GGA_X_PW86",
            "109": "GGA_X_PW91",
            "110": "GGA_X_OPTX",
            "111": "GGA_X_DK87_R1",
            "112": "GGA_X_DK87_R2",
            "113": "GGA_X_LG93",
            "114": "GGA_X_FT97_A",
            "115": "GGA_X_FT97_B",
            "116": "GGA_X_PBE_SOL",
            "117": "GGA_X_RPBE",
            "118": "GGA_X_WC",
            "119": "GGA_X_mPW91",
            "120": "GGA_X_AM05",
            "121": "GGA_X_PBEA",
            "122": "GGA_X_MPBE",
            "123": "GGA_X_XPBE",
            "124": "GGA_X_2D_B86_MGC",
            "125": "GGA_X_BAYESIAN",
            "126": "GGA_X_PBE_JSJR",
            "127": "GGA_X_2D_B88",
            "128": "GGA_X_2D_B86",
            "129": "GGA_X_2D_PBE",
            "130": "GGA_C_PBE",
            "131": "GGA_C_LYP",
            "132": "GGA_C_P86",
            "133": "GGA_C_PBE_SOL",
            "134": "GGA_C_PW91",
            "135": "GGA_C_AM05",
            "136": "GGA_C_XPBE",
            "137": "GGA_C_LM",
            "138": "GGA_C_PBE_JRGX",
            "139": "GGA_X_OPTB88_VDW",
            "140": "GGA_X_PBEK1_VDW",
            "141": "GGA_X_OPTPBE_VDW",
            "160": "GGA_XC_LB",
            "161": "GGA_XC_HCTH_93",
            "162": "GGA_XC_HCTH_120",
            "163": "GGA_XC_HCTH_147",
            "164": "GGA_XC_HCTH_407",
            "165": "GGA_XC_EDF1",
            "166": "GGA_XC_XLYP",
            "167": "GGA_XC_B97",
            "168": "GGA_XC_B97_1",
            "169": "GGA_XC_B97_2",
            "170": "GGA_XC_B97_D",
            "171": "GGA_XC_B97_K",
            "172": "GGA_XC_B97_3",
            "173": "GGA_XC_PBE1W",
            "174": "GGA_XC_MPWLYP1W",
            "175": "GGA_XC_PBELYP1W",
            "176": "GGA_XC_SB98_1a",
            "177": "GGA_XC_SB98_1b",
            "178": "GGA_XC_SB98_1c",
            "179": "GGA_XC_SB98_2a",
            "180": "GGA_XC_SB98_2b",
            "181": "GGA_XC_SB98_2c",
            "401": "HYB_GGA_XC_B3PW91",
            "402": "HYB_GGA_XC_B3LYP",
            "403": "HYB_GGA_XC_B3P86",
            "404": "HYB_GGA_XC_O3LYP",
            "405": "HYB_GGA_XC_mPW1K",
            "406": "HYB_GGA_XC_PBEH",
            "407": "HYB_GGA_XC_B97",
            "408": "HYB_GGA_XC_B97_1",
            "410": "HYB_GGA_XC_B97_2",
            "411": "HYB_GGA_XC_X3LYP",
            "412": "HYB_GGA_XC_B1WC",
            "413": "HYB_GGA_XC_B97_K",
            "414": "HYB_GGA_XC_B97_3",
            "415": "HYB_GGA_XC_mPW3PW",
            "416": "HYB_GGA_XC_B1LYP",
            "417": "HYB_GGA_XC_B1PW91",
            "418": "HYB_GGA_XC_mPW1PW",
            "419": "HYB_GGA_XC_mPW3LYP",
            "420": "HYB_GGA_XC_SB98_1a",
            "421": "HYB_GGA_XC_SB98_1b",
            "422": "HYB_GGA_XC_SB98_1c",
            "423": "HYB_GGA_XC_SB98_2a",
            "424": "HYB_GGA_XC_SB98_2b",
            "425": "HYB_GGA_XC_SB98_2c",
            "201": "MGGA_X_LTA",
            "202": "MGGA_X_TPSS",
            "203": "MGGA_X_M06L",
            "204": "MGGA_X_GVT4",
            "205": "MGGA_X_TAU_HCTH",
            "206": "MGGA_X_BR89",
            "207": "MGGA_X_BJ06",
            "208": "MGGA_X_TB09",
            "209": "MGGA_X_RPP09",
            "231": "MGGA_C_TPSS",
            "232": "MGGA_C_VSXC",
            "301": "LCA_OMC",
            "302": "LCA_LCH",
        }

    def _extract(self, name, source, default=None):
        for key in source.keys():
            if key.lower() == name.lower():
                return source.pop(key)
        return default

    def parse_method(self):
        sec_method = self.archive.section_run[0].m_create(Method)
        sec_method.electronic_structure_method = 'DFT'

        data = self._extract('dft', self.yaml_dict, {})
        sec_method.total_charge = self._extract('qcharge', data, 0)
        sec_method.scf_max_iteration = self._extract('itermax', data, 0)
        sec_method.number_of_spin_channels = self._extract('nspin', data, 1)

        xc_id = self._extract('xc id', data)
        if xc_id is None:
            xc_id = self._extract('ixc', data)
        if xc_id < 0:
            # libxc
            xc_id = '%06d' % abs(xc_id)
            xc_functionals = [self.xc_mapping.get(xc_id[:3]), self.xc_mapping.get(xc_id[3:])]
        else:
            xc_functionals = self.xc_mapping.get(xc_id, [])

        xc_functionals = [f for f in xc_functionals if f is not None]
        for functional in xc_functionals:
            sec_xc_functional = sec_method.m_create(XCFunctionals)
            sec_xc_functional.XC_functional_name = functional
        sec_method.XC_functional = '_'.join(xc_functionals)

    def parse_system(self):
        sec_system = self.archive.section_run[0].m_create(System)

        data = self._extract('Atomic structure', self.yaml_dict, {})
        labels = []
        positions = []
        for atom in self._extract('positions', data, []):
            for label, position in atom.items():
                if label in chemical_symbols:
                    # some entries may not be symbols
                    labels.append(label)
                    positions.append(position)
        if labels:
            sec_system.atom_positions = positions * ureg.angstrom
            sec_system.atom_labels = labels

        cell = self._extract('cell', data)
        if cell is None:
            data = self._extract('Sizes of the simulation domain', self.yaml_dict, {})
            cell = self._extract('angstroem', data)
        if cell is not None:
            sec_system.lattice_vectors = np.diag(cell) * ureg.angstrom
            sec_system.configuration_periodic_dimensions = [True, True, True]

        data = self._extract('Atomic System Properties', self.yaml_dict, {})
        sec_system.number_of_atoms = self._extract('number of atoms', data, 0)

        pbc = self._extract('boundary conditions', data, 'Periodic').lower()
        if pbc == 'free':
            sec_system.configuration_periodic_dimensions = [False, False, False]
        elif pbc == 'periodic':
            sec_system.configuration_periodic_dimensions = [True, True, True]
        elif pbc == 'surface':
            sec_system.configuration_periodic_dimensions = [True, False, True]

    def parse_scc(self):
        sec_scc = self.archive.section_run[0].m_create(SingleConfigurationCalculation)

        energy = self._extract('Energy (Hartree)', self.yaml_dict)
        if energy is not None:
            sec_scc.energy_total = energy * ureg.hartree

        forces = self._extract('Atomic Forces (Ha/Bohr)', self.yaml_dict)
        if forces is not None:
            sec_scc.atom_forces = [list(f.values())[0] for f in forces] * (ureg.hartree / ureg.bohr)

        data = self._extract('Ground State Optimization', self.yaml_dict, [{}])
        hamiltonian = self._extract('hamiltonian optimization', data[0])
        if hamiltonian is None:
            return

        energy_mapping = {
            'exc': 'energy_XC', 'evxc': 'energy_XC_potential',
            'eh': 'energy_correction_hartree', 'ekin': 'electronic_kinetic_energy',
            'eks': 'energy_total', 'd': 'energy_change'}

        subspace = self._extract('subspace optimization', hamiltonian[0], {})
        wavefunction = self._extract('wavefunctions iterations', subspace, [])
        sec_scc.number_of_scf_iterations = len(wavefunction)
        for iteration in wavefunction:
            sec_scf = sec_scc.m_create(ScfIteration)
            energies = self._extract('energies', iteration, {})
            for key, val in energies.items():
                key = energy_mapping.get(key.lower())
                if key is not None:
                    setattr(sec_scf, '%s_scf_iteration' % key, val * ureg.hartree)

            for key, val in iteration.items():
                key = energy_mapping.get(key.lower())
                if key is not None:
                    setattr(sec_scf, '%s_scf_iteration' % key, val * ureg.hartree)

    def parse(self, filepath, archive, logger):
        self.filepath = os.path.abspath(filepath)
        self.archive = archive
        self.logger = logger if logger is not None else logging.getLogger(__name__)

        with open(self.filepath) as f:
            try:
                # we simply load everything at once as the metainfo framework does not
                # support streaming
                self.yaml_dict = yaml.load(f, Loader=CLoader)
            except Exception:
                try:
                    self.yaml_dict = yaml.safe_load(f)
                except Exception:
                    self.logger.error('Error loading yaml file.')
                    return

        sec_run = self.archive.m_create(Run)
        sec_run.program_name = 'BigDFT'
        sec_run.program_basis_set_type = 'real-space grid'
        sec_run.program_version = str(self.yaml_dict.pop('Version Number', ''))

        self.parse_method()
        self.parse_system()
        self.parse_scc()

        sec_scc = sec_run.section_single_configuration_calculation[-1]
        sec_scc.single_configuration_calculation_to_system_ref = sec_run.section_system[-1]
        sec_scc.single_configuration_to_calculation_method_ref = sec_run.section_method[-1]
