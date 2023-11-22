#define PY_SSIZE_T_CLEAN
#include <python3.11/Python.h>
#include <python3.11/structmember.h>
#include <stddef.h> /* for offsetof() */
#include <stdio.h>
#include "creature.h"
#include "generation_manager.h"


extern void maxmul(float *A, float* B, float *C, int size);
static PyObject* pymaxmul(PyObject* self, PyObject* args)  {
    float *ap, *bp, *cp;
    int s;
    if (!PyArg_ParseTuple(args, "llli", &ap, &bp, &cp, &s)) {
        return NULL;
    }
    maxmul(ap, bp, cp, s);
    Py_RETURN_NONE;
}


// Python: Returns package version
static PyObject* version(PyObject* self) {
    return Py_BuildValue("s", "Version 0.0.1");
}


// Wrap all functions together
static PyMethodDef ModuleMethods[] = {
    {"version", (PyCFunction)version, METH_NOARGS, "Returns module version"},
    //{"test_cuda", (PyCFunction)test_cuda, METH_NOARGS, "Tests CUDA"},
    {"maxmul", (PyCFunction)pymaxmul, METH_VARARGS, "Tests CUDA"},
    {NULL, NULL, 0, NULL},
};


// Package module info together
static struct PyModuleDef Module = {
    .m_base = PyModuleDef_HEAD_INIT,
    .m_name = "NEAT", //name of module
    .m_doc = "NEAT Library Implemented in C and CUDA", //module description
    .m_size = -1, //global state
    .m_methods = ModuleMethods, //pass in our PyMethodDef
};


// Initialize module, function name must match file name
PyMODINIT_FUNC PyInit_neat(void) {
    PyObject *m;

    m = PyModule_Create(&Module); //create the module
    if (m == NULL) {
        return NULL;
    }

    if (PyType_Ready(&PyCreature) < 0) { //ensure Creature is good
        return NULL;
    }
    Py_INCREF(&PyCreature);
    if (PyModule_AddObject(m, "Creature", (PyObject *) &PyCreature) < 0) {
        Py_DECREF(&PyCreature);
        Py_DECREF(m);
        return NULL;
    }

    if (PyType_Ready(&PyGenerationManager) < 0) { //ensure GenerationManager is good
        return NULL;
    }
    Py_INCREF(&PyGenerationManager);
    if (PyModule_AddObject(m, "Creature", (PyObject *) &PyGenerationManager) < 0) {
        Py_DECREF(&PyGenerationManager);
        Py_DECREF(m);
        return NULL;
    }

    return m;
}




