import numpy as np

from input_data import SphereSelection
from assignment import Assigner

assigner = Assigner("../data/S390_steel.rrng")

print(assigner)

for file_prefix, z0 in [("R5083_23208-v01-roi_tempered", 3), ("R5083_22972-v01_austenited", 150)]:

    for sample_size, suffix in [(10_000, "small"), (None, "full")]:

        data = SphereSelection("../data/%s.pos"%file_prefix,
                               (0, 0, z0), 24, sample_size=sample_size)

        print(data)

        assignment = assigner.assign(data)

        assignment.write_files(f"../data/selections/{file_prefix}_{suffix}")

