import numpy as np

from data_loading import SphereSelection
from assignment import Assigner
from pr.pr_histograms import PrCalculator

import matplotlib.pyplot as plt

do_calc = False

for file_prefix, z0 in [("R5083_23208-v01-roi_tempered", 3), ("R5083_22972-v01_austenited", 150)]:

    data = SphereSelection("../data/%s.pos"%file_prefix,
                           (0, 0, z0), 24, sample_size=200_000)


    # data = PosData("data/R5083_23208-v01-roi_tempered.pos")
    # data = PosData("data/R5083_22972-v01_austenited.pos")

    print(data)

    plt.figure("%s - sample"%file_prefix)
    # data.show_sample(autoshow=False)



    assigner = Assigner("../data/S390_steel.rrng")
    print(assigner)
    assignment = assigner.assign(data)

    # plt.figure("%s - sample" % file_prefix)
    # assignment.show_ion_plots(autoshow=True)

    if do_calc:
        pr_calc = PrCalculator(r_bin_edges=np.linspace(0.0, 48.0, 49))

        pr = pr_calc.calculate(assignment, sample=data)

        pr.save("../data/%s.pickle"%file_prefix)

