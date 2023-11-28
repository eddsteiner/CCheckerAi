#ifndef CREATURE_H_
#define CREATURE_H_


#define PY_SSIZE_T_CLEAN
#include <python3.11/Python.h>
#include "genome.h"


// Contains a genome and its resultant arrays.
typedef struct Creature {
    PyObject_HEAD;
    Arrays* arrays;
} Creature;


// Contains a genome and its resultant arrays, focused on the C backend.
typedef struct CCreature {
    Genome genome;
    Arrays arrays;
} CCreature;


// Simple way to deallocate a CCreature's internals.
static void deallocate_ccreature_internals(CCreature* ccreature) {
    dealloc_genome_internals(&ccreature->genome);
    dealloc_array_internals(&ccreature->arrays);
}


extern PyTypeObject PyCreature;


#endif //CREATURE_H_

