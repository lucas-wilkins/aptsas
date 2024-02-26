import numpy as np
import time

""" What's faster, sqrt then binning into even bins, or binning into square bins"""


linear_bin_edges = np.linspace(0, 1, 51)
square_bin_edges = linear_bin_edges**2

linear_times = []
square_times = []

linear_outputs = []
square_outputs = []

n_tests = 10

for i in range(n_tests):
    print("Run",i+1,"of",n_tests)

    test_points = np.random.random((5000 ** 2,))

    # Linear
    tic = time.time()
    hist, _ = np.histogram(np.sqrt(test_points), bins=linear_bin_edges)
    linear_times.append(time.time() - tic)
    linear_outputs.append(hist)

    # Square
    tic = time.time()
    hist, _ = np.histogram(test_points, bins=square_bin_edges)
    square_times.append(time.time() - tic)
    square_outputs.append(hist)

print("Linear:", np.mean(linear_times), "+-", np.std(linear_times))
print("Square:", np.mean(square_times), "+-", np.std(square_times))

print("No sqrt speed up %.2g%%"%(np.abs(100*(np.mean(square_times)/np.mean(linear_times)) - 100)))

import matplotlib.pyplot as plt


bin_centres = 0.5*(linear_bin_edges[1:] + linear_bin_edges[:-1])
for linear, square in zip(linear_outputs, square_outputs):
    plt.plot(bin_centres, linear, color='b')
    plt.plot(bin_centres, square, color='r')

# plt.plot(bin_centres, 1e6*bin_centres**2)

plt.show()