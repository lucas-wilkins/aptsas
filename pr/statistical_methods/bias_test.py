import numpy as np

from input_data import SphereSelection
from assignment import Assigner
from pr.pr_analysis import PrCalculator, Prs

rerun_calc = True

assigner = Assigner("../../data/S390_steel.rrng")

for sample_size in 2**np.arange(np.log2(100), np.log2(200_000)):
    sample_size = int(sample_size)+1

    data = SphereSelection("../../data/simulated/random.pos", (0,0,0), 24, sample_size=sample_size)
    print(data)

    assignment = assigner.assign(data)

    if rerun_calc:
        pr_calc = PrCalculator(r_bin_edges=np.linspace(0.0, 48.0, 49))
        pr = pr_calc.calculate(assignment, sample=data)

        pr.save(f"bias_test_data/size_dependence/{sample_size}.pickle")
