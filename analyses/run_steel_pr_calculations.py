import numpy as np

from loadpos import PosData
from assignment import Assigner
from naive_debye import NaiveDebye
from fq_scattering import FqScatteringCalculator
from volume_statistics import volume_statistics
from pr.pr_histograms import PrCalculator

from pr.compensated_sample import SphericalSample

data = PosData("../data/R5083_23208-v01-roi_tempered.pos", downsample=10_000)
# data = PosData("data/R5083_23208-v01-roi_tempered.pos")
# data = PosData("data/R5083_22972-v01_austenited.pos")



print(data)




sample = SphericalSample(data, (0, 0, 3), 24, invert=False)

assigner = Assigner("../data/S390_steel.rrng")
print(assigner)
assignment = assigner.assign(sample)

# sample.show_sample()

pr_calc = PrCalculator(r_bin_edges=np.linspace(0.0, 48.0, 49))

pr = pr_calc.calculate(assignment)

pr.save("data/test_prs.pickle")

