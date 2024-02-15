from typing import Sequence
import numpy as np

from assignment import Assignment
from simdata import ScatteringOutput

class NaiveDebye:

    """ Calculate scattering based on the Debye formula, does not account for there being a finite
    volume, however it does return a shape factor"""
    def __init__(self, assignment: Assignment):
        self.assignment = assignment
        self.output = None

    def run(self, qs_angstrom: Sequence[float], verbose=True, max_chunk=1_000):
        ions = [key for key in self.assignment.coordinates_and_mz.keys()]
        qs_nm = np.array(qs_angstrom)*10

        counts = [self.assignment.coordinates[ion].shape[0] for ion in ions]
        slds = [self.assignment.slds[ion] for ion in ions]

        bulk_sld = np.sum([sld*count for sld, count in zip(slds, counts)]) / np.sum(counts)

        rel_slds = {ion: sld - bulk_sld for ion, sld in zip(ions, slds)}

        shape_factor = np.zeros_like(qs_nm)
        scattering = np.zeros_like(qs_nm)

        qs_nm = qs_nm.reshape(-1, 1)

        for i, ion1 in enumerate(ions):
            for j, ion2 in enumerate(ions):
                if i >= j:

                    if verbose:
                        print(ion1, "to", ion2)

                    # Double the contribution from "off diagonal" elements
                    factor = 1 if i == j else 2

                    sld1 = rel_slds[ion1]
                    sld2 = rel_slds[ion2]
                    sld_factor = sld1*sld2

                    # calculate distances
                    pos1 = self.assignment.coordinates[ion1]
                    pos2 = self.assignment.coordinates[ion2]

                    # calculate parameters for chunking
                    n1 = pos1.shape[0]
                    n2 = pos2.shape[0]

                    chunk_edges_1 = [i for i in range(0, n1, max_chunk)]
                    if n1 > chunk_edges_1[-1]:
                        chunk_edges_1.append(n1)

                    chunk_edges_2 = [i for i in range(0, n2, max_chunk)]
                    if n2 > chunk_edges_2[-1]:
                        chunk_edges_2.append(n2)

                    print(f"  {ion1} count: {n1}, chunk factor {len(chunk_edges_1)-1}")
                    print(f"  {ion2} count: {n2}, chunk factor {len(chunk_edges_2)-1}")

                    # Iterate over chunks
                    chunk_counter = 0
                    total_chunks = (len(chunk_edges_1)-1)*(len(chunk_edges_2)-1)
                    for chunk_index_1, (start_1, stop_1) in enumerate(zip(chunk_edges_1[:-1], chunk_edges_1[1:])):
                        for chunk_index_2, (start_2, stop_2) in enumerate(zip(chunk_edges_2[:-1], chunk_edges_2[1:])):

                            chunk_counter += 1
                            if verbose:
                                print(f"  Chunk {chunk_counter} of {total_chunks}")

                            x_diff = pos1[start_1:stop_1, 0].reshape(1, -1) - pos2[start_2:stop_2, 0].reshape(-1, 1)
                            y_diff = pos1[start_1:stop_1, 1].reshape(1, -1) - pos2[start_2:stop_2, 1].reshape(-1, 1)
                            z_diff = pos1[start_1:stop_1, 2].reshape(1, -1) - pos2[start_2:stop_2, 2].reshape(-1, 1)

                            r = np.sqrt(x_diff**2 + y_diff**2 + z_diff**2)

                            r = r.reshape(1, -1)

                            # calculate scattering
                            components = np.sinc(r * qs_nm)

                            # Remove self scattering
                            if i == j and chunk_index_1 == chunk_index_2:
                                np.fill_diagonal(components, 0.0)

                            components = np.sum(components, axis=1)
                            # add to shape factor and scattering
                            shape_factor += factor*components

                            scattering += factor*sld_factor*components

        out = ScatteringOutput(q=qs_angstrom, scattering=scattering, shape=shape_factor)
        self.output = out
        return out