import numpy as np

from pr.pr_histograms import Prs

prs = Prs.load("../data/test_prs.pickle")
#
# import matplotlib.pyplot as plt
# plt.plot(prs.r_values, prs.scaling)
# plt.show()

# prs.show_raw_atom_hists()
prs.show_scaled_atom_hists()

