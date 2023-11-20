#define PY_SSIZE_T_CLEAN
#include <python3.11/Python.h>


// Support struct
typedef struct {
    PyObject_HEAD
    /* Type-specific fields go here. */
    double x;
    double y;
} Coords;

