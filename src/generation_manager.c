#define PY_SSIZE_T_CLEAN
#include <python3.11/Python.h>
#include <python3.11/structmember.h>
#include <python3.11/floatobject.h>
#include <python3.11/modsupport.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdio.h>
#include "genome.h"
#include "creature.h"



/*
    STRUCTS AND METHODS
*/


// Contains a genome and its resultant arrays.
typedef struct GenerationManager {
    PyObject_HEAD;

    long population_size; //used by C and Python
    long generation_number; //used by Python
    long input_count;
    long output_count;

    CCreature* population; //used by C
} GenerationManager;


///// Deallocate a genome
//static void dealloc_generation_manager(GenerationManager* genome) {
//    //free(genome->nodes);
//    //free(genome->connections);
//}


typedef struct Vector {
    int capacity;
    int length;
    int elem_size;
    char* elems;
} Vector;


// Create a new vector with default new size of 2
static Vector* vector_new(int elem_size) {
    Vector* vec = malloc(sizeof(Vector));
    vec->capacity = 2;
    vec->length = 0;
    vec->elem_size = elem_size;
    vec->elems = malloc(elem_size * 2);
    return vec;
}


// Simple method to push onto a Vector
static void vector_push(Vector* vec, void* val) {
    char* bval = (char*)val;
    if (vec->length < vec->capacity - 1) { //simply append the new value
        for (int i = 0; i < vec->elem_size; i++) { //push all bytes for the new value
            vec->elems[vec->length * vec->elem_size + i] = bval[i];
        }
        vec->length = vec->length + 1;
    } else { //need to reallocate, then push
        char* new_elems = malloc(vec->elem_size * vec->capacity * 2);
        memcpy(new_elems, vec->elems, vec->elem_size * vec->capacity);
        free(vec->elems);
        vec->elems = new_elems;

        // now push after reallocating
        for (int i = 0; i < vec->elem_size; i++) { //push all bytes for the new value
            vec->elems[vec->length * vec->elem_size + i] = bval[i];
        }
        vec->length = vec->length + 1;
    }
}


// Index a vector
static void* vector_index(Vector* vec, int index) {
    return &vec[index * vec->elem_size];
}


// Update a vector
static void vector_update(Vector* vec, int index, void* val) {
    char* cur = vector_index(vec, index);
    for (int i = 0; i < vec->elem_size; i++) { //push all bytes for the new value
        cur[i] = ((char*)val)[i];
    }
}


typedef struct Bucket {
    int in;
    Vector* outs;
} Bucket;


// Topological sort for a potential genome, returns NULL if invalid genome
static Topo* toposort(Genome* genome) {
    int len = genome->node_count;
    //int* layer_nums
    Vector* buckets = vector_new(sizeof(Bucket));
    return NULL;
}


// Initialize a new generation filled with dumb creatures
static CCreature* fresh_generation(GenerationManager* self) {
    long input_count = self->input_count;
    long output_count = self->output_count;
    CCreature* ret = malloc(sizeof(CCreature) * self->population_size);
    CCreature* cur;
    int random;

    // for every Creature
    for (int i = 0; i < self->population_size; i++) {
        cur = &ret[i];
        cur->genome.node_count = input_count + output_count;
        cur->genome.connection_count = input_count * output_count;
        cur->genome.nodes = malloc(sizeof(NodeGene) * (input_count + output_count));
        cur->genome.connections = malloc(sizeof(ConnectionGene) * (input_count * output_count));
        NodeGene* nodes = cur->genome.nodes;
        ConnectionGene* connections = cur->genome.connections;

        // create input nodes
        for (int j = 0; j < input_count; j++) {
            nodes[j].id = j;
            nodes[j].type = 0;
        }

        // create output nodes and connections
        for (int j = 0; j < output_count; j++) { //for every output
            nodes[j + input_count].id = j + input_count; //create output node
            nodes[j + input_count].type = 1;

            for (int k = 0; k < input_count; k++) { //connect this output node to every input
                connections[j * input_count + k].in = k;
                connections[j * input_count + k].out = j + input_count;
                connections[j * input_count + k].innov = j * input_count + k;
                random = rand(); //positive up to 2_147_483_647
                connections[j * input_count + k].weight = (double)random / 214748364 - 5; //randomized from -5 to 5
                random = rand(); //positive up to 2_147_483_647
                connections[j * input_count + k].enabled = random % 2; //randomized 0 or 1
            }
        }
    }

    // run arrays initializer to convert the genes into arrays, need to make function for that
    return ret;
}



/*
    INITIALIZATION AND DEALLOCATION
*/


static PyObject* GenerationManager_new(PyTypeObject* type, PyObject* args, PyObject* kwds) {
    GenerationManager* self;
    self = (GenerationManager*)type->tp_alloc(type, 0);
    if (self == NULL) {
        Py_RETURN_NONE;
    }
    //self->genome.nodes = NULL; //self->genome.node_count = 0;
    //self->genome.connections = NULL;
    //self->genome.connection_count = 0;
    //self->population_size = 0;
    //self->population = fresh_generation();
    //self->generation_number = 0;
    return (PyObject*) self;
}


static int GenerationManager_init(GenerationManager *self, PyObject *args, PyObject *kwds) {
    static char *kwlist[] = {"input_count", "output_count", "population_size", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, kwds, "lll", kwlist, &self->input_count, &self->output_count, &self->population_size)) {
        return -1;
    }
    if (self->input_count < 1 || self->output_count < 1 || self->population_size < 1) {
        PyErr_SetString(PyExc_ValueError, "input_count, output_count, and population_size must be integers greater than 0");
        return -1;
    }
    self->generation_number = 0;
    return 0;
}


static void GenerationManager_dealloc(GenerationManager* self) {
    Py_TYPE(self)->tp_free((PyObject*) self);
}



/*
    GETTERS AND SETTERS
*/


static PyObject* GenerationManager_get_population_size(GenerationManager* self, void* closure) {
    return PyLong_FromLong(self->population_size);
}


//static PyObject* Creature_get_connection_count(Creature* self, void* closure) {
//    return PyLong_FromLong(self->genome.connection_count);
//}



/*
    METHODS
*/


// Manages deallocations when updating the population
static void deallocate_population(CCreature* old, int count) {
    for (int i = 999; i > 999 - count; i--) {
        deallocate_ccreature_internals(&old[i]);
    }
    free(old);
}


// Converts a CCreature to a Creature, but be warned about deallocation
static PyObject* creature_as_python_pointer(CCreature* ccreature) {
    Creature* creature;

    if (PyType_Ready(&PyCreature) != 0) {
        Py_RETURN_NONE;
    }
    creature = PyObject_New(Creature, &PyCreature);
    creature = (Creature*)PyObject_Init((PyObject*)creature, &PyCreature);

    if (creature == NULL) {
        Py_RETURN_NONE;
    }
    creature->arrays = &ccreature->arrays;
    return (PyObject*)creature;
}


// Converts a CCreature to a Creature, but copies all arrays
static PyObject* creature_as_python_unique(CCreature* ccreature) {
    Creature* creature;

    if (PyType_Ready(&PyCreature) != 0) {
        Py_RETURN_NONE;
    }
    creature = PyObject_New(Creature, &PyCreature);
    creature = (Creature*)PyObject_Init((PyObject*)creature, &PyCreature);

    if (creature == NULL) {
        Py_RETURN_NONE;
    }
    copy_arrays(creature->arrays, &ccreature->arrays);
    return (PyObject*)creature;
}


// Return the current best Creature in this generation (with a copied set of arrays)
static PyObject* get_current_best(GenerationManager* self, PyObject* Py_UNUSED(ignored)) {
    return creature_as_python_unique(&self->population[0]);
}


// Return the entire current generation as a Python list of Creatures
static PyObject* get_current_generation(GenerationManager* self, PyObject* Py_UNUSED(ignored)) {
    PyObject* gen_list = PyList_New(self->population_size);
    if (gen_list == NULL) {
        Py_RETURN_NONE;
    }
    PyObject* cur_creature;
    for (int i = 0; i < self->population_size; i++) {
        PyList_SetItem(gen_list, i, creature_as_python_pointer(&self->population[i]));
    }
    Py_RETURN_NONE;
}






//static PyObject* total_gene_count(Creature* self, PyObject* Py_UNUSED(ignored)) {
//    return PyLong_FromLong(self->genome.connection_count + self->genome.node_count);
//}



/*
    FINALIZING
*/


static PyMemberDef GenerationManager_members[] = {
    {NULL},
};


static PyGetSetDef GenerationManager_getsetters[] = {
    //{"node_count", (getter)Creature_get_node_count, (setter)NULL, "node count", NULL},
    //{"connection_count", (getter)Creature_get_connection_count, (setter)NULL, "connection count", NULL},
    {"population_size", (getter)GenerationManager_get_population_size, (setter)NULL, "population size", NULL},
    {NULL},
};


static PyMethodDef GenerationManager_methods[] = {
    //{"total_gene_count", (PyCFunction)total_gene_count, METH_NOARGS, "total gene count"},
    {"get_current_best", (PyCFunction)get_current_best, METH_NOARGS, "get current best"},
    {NULL},
};


PyTypeObject PyGenerationManager = {
    .ob_base = PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "NEAT.GenerationManager",
    .tp_doc = PyDoc_STR("Manages all functionality for a NEAT generation."),
    .tp_basicsize = sizeof(GenerationManager),
    .tp_itemsize = 0,
    .tp_flags = Py_TPFLAGS_DEFAULT,
    .tp_new = GenerationManager_new,
    .tp_init = (initproc) GenerationManager_init,
    .tp_dealloc = (destructor) GenerationManager_dealloc,
    .tp_members = GenerationManager_members,
    .tp_getset = GenerationManager_getsetters,
    .tp_methods = GenerationManager_methods,
};



