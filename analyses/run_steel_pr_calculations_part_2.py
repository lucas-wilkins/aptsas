import numpy as np

from pr.pr_histograms import Prs

prs = Prs.load("../data/test_prs.pickle")

prs.show_raw_atom_hists()