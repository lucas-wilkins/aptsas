import numpy as np

from plotting import show_sample

class PosData:
    """ Positions and mass/charge ratio from a .pos file, along with a few helper functions """
    def __init__(self, filename: str, downsample: int|None = None):
        self.filename = filename

        with open(filename, 'rb') as fid:
            # Load as bigendian 16-bit floats
            dt = np.dtype('f')
            dt = dt.newbyteorder('>')

            self.data = np.frombuffer(fid.read(), dtype=dt)

        self.data = self.data.reshape(-1, 4)

        if downsample is not None:
            n = min([self.data.shape[0], downsample])
            inds = np.random.choice(self.data.shape[0], n)
            self.data = self.data[inds, :]

    def __repr__(self):
        return f"PosData({self.filename}, n={self.n})"

    @property
    def n(self):
        return self.data.shape[0]

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