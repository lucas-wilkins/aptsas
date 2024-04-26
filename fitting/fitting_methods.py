import numpy as np

def generate_basis(r_values, q_values, scale, n_basis):
    r_bases = []
    q_bases = []
    for n in range(1, n_basis):
        r_basis = np.exp(-scale*r_values) * (r_values**n)
        r_bases.append(r_basis)

    return r_basis, q_bases


if __name__ == "__main__":
    r_values = np.linspace(0,100,101)

    generate_basis(r_values, None, 1, 20)

