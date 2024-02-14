import struct
import sys

import matplotlib.pyplot as plt

filename = "R5083_23208-v01-roi.pos"

with open(filename, 'rb') as fid:

    x = []
    y = []
    z = []
    m = []

    data = fid.read()
    for i in range(0,100000,16):
        unpacked = struct.unpack('>ffff', data[i:i+16])
        print(unpacked)

        x.append(unpacked[0])
        y.append(unpacked[1])
        z.append(unpacked[2])
        m.append(unpacked[3])

#plt.scatter(x,y)
#plt.scatter(x,z)

plt.hist(m, bins=1000)
plt.show()

    
