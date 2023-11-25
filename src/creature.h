#ifndef CREATURE_H_
#define CREATURE_H_


#define PY_SSIZE_T_CLEAN
#include <python3.11/Python.h>
#include "genome.h"


// Contains a genome and its resultant arrays.
typedef struct Creature {
    PyObject_HEAD;
    Genome genome;
} Creature;


// Contains a genome and its resultant arrays, focused on the C backend.
typedef struct CCreature {
    Genome genome;
} CCreature;


extern PyTypeObject PyCreature;


#endif //CREATURE_H_

