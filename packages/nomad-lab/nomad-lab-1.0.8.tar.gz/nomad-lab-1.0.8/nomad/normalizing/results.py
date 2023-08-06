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

import re
import numpy as np
from typing import Dict, List, Union, Any, Set
import ase.data
from ase import Atoms
from matid import SymmetryAnalyzer
import matid.geometry

from nomad import config
from nomad.units import ureg
from nomad import atomutils
from nomad.utils import deep_get
from nomad.normalizing.normalizer import Normalizer
from nomad.normalizing.method import MethodNormalizer
from nomad.normalizing.material import MaterialNormalizer
from nomad.datamodel.optimade import Species
from nomad.datamodel.metainfo.simulation.system import System, Symmetry as SystemSymmetry
from nomad.datamodel.results import (
    BandGap,
    Results,
    Material,
    Method,
    GeometryOptimization,
    Properties,
    Structures,
    Structure,
    StructureOriginal,
    StructurePrimitive,
    StructureConventional,
    StructureOptimized,
    LatticeParameters,
    WyckoffSet,
    EnergyVolumeCurve,
    BulkModulus,
    ShearModulus,
    MechanicalProperties,
    ElectronicProperties,
    VibrationalProperties,
    BandStructureElectronic,
    BandStructurePhonon,
    DOSElectronic,
    DOSPhonon,
    EnergyFreeHelmholtz,
    HeatCapacityConstantVolume
)

re_label = re.compile("^([a-zA-Z][a-zA-Z]?)[^a-zA-Z]*")
elements = set(ase.data.chemical_symbols)


def valid_array(array: Any) -> bool:
    """Checks if the given variable is a non-empty array.
    """
    return array is not None and len(array) > 0


def isint(value: Any) -> bool:
    """Checks if the given variable can be interpreted as an integer.
    """
    try:
        int(value)
        return True
    except ValueError:
        return False


class ResultsNormalizer(Normalizer):
    domain = None

    def normalize(self, logger=None) -> None:
        # Setup logger
        if logger is not None:
            self.logger = logger.bind(normalizer=self.__class__.__name__)

        results = self.entry_archive.results
        if results is None:
            results = self.entry_archive.m_create(Results)
        if results.properties is None:
            results.m_create(Properties)

        if self.section_run:
            self.normalize_run(logger=self.logger)

        for measurement in self.entry_archive.measurement:
            self.normalize_measurement(measurement, logger=self.logger)

        # Add the list of available_properties: it is a selected subset of the
        # stored properties.
        available_property_names = {
            "properties.electronic.band_structure_electronic.band_gap": "electronic.band_structure_electronic.band_gap",
            "properties.electronic.band_structure_electronic": "band_structure_electronic",
            "properties.electronic.dos_electronic": "dos_electronic",
            "properties.vibrational.dos_phonon": "dos_phonon",
            "properties.vibrational.band_structure_phonon": "band_structure_phonon",
            "properties.vibrational.energy_free_helmholtz": "energy_free_helmholtz",
            "properties.vibrational.heat_capacity_constant_volume": "heat_capacity_constant_volume",
            "properties.geometry_optimization": "geometry_optimization",
            "properties.mechanical.bulk_modulus": "bulk_modulus",
            "properties.mechanical.shear_modulus": "shear_modulus",
            "properties.mechanical.energy_volume_curve": "energy_volume_curve",
            "properties.spectroscopy.eels": "eels",
        }
        available_properties: List[str] = []
        for path, shortcut in available_property_names.items():
            if deep_get(results, *path.split(".")) is not None:
                available_properties.append(shortcut)
        results.properties.available_properties = sorted(available_properties)

    def normalize_measurement(self, measurement, logger) -> None:
        results = self.entry_archive.results

        # Method
        if results.method is None:
            results.method = Method(
                method_name=measurement.method_abbreviation)

        # Material
        if results.material is None:
            results.material = Material()
        material = results.material
        if len(measurement.sample) > 0:
            sample = measurement.sample[0]
            if len(sample.elements) > 0:
                material.elements = sample.elements
            else:
                # Try to guess elements from sample formula or name
                if sample.chemical_formula:
                    try:
                        material.elements = ase.Atoms(sample.chemical_formula).get_chemical_symbols()
                    except Exception:
                        if sample.name:
                            try:
                                material.elements = ase.Atoms(sample.name).get_chemical_symbols()
                            except Exception:
                                pass

            if sample.chemical_formula:
                material.chemical_formula_descriptive = sample.chemical_formula

        try:
            material.elements = material.elements if material.elements else []
            atoms = None
            if material.chemical_formula_descriptive:
                try:
                    atoms = ase.Atoms(material.chemical_formula_descriptive)
                except Exception as e:
                    logger.warn('could not normalize formula, using elements next', exc_info=e)

            if atoms is None:
                atoms = ase.Atoms(''.join(material.elements))

            formula = atoms.get_chemical_formula()
            if formula:
                results.material.chemical_formula_hill = atomutils.get_formula_hill(formula)
                results.material.chemical_formula_descriptive = results.material.chemical_formula_hill
                results.material.chemical_formula_reduced = atoms.get_chemical_formula(mode='reduce')
        except Exception as e:
            logger.warn('could not normalize material', exc_info=e)

    def normalize_run(self, logger=None) -> None:
        # Fetch different information resources from which data is gathered
        repr_system = None
        for section in self.section_run.system:
            if section.is_representative:
                repr_system = section
                break
        try:
            optimade = self.entry_archive.metadata.optimade
        except Exception:
            optimade = None

        repr_symmetry = None
        if repr_system and repr_system.symmetry:
            repr_symmetry = repr_system.symmetry[0]

        # Create the section and populate the subsections
        results = self.entry_archive.results
        properties, conv_atoms, wyckoff_sets, spg_number = self.properties(repr_system, repr_symmetry)
        results.properties = properties
        results.material = MaterialNormalizer(
            self.entry_archive,
            repr_system,
            repr_symmetry,
            spg_number,
            conv_atoms,
            wyckoff_sets,
            optimade,
            logger
        ).material()
        results.method = MethodNormalizer(self.entry_archive, repr_system, results.material, logger).method()

    def species(self, labels: List[str], atomic_numbers: List[int], struct: Structure) -> None:
        """Given a list of species labels, creates the corresponding Species
        sections in the given structure.
        """
        if labels is None or atomic_numbers is None:
            return
        species: Set[str] = set()
        for label, atomic_number in zip(labels, atomic_numbers):
            if label not in species:
                species.add(label)
                i_species = struct.m_create(Species)
                i_species.name = label
                try:
                    symbol = atomutils.chemical_symbols([atomic_number])[0]
                except ValueError:
                    self.logger.info("could not identify chemical symbol for atomic number {}".format(atomic_number))
                else:
                    i_species.chemical_symbols = [symbol]
                i_species.concentration = [1.0]

    def band_structure_electronic(self) -> Union[BandStructureElectronic, None]:
        """Returns a new section containing an electronic band structure. In
        the case of multiple valid band structures, only the latest one is
        considered.

       Band structure is reported only under the following conditions:
          - There is a non-empty array of kpoints.
          - There is a non-empty array of energies.
        """
        path = ["run", "calculation", "band_structure_electronic"]
        for bs in self.traverse_reversed(path):
            if not bs.segment:
                continue
            valid = True
            for segment in bs.segment:
                energies = segment.energies
                k_points = segment.kpoints
                if not valid_array(energies) or not valid_array(k_points):
                    valid = False
                    break
            if valid:
                # Fill band structure data to the newer, improved data layout
                bs_new = BandStructureElectronic()
                bs_new.reciprocal_cell = bs
                bs_new.segment = bs.segment
                bs_new.spin_polarized = bs_new.segment[0].energies.shape[0] > 1
                bs_new.energy_fermi = bs.energy_fermi
                for info in bs.band_gap:
                    info_new = bs_new.m_create(BandGap)
                    info_new.index = info.index
                    info_new.value = info.value
                    info_new.type = info.type
                    info_new.energy_highest_occupied = info.energy_highest_occupied
                    info_new.energy_lowest_unoccupied = info.energy_lowest_unoccupied
                return bs_new

        return None

    def dos_electronic(self) -> Union[DOSElectronic, None]:
        """Returns a reference to the section containing an electronic dos. In
        the case of multiple valid DOSes, only the latest one is reported.

       DOS is reported only under the following conditions:
          - There is a non-empty array of dos_values_normalized.
          - There is a non-empty array of dos_energies.
        """
        path = ["run", "calculation", "dos_electronic"]
        for dos in self.traverse_reversed(path):
            energies = dos.energies
            values = np.array([d.value.magnitude for d in dos.total])
            if valid_array(energies) and valid_array(values):
                dos_new = DOSElectronic()
                dos_new.energies = dos
                dos_new.total = dos.total
                n_channels = values.shape[0]
                dos_new.spin_polarized = n_channels > 1
                dos_new.energy_fermi = dos.energy_fermi
                for info in dos.band_gap:
                    info_new = dos_new.m_create(BandGap)
                    info_new.index = info.index
                    info_new.energy_highest_occupied = info.energy_highest_occupied
                    info_new.energy_lowest_unoccupied = info.energy_lowest_unoccupied
                return dos_new

        return None

    def band_structure_phonon(self) -> Union[BandStructurePhonon, None]:
        """Returns a new section containing a phonon band structure. In
        the case of multiple valid band structures, only the latest one is
        considered.

       Band structure is reported only under the following conditions:
          - There is a non-empty array of kpoints.
          - There is a non-empty array of energies.
        """
        path = ["run", "calculation", "band_structure_phonon"]
        for bs in self.traverse_reversed(path):
            if not bs.segment:
                continue
            valid = True
            for segment in bs.segment:
                energies = segment.energies
                k_points = segment.kpoints
                if not valid_array(energies) or not valid_array(k_points):
                    valid = False
                    break
            if valid:
                # Fill band structure data to the newer, improved data layout
                bs_new = BandStructurePhonon()
                bs_new.segment = bs.segment
                return bs_new

        return None

    def dos_phonon(self) -> Union[DOSPhonon, None]:
        """Returns a section containing phonon dos data. In the case of
        multiple valid data sources, only the latest one is reported.

       DOS is reported only under the following conditions:
          - There is a non-empty array of values.
          - There is a non-empty array of energies.
        """
        path = ["run", "calculation", "dos_phonon"]
        for dos in self.traverse_reversed(path):
            energies = dos.energies
            values = np.array([d.value.magnitude for d in dos.total])
            if valid_array(energies) and valid_array(values):
                dos_new = DOSPhonon()
                dos_new.energies = dos
                dos_new.total = dos.total
                return dos_new

        return None

    def energy_free_helmholtz(self) -> Union[EnergyFreeHelmholtz, None]:
        """Returns a section Helmholtz free energy data. In the case of
        multiple valid data sources, only the latest one is reported.

       Helmholtz free energy is reported only under the following conditions:
          - There is a non-empty array of temperatures.
          - There is a non-empty array of energies.
        """
        path = ["workflow", "thermodynamics"]
        for thermo_prop in self.traverse_reversed(path):
            temperatures = thermo_prop.temperature
            energies = thermo_prop.vibrational_free_energy_at_constant_volume
            if valid_array(temperatures) and valid_array(energies):
                energy_free = EnergyFreeHelmholtz()
                energy_free.energies = thermo_prop
                energy_free.temperatures = thermo_prop
                return energy_free

        return None

    def heat_capacity_constant_volume(self) -> Union[HeatCapacityConstantVolume, None]:
        """Returns a section containing heat capacity data. In the case of
        multiple valid data sources, only the latest one is reported.

       Heat capacity is reported only under the following conditions:
          - There is a non-empty array of temperatures.
          - There is a non-empty array of energies.
        """
        path = ["workflow", "thermodynamics"]
        for thermo_prop in self.traverse_reversed(path):
            temperatures = thermo_prop.temperature
            heat_capacities = thermo_prop.heat_capacity_c_v
            if valid_array(temperatures) and valid_array(heat_capacities):
                heat_cap = HeatCapacityConstantVolume()
                heat_cap.heat_capacities = thermo_prop
                heat_cap.temperatures = thermo_prop
                return heat_cap

        return None

    def geometry_optimization(self) -> Union[GeometryOptimization, None]:
        """Populates both geometry optimization methodology and calculated
        properties based on the first found geometry optimization workflow.
        """
        path = ["workflow"]
        for workflow in self.traverse_reversed(path):
            # Check validity
            if workflow.type == "geometry_optimization" and workflow.calculations_ref:

                geo_opt = GeometryOptimization()
                geo_opt_wf = workflow.geometry_optimization
                geo_opt.trajectory = workflow.calculations_ref
                system_ref = workflow.calculation_result_ref.system_ref
                structure_optimized = self.nomad_system_to_structure(StructureOptimized, system_ref)
                if structure_optimized:
                    geo_opt.structure_optimized = structure_optimized
                if geo_opt_wf is not None:
                    geo_opt.type = geo_opt_wf.type
                    geo_opt.convergence_tolerance_energy_difference = geo_opt_wf.convergence_tolerance_energy_difference
                    geo_opt.convergence_tolerance_force_maximum = geo_opt_wf.convergence_tolerance_force_maximum
                    if geo_opt_wf.energies is not None:
                        geo_opt.energies = geo_opt_wf
                    geo_opt.final_energy_difference = geo_opt_wf.final_energy_difference
                    geo_opt.final_force_maximum = geo_opt_wf.final_force_maximum
                    geo_opt.final_displacement_maximum = geo_opt_wf.final_displacement_maximum
                return geo_opt

        return None

    def properties(
            self,
            repr_system: System,
            repr_symmetry: SystemSymmetry) -> tuple:
        """Returns a populated Properties subsection."""
        properties = Properties()

        # Structures
        struct_orig = None
        struct_prim = None
        struct_conv = None
        conv_atoms = None
        wyckoff_sets = None
        spg_number = None
        if repr_system:
            original_atoms = repr_system.m_cache.get("representative_atoms")
            if original_atoms:
                prim_atoms = None
                structural_type = repr_system.type
                if structural_type == "bulk":
                    conv_atoms, prim_atoms, wyckoff_sets, spg_number = self.structures_bulk(repr_symmetry)
                elif structural_type == "2D":
                    conv_atoms, prim_atoms, wyckoff_sets, spg_number = self.structures_2d(original_atoms)
                elif structural_type == "1D":
                    conv_atoms, prim_atoms = self.structures_1d(original_atoms)

                struct_orig = self.ase_atoms_to_structure(StructureOriginal, original_atoms)
                struct_prim = self.ase_atoms_to_structure(StructurePrimitive, prim_atoms)
                wyckoff_sets_serialized = wyckoff_sets if structural_type == "bulk" else None
                struct_conv = self.ase_atoms_to_structure(StructureConventional, conv_atoms, wyckoff_sets_serialized)

        if struct_orig or struct_prim or struct_conv:
            structures = Structures()
            if struct_conv:
                structures.structure_conventional = struct_conv
            if struct_prim:
                structures.structure_primitive = struct_prim
            if struct_orig:
                structures.structure_original = struct_orig
            properties.structures = structures

        # Electronic
        bs_electronic = self.band_structure_electronic()
        dos_electronic = self.dos_electronic()
        if bs_electronic or dos_electronic:
            electronic = ElectronicProperties()
            if bs_electronic:
                electronic.band_structure_electronic = bs_electronic
            if dos_electronic:
                electronic.dos_electronic = dos_electronic
            properties.electronic = electronic

        # Vibrational
        bs_phonon = self.band_structure_phonon()
        dos_phonon = self.dos_phonon()
        energy_free = self.energy_free_helmholtz()
        heat_cap = self.heat_capacity_constant_volume()
        if bs_phonon or dos_phonon or energy_free or heat_cap:
            vibrational = VibrationalProperties()
            if dos_phonon:
                vibrational.dos_phonon = dos_phonon
            if bs_phonon:
                vibrational.band_structure_phonon = bs_phonon
            if energy_free:
                vibrational.energy_free_helmholtz = energy_free
            if heat_cap:
                vibrational.heat_capacity_constant_volume = heat_cap
            properties.vibrational = vibrational

        # Mechanical
        energy_volume_curves = self.energy_volume_curves()
        bulk_modulus = self.bulk_modulus()
        shear_modulus = self.shear_modulus()
        geometry_optimization = self.geometry_optimization()
        if energy_volume_curves or bulk_modulus or shear_modulus or geometry_optimization:
            mechanical = MechanicalProperties()
            for ev in energy_volume_curves:
                mechanical.m_add_sub_section(MechanicalProperties.energy_volume_curve, ev)
            for bm in bulk_modulus:
                mechanical.m_add_sub_section(MechanicalProperties.bulk_modulus, bm)
            for sm in shear_modulus:
                mechanical.m_add_sub_section(MechanicalProperties.shear_modulus, sm)
            properties.mechanical = mechanical

        # Geometry optimization
        properties.geometry_optimization = self.geometry_optimization()

        try:
            n_calc = len(self.section_run.calculation)
        except Exception:
            n_calc = 0
        properties.n_calculations = n_calc

        return properties, conv_atoms, wyckoff_sets, spg_number

    def wyckoff_sets(self, struct: StructureConventional, wyckoff_sets: Dict) -> None:
        """Populates the Wyckoff sets in the given structure.
        """
        for group in wyckoff_sets:
            wset = struct.m_create(WyckoffSet)
            if group.x is not None or group.y is not None or group.z is not None:
                if group.x is not None:
                    wset.x = float(group.x)
                if group.y is not None:
                    wset.y = float(group.y)
                if group.z is not None:
                    wset.z = float(group.z)
            wset.indices = group.indices
            wset.element = group.element
            wset.wyckoff_letter = group.wyckoff_letter

    def structures_bulk(self, repr_symmetry):
        """The symmetry of bulk structures has already been analyzed. Here we
        use the cached results.
        """
        conv_atoms = None
        prim_atoms = None
        wyckoff_sets = None
        spg_number = None
        if repr_symmetry:
            symmetry_analyzer = repr_symmetry.m_cache.get("symmetry_analyzer")
            if symmetry_analyzer:
                spg_number = symmetry_analyzer.get_space_group_number()
                conv_atoms = symmetry_analyzer.get_conventional_system()
                prim_atoms = symmetry_analyzer.get_primitive_system()

                # For some reason MatID seems to drop the periodicity, reintroduce it here.
                conv_atoms.set_pbc(True)
                prim_atoms.set_pbc(True)
                try:
                    wyckoff_sets = symmetry_analyzer.get_wyckoff_sets_conventional(return_parameters=True)
                except Exception:
                    self.logger.error('Error resolving Wyckoff sets.')
                    wyckoff_sets = []

        return conv_atoms, prim_atoms, wyckoff_sets, spg_number

    def structures_2d(self, original_atoms):
        conv_atoms = None
        prim_atoms = None
        wyckoff_sets = None
        spg_number = None
        try:
            # Get dimension of system by also taking into account the covalent radii
            dimensions = matid.geometry.get_dimensions(original_atoms, [True, True, True])
            basis_dimensions = np.linalg.norm(original_atoms.get_cell(), axis=1)
            gaps = basis_dimensions - dimensions
            periodicity = gaps <= config.normalize.cluster_threshold

            # If two axis are not periodic, return. This only happens if the vacuum
            # gap is not aligned with a cell vector or if the linear gap search is
            # unsufficient (the structure is "wavy" making also the gap highly
            # nonlinear).
            if sum(periodicity) != 2:
                self.logger.error("could not detect the periodic dimensions in a 2D system")
                return conv_atoms, prim_atoms, wyckoff_sets, spg_number

            # Center the system in the non-periodic direction, also taking
            # periodicity into account. The get_center_of_mass()-function in MatID
            # takes into account periodicity and can produce the correct CM unlike
            # the similar function in ASE.
            pbc_cm = matid.geometry.get_center_of_mass(original_atoms)
            cell_center = 0.5 * np.sum(original_atoms.get_cell(), axis=0)
            translation = cell_center - pbc_cm
            symm_system = original_atoms.copy()
            symm_system.translate(translation)
            symm_system.wrap()

            # Set the periodicity according to detected periodicity in order
            # for SymmetryAnalyzer to use the symmetry analysis designed for 2D
            # systems.
            symm_system.set_pbc(periodicity)
            symmetry_analyzer = SymmetryAnalyzer(
                symm_system,
                config.normalize.symmetry_tolerance,
                config.normalize.flat_dim_threshold
            )

            spg_number = symmetry_analyzer.get_space_group_number()
            wyckoff_sets = symmetry_analyzer.get_wyckoff_sets_conventional(return_parameters=False)
            conv_atoms = symmetry_analyzer.get_conventional_system()
            prim_atoms = symmetry_analyzer.get_primitive_system()

            # Reduce cell size to just fit the system in the non-periodic
            # dimensions.
            conv_atoms = atomutils.get_minimized_structure(conv_atoms)
            prim_atoms = atomutils.get_minimized_structure(prim_atoms)

            # Swap the cell axes so that the non-periodic one is always the
            # last basis (=c)
            swap_dim = 2
            for i, periodic in enumerate(conv_atoms.get_pbc()):
                if not periodic:
                    non_periodic_dim = i
                    break
            if non_periodic_dim != swap_dim:
                atomutils.swap_basis(conv_atoms, non_periodic_dim, swap_dim)
                atomutils.swap_basis(prim_atoms, non_periodic_dim, swap_dim)
        except Exception as e:
            self.logger.error(
                'could not construct a conventional system for a 2D material',
                exc_info=e
            )

        return conv_atoms, prim_atoms, wyckoff_sets, spg_number

    def structures_1d(self, original_atoms):
        conv_atoms = None
        prim_atoms = None
        try:
            # First get a symmetry analyzer and the primitive system
            symm_system = original_atoms.copy()
            symm_system.set_pbc(True)
            symmetry_analyzer = SymmetryAnalyzer(
                symm_system,
                config.normalize.symmetry_tolerance,
                config.normalize.flat_dim_threshold
            )
            prim_atoms = symmetry_analyzer.get_primitive_system()
            prim_atoms.set_pbc(True)

            # Get dimension of system by also taking into account the covalent radii
            dimensions = matid.geometry.get_dimensions(prim_atoms, [True, True, True])
            basis_dimensions = np.linalg.norm(prim_atoms.get_cell(), axis=1)
            gaps = basis_dimensions - dimensions
            periodicity = gaps <= config.normalize.cluster_threshold

            # If one axis is not periodic, return. This only happens if the vacuum
            # gap is not aligned with a cell vector.
            if sum(periodicity) != 1:
                self.logger.error("could not detect the periodic dimensions in a 1D system")
                return conv_atoms, prim_atoms

            # Translate to center of mass
            conv_atoms = prim_atoms.copy()
            pbc_cm = matid.geometry.get_center_of_mass(prim_atoms)
            cell_center = 0.5 * np.sum(conv_atoms.get_cell(), axis=0)
            translation = cell_center - pbc_cm
            translation[periodicity] = 0
            conv_atoms.translate(translation)
            conv_atoms.wrap()
            conv_atoms.set_pbc(periodicity)

            # Reduce cell size to just fit the system in the non-periodic dimensions.
            conv_atoms = atomutils.get_minimized_structure(conv_atoms)

            # Swap the cell axes so that the periodic one is always the first
            # basis (=a)
            swap_dim = 0
            for i, periodic in enumerate(periodicity):
                if periodic:
                    periodic_dim = i
                    break
            if periodic_dim != swap_dim:
                atomutils.swap_basis(conv_atoms, periodic_dim, swap_dim)

            prim_atoms = conv_atoms
        except Exception as e:
            self.logger.error(
                'could not construct a conventional system for a 1D material',
                exc_info=e
            )
        return conv_atoms, prim_atoms

    def ase_atoms_to_structure(self, structure_class, atoms: Atoms, wyckoff_sets: dict = None):
        """Returns a populated instance of the given structure class from an
        ase.Atoms-object.
        """
        if not atoms or not structure_class:
            return None
        struct = structure_class()
        struct.species_at_sites = atoms.get_chemical_symbols()
        self.species(atoms.get_chemical_symbols(), atoms.get_atomic_numbers(), struct)
        struct.cartesian_site_positions = atoms.get_positions() * ureg.angstrom
        lattice_vectors = atoms.get_cell()
        if lattice_vectors is not None:
            lattice_vectors = (lattice_vectors * ureg.angstrom).to(ureg.meter).magnitude
            struct.dimension_types = [1 if x else 0 for x in atoms.get_pbc()]
            struct.lattice_vectors = lattice_vectors
            cell_volume = atomutils.get_volume(lattice_vectors)
            struct.cell_volume = cell_volume
            if atoms.get_pbc().all() and cell_volume:
                mass = atomutils.get_summed_atomic_mass(atoms.get_atomic_numbers())
                struct.mass_density = mass / cell_volume
                struct.atomic_density = len(atoms) / cell_volume
            if wyckoff_sets:
                self.wyckoff_sets(struct, wyckoff_sets)
            struct.lattice_parameters = self.lattice_parameters(lattice_vectors)
        return struct

    def nomad_system_to_structure(self, structure_class, system: System) -> Structure:
        """Returns a populated instance of the given structure class from a
        NOMAD System-section.
        """
        if not system or not structure_class:
            return None

        struct = structure_class()
        struct.cartesian_site_positions = system.atoms.positions
        struct.species_at_sites = system.atoms.labels
        self.species(system.atoms.labels, system.atoms.species, struct)
        lattice_vectors = system.atoms.lattice_vectors
        if lattice_vectors is not None:
            lattice_vectors = lattice_vectors.magnitude
            struct.dimension_types = np.array(system.atoms.periodic).astype(int)
            struct.lattice_vectors = lattice_vectors
            cell_volume = atomutils.get_volume(lattice_vectors)
            struct.cell_volume = cell_volume
            if all(system.atoms.periodic) and cell_volume:
                if system.atoms.species is not None:
                    mass = atomutils.get_summed_atomic_mass(system.atoms.species)
                    struct.mass_density = mass / cell_volume
                struct.atomic_density = len(system.atoms.labels) / cell_volume
            struct.lattice_parameters = self.lattice_parameters(lattice_vectors)
        return struct

    def lattice_parameters(self, lattice_vectors) -> LatticeParameters:
        """Converts the given cell into LatticeParameters. Undefined angle
        values are not stored.
        """
        param_values = atomutils.cell_to_cellpar(lattice_vectors)
        params = LatticeParameters()
        params.a = float(param_values[0])
        params.b = float(param_values[1])
        params.c = float(param_values[2])
        alpha = float(param_values[3])
        params.alpha = None if np.isnan(alpha) else alpha
        beta = float(param_values[4])
        params.beta = None if np.isnan(beta) else beta
        gamma = float(param_values[5])
        params.gamma = None if np.isnan(gamma) else gamma
        return params

    def energy_volume_curves(self) -> List[EnergyVolumeCurve]:
        """Returns a list containing the found EnergyVolumeCurves.
        """
        workflows = self.entry_archive.workflow
        ev_curves = []
        for workflow in workflows:
            # Equation of state must be present
            equation_of_state = workflow.equation_of_state
            if not equation_of_state:
                continue

            # Volumes must be present
            volumes = equation_of_state.volumes
            if not valid_array(volumes):
                self.logger.warning("missing eos volumes")
                continue

            # Raw EV curve
            energies_raw = equation_of_state.energies
            if valid_array(energies_raw):
                ev_curves.append(EnergyVolumeCurve(
                    type="raw",
                    volumes=equation_of_state,
                    energies_raw=equation_of_state,
                ))
            else:
                self.logger.warning("missing eos energies")

            # Fitted EV curves
            fits = equation_of_state.eos_fit
            if not fits:
                continue
            for fit in fits:
                energies_fitted = fit.fitted_energies
                function_name = fit.function_name
                if valid_array(energies_fitted):
                    ev_curves.append(EnergyVolumeCurve(
                        type=function_name,
                        volumes=equation_of_state,
                        energies_fit=fit,
                    ))

        return ev_curves

    def bulk_modulus(self) -> List[BulkModulus]:
        """Returns a list containing the found BulkModulus.
        """
        workflows = self.entry_archive.workflow
        bulk_modulus = []
        for workflow in workflows:
            # From elastic workflow
            elastic = workflow.elastic
            if elastic:
                bulk_modulus_vrh = elastic.bulk_modulus_hill
                if bulk_modulus_vrh:
                    bulk_modulus.append(BulkModulus(
                        type="voigt_reuss_hill_average",
                        value=bulk_modulus_vrh,
                    ))
                bulk_modulus_voigt = elastic.bulk_modulus_voigt
                if bulk_modulus_voigt:
                    bulk_modulus.append(BulkModulus(
                        type="voigt_average",
                        value=bulk_modulus_voigt,
                    ))
                bulk_modulus_reuss = elastic.bulk_modulus_reuss
                if bulk_modulus_reuss:
                    bulk_modulus.append(BulkModulus(
                        type="reuss_average",
                        value=bulk_modulus_reuss,
                    ))

            # From energy-volume curve fit
            equation_of_state = workflow.equation_of_state
            if equation_of_state:
                fits = equation_of_state.eos_fit
                if not fits:
                    continue
                for fit in fits:
                    modulus = fit.bulk_modulus
                    function_name = fit.function_name
                    if modulus is not None and function_name:
                        bulk_modulus.append(BulkModulus(
                            type=function_name,
                            value=modulus,
                        ))
                    else:
                        self.logger.warning("missing eos fitted energies and/or function name")

        return bulk_modulus

    def shear_modulus(self) -> List[ShearModulus]:
        """Returns a list containing the found ShearModulus.
        """
        workflows = self.entry_archive.workflow
        shear_modulus = []
        for workflow in workflows:
            # From elastic workflow
            elastic = workflow.elastic
            if elastic:
                shear_modulus_vrh = elastic.shear_modulus_hill
                if shear_modulus_vrh:
                    shear_modulus.append(ShearModulus(
                        type="voigt_reuss_hill_average",
                        value=shear_modulus_vrh,
                    ))
                shear_modulus_voigt = elastic.shear_modulus_voigt
                if shear_modulus_voigt:
                    shear_modulus.append(ShearModulus(
                        type="voigt_average",
                        value=shear_modulus_voigt,
                    ))
                shear_modulus_reuss = elastic.shear_modulus_reuss
                if shear_modulus_reuss:
                    shear_modulus.append(ShearModulus(
                        type="reuss_average",
                        value=shear_modulus_reuss,
                    ))

        return shear_modulus

    def traverse_reversed(self, path: List[str]) -> Any:
        """Traverses the given metainfo path in reverse order. Useful in
        finding the latest reported section or value.
        """
        def traverse(root, path, i):
            sections = getattr(root, path[i])
            if isinstance(sections, list):
                for section in reversed(sections):
                    if i == len(path) - 1:
                        yield section
                    else:
                        for s in traverse(section, path, i + 1):
                            yield s
            else:
                if i == len(path) - 1:
                    yield sections
                else:
                    for s in traverse(sections, path, i + 1):
                        yield s
        for t in traverse(self.entry_archive, path, 0):
            if t is not None:
                yield t
