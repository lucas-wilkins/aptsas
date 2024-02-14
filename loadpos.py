import numpy as np

class PosData:
    """ Positions and mass/charge ratio from a .pos file, along with a few helper functions """
    def __init__(self, filename):
        self.filename = filename

        with open(filename, 'rb') as fid:
            # Load as bigendian 16-bit floats
            dt = np.dtype('f')
            dt = dt.newbyteorder('>')

            self.data = np.frombuffer(fid.read(), dtype=dt)

        self.data = self.data.reshape(-1, 4)

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
        import matplotlib.pyplot as plt

        n = min([self.n, n])

        plt.figure()

        plt.subplot(2, 2, 1)
        plt.scatter(self.x[:n], self.y[:n])
        plt.xlabel("X")
        plt.ylabel("Y")

        plt.subplot(2, 2, 2)
        plt.scatter(self.x[:n], self.z[:n])
        plt.xlabel("X")
        plt.ylabel("Z")

        plt.subplot(2, 2, 3)
        plt.scatter(self.y[:n], self.z[:n])
        plt.xlabel("Y")
        plt.ylabel("Z")

        plt.subplot(2, 2, 4)
        plt.hist(self.m_over_z[:n], bins=200)
        plt.xlabel("m/z")
        plt.ylabel("counts")

        if autoshow:
            plt.show()
