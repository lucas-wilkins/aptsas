import os

import numpy as np
import matplotlib.pyplot as plt

from pr.pr_analysis import Prs

directory = "bias_test_data/repeats/1000"

files = os.listdir(directory)
files = [file for file in files if file.endswith(".pickle")]
files.sort(key=lambda filename: int(filename.split(".")[0]))

data = []
raw = []

plt.figure("Curves")
for file in files:

    prs = Prs.load(os.path.join(directory, file))
    calculated = prs.scaled_atom_prs["C"]["C"]

    plt.plot(prs.r_values, calculated)

    data.append(calculated)
    raw.append(prs.atom_prs["C"]["C"])

data = np.array(data)
raw = np.array(raw)

print(data.shape)

expected_density = (1000 / prs.volume)**2 # We've ignored self, hence n(n-1)

print(expected_density)


plt.figure("Percentiles")

for percentile in range(10, 100, 10):

    values = [np.percentile(data[:, i], q=percentile) for i in range(data.shape[1])]

    plt.plot(prs.r_values, values, color='b')

plt.plot(prs.r_values, np.mean(data, axis=0), color='k')

plt.figure("Covariance (scaled)")

# plt.pcolor(np.cov(data.T)))
# plt.pcolor(np.log(np.abs(np.cov(data.T))))
plt.pcolor(np.corrcoef(data.T))



plt.figure("Covariance (unscaled)")

plt.pcolor(np.cov(raw.T))


plt.show()
