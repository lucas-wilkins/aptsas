import numpy as np

def uniform_block(n_points: int, edge_size: float, mass_charge_ratio: float):
    """ Random points within a volume """
    return np.hstack([
        np.random.random((n_points, 3)) * edge_size - edge_size/2,
        np.ones((n_points, 1), dtype=float)*mass_charge_ratio])


def fcc_crystal_points(edge_size: float, unit_cell_size: float):
    """ Points for face centred cubic cell """

    points_1D = np.arange(-edge_size/2, edge_size/2, unit_cell_size)
    x, z, y = np.meshgrid(points_1D, points_1D, points_1D)

    x = x.reshape(-1)
    y = y.reshape(-1)
    z = z.reshape(-1)

    points = np.vstack([x, y, z]).T

    points = np.vstack([
        points,
        points + np.array([0.5*unit_cell_size, 0.5*unit_cell_size, 0]),
        points + np.array([0.5*unit_cell_size, 0, 0.5*unit_cell_size]),
        points + np.array([0, 0.5*unit_cell_size, 0.5*unit_cell_size])
        ])

    return points

def diamond(size_nm: float):
    """ Simulated data for diamond """
    unit_cell_size = 3.567 / 10 # nm
    mass_charge = 12.0

    type_1 = fcc_crystal_points(size_nm, unit_cell_size)
    type_2 = type_1 + 0.25*unit_cell_size*np.array([1,1,1])

    points = np.vstack([type_1, type_2])
    n_points = points.shape[0]

    return np.hstack([points, mass_charge * np.ones((n_points, 1))])

def show_points(points):
    import matplotlib.pyplot as plt

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    ax.scatter(points[:,0], points[:,1], points[:,2])

    plt.show()

def write_pos_file(data: np.ndarray, filename: str):
    assert data.shape[1] == 4

    with open(filename, 'wb') as fid:

        # Load as bigendian 16-bit floats
        dt = np.dtype('f')
        dt = dt.newbyteorder('>')

        fid.write(np.array(data, dtype=dt).tobytes())

        # data = np.frombuffer(fid.read(), dtype=dt)

def make_simulated_data():
    diamond_data = diamond(50)
    print("Diamond data:", diamond_data.shape)
    write_pos_file(diamond_data, "data/simulated/diamond.pos")

    random_data = uniform_block(22425768, 50, 12)
    print("Random data:", random_data.shape)
    write_pos_file(random_data, "data/simulated/random.pos")


if __name__ == "__main__":



    make_simulated_data()

    # points = fcc_crystal_points(2, 1)
    # points = diamond(0.5)
    # show_points(points)