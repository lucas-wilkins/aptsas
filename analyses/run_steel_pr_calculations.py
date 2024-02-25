import numpy as np

from data_loading import SphereSelection
from assignment import Assigner
from naive_debye import NaiveDebye
from fq_scattering import FqScatteringCalculator
from volume_statistics import volume_statistics
from pr.pr_histograms import PrCalculator


data = SphereSelection("../data/R5083_23208-v01-roi_tempered.pos",
                       (0, 0, 3), 24, sample_size=100_000)

# data = PosData("data/R5083_23208-v01-roi_tempered.pos")
# data = PosData("data/R5083_22972-v01_austenited.pos")

print(data)

data.show_sample()



assigner = Assigner("../data/S390_steel.rrng")
print(assigner)
assignment = assigner.assign(data)


pr_calc = PrCalculator(r_bin_edges=np.linspace(0.0, 48.0, 49))

pr = pr_calc.calculate(assignment, sample=data)

pr.save("../data/test_prs.pickle")

