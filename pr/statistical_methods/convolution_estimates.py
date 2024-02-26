""" Some simulations to look at how we estimate convolutions """

import numpy as np
import matplotlib.pyplot as plt

# Consider two samples from discrete distributions with two non-zero values each
# The probabilities for a single sample being drawn from them are
#
# The counts for each value are x0, x1, and y0, y1
#
# Pr(x0=1, 1) = p
# Pr(x1=1, 1) = 1-p
#
#  and
#
# Pr(y0=1, 1) = q
# Pr(y1=1, 1) = 1-q
#
# And more generally, Pr(x0, n) = nCx p^x0 (1-p)^(n-x0), and so forth for each one
#
# The convolved probability distribution is
#
# Pz[-1 ] = p (1-q)
# Pz[ 0 ] = p q + (1-p) (1-q)
# Pz[ 1 ] = (1-q) p
#
# How well do we estimate this from samples????
#

pqnms = [
    (0.1, 0.2, 10, 10),
    (0.1, 0.2, 100, 100),
    (0.1, 0.2, 1000, 1000),
    (0.3, 0.8, 100, 10),
    (0.3, 0.8, 100, 100),
    (0.3, 0.8, 100, 1000),
    ]

for pqmn in pqnms[:]:

    p, q, n, m = pqmn

    z_m1_samples = []
    z_0_samples = []
    z_1_samples = []

    for i in range(10000):
        x = np.random.binomial(n, p)
        y = np.random.binomial(m, q)

        z_m1 = x * (m - y)
        z_0 = x * y + (m - y) * (n - x)
        z_1 = (n - x) * y

        z_m1_samples.append(z_m1)
        z_0_samples.append(z_0)
        z_1_samples.append(z_1)

    # Mean model

    mu_x0 = n*p
    mu_x1 = n*(1-p)
    mu_y0 = m*q
    mu_y1 = m*(1-q)

    v_x = n*p*(1-p)
    v_y = m*q*(1-q)

    z_m1_truth = mu_x0 * mu_y1
    z_0_truth = mu_x0 * mu_y0 + mu_x1 * mu_y1
    z_1_truth = mu_x1 * mu_y0

    # Variance model - assume independence - BUT THEY'RE NOT in the addition, ughhhhhh
    v_m1 = mu_x0*mu_x0*v_y + mu_y1*mu_y1*v_x + v_x*v_y
    v_0 = (mu_x0*mu_x0*v_y + mu_y0*mu_y0*v_x + v_x*v_y) + (mu_x1*mu_x1*v_y + mu_y1*mu_y1*v_x + v_x*v_y)
    v_1 = mu_x1*mu_x1*v_y + mu_y0*mu_y0*v_x + v_x*v_y


    samples = [z_m1_samples, z_0_samples, z_1_samples]

    # Plots

    #
    # plt.figure(f"{pqmn}, histograms")
    #
    # n_bins = 20
    #
    # plt.subplot(1,3,1)
    # plt.hist(z_m1_samples, bins=n_bins)
    #
    # plt.subplot(1,3,2)
    # plt.hist(z_0_samples, bins=n_bins)
    #
    # plt.subplot(1,3,3)
    # plt.hist(z_1_samples, bins=n_bins)


    # plt.figure(f"{pqmn}, calculation")
    # plt.plot([z_m1_truth, z_0_truth, z_1_truth])
    #
    #
    # plt.plot([np.mean(s) for s in samples])

    plt.figure(f"{pqmn}, variance")
    plt.plot([v_m1, v_0, v_1])
    plt.plot([np.var(s) for s in samples])

    # plt.plot(np.array([np.mean(s) for s in samples]), np.array([np.var(s) for s in samples]))

plt.show()
