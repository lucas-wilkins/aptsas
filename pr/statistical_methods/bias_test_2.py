import numpy as np

from input_data import SphereSelection
from assignment import Assigner
from pr.pr_analysis import PrCalculator, Prs

rerun_calc = False

assigner = Assigner("../../data/S390_steel.rrng")

sample_size = 1000

for repeat in range(1000):

    data = SphereSelection("../../data/simulated/random.pos", (0,0,0), 24, sample_size=sample_size)
    print(data)

    assignment = assigner.assign(data)

    if rerun_calc:
        pr_calc = PrCalculator(r_bin_edges=np.linspace(0.0, 48.0, 49))
        pr = pr_calc.calculate(assignment, sample=data)

        pr.save(f"bias_test_data/repeats/{sample_size}/{repeat}.pickle")
