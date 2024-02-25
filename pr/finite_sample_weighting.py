import numpy as np
from scipy.spatial import ConvexHull

from pr.geodesic import Geodesic

def finite_sample_weighting(data_nm: np.ndarray, r_bin_edges: np.ndarray, anglular_divisions: int = 2, verbose=True):

    """ Calculate the correction for pair distributions

    Basically, a correlation function for the shape of the sample
    """

    angular_sample_points, angle_weights = Geodesic.by_divisions(anglular_divisions)

    if data_nm.shape[1] != 3:
        raise ValueError("Expected n-by-3 array")

    if verbose:
        print("Calculating convex hull")

    hull = ConvexHull(data_nm.data)

    full_volume = hull.volume

    print(hull.vertices)


    # Can calculate the volume factor by translating the hull
    # in a sample of directions around a sphere, finding the intersection
    # with the original hull, and calculating the volume

    # Can use convex hull on the intersection for the volume as the intersection
    # should be convex (it might not be the fastest way though).

def spherical_cap_volume_factor(h_over_r):
    """ Value proportion to cap volume, h is height of cap, r is radius of curvature"""

    return (h_over_r ** 2) * (3 - h_over_r)

def sphere_undersampling(sphere_radius, r_values):
    """ P(r) weighting for spherical sample

    The number of samples possible at distance r is just the probability
    """

    full_volume = spherical_cap_volume_factor(1)

    h_over_r = 1 - 0.5 * np.array(r_values) / sphere_radius

    output = np.zeros_like(h_over_r)

    big_enough = h_over_r >= 0

    output[big_enough] = spherical_cap_volume_factor(h_over_r[big_enough])/full_volume

    return output

def sphere_undersampling_integral_function(s: np.ndarray):
    inds = s <= 1
    output = np.ones_like(s)

    s = s[inds]
    output[inds] = s*(8 + s*(s*s-6))/3

    return output



if __name__ == "__main__":

    import matplotlib.pyplot as plt

    r_values = np.linspace(0,15, 101)
    s_values = np.linspace(0, 2, 101)

    plt.figure()
    plt.plot(r_values, sphere_undersampling(5, r_values))
    plt.figure()
    plt.plot(r_values, sphere_undersampling(5, r_values)*r_values**2)

    plt.figure()
    plt.plot(s_values, sphere_undersampling_integral_function(s_values))

    plt.figure()
    plt.plot(s_values[1:],
             sphere_undersampling_integral_function(s_values[1:]) -
             sphere_undersampling_integral_function(s_values[:-1]))


    plt.show()