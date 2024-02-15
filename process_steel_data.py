import numpy as np

from loadpos import PosData
from assignment import Assigner
from naive_debye import NaiveDebye

data = PosData("data/R5083_23208-v01-roi_tempered.pos", downsample=30_000)
# data = PosData("data/R5083_22972-v01_austenited.pos")

print(data)

# data.show_sample()

assigner = Assigner("data/S390_steel.rrng")

print(assigner)

assignment = assigner.assign(data)

print(assignment)

# assignment.ion_plot("Fe")
# assignment.ion_plots()

calc = NaiveDebye(assignment)

qs = 10**np.linspace(-3, 0, 101)

scattering = calc.run(qs)
scattering.save_csv("data/test.csv")

