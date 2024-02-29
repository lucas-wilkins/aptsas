import numpy as np

import warnings

from plotting import show_sample
from shape_factors import sphere_undersampling_integral_function, sphere_undersampling_integral_with_r_squared


class PosDataBaseClass:
    """ Base class for .pos file sourced data """

    def __init__(self, filename: str):

        self.filename = filename

        with open(filename, 'rb') as fid:
            # Load as bigendian 16-bit floats
            dt = np.dtype('f')
            dt = dt.newbyteorder('>')

            data = np.frombuffer(fid.read(), dtype=dt)

        data = data.reshape(-1, 4)

        self.data = self.sampling(data)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.filename}, n={self.n})"

    @property
    def n(self):
        return self.data.shape[0]

    @property
    def coordinates(self):
        return self.data[:, :3]

    @property
    def x(self):
        return self.data[:, 0]

    @property
    def y(self):
        return self.data[:, 1]

    @property
    def z(self):
        return self.data[:, 2]

    @property
    def m_over_z(self):
        return self.data[:, 3]

    def show_sample(self, autoshow: bool=True, n=10_000):
       show_sample(self.data, autoshow=autoshow, n=n, name=self.filename)

    def sampling(self, data: np.ndarray) -> np.ndarray:
        """ Sampling function """
        raise NotImplementedError("Sampling not implemented yet")

    def pr_weighting(self, bin_edges: np.ndarray) -> np.ndarray | None:
        # TODO: implement general shape compensation
        warnings.warn("Cannot weight arbitrary shapes (yet)")

        return None

class FullFile(PosDataBaseClass):
    """ Load a .pos file with no subsampling"""
    def sampling(self, data: np.ndarray):
        return data

class RandomSelection(PosDataBaseClass):
    """ Load a sample of a given size from a pos file"""

    def __init__(self, filename: str, sample_size: int):
        self.sample_size = sample_size

        super().__init__(filename)

    def sampling(self, data: np.ndarray) -> np.ndarray:

        n = min([data.shape[0], self.sample_size])
        inds = np.random.choice(data.shape[0], n)
        return data[inds, :]


class SphereSelection(PosDataBaseClass):
    """ Sample from a sphere """

    def __init__(self,
                 filename: str,
                 centre: tuple[float, float, float],
                 sphere_radius: float,
                 sample_size: int | None = None,
                 invert=False):

        self.centre = np.array(centre)
        self.radius = sphere_radius
        self.sample_size = sample_size
        self.invert = invert

        super().__init__(filename)

    def sampling(self, data: np.ndarray):
        r_sq_values = np.sum((data[:, :3] - self.centre)**2, axis=1)
        selection = r_sq_values <= self.radius ** 2

        if self.invert:
            selection = np.logical_not(selection)

        output = data[selection, :]
        n = output.shape[0]

        if self.sample_size is not None and n > self.sample_size:

            sample_inds = np.random.choice(n, self.sample_size, replace=False)
            output = output[sample_inds, :]

        return output

    def pr_weighting(self, bin_edges: np.ndarray):
        cdf = sphere_undersampling_integral_with_r_squared(bin_edges, self.radius)
        return cdf[1:] - cdf[:-1]

