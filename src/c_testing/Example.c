#define PY_SSIZE_T_CLEAN
#include <python3.10/Python.h>
#include <python3.10/structmember.h>
//#include <python3.10/tupleobject.h>
//#include <python3.10/sliceobject.h>
//#include <python3.10/floatobject.h>
//#include <Python.h>
#include <stddef.h> /* for offsetof() */
#include <stdio.h>
#include "structmanager.h"



// Custom Python type
typedef struct {
    PyObject_HEAD
    /* Type-specific fields go here. */
    double number;
    double number1;
} CustomObject;


static void Custom_dealloc(CustomObject* self) {
    //Py_XDECREF(self->first); //deallocates python objects
    //Py_XDECREF(self->last);
    Py_TYPE(self)->tp_free((PyObject*) self);
}


static PyObject* Custom_new(PyTypeObject* type, PyObject* args, PyObject* kwds) {
    CustomObject* self;
    self = (CustomObject*) type->tp_alloc(type, 0);
    if (self != NULL) {
        self->number = 0.0;
        self->number1 = 0.0;
    }
    return (PyObject*) self;
}


static int Custom_init(CustomObject *self, PyObject *args, PyObject *kwds) {
    static char *kwlist[] = {"first", "last", "number", NULL};

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "|ff", kwlist,
                                     &self->number,
                                     &self->number1))
        return -1;
    return 0;
}


static PyMemberDef Custom_members[] = {
    {"number", T_FLOAT, offsetof(CustomObject, number), 0,
     "custom number"},
    {"number1", T_FLOAT, offsetof(CustomObject, number1), 0,
     "custom number"},
    {NULL}  /* Sentinel */
};


static PyMethodDef Custom_methods[] = {
    //{"name", (PyCFunction) Custom_name, METH_NOARGS,
    // "Return the name, combining the first and last name"
    //},
    {NULL}  /* Sentinel */
};


// Python: Wrapper for CustomObject
static PyTypeObject CustomType = {
    .ob_base = PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "custom.Custom",
    .tp_doc = PyDoc_STR("Custom objects"),
    .tp_basicsize = sizeof(CustomObject),
    .tp_itemsize = 0,
    .tp_flags = Py_TPFLAGS_DEFAULT,
    //.tp_new = PyType_GenericNew,
    .tp_new = Custom_new,
    .tp_init = (initproc) Custom_init,
    .tp_dealloc = (destructor) Custom_dealloc,
    .tp_members = Custom_members,
    .tp_methods = Custom_methods,
};




// Find the primes between a range.
int CfindPrimes(int num1, int num2) {
    int flag_var, i, j;
    printf("The prime numbers in (%d, %d) are:\n", num1, num2);
    
    for (i = num1 + 1; i < num2; i++) {
        flag_var = 0;
        for (j = 2; j <= i/2; j++) {
            if (i % j == 0) {
                flag_var = 1;
                break;
            }
        }
        if (flag_var == 0) {
            printf("%d\n", i);
        }
    }
    return 0;
}


// Python: Wrapper for CfindPrimes
static PyObject* findPrimes(PyObject* self, PyObject* args) {
    int num1, num2, sts;
    if (!PyArg_ParseTuple(args, "ii", &num1, &num2)) {
        return NULL;
    }
    sts = CfindPrimes(num1, num2);
    return PyLong_FromLong(sts);
}


// Python: Returns two integers
static PyObject* return_two(PyObject* self) {
    return Py_BuildValue("ii", 123, 321); 
}


// Python: Returns package version
static PyObject* version(PyObject* self) {
    return Py_BuildValue("s", "Version 0.0.1");
}


// Wrap all functions together
static PyMethodDef ModuleMethods[] = {
    {"findPrimes", findPrimes, METH_VARARGS, "Calculates all primes between num1 and num2"},
    {"version", (PyCFunction)version, METH_NOARGS, "Returns module version"},
    {"return_two", (PyCFunction)return_two, METH_NOARGS, "Returns two integers"},
    {NULL, NULL, 0, NULL},
};


// Package module info together
static struct PyModuleDef Module = {
    .m_base = PyModuleDef_HEAD_INIT,
    .m_name = "Example", //name of module
    .m_doc = "findPrimes Module", //module description
    .m_size = -1, //global state
    .m_methods = ModuleMethods, //pass in our PyMethodDef
};


//// Initializer
//PyMODINIT_FUNC PyInit_Example(void) {
//    return PyModule_Create(&Module);
//}


//PyMODINIT_FUNC PyInit_Example(void) {
//    PyObject *m;
//
//    m = PyModule_Create(&Module);
//    if (m == NULL)
//        return NULL;
//
//    SpamError = PyErr_NewException("spam.error", NULL, NULL);
//    Py_XINCREF(SpamError);
//    if (PyModule_AddObject(m, "error", SpamError) < 0) {
//        Py_XDECREF(SpamError);
//        Py_CLEAR(SpamError);
//        Py_DECREF(m);
//        return NULL;
//    }
//
//    return m;
//}




// Initialize module, function name must match file name
PyMODINIT_FUNC PyInit_Example(void) {
    PyObject *m;

    if (PyType_Ready(&CustomType) < 0) { //ensure CustomType is good
        return NULL;
    }


    m = PyModule_Create(&Module); //create the module
    if (m == NULL) {
        return NULL;
    }

    Py_INCREF(&CustomType);
    if (PyModule_AddObject(m, "Custom", (PyObject *) &CustomType) < 0) {
        Py_DECREF(&CustomType);
        Py_DECREF(m);
        return NULL;
    }

    if (PyType_Ready(&StructManager) < 0) { //ensure CustomType is good
        return NULL;
    }
    Py_INCREF(&StructManager);
    if (PyModule_AddObject(m, "StructManager", (PyObject *) &StructManager) < 0) {
        Py_DECREF(&StructManager); 
        Py_DECREF(m);
        return NULL;
    }

    return m;
}














