#include <python3.10/Python.h>
#include <stdio.h>

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

static PyObject* findPrimes(PyObject* self, PyObject* args) {
    int num1, num2, sts;
    if (!PyArg_ParseTuple(args, "ii", &num1, &num2)) {
        return NULL;
    }
    sts = CfindPrimes(num1, num2);
    return PyLong_FromLong(sts);
}

static PyObject* version(PyObject* self) {
    return Py_BuildValue("s", "Version 0.0.1");
}

static PyMethodDef Examples[] = {
    {"findPrimes", findPrimes, METH_VARARGS, "Calculates all primes between num1 and num2"},
    {"version", (PyCFunction)version, METH_NOARGS, "Returns module version"},
    {NULL, NULL, 0, NULL},
};

static struct PyModuleDef Example = {
    PyModuleDef_HEAD_INIT,
    "Example",
    "findPrimes Module",
    -1, //global state
    Examples //pass in our PyMethodDef
};

// Initializer Function
PyMODINIT_FUNC PyInit_Example(void) {
    return PyModule_Create(&Example);
}














