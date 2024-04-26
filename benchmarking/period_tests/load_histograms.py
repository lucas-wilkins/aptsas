import numpy as np
import os
from pr.pr_analysis import Prs
import matplotlib.pyplot as plt
from collections import defaultdict
from shape_factors import sphere_undersampling_integral_with_r_squared
from benchmarking.period_tests.period_tests import analytic_cosine_3d

from fitting.direct_scattering import calculate_scattering

path = "../../data/simulated/period_tests"

raw_data = defaultdict(list)
analytic = {}

for f in sorted(os.listdir(path)):

    if f.endswith(".prs"):

        name_parts = f.split(".")[0].split("_")

        period = int(name_parts[0])

        filename = os.path.join(path, f)

        pr = Prs.load(filename)

        datum = pr.ion_prs["C"]["C"]

        # plt.plot(datum)

        sphere_factor_integral = sphere_undersampling_integral_with_r_squared(pr.r_bin_edges, 50)
        sphere_factor = sphere_factor_integral[1:] - sphere_factor_integral[:-1]

        raw_data[period].append(datum/sphere_factor)


        analytic[period] = analytic_cosine_3d(period/(200*np.pi), r_values=pr.r_values)


data = {}

keys = sorted([key for key in raw_data])

plt.figure("Correlation")
for period in keys:
    data[period] = np.mean(np.array(raw_data[period]), axis=0)
    data[period] /= np.max(data[period])


    offset = 2*((period-1)%5)

    plot_num = ((period-1) // 5) + 1

    print(period, plot_num, offset)

    plt.subplot(2,2,plot_num)

    plt.plot(pr.r_values, data[period]/np.mean(data[period]) + offset)
    plt.plot(pr.r_values, analytic[period]/np.mean(analytic[period]) + offset, color='k')
    #
    # plt.plot(pr.r_values, data[period] + offset)
    # plt.plot(pr.r_values, analytic[period]/(50) + offset, color='k')


    plt.text(0, 1+offset, str(period))

    plt.ylim([0,12])
    plt.yticks([],[])


plt.figure("Scattering")
qs = 10**np.linspace(-3,0.5,100)
for period in keys:
    offset = 2*((period-1)%5)

    plot_num = ((period-1) // 5) + 1

    print(period, plot_num, offset)

    plt.subplot(2,2,plot_num)

    scattering = calculate_scattering(pr.r_values, data[period], qs)

    plt.loglog(qs, scattering)


plt.show()