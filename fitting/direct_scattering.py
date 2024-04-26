import numpy as np

def calculate_scattering(r_values: np.ndarray, correlation_function: np.ndarray, q_values: np.ndarray):
    correlation_function -= np.mean(correlation_function)
    correlation_function = correlation_function.reshape(-1, 1)

    qr = r_values.reshape(-1, 1) * q_values.reshape(1, -1)

    mat = np.sinc(qr) * correlation_function

    return np.sum(mat, axis=0)