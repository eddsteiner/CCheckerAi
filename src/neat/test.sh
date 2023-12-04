LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$(pwd)
nvcc --ptxas-options=-v --compiler-options '-fPIC' -o lib/libmaxmul.so --shared lib/maxmul.cu &&
maturin develop
python test.py

