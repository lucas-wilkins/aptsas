import numpy as np

def uniform_block(n_points: int, edge_size: float, mass_charge_ratio: float):
    return np.hstack([
        np.random.random((n_points, 3)) * edge_size - edge_size/2,
        np.ones((n_points, 1), dtype=float)*mass_charge_ratio])


def fcc_crystal(edge_size: float, unit_cell_size: float, mass_charge_ratio: float):
    pass
def write_pos_file(data: np.ndarray, filename: str):
    assert data.shape[1] == 4

if __name__ == "__main__":
    pass