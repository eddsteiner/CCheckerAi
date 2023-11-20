LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$(pwd)
nvcc --ptxas-options=-v --compiler-options '-fPIC' -o libmaxmul.so --shared maxmul.cu &&
gcc -shared -o neat.so -fPIC neat.c libmaxmul.so &&
python3 testing.py

#LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$(pwd)
#echo hi2
#nvcc --ptxas-options=-v --compiler-options '-fPIC' -o libmaxmul.so --shared maxmul.cu
#echo hi1
#python3 testing.py
#echo hi





