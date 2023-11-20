import ctypes
import numpy as np

print("aaa")

a = np.array([-1, 2, 4, 0, 5, 3, 6, 2, 1], dtype = np.float32)
b = np.array([3, 0, 2, 3, 4, 5, 4, 7, 2], dtype = np.float32)
c = np.zeros(9, dtype = np.float32)

#apoint, read_only_flag = a.__array_interface__["data"]
#bpoint, read_only_flag = b.__array_interface__["data"]
#cpoint, read_only_flag = c.__array_interface__["data"]
apoint = ctypes.c_long(a.ctypes.data)
bpoint = ctypes.c_long(b.ctypes.data)
cpoint = ctypes.c_long(c.ctypes.data)

print("\nCTYPES TESTING")
#clong = ctypes.c_long(point)
#print(f"new point: {clong}")
testdll = ctypes.cdll.LoadLibrary("./libmaxmul.so")

print(apoint)
print(bpoint)
print(cpoint)

print(a)
print(b)
print(c)

print(testdll.maxmul)
print(testdll.maxmul.argtypes)
#res = testdll.maxmul(ctypes.pointer(apoint), ctypes.pointer(bpoint), ctypes.pointer(cpoint), 3)
res = testdll.maxmul(apoint, bpoint, cpoint, 3)
print(res)
print(c)

