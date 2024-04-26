import numpy as np
import os

from input_data import SphereSelection
from assignment import Assigner
from pr.pr_analysis import PrCalculator

assigner = Assigner("../../data/S390_steel.rrng")

print(assigner)

path = "../../data/simulated/period_tests"

calc = PrCalculator(np.linspace(0,100, 1001))

for f in sorted(os.listdir(path)):

    if f.endswith(".pos"):

        name = f.split(".")[0]

        filename = os.path.join(path, f)

        print(filename)

        data = SphereSelection(filename, (0,0,0), 50)

        assignment = assigner.assign(data)

        prs = calc.calculate(assignment, data)


        prs.save(os.path.join(path, f"{name}.prs"))