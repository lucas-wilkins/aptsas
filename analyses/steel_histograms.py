import matplotlib.pyplot as plt

from pr.external_distance_histogram import ExternalHistogramData

for file_prefix in ["R5083_23208-v01-roi_tempered", "R5083_22972-v01_austenited"]:
    # for file_suffix in ["small", "full"]:
    for file_suffix in ["full"]:
        directory = f"../data/selections/{file_prefix}_{file_suffix}"

        data = ExternalHistogramData(directory, 24)

        data.plot(False)


plt.show()