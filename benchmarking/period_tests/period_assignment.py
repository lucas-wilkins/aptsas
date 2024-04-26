import numpy as np
import os

from input_data import SphereSelection
from assignment import Assigner

assigner = Assigner("../../data/S390_steel.rrng")

print(assigner)

path = "../../data/simulated/period_tests"

for f in sorted(os.listdir(path)):

    name = f.split(".")[0]

    filename = os.path.join(path, f)

    data = SphereSelection(filename, (0,0,0), 50)

    print(data)

    assignment = assigner.assign(data)

    assignment.write_files(f"../../data/simulated/period_test_components/%s"%name)

