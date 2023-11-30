LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$(pwd)
nvcc --ptxas-options=-v --compiler-options '-fPIC' -o maxmul.so --shared maxmul.cu &&
gcc -shared -o neat.so -fPIC neat.c creature.c generation_manager.c genome.c maxmul.so &&
gcc -o testing testing.c vector.c &&
python3 testing.py
./testing

#LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$(pwd)
#echo hi2
#nvcc --ptxas-options=-v --compiler-options '-fPIC' -o libmaxmul.so --shared maxmul.cu
#echo hi1
#python3 testing.py
#echo hi





