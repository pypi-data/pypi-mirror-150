import numpy as np
import logging
import ase
from ase.io.ulm import Reader

from .metainfo import m_env
from nomad.units import ureg
from nomad.parsing import FairdiParser
from nomad.parsing.file_parser import FileParser, TarParser, XMLParser, DataTextParser
from nomad.datamodel.metainfo.common_dft import Run, BasisSetCellDependent, System,\
    BasisSetAtomCentered, SamplingMethod, Method, XCFunctionals, Eigenvalues,\
    SingleConfigurationCalculation, VolumetricData, KBand, KBandSegment


class GPWParser(TarParser):
    def __init__(self):
        super().__init__()
        self._version_map = {6: '1.1.0', 5: '0.11.0', 3: '0.10.0'}
        self._info_map = {
            'energy_total': 'Epot', 'energy_XC': 'Exc', 'electronic_kinetic_energy': 'Ekin',
            'energy_correction_entropy': 'S', 'atom_forces_free': 'CartesianForce',
            'atom_positions': 'CartesianPositions', 'occupation': 'OccupationNumbers',
            'kpoints': 'IBZKPoints'}

    def init_parameters(self):
        self._info = None

    @property
    def info(self):
        if self._info is None:
            self._info = dict()
            xml_file = self.get('info.xml', None)
            if xml_file is None:
                return
            self.xml_file = xml_file
            xml_parser = XMLParser(xml_file, logger=self.logger)

            def convert(val):
                if isinstance(val, list):
                    return [convert(v) for v in val]
                try:
                    if val in ['True', 'False']:
                        return val == 'True'
                    else:
                        val = float(val)
                        if val % 1.0 == 0.0:
                            val = int(val)
                        return val
                except Exception:
                    return val

            # parameters
            self._info['parameter'] = {
                'lengthunit': 'angstrom', 'energyunit': 'eV', 'timeunit': 'femtosecond'}
            self._info['parameter'].update({p['name'].lower(): convert(
                p['value']) for p in xml_parser.get('parameter/', [])})

            # array shapes, types, dimensions
            self._info['array'] = dict()
            dimension = dict()
            for arr in xml_parser.root.findall('./array'):
                name = arr.attrib.get('name', None)
                dtype = arr.attrib.get('type', None)
                if name is None or dtype is None:
                    continue
                shape = []
                for dim in arr.findall('./dimension'):
                    length = int(dim.attrib.get('length', 0))
                    shape.append(length)
                    dimension[dim.attrib.get('name')] = length
                self._info['array'][name.lower()] = dict(dtype=dtype, shape=shape)
            self._info['array_dimension'] = dimension

            self._info['bytesswap'] = (
                xml_parser.root.attrib['endianness'] == 'little') != np.little_endian
        return self._info

    def get_parameter(self, key, unit=None):
        key = self._info_map.get(key, key)
        return self.info['parameter'].get(key.lower(), None)

    def get_array(self, key, unit=None):
        key = self._info_map.get(key, key)
        file_object = self.get(key)
        if file_object is None:
            return

        key = key.lower()
        shape = self.info['array'].get(key, {}).get('shape', None)
        dtype = self.info['array'].get(key, {}).get('dtype', None)
        dtype = np.dtype({'int': 'int32'}.get(dtype, dtype))
        size = np.prod(shape) * dtype.itemsize

        file_object.seek(0)
        parser = DataTextParser(
            mainfile_contents=file_object.read(size), logger=self.logger, dtype=dtype)
        if parser.data is None:
            return

        array = parser.data
        if self._info['bytesswap']:
            array = array.byteswap()
        if dtype == np.int32:
            array = np.asarray(array, int)
        array.shape = shape
        return array

    def get_array_dimension(self, key):
        if key == 'ngpts':
            val = [self.get_array_dimension('ngpts%s' % n) for n in ['x', 'y', 'z']]
        else:
            val = self.info['array_dimension'].get(key)
        return val

    def get_program_version(self):
        return self._version_map.get(self.get_parameter('version'), '0.9.0')

    def get_smearing_width(self):
        return self.get_parameter('fermiwidth')


class GPW2Parser(FileParser):
    def __init__(self):
        super().__init__(None)

    def init_parameters(self):
        self._info = None

    @property
    def ulm(self):
        if self._file_handler is None:
            try:
                self._file_handler = Reader(self.mainfile)
            except Exception:
                pass
        return self._file_handler

    @property
    def info(self):
        if self._info is None:
            self._info = dict()
            self._info['parameter'] = {
                'mode': 'fd', 'xc': 'LDA', 'occupations': None, 'poissonsolver': None,
                'h': None, 'gpts': None, 'kpts': [(0.0, 0.0, 0.0)], 'nbands': None,
                'charge': 0, 'setups': {}, 'basis': {}, 'spinpol': None, 'fixdensity': False,
                'filter': None, 'mixer': None, 'eigensolver': None, 'background_charge': None,
                'external': None, 'random': False, 'hund': False, 'maxiter': 333,
                'idiotproof': True, 'symmetry': {
                    'point_group': True, 'time_reversal': True, 'symmorphic': True,
                    'tolerance': 1e-7},
                'convergence': {
                    'energy': 0.0005, 'density': 1.0e-4, 'eigenstates': 4.0e-8,
                    'bands': 'occupied', 'forces': np.inf},
                'dtype': None, 'width': None, 'verbose': 0, 'lengthunit': 'angstrom',
                'energyunit': 'eV', 'timeunit': 'femtosecond'}
            if self.ulm is not None:
                self._info['parameter'].update(self.ulm.parameters.asdict())
        return self._info

    def get_parameter(self, key):
        try:
            if key == 'planewavecutoff':
                val = self.get_parameter('mode').get('ecut', None)
            elif key == 'basisset':
                val = self.get_parameter('basis')
            elif key == 'energyerror':
                val = self.get_parameter('convergence').get('energy', None)
            elif key == 'xcfunctional':
                val = self.get_parameter('xc')
            # in gpw format, energies are parameters
            elif key == 'energy_total':
                val = self.ulm.hamiltonian.e_total_extrapolated
            elif key == 'energy_free':
                val = self.ulm.hamiltonian.e_total_free
            elif key == 'energy_XC':
                val = self.ulm.hamiltonian.e_xc
            elif key == 'electronic_kinetic_energy':
                val = self.ulm.hamiltonian.e_kinetic
            elif key == 'energy_correction_entropy':
                val = self.ulm.hamiltonian.e_entropy
            elif key == 'fermilevel':
                val = self.ulm.occupations.fermilevel
            elif key == 'split':
                val = self.ulm.occupations.split
            elif key == 'converged':
                val = self.ulm.scf.converged
            else:
                val = self.info['parameter'].get(key.lower(), None)
        except Exception:
            val = None
        return val

    def get_array(self, key):
        if self.ulm is None:
            return
        try:
            if key == 'unitcell':
                val = self.ulm.atoms.cell
            elif key == 'atomicnumbers':
                val = self.ulm.atoms.numbers
            elif key == 'atom_positions':
                val = self.ulm.atoms.positions
            elif key == 'boundaryconditions':
                val = self.ulm.atoms.pbc
            elif key == 'momenta':
                val = self.ulm.atoms.momenta
            elif key == 'atom_forces_free_raw':
                val = self.ulm.results.forces
            elif key == 'magneticmoments':
                val = self.ulm.results.magmoms
            elif key == 'eigenvalues':
                val = self.ulm.wave_functions.eigenvalues
            elif key == 'occupation':
                val = self.ulm.wave_functions.occupations
            # TODO no koints data in ulm?
            elif key == 'kpoints':
                val = self.ulm.IBZKPoints
            elif key == 'density':
                val = self.ulm.density.density
            elif key == 'potential_effective':
                val = self.ulm.hamiltonian.potential
            elif key == 'band_paths':
                val = self.ulm.wave_functions.band_paths.asdict()
            else:
                val = self.ulm.asdict().get(key, None)
        except Exception:
            val = None
        return val

    def get_array_dimension(self, key):
        if key == 'ngpts':
            val = self.ulm.density.density.shape
        else:
            val = self.ulm.asdict().get(key, None)
        return val

    def get_program_version(self):
        return self.ulm.gpaw_version

    def get_smearing_width(self):
        if self.get_parameter('occupations') is None:
            return 0.0 if tuple(self.get_parameter('kpts')) == (1, 1, 1) else 0.1
        else:
            return self.get_parameter('occupations').get('width')


class GPAWParser(FairdiParser):
    def __init__(self):
        super(). __init__(
            name='parsers/gpaw', code_name='GPAW', code_homepage='https://wiki.fysik.dtu.dk/gpaw/',
            mainfile_name_re=(r'^.*\.(gpw2|gpw)$'),
            mainfile_mime_re=r'application/(x-tar|octet-stream)')

        self._metainfo_env = m_env
        self.gpw_parser = GPWParser()
        self.gpw2_parser = GPW2Parser()
        self._xc_map = {
            'LDA': ['LDA_X', 'LDA_C_PW'],
            'PW91': ['GGA_X_PW91', 'GGA_C_PW91'],
            'PBE': ['GGA_X_PBE', 'GGA_C_PBE'],
            'PBEsol': ['GGA_X_PBE_SOL', 'GGA_C_PBE_SOL'],
            'revPBE': ['GGA_X_PBE_R', 'GGA_C_PBE'],
            'RPBE': ['GGA_X_RPBE', 'GGA_C_PBE'],
            'BLYP': ['GGA_X_B88', 'GGA_C_LYP'],
            'HCTH407': ['GGA_XC_HCTH_407'],
            'WC': ['GGA_X_WC', 'GGA_C_PBE'],
            'AM05': ['GGA_X_AM05', 'GGA_C_AM05'],
            'M06-L': ['MGGA_X_M06_L', 'MGGA_C_M06_L'],
            'TPSS': ['MGGA_X_TPSS', 'MGGA_C_TPSS'],
            'revTPSS': ['MGGA_X_REVTPSS', 'MGGA_C_REVTPSS'],
            'mBEEF': ['MGGA_X_MBEEF', 'GGA_C_PBE_SOL']}

    def init_parser(self, filepath, logger):
        self.parser = self.gpw_parser
        self.parser.mainfile = filepath
        if self.parser.mainfile_obj is None:
            self.parser = self.gpw2_parser
            self.parser.mainfile = filepath
        self.parser.logger = logger

    def apply_unit(self, val, unit):
        units_map = {
            'ev': ureg.eV, 'hartree': ureg.hartree, 'angstrom': ureg.angstrom,
            'bohr': ureg.bohr, 'femtosecond': ureg.fs}
        p_unit = self.parser.info['parameter'].get(unit, '').lower()
        unit = units_map.get(p_unit, p_unit) if p_unit else unit
        return val * unit

    def get_basis_set_name(self):
        basis_set = self.archive.section_run[-1].program_basis_set_type
        if basis_set == 'plane waves':
            pw_cutoff = self.parser.get_parameter('planewavecutoff')
            pw_cutoff = self.apply_unit(pw_cutoff, 'energyunit')
            return 'PW_%.1f_Ry' % (pw_cutoff.to('rydberg').magnitude)
        elif basis_set == 'real space grid':
            cell = self.parser.get_array('unitcell')
            ngpts = self.parser.get_array_dimension('ngpts')
            if cell is None or ngpts is None:
                return
            h_grid = np.linalg.norm(cell, axis=1) / np.array(ngpts[:3])
            h_grid = self.apply_unit(np.sum(h_grid) / 3.0, 'lengthunit')
            return 'GR_%.1f' % (h_grid.to('fm').magnitude)
        elif basis_set == 'numeric AOs':
            return self.parser.get_parameter('basisset')

    def get_mode(self):
        mode = self.parser.get_parameter('mode')
        if isinstance(mode, dict):
            mode = mode.get('name', None)
        return mode

    def get_nspin(self):
        # TODO another way determine spin?
        magnetic_moments = self.parser.get_array('magneticmoments')
        return 1 if magnetic_moments is None else 2

    def get_fermi_level(self):
        fermi_level = [self.parser.get_parameter('fermilevel')] * self.get_nspin()
        if None in fermi_level:
            return
        split = self.parser.get_parameter('split')
        if split is not None:
            fermi_level = [v + (-i + 0.5) * split for i, v in enumerate(fermi_level)]
        return self.apply_unit(fermi_level, 'energyunit')

    def parse_method(self):
        sec_method = self.archive.section_run[-1].m_create(Method)
        sec_method.relativity_method = 'pseudo_scalar_relativistic'
        sec_method.electronic_structure_method = 'DFT'

        threshold_energy = self.parser.get_parameter('energyerror')
        sec_method.scf_threshold_energy_change = self.apply_unit(threshold_energy, 'energyunit')

        smearing_width = self.parser.get_smearing_width()
        if smearing_width is not None:
            sec_method.smearing_kind = 'fermi'
            sec_method.smearing_width = self.apply_unit(
                smearing_width, 'energyunit').to('joule').magnitude

        charge = self.parser.get_parameter('charge')
        if charge is not None:
            sec_method.total_charge = int(charge)

        xc_functional = self.parser.get_parameter('xcfunctional')
        for xc in self._xc_map.get(xc_functional, [xc_functional]):
            sec_xc_functionals = sec_method.m_create(XCFunctionals)
            sec_xc_functionals.XC_functional_name = xc

        method_keys = [
            'fix_magnetic_moment', 'fix_density', 'density_convergence_criterion',
            'mix_class', 'mix_beta', 'mix_weight', 'mix_old', 'maximum_angular_momentum',
            'symmetry_time_reversal_switch']
        for key in method_keys:
            val = self.parser.get_parameter(key.replace('_', ''))
            if val is None:
                continue
            setattr(sec_method, 'x_gpaw_%s' % key, val)

    def parse_scc(self):
        sec_run = self.archive.section_run[-1]
        sec_scc = sec_run.m_create(SingleConfigurationCalculation)

        # energies (in gpw, energies are part of parameters)
        energy_keys = [
            'energy_total', 'energy_free', 'energy_XC', 'electronic_kinetic_energy',
            'energy_correction_entropy']
        for key in energy_keys:
            val = self.parser.get_parameter(key)
            if val is not None:
                setattr(sec_scc, key, self.apply_unit(val, 'energyunit'))

        # forces
        forces_key = ['atom_forces_free', 'atom_forces_free_raw']
        for key in forces_key:
            val = self.parser.get_array(key)
            if val is not None:
                energyunit = self.apply_unit(1, 'energyunit').units
                lengthunit = self.apply_unit(1, 'lengthunit').units
                setattr(sec_scc, key, val * energyunit / lengthunit)

        # magnetic moments
        magnetic_moments = self.parser.get_array('magneticmoments')
        if magnetic_moments is not None:
            sec_scc.x_gpaw_magnetic_moments = magnetic_moments
            sec_scc.x_gpaw_fixed_spin_Sz = magnetic_moments.sum() / 2.

        # fermi level
        fermi_level = self.get_fermi_level()
        if fermi_level is not None:
            sec_scc.energy_reference_fermi = fermi_level

        # eigenvalues
        eigenvalues = self.parser.get_array('eigenvalues')
        if eigenvalues is not None:
            sec_eigenvalues = sec_scc.m_create(Eigenvalues)
            sec_eigenvalues.eigenvalues_kind = 'normal'
            sec_eigenvalues.eigenvalues_values = self.apply_unit(eigenvalues, 'energyunit')
            for key in ['occupation', 'kpoints']:
                val = self.parser.get_array(key)
                if val is None:
                    continue
                setattr(sec_eigenvalues, 'eigenvalues_%s' % key, val)

        # band path (TODO only in ulm?)
        band_paths = self.parser.get_array('band_paths')
        if band_paths is not None:
            sec_k_band = sec_scc.m_create(KBand)
            for band_path in band_paths:
                sec_band_seg = sec_k_band.m_create(KBandSegment)
                if band_path.get('eigenvalues', None) is not None:
                    sec_band_seg.band_energies = self.apply_unit(band_path.get(
                        'eigenvalues'), 'energyunit')
                kpoints = band_path.get('kpoints', None)
                if kpoints is not None:
                    sec_band_seg.band_k_points = kpoints
                    sec_band_seg.band_segm_start_end = np.asarray(kpoints[0], kpoints[-1])
                if band_path.get('labels', None) is not None:
                    sec_band_seg.band_segm_labels = band_path.get('labels')

        # volumetric data
        density = self.parser.get_array('density')
        if density is not None:
            cell = self.parser.get_array('unitcell')
            origin = -0.5 * cell.sum(axis=0)
            pbc = self.parser.get_array('boundaryconditions')
            npoints = np.array(density.shape[1:])
            npoints = [(npt + 1) if not pbc[i] else npt for i, npt in enumerate(npoints)]
            displacements = cell / np.array(npoints)
            lengthunit = self.apply_unit(1, 'lengthunit').units
            energyunit = self.apply_unit(1, 'energyunit').units
            for key in ['density', 'potential_effective']:
                val = self.parser.get_array(key)
                if val is None:
                    continue
                sec_vol = sec_scc.m_create(VolumetricData)
                sec_vol.volumetric_data_kind = key
                sec_vol.volumetric_data_origin = (origin * lengthunit).to('m').magnitude
                sec_vol.volumetric_data_displacements = (displacements * lengthunit).to('m').magnitude
                if key == 'density':
                    val = (val / lengthunit ** 3).to('1/m**3')
                else:
                    val = (val * energyunit / lengthunit ** 3).to('J/m**3')
                sec_vol.volumetric_data_values = val.magnitude

        converged = self.parser.get_parameter('converged')
        if converged is not None:
            sec_scc.single_configuration_calculation_converged = converged

        sec_scc.single_configuration_calculation_to_system_ref = sec_run.section_system[-1]
        sec_scc.single_configuration_to_calculation_method_ref = sec_run.section_method[-1]

    def parse_system(self):
        sec_system = self.archive.section_run[-1].m_create(System)

        cell = self.parser.get_array('unitcell')
        if cell is not None:
            cell = self.apply_unit(cell, 'lengthunit')
            sec_system.lattice_vectors = cell
            sec_system.simulation_cell = cell

        sec_system.atom_labels = [
            ase.data.chemical_symbols[z] for z in self.parser.get_array('atomicnumbers')]

        positions = self.parser.get_array('atom_positions')
        sec_system.atom_positions = self.apply_unit(positions, 'lengthunit')

        pbc = [True, True, True] if self.get_mode() == 'pw' else np.array(
            self.parser.get_array('boundaryconditions'), bool)
        sec_system.configuration_periodic_dimensions = pbc

        momenta = self.parser.get_array('momenta')
        if momenta is not None:
            masses = np.array([ase.data.atomic_masses[self.parser.get_array('atomicnumbers')]])
            velocities = momenta / masses.reshape(-1, 1)
            sec_system.atom_velocities = velocities * ase.units.fs / ase.units.Angstrom * ureg.angstrom / ureg.fs

    def parse(self, filepath, archive, logger):
        self.filepath = filepath
        self.archive = archive
        self.logger = logging.getLogger(__name__) if logger is None else logger
        self.init_parser(filepath, logger)

        sec_run = self.archive.m_create(Run)
        sec_run.program_name = 'GPAW'
        sec_run.program_version = self.parser.get_program_version()

        mode = self.get_mode()
        if mode == 'pw':
            sec_run.program_basis_set_type = 'plane waves'
            sec_basis = sec_run.m_create(BasisSetCellDependent)
            pw_cutoff = self.parser.get_parameter('planewavecutoff')
            pw_cutoff = self.apply_unit(pw_cutoff, 'energyunit')
            sec_basis.basis_set_planewave_cutoff = pw_cutoff
            sec_basis.basis_set_cell_dependent_name = self.get_basis_set_name()
        elif mode == 'fd':
            sec_basis = sec_run.m_create(BasisSetCellDependent)
            sec_run.program_basis_set_type = 'real space grid'
            sec_basis.basis_set_cell_dependent_name = self.get_basis_set_name()
        elif mode == 'lcao':
            sec_run.program_basis_set_type = 'numeric AOs'
            sec_basis = sec_run.m_create(BasisSetAtomCentered)
            sec_basis.basis_set_atom_centered_short_name = self.get_basis_set_name()

        sec_sampling_method = sec_run.m_create(SamplingMethod)
        sec_sampling_method.sampling_method = 'geometry_optimization'
        sec_sampling_method.ensemble_type = 'NVE'

        self.parse_method()

        self.parse_system()

        self.parse_scc()
