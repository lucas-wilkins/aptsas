import numpy as np
import warnings

from typing import Sequence
from collections import defaultdict

from input_data import PosDataBaseClass
from assignment import Assignment
import pickle

class Prs:
    def __init__(self,
                 r_values: np.ndarray,
                 r_bin_edges: np.ndarray,
                 ion_prs: dict[str, dict[str, np.ndarray]],
                 atom_prs: dict[str, dict[str, np.ndarray]],
                 scaling: Sequence[float] | None,
                 scaled_ion_prs: dict[str, dict[str, np.ndarray]] | None,
                 scaled_atom_prs: dict[str, dict[str, np.ndarray]] | None,
                 volume: float | None):

        self.r_values = r_values
        self.r_bin_edges = r_bin_edges
        self.ion_prs = ion_prs
        self.atom_prs = atom_prs
        self.scaling = scaling
        self.scaled_ion_prs = scaled_ion_prs
        self.scaled_atom_prs = scaled_atom_prs
        self.volume = volume

    def show_raw_ion_hists(self, autoshow=True):
        import matplotlib.pyplot as plt
        for ion1 in self.ion_prs:
            for ion2 in self.ion_prs[ion1]:
                # plt.figure(f"{ion1} - {ion2}")
                plt.plot(self.r_values, self.ion_prs[ion1][ion2])

        if autoshow:
            plt.show()


    def show_raw_atom_hists(self, autoshow=True):
        import matplotlib.pyplot as plt

        atoms = [key for key in self.atom_prs.keys()]

        for i, atom1 in enumerate(atoms):
            for atom2 in atoms[i:]:
                # plt.figure(f"{atom1} - {atom2}")
                plt.plot(self.r_values, self.atom_prs[atom1][atom2])

        if autoshow:
            plt.show()


    def show_scaled_atom_hists(self, autoshow=True):
        import matplotlib.pyplot as plt

        atoms = [key for key in self.scaled_atom_prs.keys()]

        binned_r2 = (self.r_bin_edges**3)/3
        binned_r2 = binned_r2[1:] - binned_r2[:-1]
        binned_r2 /= np.sum(binned_r2)

        for i, atom1 in enumerate(atoms):
            for atom2 in atoms[i:]:
                # plt.figure(f"{atom1} - {atom2}")
                plt.plot(self.r_values, self.scaled_atom_prs[atom1][atom2] / binned_r2)

        if autoshow:
            plt.show()

    def show_scaled_atom_hists_table(self, autoshow=True, numbers=False, full_range=False, show_mean=True):
        import matplotlib.pyplot as plt

        atoms = [key for key in self.scaled_atom_prs.keys()]

        # binned_r2 = (self.r_bin_edges ** 3) / 3
        # binned_r2 = binned_r2[1:] - binned_r2[:-1]
        # binned_r2 /= np.sum(binned_r2)

        n = len(atoms)

        for i, atom1 in enumerate(atoms):
            for j, atom2 in enumerate(atoms):


                plt_no = 1 + i + n*j
                plt.subplot(n, n, plt_no)
                plot_data = self.scaled_atom_prs[atom1][atom2] #/ binned_r2
                plt.plot(self.r_values, plot_data)

                if show_mean:
                    m = np.mean(plot_data)
                    plt.plot(self.r_values, np.ones_like(self.r_values)*m)

                if full_range:
                    plt.ylim([0, 1.05*np.max(plot_data)])

                if not numbers:
                    plt.xticks([],[])
                    plt.yticks([],[])

                if i == 0:
                    plt.ylabel(atom2)

                if j == 0:
                    plt.title(atom1)

        if autoshow:
            plt.show()

    def show_scaled_ion_hists_table(self, autoshow=True, numbers=False, full_range=False, show_mean=True):
        import matplotlib.pyplot as plt

        ions = [key for key in self.scaled_ion_prs.keys()]

        # binned_r2 = (self.r_bin_edges ** 3) / 3
        # binned_r2 = binned_r2[1:] - binned_r2[:-1]
        # binned_r2 /= np.sum(binned_r2)

        n = len(ions)

        for i, ion1 in enumerate(ions):
            for j, ion2 in enumerate(ions):


                plt_no = 1 + i + n*j
                plt.subplot(n, n, plt_no)
                plot_data = self.scaled_ion_prs[ion1][ion2] #/ binned_r2
                plt.plot(self.r_values, plot_data)

                if show_mean:
                    m = np.mean(plot_data)
                    plt.plot(self.r_values, np.ones_like(self.r_values)*m)

                if full_range:
                    plt.ylim([0, 1.05*np.max(plot_data)])

                if not numbers:
                    plt.xticks([],[])
                    plt.yticks([],[])

                if i == 0:
                    plt.ylabel(ion2)

                if j == 0:
                    plt.title(ion1)

        if autoshow:
            plt.show()


    def save(self, filename: str):
        data = {
            "r_values": self.r_values,
            "r_bin_edges": self.r_bin_edges,
            "ion_prs": self.ion_prs,
            "atom_prs": self.atom_prs,
            "scaling": self.scaling,
            "scaled_ion_prs": self.scaled_ion_prs,
            "scaled_atom_prs": self.scaled_atom_prs,
            "volume": self.volume}

        with open(filename, 'wb') as fid:
            pickle.dump(data, fid)

    @staticmethod
    def load(filename):
        with open(filename, 'rb') as fid:
            data = pickle.load(fid)

            return Prs(
                r_values=data["r_values"],
                r_bin_edges=data["r_bin_edges"],
                ion_prs=data["ion_prs"],
                atom_prs=data["atom_prs"],
                scaling=data["scaling"],
                scaled_ion_prs=data["scaled_ion_prs"],
                scaled_atom_prs=data["scaled_atom_prs"],
                volume=data["volume"] if "volume" in data else None # TODO: Remove this check when we don't have any files that might not have volume in them
            )


class PrCalculator:
    def __init__(self,
                 r_bin_edges: Sequence[float],
                 r_bin_centres: Sequence[float] | None = None):

        self.r_bin_edges = np.array(r_bin_edges)
        self.r_squared_bin_edges = np.array(r_bin_edges)**2

        if r_bin_centres is None:
            # Choose midpoint
            self.r_bin_centres = 0.5*(self.r_bin_edges[:-1] + self.r_bin_edges[1:])
        else:
            self.r_bin_centres = r_bin_centres

    def calculate(self,
                  assignment: Assignment,
                  sample: PosDataBaseClass | None = None,
                  max_chunk=5_000,
                  verbose=True,
                  self_remove_distance: float | None = 0.0001):

        """ Calculate the ass"""


        # Calculate the normalised values
        if sample is not None:
            scaling = sample.pr_weighting(bin_edges=self.r_bin_edges) # np.ndarray | None
        else:
            scaling = None

        if scaling is None:
            warnings.warn("No scaling set (sample parameter not set, or sample type does not support it)")

        # Strategy is to histogram each ion, then distribute each to the
        # atom histograms appropriately

        ion_prs: dict[str, dict[str, np.ndarray]] = defaultdict(dict)

        for ion1 in assignment.coordinates:
            for ion2 in assignment.coordinates:

                counts = np.zeros_like(self.r_bin_centres, dtype=int)

                pos1 = assignment.coordinates[ion1]
                pos2 = assignment.coordinates[ion2]

                n1 = pos1.shape[0]
                n2 = pos2.shape[0]

                chunk_edges_1 = [i for i in range(0, n1, max_chunk)]
                if n1 > chunk_edges_1[-1]:
                    chunk_edges_1.append(n1)

                chunk_edges_2 = [i for i in range(0, n2, max_chunk)]
                if n2 > chunk_edges_2[-1]:
                    chunk_edges_2.append(n2)

                if verbose:
                    print(f"{ion1} to {ion2}")
                    print(f"  {ion1} count: {n1}, chunk factor {len(chunk_edges_1) - 1}")
                    print(f"  {ion2} count: {n2}, chunk factor {len(chunk_edges_2) - 1}")

                if self_remove_distance is not None:
                    remove_distance_squared = self_remove_distance**2

                # Iterate over chunks
                chunk_counter = 0
                total_chunks = (len(chunk_edges_1) - 1) * (len(chunk_edges_2) - 1)
                for chunk_index_1, (start_1, stop_1) in enumerate(zip(chunk_edges_1[:-1], chunk_edges_1[1:])):
                    for chunk_index_2, (start_2, stop_2) in enumerate(zip(chunk_edges_2[:-1], chunk_edges_2[1:])):

                        chunk_counter += 1
                        if verbose:
                            print(f"  Chunk {chunk_counter} of {total_chunks}")

                        x_diff = pos1[start_1:stop_1, 0].reshape(1, -1) - pos2[start_2:stop_2, 0].reshape(-1, 1)
                        y_diff = pos1[start_1:stop_1, 1].reshape(1, -1) - pos2[start_2:stop_2, 1].reshape(-1, 1)
                        z_diff = pos1[start_1:stop_1, 2].reshape(1, -1) - pos2[start_2:stop_2, 2].reshape(-1, 1)

                        r_squareds = (x_diff**2 + y_diff**2 + z_diff**2).reshape(-1)

                        if self_remove_distance is not None:
                            r_squareds = r_squareds[r_squareds > remove_distance_squared]

                        hist_data, edges = np.histogram(r_squareds, bins=self.r_squared_bin_edges)

                        counts += hist_data

                ion_prs[ion1][ion2] = counts

        def dict_default():
            return defaultdict(lambda: np.zeros_like(self.r_bin_centres, dtype=int))


        # TODO: Don't think this is right
        atom_prs = defaultdict(dict_default)

        for ion1 in ion_prs:
            for ion2 in ion_prs[ion1]:
                for atom1, factor1 in assignment.ions_to_atoms[ion1]:
                    for atom2, factor2 in assignment.ions_to_atoms[ion2]:
                        atom_prs[atom1][atom2] += factor1 * factor2 * ion_prs[ion1][ion2]

        # Undefault dict them
        ion_prs = {ion1: {ion2: ion_prs[ion1][ion2] for ion2 in ion_prs[ion1]} for ion1 in ion_prs}
        atom_prs = {atom1: {atom2: atom_prs[atom1][atom2] for atom2 in atom_prs[atom1]} for atom1 in atom_prs}

        if scaling is None:
            scaled_ion_prs = None
            scaled_atom_prs = None

        else:
            scaled_ion_prs = {ion1: {ion2: ion_prs[ion1][ion2]/scaling for ion2 in ion_prs[ion1]} for ion1 in ion_prs}
            scaled_atom_prs = {atom1: {atom2: atom_prs[atom1][atom2]/scaling for atom2 in atom_prs[atom1]} for atom1 in atom_prs}

        volume = None if sample.volume() is None else sample.volume()

        return Prs(
            r_values=self.r_bin_centres,
            r_bin_edges=self.r_bin_edges,
            ion_prs=ion_prs,
            atom_prs=atom_prs,
            scaling=scaling,
            scaled_ion_prs=scaled_ion_prs,
            scaled_atom_prs=scaled_atom_prs,
            volume=volume)

