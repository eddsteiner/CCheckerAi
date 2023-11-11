#ifndef STRUCTMANAGER_H_
#define STRUCTMANAGER_H_


#define PY_SSIZE_T_CLEAN
#include <python3.10/Python.h>
#include <python3.10/structmember.h>
#include "coords.h"

//PyObject* StructManager_new(PyTypeObject* type, PyObject* args, PyObject* kwds);
//int StructManager_init(Coords *self, PyObject *args, PyObject *kwds);
//void StructManager_dealloc(Coords* self);

//extern PyMemberDef StructManager_members[];
//extern PyMethodDef StructManager_methods[];
//extern PyTypeObject StructManager;

static PyObject* StructManager_new(PyTypeObject* type, PyObject* args, PyObject* kwds) {
    Coords* self;
    self = (Coords*) type->tp_alloc(type, 0);
    if (self != NULL) {
        self->x = 0.0;
        self->y = 0.0;
    }
    return (PyObject*) self;
}


static int StructManager_init(Coords *self, PyObject *args, PyObject *kwds) {
    static char *kwlist[] = {"first", "last", "number", NULL};

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "|ff", kwlist,
                                     &self->x,
                                     &self->y))
        return -1;
    return 0;
}


static void StructManager_dealloc(Coords* self) {
    //Py_XDECREF(self->first); //deallocates python objects
    //Py_XDECREF(self->last);
    Py_TYPE(self)->tp_free((PyObject*) self);
}

static PyMemberDef StructManager_members[] = {
    {"x", T_FLOAT, offsetof(Coords, x), 0,
     "x coord"},
    {"y", T_FLOAT, offsetof(Coords, y), 0,
     "y coord"},
    {NULL}  /* Sentinel */
};


static PyMethodDef StructManager_methods[] = {
    //{"name", (PyCFunction) Custom_name, METH_NOARGS,
    // "Return the name, combining the first and last name"
    //},
    {NULL}  /* Sentinel */
};

static PyTypeObject StructManager = {
    .ob_base = PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "structManager.StructManager",
    .tp_doc = PyDoc_STR("Manages a struct"),
    .tp_basicsize = sizeof(Coords),
    .tp_itemsize = 0,
    .tp_flags = Py_TPFLAGS_DEFAULT,
    .tp_new = StructManager_new,
    .tp_init = (initproc) StructManager_init,
    .tp_dealloc = (destructor) StructManager_dealloc,
    .tp_members = StructManager_members,
    .tp_methods = StructManager_methods,
};


#endif // STRUCTMANAGER_H_
