LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$(pwd)
nvcc --ptxas-options=-v --compiler-options '-fPIC' -o dep/libmaxmul.so --shared dep/maxmul.cu &&
maturin develop &&
python test.py

