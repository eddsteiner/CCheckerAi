#ifndef STRUCTMANAGER_H_
#define STRUCTMANAGER_H_


#define PY_SSIZE_T_CLEAN
#include <python3.10/Python.h>
#include <python3.10/structmember.h>
#include <python3.10/floatobject.h>
#include <python3.10/modsupport.h>
#include "coords.h"



/*
    INITIALIZATION AND DEALLOCATION
*/


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
    static char *kwlist[] = {"x", "y", NULL};

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "|ff", kwlist,
            &self->x, &self->y)) {
        return -1;
    }
    return 0;
}


static void StructManager_dealloc(Coords* self) {
    //Py_XDECREF(self->first); //deallocates python objects
    //Py_XDECREF(self->last);
    Py_TYPE(self)->tp_free((PyObject*) self);
}



/*
    GETTERS AND SETTERS
*/


//static double StructManager_getx(Coords* self, void *closure) {
//    return self->x;
//}

static PyObject* StructManager_getx(Coords* self, void* closure) {
    return PyFloat_FromDouble(self->x);
}


static PyObject* StructManager_gety(Coords* self, void* closure) {
    return PyFloat_FromDouble(self->y);
}

//static double StructManager_gety(Coords* self, void *closure) {
//    return self->x;
//}


static int StructManager_setx(Coords* self, PyObject* value, void *closure) {
    if (value == NULL) {
        PyErr_SetString(PyExc_TypeError, "Cannot delete the attribute 'x'");
        return -1;
    }
    if (!PyFloat_Check(value)) {
        PyErr_SetString(PyExc_TypeError, "The attribute 'x' must be a float");
        return -1;
    }
    self->x = PyFloat_AsDouble(value);
    return 0;
}


static int StructManager_sety(Coords* self, PyObject* value, void *closure) {
    if (value == NULL) {
        PyErr_SetString(PyExc_TypeError, "Cannot delete the attribute 'y'");
        return -1;
    }
    if (!PyFloat_Check(value)) {
        PyErr_SetString(PyExc_TypeError, "The attribute 'y' must be a float");
        return -1;
    }
    self->y = PyFloat_AsDouble(value);
    return 0;
}



/*
    METHODS
*/


static PyObject* StructManager_add_nums(Coords* self, PyObject* Py_UNUSED(ignored)) {
    //if (self->x == NULL) {
    //    PyErr_SetString(PyExc_AttributeError, "x");
    //    return NULL;
    //}
    //printf("DEBUG: %f, %f\n", self->x, self->y);
    //return PyLong_FromLong(self->x + self->y);
    return PyFloat_FromDouble(self->x + self->y);
}


static PyObject* StructManager_set_nums(Coords* self, PyObject* args) {
    //if (self->x == NULL) {
    //    PyErr_SetString(PyExc_AttributeError, "x");
    //    return NULL;
    //}
    //printf("setting nums\n");
    self->x = 2.2;
    self->y = 4.4;
    return PyFloat_FromDouble(self->x + self->y);
}


static PyObject* StructManager_get_pointer(Coords* self, PyObject* Py_UNUSED(ignored)) {
    return PyLong_FromLong((long)self);
}


static PyObject* StructManager_copy_pointer(Coords* self, PyObject* args) {
    long* pointer;
    //PyArg_ParseTuple(args, "i", &pointer);
    if (!PyArg_ParseTuple(args, "l", &pointer)) {
        PyErr_SetString(PyExc_TypeError, "The attribute 'pointer' must be an integer");
        Py_RETURN_NONE;
    }
    Coords* point = (Coords*)pointer;
    self->x = point->x;
    self->y = point->y;
    Py_RETURN_NONE;
}



/*
    FINALIZING
*/


static PyMemberDef StructManager_members[] = {
    //{"x", T_FLOAT, offsetof(Coords, x), 0, "x coord"},
    //{"y", T_FLOAT, offsetof(Coords, y), 0, "y coord"},
    {NULL},
};


static PyGetSetDef StructManager_getsetters[] = {
    {"x", (getter)StructManager_getx, (setter)StructManager_setx, "x coordinate", NULL},
    {"y", (getter)StructManager_gety, (setter)StructManager_sety, "y coordinate", NULL},
    {NULL},
};


static PyMethodDef StructManager_methods[] = {
    {"add_nums", (PyCFunction)StructManager_add_nums, METH_NOARGS, "Add x and y together"},
    {"set_nums", (PyCFunction)StructManager_set_nums, METH_NOARGS, "Set x and y"},
    {"get_pointer", (PyCFunction)StructManager_get_pointer, METH_NOARGS, "Get the pointer to the internal struct"},
    {"copy_pointer", (PyCFunction)StructManager_copy_pointer, METH_VARARGS, "Load data from provided pointer"},
    {NULL},
};


static PyTypeObject StructManager = {
    .ob_base = PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "Custom.StructManager",
    .tp_doc = PyDoc_STR("Manages a struct"),
    .tp_basicsize = sizeof(Coords),
    .tp_itemsize = 0,
    .tp_flags = Py_TPFLAGS_DEFAULT,
    .tp_new = StructManager_new,
    .tp_init = (initproc) StructManager_init,
    .tp_dealloc = (destructor) StructManager_dealloc,
    .tp_members = StructManager_members,
    .tp_getset = StructManager_getsetters,
    .tp_methods = StructManager_methods,
};


#endif // STRUCTMANAGER_H_

