#define PY_SSIZE_T_CLEAN
#include <python3.11/Python.h>
#include <python3.11/structmember.h>
#include <python3.11/floatobject.h>
#include <python3.11/modsupport.h>
#include <stdint.h>
#include <stdlib.h>



/*
    STRUCTS AND METHODS
*/


// Contains a genome and its resultant arrays.
typedef struct GenerationManager {
    PyObject_HEAD;
    //Genome genome;
} GenerationManager;


///// Deallocate a genome
//static void dealloc_generation_manager(GenerationManager* genome) {
//    //free(genome->nodes);
//    //free(genome->connections);
//}



/*
    INITIALIZATION AND DEALLOCATION
*/


static PyObject* GenerationManager_new(PyTypeObject* type, PyObject* args, PyObject* kwds) {
    GenerationManager* self;
    self = (GenerationManager*)type->tp_alloc(type, 0);
    if (self != NULL) {
        //self->genome.nodes = NULL;
        //self->genome.node_count = 0;
        //self->genome.connections = NULL;
        //self->genome.connection_count = 0;
    }
    return (PyObject*) self;
}


static int GenerationManager_init(GenerationManager *self, PyObject *args, PyObject *kwds) {
    return 0;
}


static void GenerationManager_dealloc(GenerationManager* self) {
    Py_TYPE(self)->tp_free((PyObject*) self);
}



/*
    GETTERS AND SETTERS
*/


//static PyObject* GenerationManager_get_node_count(GenerationManager* self, void* closure) {
//    return PyLong_FromLong(self->genome.node_count);
//}


//static PyObject* Creature_get_connection_count(Creature* self, void* closure) {
//    return PyLong_FromLong(self->genome.connection_count);
//}



/*
    METHODS
*/


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
    {NULL},
};


static PyMethodDef GenerationManager_methods[] = {
    //{"total_gene_count", (PyCFunction)total_gene_count, METH_NOARGS, "total gene count"},
    {NULL},
};


PyTypeObject PyGenerationManager = {
    .ob_base = PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "NEAT.GenerationManager",
    .tp_doc = PyDoc_STR("Manages all functionality for a NEAT generation."),
    .tp_basicsize = sizeof(PyGenerationManager),
    .tp_itemsize = 0,
    .tp_flags = Py_TPFLAGS_DEFAULT,
    .tp_new = GenerationManager_new,
    .tp_init = (initproc) GenerationManager_init,
    .tp_dealloc = (destructor) GenerationManager_dealloc,
    .tp_members = GenerationManager_members,
    .tp_getset = GenerationManager_getsetters,
    .tp_methods = GenerationManager_methods,
};



