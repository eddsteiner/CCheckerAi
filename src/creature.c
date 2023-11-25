#define PY_SSIZE_T_CLEAN
#include <python3.11/Python.h>
#include <python3.11/structmember.h>
#include <python3.11/floatobject.h>
#include <python3.11/modsupport.h>
#include <stdint.h>
#include <stdlib.h>
#include "creature.h"



/*
    STRUCTS AND METHODS
*/


static NodeGene* push_node(Genome* genome, NodeGene* node) {
    int cur_size = genome->node_count;
    NodeGene* new_nodes = malloc(sizeof(NodeGene) * cur_size + 1);

    // TODO

    return new_nodes;
}



/*
    INITIALIZATION AND DEALLOCATION
*/


static PyObject* Creature_new(PyTypeObject* type, PyObject* args, PyObject* kwds) {
    Creature* self;
    self = (Creature*)type->tp_alloc(type, 0);
    if (self != NULL) {
        self->genome.nodes = NULL;
        self->genome.node_count = 0;
        self->genome.connections = NULL;
        self->genome.connection_count = 0;
    }
    return (PyObject*) self;
}


static int Creature_init(Creature *self, PyObject *args, PyObject *kwds) {
    return 0;
}


static void Creature_dealloc(Creature* self) {
    dealloc_genome_internals(&self->genome); //deallocate the genome first
    Py_TYPE(self)->tp_free((PyObject*) self);
}



/*
    GETTERS AND SETTERS
*/


static PyObject* Creature_get_node_count(Creature* self, void* closure) {
    return PyLong_FromLong(self->genome.node_count);
}


static PyObject* Creature_get_connection_count(Creature* self, void* closure) {
    return PyLong_FromLong(self->genome.connection_count);
}



/*
    METHODS
*/


static PyObject* total_gene_count(Creature* self, PyObject* Py_UNUSED(ignored)) {
    return PyLong_FromLong(self->genome.connection_count + self->genome.node_count);
}



/*
    FINALIZING
*/


static PyMemberDef Creature_members[] = {
    {NULL},
};


static PyGetSetDef Creature_getsetters[] = {
    {"node_count", (getter)Creature_get_node_count, (setter)NULL, "node count", NULL},
    {"connection_count", (getter)Creature_get_connection_count, (setter)NULL, "connection count", NULL},
    {NULL},
};


static PyMethodDef Creature_methods[] = {
    {"total_gene_count", (PyCFunction)total_gene_count, METH_NOARGS, "total gene count"},
    {NULL},
};


PyTypeObject PyCreature = {
    .ob_base = PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "NEAT.Creature",
    .tp_doc = PyDoc_STR("An individual Creature which can play Chinese Checkers."),
    .tp_basicsize = sizeof(Creature),
    .tp_itemsize = 0,
    .tp_flags = Py_TPFLAGS_DEFAULT,
    .tp_new = Creature_new,
    .tp_init = (initproc) Creature_init,
    .tp_dealloc = (destructor) Creature_dealloc,
    .tp_members = Creature_members,
    .tp_getset = Creature_getsetters,
    .tp_methods = Creature_methods,
};



