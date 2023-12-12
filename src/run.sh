LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$(pwd)
source "${HOME}""/venvs""/neat/bin/activate"
cd neat
./build.sh
cd ../
python3 main.py
#pypy3 main.py


