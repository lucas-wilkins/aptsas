import matplotlib.pyplot as plt
from data_loading import SphereSelection

for file_prefix, z0 in [("R5083_23208-v01-roi_tempered", 3), ("R5083_22972-v01_austenited", 150)]:

    data = SphereSelection("../data/%s.pos"%file_prefix,
                           (0, 0, z0), 24, sample_size=200_000, invert=False)

    data.show_sample(autoshow=False)

plt.show()