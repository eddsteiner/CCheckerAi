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
#include "vector.h"



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

    int initialized; //0 until a new population is generated or one is loaded
    Vector* input_node_ids; //makes life easier
    Vector* output_node_ids; //makes life easier

    CCreature* population; //used by C
} GenerationManager;


///// Deallocate a genome
//static void dealloc_generation_manager(GenerationManager* genome) {
//    //free(genome->nodes);
//    //free(genome->connections);
//}


typedef struct Bucket {
    int in;
    Vector* outs; //vector of ints
} Bucket;


// Topological sort for a potential genome, returns NULL if invalid genome
static Vector* toposort(GenerationManager* self, Genome* genome) {
    long* bufl = malloc(sizeof(long*)); //for all interfacing needs
    int* buf = malloc(sizeof(int*)); //for all interfacing needs
    int len = genome->node_count;
    Vector* buckets = vector_new(sizeof(Bucket)); //contains a list of buckets, each having an "in" and many "outs", all ids of nodes
    Vector* bucket_labels = vector_new(sizeof(int)); //helps to index buckets, contains the "in" for each bucket
    ConnectionGene* cur_connection;

    // first push all the input nodes to the buckets
    for (int i = 0; i < self->input_count; i++) {
        Bucket* new_buck = malloc(sizeof(Bucket));
        new_buck->in = genome->nodes->id;
        new_buck->outs = vector_new(sizeof(int));
    }

    // then push all the connections (excluding output nodes)
    for (int i = 0; i < genome->connection_count; i++) {
        cur_connection = &genome->connections[i];

        if (cur_connection->enabled == 0) { //skip any disabled connections
            continue;
        }
        if (vector_in(self->output_node_ids, &cur_connection->out)) { //don't push output nodes to a bucket
            continue;
        }

        *buf = cur_connection->in;
        int index = vector_in(bucket_labels, buf); //see if we already have this bucket
        if (index > -1) { //we've already got this node in the buckets, so grab it and append this node
            Bucket* cur_buck = vector_index(buckets, index);
            vector_push(cur_buck->outs, &cur_connection->out); //push the id of this connection's out node
        } else { //we don't have this node yet, push it and append this node
            vector_push(bucket_labels, &cur_connection->in); //push the name of the new in to buckets
            Bucket* new_buck = malloc(sizeof(Bucket));
            new_buck->in = cur_connection->in;
            new_buck->outs = vector_new(sizeof(int*));
            vector_push(new_buck->outs, &cur_connection->out); //push the connection
            *bufl = (long)new_buck;
            vector_push(buckets, bufl); //push the new bucket's address to the overall list of buckets
        }
    }

    // we have the buckets, now run the actual toposort
    // start by pushing the input nodes
    Vector* cur_layer = vector_new(sizeof(int)); //remember to start with only the input nodes
    Vector* new_layer;
    Vector* layer_nums = vector_new(sizeof(int)); //the final layer number for every node
    Vector* layer_labels = vector_new(sizeof(int)); //used to index the layer_nums vector
    for (int i = 0; i < self->input_count; i++) {
        *buf = i;
        vector_push(cur_layer, buf); //input nodes are always numbered 0..n
        vector_push(layer_labels, buf);
        *buf = 0;
        vector_push(layer_labels, buf); //start all nodes on layer 0
    }

    // now keep calculating the new layers until we reach only output nodes
    HashTable* hashtable = hashtable_new(sizeof(Vector*)); //store vectors of ints
    int running = 1;
    int loop_count = 0;
    while (running) { //runs once for every layer, making sure we haven't seen a particular layer before
        loop_count += 1;
        new_layer = vector_new(sizeof(int)); //create the next layer
        for (int i = 0; i < cur_layer->length; i++) { //want to iterate through all the current nodes
            int cur_node = *(int*)vector_index(cur_layer, i); //the node id we're currently looking at
            *buf = cur_node;
            int index = vector_in(bucket_labels, buf); //grab the bucket for the current node if it exists (it should)
            Bucket* cur_bucket = *(Bucket**)vector_index(buckets, index);
            if (cur_bucket->in != cur_node) {
                printf("BIGGGG ERRORRRRRRRR\n");
                //TODO DEALLOCATE
                return NULL;
            }
            Vector* outs = cur_bucket->outs;
            for (int j = 0; j < outs->length; j++) { //append all the outs to the new layer (no output nodes should be in any bucket)
                if (vector_in(new_layer, vector_index(outs, j)) == -1) { //if we haven't seen this out node before push it
                    vector_push(new_layer, vector_index(outs, j));
                }
            }
        }

        // all the nodes of the next layer have been pushed to new_layer
        // check whether this layer is unique or empty (output nodes shouldn't be part of the problem)
        //int hash = hashtable_hash_simple((void*)cur_layer->elems, cur_layer->length);
        if (new_layer->length == 0) { //empty, so we're done! finish up
            //int max_layer = loop_count - 1; //this loop didn't result in a new layer so we finished one ago
            Vector* layers = malloc(sizeof(Vector) * loop_count); //one vector per layer
            for (int i = 0; i < loop_count; i++) {
                layers[i] = *vector_new(sizeof(int)); //initialize all vectors
            }
            for (int i = 0; i < layer_nums->length; i++) { //go through all node ids and their layers
                int index = *(int*)vector_index(layer_nums, i);
                int* id = (int*)vector_index(layer_labels, i);
                vector_push(&layers[index], id); //push the id to the layer vector
            }
            return layers;
            
            //TODO DEALLOCATE
        }

        int contained = hashtable_contains_int_vector(hashtable, new_layer);
        if (contained == 1) { //we've already seen this vector before, genome is NOT ACYCLIC!!!
            //TODO DEALLOCATE
            return NULL;
        }

        // the new layer is not empty, so we'll have to update the layer nums and keep going
        for (int i = 0; i < new_layer->length; i++) {
            int* id = (int*)vector_index(new_layer, i); //grab the current node's id
            int index = vector_in(layer_labels, id); //grab the id's index
            *buf = loop_count;
            vector_update(layer_nums, *id, buf); //use this index to update the id's layer number
        }
        hashtable_push_int_vector(hashtable, new_layer); //remember this layer

        cur_layer = new_layer;
    }

    // unsure how to get here
    return NULL;
}


// Initialize a new generation filled with dumb creatures
static CCreature* fresh_generation(GenerationManager* self) {
    int* buf = malloc(sizeof(int));
    long input_count = self->input_count;
    long output_count = self->output_count;
    CCreature* ret = malloc(sizeof(CCreature) * self->population_size);
    CCreature* cur;
    int random;
    self->input_node_ids = vector_new(sizeof(int)); //we'll update the handy input and output node ids too
    self->output_node_ids = vector_new(sizeof(int));

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
            *buf = j; 
            vector_push(self->input_node_ids, buf); //makes life easier
        }

        // create output nodes and connections
        for (int j = 0; j < output_count; j++) { //for every output
            nodes[j + input_count].id = j + input_count; //create output node
            nodes[j + input_count].type = 1;
            *buf = j + input_count; 
            vector_push(self->output_node_ids, buf); //makes life easier

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

        // run toposort and get back the results
        Vector* topo = toposort(self, &cur->genome);

        // run arrays initializer to convert the genes into arrays, need to make function for that
        // TODO


    }

    //printf("testing, here\n");
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
    self->initialized = 0;
    // need to create a fresh generation here, or keep a boolean that says you need to call a fresh generation or load one
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



