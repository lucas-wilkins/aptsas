import numpy as np

from data_loading import SphereSelection
from assignment import Assigner
from pr.pr_histograms import PrCalculator, Prs

rerun_calc = False

data = SphereSelection("../data/simulated/random.pos", (0,0,0), 24, sample_size=100_000)

# data.show_sample()


assigner = Assigner("../data/S390_steel.rrng")
assignment = assigner.assign(data)

if rerun_calc:
    pr_calc = PrCalculator(r_bin_edges=np.linspace(0.0, 48.0, 49))
    pr = pr_calc.calculate(assignment, sample=data)

    pr.save("../data/simulated/random_prs.pickle")

prs = Prs.load("../data/simulated/random_prs.pickle")

# prs.show_raw_atom_hists()

prs.show_scaled_atom_hists_table(numbers=True, full_range=True)