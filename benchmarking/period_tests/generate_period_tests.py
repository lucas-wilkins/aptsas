from period_tests import sample_cosine_3d
import numpy as np


size = 200

n_points = 100_000

rel_freqs = [int(p) for p in np.arange(1, 21)]

for rel_freq in rel_freqs:
    freq = rel_freq/size

    for run in range(3):

        print(rel_freq, freq, run)

        filename = "../../data/simulated/period_tests/%03i_%i.pos"%(rel_freq, run)

        data = sample_cosine_3d(freq, size, 0, 0, 0, n_points)

        data = np.hstack([data, 12*np.ones((data.shape[0], 1))])

        with open(filename, 'wb') as fid:
            # bigendian 64-bit floats
            dt = np.dtype('f')
            dt = dt.newbyteorder('>')

            fid.write(np.array(data, dtype=dt).tobytes())

