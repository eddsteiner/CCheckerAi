# CCheckerAI
The purpose of this repository is to train an AI using NEAT to
play chinese checkers.

### Instructions
Prerequisites: install cuda build tools, python, rust, and maturin
Make sure to launch a python virtual environment before building
```
  cd src/neat
  ./build.sh
  cd ..
  LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$(pwd) python3 main.py
```

