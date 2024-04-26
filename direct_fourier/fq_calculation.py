import numpy as np
from typing import Callable


def sphere_density(r: float, q_direction: np.ndarray) -> Callable[[np.ndarray], np.ndarray]:
    def density_function(points: np.ndarray) -> np.ndarray:
        r_pt = np.dot(points, q_direction)

        return r*r - r_pt*r_pt

    return density_function


def fq_points(q_mags, q_direction, points, density_function: Callable[[np.ndarray], np.ndarray]):
    """ Calculate F(q) for a specific direction """

    densities = density_function(points).reshape(-1, 1)

    point_components = np.dot(points, q_direction).reshape(-1, 1)

    q = q_mags.reshape(1, -1)

    qr = point_components * q

    f_matrix = np.exp(1j * qr) / densities

    return np.sum(f_matrix, axis=0)

