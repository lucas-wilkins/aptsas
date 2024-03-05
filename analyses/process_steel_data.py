import numpy as np

from input_data import FullFile, RandomSelection
from assignment import Assigner
from naive_debye import NaiveDebye
from fq_scattering import FqScatteringCalculator
from volume_statistics import volume_statistics

data = RandomSelection("../data/R5083_23208-v01-roi_tempered.pos", sample_size=10_000)
# data = FullFile("../data/R5083_23208-v01-roi_tempered.pos")
# data = FullFile("../data/R5083_22972-v01_austenited.pos")

print(data)

# data.show_sample()

assigner = Assigner("../data/S390_steel.rrng")

print(assigner)

assignment = assigner.assign(data)

print(assignment)

# assignment.ion_plot("Fe")
# assignment.ion_plots()

calc = NaiveDebye(assignment)
# calc = FqScatteringCalculator(assignment)

qs = 10**np.linspace(-3, 0, 101)

scattering = calc.run(qs)
# scattering = calc.run(qs, q_vector=(0,0,1))
scattering.save_csv("../data/test.csv")

vol_data = volume_statistics(data.coordinates)
vol_data.save("../data/vol.txt")