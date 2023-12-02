import maturin_testing as mt
import numpy as np

a = np.array([-1, 2, 4, 0, 5, 3, 6, 2, 1], dtype = np.int32)
apoint = a.ctypes.data

mt.test_cuda()
mt.test_pointer(apoint, len(a))
