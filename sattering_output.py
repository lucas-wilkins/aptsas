import numpy as np
def load_scattering(filename: str):

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

    return ScatteringOutput(np.array(q), np.array(I), np.array(s))


class ScatteringOutput:
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
