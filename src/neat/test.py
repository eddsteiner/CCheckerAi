import neat
import numpy as np

a = np.array([-1, 2, 4, 0, 5, 3, 6, 2, 1], dtype = np.int32)
apoint = a.ctypes.data

neat.test_cuda()
neat.test_pointer(apoint, len(a))
