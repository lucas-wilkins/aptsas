from typing import Sequence
import numpy as np

from loadpos import PosData
from plotting import show_sample
from pr.finite_sample_weighting import sphere_undersampling

class CompensatedSample:
    def __init__(self, full_data: PosData):
        self._full_data = full_data

        self.data = self._get_sample()

    def _get_sample(self):
        raise NotImplementedError("Sampling method not defined")

    def undersample_function(self, bin_edges):
        raise NotImplementedError("Undersampling distribution not specified")

    def show_sample(self, autoshow=True, max_show=10_000):
        show_sample(self.data,
                    autoshow=autoshow,
                    n=max_show,
                    name=f"{self.__class__.__name__}({self._full_data.filename})")


class SphericalSample(CompensatedSample):
    def __init__(self, full_data: PosData, centre: Sequence[float], radius: float, invert=False):

        self.centre = np.array(centre)
        self.radius = radius
        self.invert = invert

        super().__init__(full_data)

    def _get_sample(self):
        if self.invert:
            inds = np.sum((self._full_data.coordinates - self.centre) ** 2, axis=1) > self.radius ** 2
        else:
            inds = np.sum((self._full_data.coordinates - self.centre) ** 2, axis=1) <= self.radius ** 2

        return self._full_data.data[inds, :]

