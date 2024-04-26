"""

Creates periodic data with a known autocorrelation function, and saves the data along with the prediction

"""

import numpy as np
import matplotlib.pyplot as plt

def example_2d(freq: float, n_periods: int, n_per_period: int):
    size = n_periods/freq
    x = np.linspace(-size, size, 2*n_periods*n_per_period+1)
    y = x.copy()

    x_mesh, y_mesh = np.meshgrid(x, y)

    values = np.cos(2*np.pi*freq*x_mesh) + np.cos(2*np.pi*freq*y_mesh)

    plt.pcolor(x, y, values)
    plt.show()

def sample_cosine_3d(freq: float, size: float, phase_x: float, phase_y: float, phase_z: float, n_samples: int):
    count = 0
    output = []
    while count < n_samples:
        # print(count)

        these_samples = 12*(n_samples - count) + 10

        raw_points = size*(np.random.rand(these_samples, 3) - 0.5)
        rejection_p = np.random.rand(these_samples)

        values = (1/6)*(
                np.cos(2*np.pi*raw_points[:, 0]*freq + phase_x) +
                np.cos(2*np.pi*raw_points[:, 1]*freq + phase_y) +
                np.cos(2*np.pi*raw_points[:, 2]*freq + phase_z))

        keep = values > rejection_p

        keep_points = raw_points[keep, :]

        if keep_points.shape[0] > n_samples - count:
            keep_points = keep_points[:n_samples - count, :]

        output.append(keep_points)
        count += keep_points.shape[0]


    return np.vstack(output)


def example_sample():
    points = sample_cosine_3d(2, 2, 1, 2, 3, 10_000)
    plt.scatter(points[:, 0], points[:, 1])
    plt.show()


def analytic_cosine_3d(freq: float, r_values: np.ndarray):
    """ Analytic result of the radial autocorrelation """
    return 6*np.pi*(np.sinc(2*np.pi*freq*r_values)) + 4*np.pi


if __name__ == "__main__":
    #example_sample()
    example_2d(10, 3, 20)


