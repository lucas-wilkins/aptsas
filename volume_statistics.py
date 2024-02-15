from dataclasses import dataclass

import numpy as np


from scipy.spatial import ConvexHull



@dataclass
class VolumeStats:
    volume_nm: float
    n_points: int
    mean_sample_volume_nm: float
    mean_gap_nm: float
    mean_gap_angstroms: float
    cutoff_q: float

    def save(self, filename):
        with open(filename, 'w') as fid:
            fid.write(repr(self))

def volume_statistics(data_nm: np.ndarray, verbose=True):

    if data_nm.shape[1] != 3:
        raise ValueError("Expected n-by-3 array")

    if verbose:
        print("Calculating convex hull")

    hull = ConvexHull(data_nm.data)
    n = data_nm.shape[0]

    volume = hull.volume

    return VolumeStats(
        volume_nm=volume,
        n_points=n,
        mean_sample_volume_nm=volume/n,
        mean_gap_nm=(volume/n)**(1/3),
        mean_gap_angstroms=10*((volume/n)**(1/3)),
        cutoff_q=1/(10*((volume/n)**(1/3))))