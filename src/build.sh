nvcc --ptxas-options=-v --compiler-options '-fPIC' -o libmaxmul.so --shared maxmul.cu &&
gcc -shared -o neat.so -fPIC neat.c libmaxmul.so &&
LD_LIBRARY_PATH=. python testing.py





