from pr.external_distance_histogram import ExternalHistogrammer

cmd = "../../distance_histograms/target/debug/distance_histograms.exe"

for file_prefix in ["R5083_23208-v01-roi_tempered", "R5083_22972-v01_austenited"]:
    for file_suffix in ["small", "full"]:
        directory = f"../data/selections/{file_prefix}_{file_suffix}"

        print(directory)

        histogrammer = ExternalHistogrammer(directory, delta_r=0.1, max_r=48, max_cores=10, cmd=cmd)

        histogrammer.run()
