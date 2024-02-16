import numpy as np

from loadpos import PosData
from assignment import Assigner
from naive_debye import NaiveDebye
from fq_scattering import FqScatteringCalculator
from volume_statistics import volume_statistics

from pr.finite_sample_weighting import finite_sample_weighting

# data = PosData("data/R5083_23208-v01-roi_tempered.pos", downsample=10_000)
data = PosData("data/R5083_23208-v01-roi_tempered.pos")
# data = PosData("data/R5083_22972-v01_austenited.pos")



print(data)

# # data.show_sample()
#
# assigner = Assigner("data/S390_steel.rrng")
#
# print(assigner)
#
# assignment = assigner.assign(data)
#
# print(assignment)

# assignment.ion_plot("Fe")
# assignment.ion_plots()

qs = 10**np.linspace(-3, 0, 101)

finite_sample_weighting(data.coordinates, None)