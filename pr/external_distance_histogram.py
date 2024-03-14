import math
import os
import pickle
import time
import subprocess

class ExternalHistogrammer:
    def __init__(self, directory: str, delta_r: float, max_r: float, max_cores=10, cmd="distance_histogram"):
        self.directory = directory
        self.output_directory = os.path.join(self.directory, "histograms")
        self.cmd = cmd

        if not os.path.exists(self.output_directory):
            os.mkdir(self.output_directory)

        self.delta_r = delta_r
        self.max_radius = max_r
        self.cores_parameter = int(math.sqrt(max_cores))

        with open(os.path.join(self.directory, "metadata.pickle"), 'rb') as fid:
            self.ions_to_atoms = pickle.load(fid)

        self.ion_types = [ion for ion in self.ions_to_atoms.keys()]

        self.counts = []
        for ion in self.ion_types:
            file_size = os.path.getsize(os.path.join(self.directory, f"{ion}.xyz"))
            self.counts.append(file_size // 24)


    def run(self):

        with open(os.path.join(self.output_directory, "log.log"), 'w') as logfile:

            for i, (ion1, count1) in enumerate(zip(self.ion_types, self.counts)):
                for ion2, count2 in zip(self.ion_types[i:], self.counts[i:]):
                    print(ion1, ion2)

                    tic = time.time()

                    # Set up request

                    input_filename_1 = os.path.join(self.directory, f"{ion1}.xyz")
                    input_filename_2 = os.path.join(self.directory, f"{ion2}.xyz")

                    output_filename = os.path.join(self.output_directory, f"{ion1}-{ion2}.csv")

                    process = subprocess.Popen([
                        self.cmd,
                        input_filename_1, input_filename_2,
                        f"-o{output_filename}",
                        f"-d{self.delta_r}",
                        f"-m{self.max_radius}",
                        f"-n{self.cores_parameter}"])

                    process.wait()

                    # done

                    toc = time.time() - tic

                    self_entries = count1 if ion1 == ion2 else 0
                    log_entry = f"{ion1}, {ion2}, {count1}, {count2}, {count1*count2}, {self_entries}, {toc}\n"

                    logfile.write(log_entry)