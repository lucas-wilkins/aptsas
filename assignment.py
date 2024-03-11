from typing import Sequence
from collections import defaultdict

import os
import pickle

import numpy as np
import periodictable

from input_data import PosDataBaseClass
from ion_slds import molecular_sld
from plotting import show_sample

class ParseError(Exception):
    pass

class LineCounter:
    """ Use for counting lines so that useful errors can be given"""
    def __init__(self, fid, verbose=False, max_lines=1000):
        self.fid = fid
        self.line_no = 0
        self.line = ""
        self.verbose = verbose
        self.max_lines = max_lines

    def next(self):
        line = self.fid.readline()

        # Check for EOF
        if line == "":
            if self.verbose:
                print(f" --- Last Line: {self.line_no} ---")
            raise StopIteration()

        self.line = line.strip()
        self.line_no += 1

        if self.verbose:
            print(f"{self.line_no}: {self.line}")

        if self.line_no > self.max_lines:
            raise ParseError("Max line count reached")

        return self.line


class Assignment:

    """ Object to assigned tomography data"""
    def __init__(self,
                 filename: str,
                 coordinates_and_mz: dict[str, np.ndarray],
                 countwise_element_ratios: dict[str, float],
                 slds: dict[str, float],
                 sld_times_volumes: dict[str, float],
                 ions_to_atoms: dict[str, list[tuple[str, int]]]):

        self.filename = filename
        self.coordinates_and_mz = coordinates_and_mz
        self.countwise_element_ratios = countwise_element_ratios
        self.slds = slds
        self.sld_times_volumes = sld_times_volumes
        self.ions_to_atoms = ions_to_atoms

    @property
    def coordinates(self) -> dict[str, np.ndarray]:
        """ Coordinates of a given ion type"""
        return {el: self.coordinates_and_mz[el][:,:3] for el in self.coordinates_and_mz}

    def show_ion_plot(self, ion: str, autoshow: bool=True, n: int = 10_000):
        data = self.coordinates_and_mz[ion]
        show_sample(data, autoshow=autoshow, n=n, name=ion)


    def show_ion_plots(self, autoshow: bool=True, n: int = 10_000):
        import matplotlib.pyplot as plt

        for ion in self.coordinates_and_mz:
            data = self.coordinates_and_mz[ion]
            show_sample(data, autoshow=False, n=n, name=ion)

        if autoshow:
            plt.show()

    @property
    def ions(self):
        return [key for key in self.coordinates_and_mz.keys()]

    def __repr__(self):
        el_frac = reversed(sorted(self.countwise_element_ratios.items(), key=lambda x: x[1]))
        pretty = ["%s(%i%%)"%(el, int(100*frac)) if frac > 0.01 else el for el, frac in el_frac]
        comp_string = " ".join(pretty)
        return f"Assignment({self.filename}, {comp_string})"

    def write_files(self, path: str, verbose=False):

        if not os.path.exists(path):
            try:
                os.mkdir(path)
            except:
                raise FileNotFoundError(f"No parent directory for creating '{path}'")

        if os.path.isdir(path):

            for ion in self.ions:

                filename = os.path.join(path, ion + ".xyz")

                if verbose:
                    print("Writing", filename)

                with open(filename, 'wb') as fid:
                    write_data = self.coordinates[ion].astype(dtype=float)
                    write_data.tofile(fid)

            filename = os.path.join(path, "metadata.pickle")

            with open(filename, 'wb') as fid:
                pickle.dump(self.ions_to_atoms, fid)

            if verbose:
                print("Writing", filename)


        else:
            raise ValueError("Expected to be given a directory")



class Assigner:
    """ m/z assignment based on an .rrng file, reads a .rrng file and provides the `assign`
     method to apply the assigment"""
    def __init__(self, filename: str, verbose=False):

        self.elements: list[str] = []

        self.ranges: dict[str, list[tuple[float, float]]] = defaultdict(list)
        self.volumes: dict[str, float] = {}    # Volumes of ions
        self.slds: dict[str, float] = {}       # SLDs
        self.sld_volume: dict[str, float] = {} # SLDs x volume
        self.elemental_ion_breakdown: dict[str, list[tuple[str, int]]] = {} # machine friendly ion representation

        # Load the data, file looks toml like, but it's not toml
        with open(filename, 'r') as fid:

            counter = LineCounter(fid, verbose=verbose)

            try:

                while not counter.line.startswith("[Ions]"):
                    counter.next()
                    # print(counter.line)

                counter.next()  # Skip "Number=" line
                counter.next()  # ...and load the next one ready for the check

                while not counter.line.startswith("[Ranges]"):
                    self.elements.append(counter.line.strip().split("=")[1])
                    counter.next()

                # Line should now be the [Ranges] line
                counter.next() # Skip to the "Number=" line

                # Create the categorisation

                # while loop should be exited by StopIteration or by hitting max counter
                while True:

                    # Do .next first because we still have a line to skip, and because doing
                    # it at the start of a loop is a more maintainable place
                    counter.next()

                    # Ignore blank likes
                    if counter.line == "":
                        continue

                    # Store the line data:
                    # The format isn't quite optimal for what we want to do with it
                    # We want to know if we have a single ion or a cluster

                    after_eq = counter.line.split("=")[1]
                    tokens = after_eq.split()

                    start = float(tokens[0])
                    stop = float(tokens[1])

                    volume = 0.0

                    # Get the composition

                    components: list[tuple[str, int]] = []

                    for token in tokens[2:]:
                        if token.startswith("Vol:"):
                            volume = float(tokens[2].split(":")[1])
                            continue

                        if token.startswith("Color:"):
                            # Ignore this one
                            continue

                        parts = token.split(":")

                        element = parts[0]
                        count = int(parts[1])

                        components.append((element, count))



                    # Sort element symbols alphabetically, so make sure we have a unique representation of the ion
                    components = sorted(components, key=lambda x: x[0])

                    formula = "".join([el + str(n if n > 1 else "") for el, n in components])

                    self.volumes[formula] = volume
                    self.ranges[formula].append((start, stop))
                    self.elemental_ion_breakdown[formula] = components
                    self.slds[formula] = molecular_sld(components)

                    self.sld_volume[formula] = self.slds[formula] * self.volumes[formula]


            except StopIteration:
                pass # A good place to stop

            except Exception as e:

                raise ParseError(f"Parsing failed on line {counter.line_no}: '{counter.line.strip()}' -- {e}")



    def __repr__(self):
        s = ", ".join(self.elements)
        return f"{self.__class__.__name__}({s})"

    def assign(self, pos: PosDataBaseClass):
        """ Apply the assignment to X,Y,Z,M/Z data (takes a PosData object)"""

        # Do the main assignment

        assigned_raw = defaultdict(list)

        for ion in self.ranges:
            for start, stop in self.ranges[ion]:
                inds = np.logical_and(
                    pos.data[:, 3] >= start,
                    pos.data[:, 3] <= stop)

                if np.sum(inds) > 0:
                    assigned_raw[ion].append(pos.data[inds, :])

        assigned = {ion: np.concatenate(assigned_raw[ion]) for ion in assigned_raw}

        # Calculate countwise element ratios
        element_counts = defaultdict(int)

        total_atoms = 0
        for ion in assigned:
            n_atoms = assigned[ion].shape[0]
            for element, atoms_per_ion in self.elemental_ion_breakdown[ion]:
                contribution = n_atoms * atoms_per_ion
                element_counts[element] += contribution
                total_atoms += contribution

        element_ratios = {el: element_counts[el]/total_atoms for el in element_counts}

        return Assignment(
            filename=pos.filename,
            coordinates_and_mz=assigned,
            countwise_element_ratios=element_ratios,
            slds=self.slds,
            sld_times_volumes=self.sld_volume,
            ions_to_atoms=self.elemental_ion_breakdown)