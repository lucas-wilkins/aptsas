import matplotlib.pyplot as plt

from pr.pr_histograms import Prs

for file_prefix in ["R5083_23208-v01-roi_tempered", "R5083_22972-v01_austenited"]:

    prs = Prs.load("../data/%s.pickle"%file_prefix)
    #
    # import matplotlib.pyplot as plt
    # plt.plot(prs.r_values, prs.scaling)
    # plt.show()

    plt.figure(file_prefix)

    # prs.show_raw_atom_hists()
    # prs.show_scaled_atom_hists()
    prs.show_scaled_atom_hists_table(full_range=True, autoshow=True)

plt.show()