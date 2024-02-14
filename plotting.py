import numpy as np


def show_sample(data: np.ndarray, autoshow: bool = True, n=10_000, name: str|None=None):
    import matplotlib.pyplot as plt

    if n < data.shape[0]:
        inds = np.random.choice(data.shape[0], size=n)
        data = data[inds, :]


    if name is None:
        plt.figure()
    else:
        plt.figure(name)

    plt.subplot(2, 2, 1)
    plt.scatter(data[:, 0], data[:, 1], s=0.1)
    plt.xlabel("X")
    plt.ylabel("Y")

    plt.subplot(2, 2, 2)
    plt.scatter(data[:, 0], data[:, 2], s=0.1)
    plt.xlabel("X")
    plt.ylabel("Z")

    plt.subplot(2, 2, 3)
    plt.scatter(data[:, 1], data[:, 2], s=0.1)
    plt.xlabel("Y")
    plt.ylabel("Z")

    plt.subplot(2, 2, 4)
    plt.hist(data[:, 3], bins=200)
    plt.xlabel("m/z")
    plt.ylabel("counts")

    if autoshow:
        plt.show()
