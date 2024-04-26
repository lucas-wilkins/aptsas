import math
import os
import pickle
import time
import subprocess
import pathlib

import numpy as np

from shape_factors import sphere_undersampling_integral_with_r_squared

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
            ion_file = os.path.join(self.directory, f"{ion}.xyz")
            if os.path.exists(ion_file):
                file_size = os.path.getsize(ion_file)

                self.counts.append(file_size // 24)
            else:
                self.counts.append(0)


    def run(self):

        with open(os.path.join(self.output_directory, "log.log"), 'w') as logfile:

            for i, (ion1, count1) in enumerate(zip(self.ion_types, self.counts)):
                if count1 == 0:
                    continue

                for ion2, count2 in zip(self.ion_types[i:], self.counts[i:]):
                    if count2 == 0:
                        continue

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


class ExternalHistogramData:
    def __init__(self, directory: str, radius: float):

        self.name = directory
        self.radius = radius
        self.volume = (4/3)*np.pi*(radius**3)

        base = pathlib.Path(directory)
        metadata = base / "metadata.pickle"
        with open(metadata, 'rb') as fid:
            self.ions_makeup = pickle.load(fid)
            self.ions = [ion for ion in self.ions_makeup.keys()]

        data_dir = base / "histograms"

        self.selfs = {}
        self.means = {}
        with open(data_dir / "log.log", 'r') as fid:
            for line in fid:
                parts = line.split(",")
                ion1 = parts[0].strip()
                ion2 = parts[1].strip()

                if ion1 in self.selfs:
                    self.selfs[ion1][ion2] = float(parts[5])
                else:
                    self.selfs[ion1] = {ion2: float(parts[5])}

                if ion1 in self.means:
                    self.means[ion1][ion2] = float(parts[4]) / (self.volume**2)
                else:
                    self.means[ion1] = {ion2: float(parts[4]) / (self.volume**2)}


        self.raw_data = {}
        self.raw_no_selfs = {}
        self.scaled_data = {}
        self.r_left = None
        self.r_right = None

        for i, ion1 in enumerate(self.ions):
            for ion2 in self.ions[i:]:
                filename = data_dir / f"{ion1}-{ion2}.csv"
                print(filename)

                lefts = []
                rights = []
                values = []

                with open(filename, 'r') as fid:
                    for line in fid:
                        parts = line.split(",")
                        lefts.append(float(parts[0]))
                        rights.append(float(parts[1]))
                        values.append(float(parts[2]))

                self.r_left = np.array(lefts)
                self.r_right = np.array(rights)
                self.bin_sizes = self.r_right - self.r_left

                # calculate scaling factor
                left_int = sphere_undersampling_integral_with_r_squared(self.r_left, radius)
                right_int = sphere_undersampling_integral_with_r_squared(self.r_right, radius)

                scaling = (right_int - left_int)/(self.bin_sizes**3)

                values = np.array(values)
                if ion1 in self.raw_data:
                    self.raw_data[ion1][ion2] = values
                else:
                    self.raw_data[ion1] = {ion2: values}

                no_selfs = values.copy()
                no_selfs[0] -= self.selfs[ion1][ion2]
                if ion1 in self.raw_no_selfs:
                    self.raw_no_selfs[ion1][ion2] = no_selfs
                else:
                    self.raw_no_selfs[ion1] = {ion2: no_selfs}

                if ion1 in self.scaled_data:
                    self.scaled_data[ion1][ion2] = no_selfs/scaling
                else:
                    self.scaled_data[ion1] = {ion2: no_selfs/scaling}

        self.r_mid = 0.5*(self.r_left + self.r_right)


        # Calculate the atom-wise data

        for ion1 in self.ions:
            for ion2 in self.ions:
                pass

    def plot(self, autoshow=True):
        import matplotlib.pyplot as plt
        n_ions = len(self.ions)

        plt.figure(self.name)

        for i, ion1 in enumerate(self.ions):
            for j, ion2 in enumerate(self.ions):
                if j >= i:
                    plt.subplot(n_ions, n_ions, i+n_ions*j + 1)
                    # plt.title(f"{i}, {j}")

                    plt.plot(self.r_mid, self.scaled_data[ion1][ion2])

                    means = np.ones_like(self.r_mid)*self.means[ion1][ion2]
                    plt.plot(self.r_mid, means)

                    plt.xticks([])
                    plt.yticks([])

        if autoshow:
            plt.show()