#nvcc -c -o libmaxmul.so maxmul.cu
nvcc --ptxas-options=-v --compiler-options '-fPIC' -o libmaxmul.so --shared maxmul.cu
gcc cudatest.c -o cudatest libmaxmul.so
LD_LIBRARY_PATH=. ./cudatest


