LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$(pwd)
nvcc --ptxas-options=-v --compiler-options '-fPIC' -o maxmul.so --shared maxmul.cu &&
gcc -shared -o neat.so -fPIC neat.c creature.c generation_manager.c genome.c vector.c maxmul.so &&
python3 main.py





