import numpy as np
import matplotlib.pyplot as plt

def create_exp_basis(r_values, exp_constant, n):



    exp_part = np.exp(-r_values / exp_constant)

    basis_functions = [exp_part * ((r_values/exp_constant) ** i) for i in range(n)]

    return basis_functions

r_values = np.linspace(0,100,51)

for basis_function in create_exp_basis(r_values, 2.0, 5):
    plt.plot(r_values, basis_function)

plt.show()