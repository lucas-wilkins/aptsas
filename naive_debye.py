from typing import Sequence
import numpy as np

from assignment import Assignment

def load_debye(filename: str):

    q = []
    I = []
    s = []

    with open(filename, 'r') as fid:
        for line in fid:
            try:
                parts = line.strip().split(",")
                q.append(float(parts[0]))
                I.append(float(parts[1]))
                s.append(float(parts[2]))
            except:
                pass

    return NaiveDebyeOutput(np.array(q), np.array(I), np.array(s))

class NaiveDebyeOutput:
    def __init__(self, q: np.ndarray, scattering: np.ndarray, shape: np.ndarray):
        self.q = q
        self.scattering = scattering
        self.shape = shape

    def save_csv(self, filename: str):
        """ Write data to csv file"""
        with open(filename, 'w') as fid:
            for qIs in zip(self.q, self.scattering, self.shape):
                fid.write("%g, %g, %g\n" % qIs)

    def show(self, autoshow=True):
        import matplotlib.pyplot as plt

        plt.figure()

        plt.subplot(1,2,1)
        plt.loglog(self.q, self.scattering)
        plt.xlabel("q (A^-1)")
        plt.ylabel("I")
        plt.title("Scattering")

        plt.subplot(1,2,2)
        plt.loglog(self.q, self.shape)
        plt.xlabel("q (A^-1)")
        plt.ylabel("I")
        plt.title("Shape Factor")
        #
        # plt.subplot(2,2,3)
        # plt.loglog(self.q, self.scattering / self.shape)
        # plt.xlabel("q (A^-1)")
        # plt.ylabel("I")
        # plt.title("Unshaped")


        if autoshow:
            plt.show()

class NaiveDebye:

    """ Calculate scattering based on the Debye formula, does not account for there being a finite
    volume, however it does return a shape factor"""
    def __init__(self, assignment: Assignment):
        self.assignment = assignment
        self.output = None

    def run(self, qs_angstrom: Sequence[float], verbose=True, max_chunk=1_000):
        ions = [key for key in self.assignment.coordinates_and_mz.keys()]
        qs_nm = np.array(qs_angstrom)*10

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

                    sld1 = self.assignment.slds[ion1]
                    sld2 = self.assignment.slds[ion2]
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
                    for start_1, stop_1 in zip(chunk_edges_1[:-1], chunk_edges_1[1:]):
                        for start_2, stop_2 in zip(chunk_edges_2[:-1], chunk_edges_2[1:]):

                            chunk_counter += 1
                            if verbose:
                                print(f"  Chunk {chunk_counter} of {total_chunks}")

                            x_diff = pos1[start_1:stop_1, 0].reshape(1, -1) - pos2[start_2:stop_2, 0].reshape(-1, 1)
                            y_diff = pos1[start_1:stop_1, 1].reshape(1, -1) - pos2[start_2:stop_2, 1].reshape(-1, 1)
                            z_diff = pos1[start_1:stop_1, 2].reshape(1, -1) - pos2[start_2:stop_2, 2].reshape(-1, 1)

                            r = np.sqrt(x_diff**2 + y_diff**2 + z_diff**2)

                            r = r.reshape(1, -1)

                            # calculate scattering
                            components = np.sum(np.sinc(r * qs_nm), axis=1)

                            # add to shape factor and scattering
                            shape_factor += factor*components

                            scattering += factor*sld_factor*components

        return NaiveDebyeOutput(q=qs_angstrom, scattering=scattering, shape=shape_factor)