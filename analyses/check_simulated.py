import numpy as np

from data_loading import SphereSelection

data = SphereSelection("../data/simulated/diamond.pos", (0,0,0), 5)

data.show_sample(n=100_000)