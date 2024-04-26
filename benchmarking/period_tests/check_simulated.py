import os

from input_data import SphereSelection
import matplotlib.pyplot as plt

path = "../../data/simulated/period_tests"

for f in sorted(os.listdir(path)):

    if f.endswith("0.pos"):
        filename = os.path.join(path, f)

        data = SphereSelection(filename, (0,0,0), 50)

        data.show_sample(n=100_000, autoshow=False)

plt.show()