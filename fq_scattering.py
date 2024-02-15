from typing import Sequence
import numpy as np

from assignment import Assignment
from simdata import ScatteringOutput

class FqScatteringCalculator:

    def __init__(self, assignment: Assignment):
        self.assignment = assignment

    def run(self, q_mags_angstrom: Sequence[float], q_vector: Sequence[float], verbose=True):

        f = np.zeros(len(q_mags_angstrom), dtype=complex)
        f_shape = np.zeros_like(f)

        q_mags = 10*np.array(q_mags_angstrom).reshape(-1, 1) # APT measurements are in nm
        imag_mags = 1j*q_mags

        q_vector = np.array(q_vector)
        q_vector = q_vector / np.sqrt(np.sum(q_vector**2))

        # SLDs
        counts = [self.assignment.coordinates[ion].shape[0] for ion in self.assignment.ions]
        slds = [self.assignment.slds[ion] for ion in self.assignment.ions]

        bulk_sld = np.sum([sld * count for sld, count in zip(slds, counts)]) / np.sum(counts)

        rel_slds = {ion: sld - bulk_sld for ion, sld in zip(self.assignment.ions, slds)}

        for ion in self.assignment.ions:
            if verbose:
                print(f"{ion} ({self.assignment.coordinates[ion].shape[0]} samples)")

            rho = rel_slds[ion]

            v_components = np.dot(self.assignment.coordinates[ion], q_vector).reshape(1, -1)

            contribution = np.sum(np.exp(v_components*imag_mags), axis=1)

            f += rho * contribution

            f_shape += contribution

        scattering = f.real**2 + f.imag**2
        shape = f_shape.real**2 + f_shape.imag**2

        return ScatteringOutput(q_mags_angstrom, scattering=scattering, shape=shape)