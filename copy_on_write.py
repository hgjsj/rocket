import numpy as np
import mmap

mm = np.lib.format.open_memmap("/tmp/test.log", mode="w+", shape=(1024,1024,50))
mm[::] = 1
cow = np.lib.format.open_memmap("/tmp/test.log", mode="c", shape=(1024,1024,50))
cow[0,0,0] = 6
print(mm[0,0,0])
print(cow[0,0,0])
cow[::] = 7
