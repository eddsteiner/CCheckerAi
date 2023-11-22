#ifndef CREATURE_H_
#define CREATURE_H_


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


typedef struct NodeGene NodeGene;
typedef struct ConnectionGene ConnectionGene;
typedef struct Genome Genome;
typedef struct Creature Creature;

void dealloc_genome(Genome* genome);
NodeGene* push_node(Genome* genome, NodeGene* node);



/*
    INITIALIZATION AND DEALLOCATION
*/


PyObject* Creature_new(PyTypeObject* type, PyObject* args, PyObject* kwds);
int Creature_init(Creature *self, PyObject *args, PyObject *kwds);
void Creature_dealloc(Creature* self);



/*
    GETTERS AND SETTERS
*/


PyObject* Creature_get_node_count(Creature* self, void* closure);
PyObject* Creature_get_connection_count(Creature* self, void* closure);



/*
    METHODS
*/


PyObject* total_gene_count(Creature* self, PyObject* Py_UNUSED(ignored));



/*
    FINALIZING
*/

//static PyMemberDef Creature_members[] = {
//    {NULL},
//};
//
//
//static PyGetSetDef Creature_getsetters[] = {
//    {"node_count", (getter)Creature_get_node_count, (setter)NULL, "node count", NULL},
//    {"connection_count", (getter)Creature_get_connection_count, (setter)NULL, "connection count", NULL},
//    {NULL},
//};
//
//
//static PyMethodDef Creature_methods[] = {
//    {"total_gene_count", (PyCFunction)total_gene_count, METH_NOARGS, "total gene count"},
//    {NULL},
//};
//
//
//static PyTypeObject PyCreature = {
//    .ob_base = PyVarObject_HEAD_INIT(NULL, 0)
//    .tp_name = "NEAT.Creature",
//    .tp_doc = PyDoc_STR("TODO description"),
//    .tp_basicsize = sizeof(PyCreature),
//    .tp_itemsize = 0,
//    .tp_flags = Py_TPFLAGS_DEFAULT,
//    .tp_new = Creature_new,
//    .tp_init = (initproc) Creature_init,
//    .tp_dealloc = (destructor) Creature_dealloc,
//    .tp_members = Creature_members,
//    .tp_getset = Creature_getsetters,
//    .tp_methods = Creature_methods,
//};

extern PyTypeObject PyCreature;


#endif //CREATURE_H_

