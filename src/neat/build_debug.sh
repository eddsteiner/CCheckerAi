LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$(pwd)
nvcc --ptxas-options=-v --compiler-options '-fPIC' -o dep/libfeedforward.so --shared dep/feedforward.cu &&
maturin develop

