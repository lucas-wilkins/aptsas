import numpy as np
from scipy.special import sici

def calculate_scattering(r_bin_edges: np.ndarray, pair_density_distribution: np.ndarray, q_values: np.ndarray):

    qs = q_values.reshape(1, -1)
    r_edges = r_bin_edges.reshape(-1, 1)
    pair_density = pair_density_distribution.reshape(-1, 1)

    sinc_integrals_edges = sici(qs * r_edges)[0] / qs
    sinc_integrals = sinc_integrals_edges[1:, :] - sinc_integrals_edges[:-1, :]

    return np.sum(sinc_integrals * pair_density, axis=0)


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    from shape_factors import sphere_undersampling_integral_function, sphere_undersampling_integral_with_r_squared

    plt.figure("Realspace")

    r_edges = np.linspace(0, 200, 201)
    pair_density = sphere_undersampling_integral_with_r_squared(r_edges, 100)
    # pair_density = sphere_undersampling_integral_function(r_edges/100)

    r_centres = 0.5*(r_edges[1:] + r_edges[:-1])
    pair_density = pair_density[1:] - pair_density[:-1]

    plt.plot(r_centres, pair_density)

    plt.figure("Scattering")

    q_values = 10**np.linspace(-3, 0.5, 1001)

    iq = calculate_scattering(r_edges, pair_density, q_values)
    plt.loglog(q_values, iq)

    plt.show()

