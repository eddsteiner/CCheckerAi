nvcc --ptxas-options=-v --compiler-options '-fPIC' -o libmaxmul.so --shared maxmul.cu &&
gcc pythoncuda.c -o pythoncuda libmaxmul.so &&
LD_LIBRARY_PATH=. python cudatest.py




