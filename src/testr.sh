LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$(pwd)
source "${HOME}""/venvs""/neat/bin/activate"
cd neat
./test.sh
./testing
cd ../
python3 testing.py


#LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$(pwd)
#echo hi2
#nvcc --ptxas-options=-v --compiler-options '-fPIC' -o libmaxmul.so --shared maxmul.cu
#echo hi1
#python3 testing.py
#echo hi




