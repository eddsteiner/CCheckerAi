nvcc -c -o libmaxmul.so maxmul.cu
python setup.py build
#cp build/lib.linux-x86_64-3.10/Example.cpython-310-x86_64-linux-gnu.so .
cp build/lib.linux-x86_64-cpython-310/Example.cpython-310-x86_64-linux-gnu.so .
#nvcc --ptxas-options=-v --compiler-options '-fPIC' -o libmaxmul.so --shared maxmul.cu

