import os

import numpy as np
import matplotlib.pyplot as plt

from pr.pr_analysis import Prs

directory = "bias_test_data/size_dependence"

files = os.listdir(directory)
files = [file for file in files if file.endswith(".pickle")]
files.sort(key=lambda filename: int(filename.split(".")[0]))

for file in files:
    data = Prs.load(os.path.join(directory, file))

    calculated = data.scaled_atom_prs["C"]["C"]
    calculated /= np.mean(calculated)

    plt.plot(data.r_values, calculated)

plt.show()
