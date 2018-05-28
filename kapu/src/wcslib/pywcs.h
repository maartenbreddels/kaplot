#include <wcs.h>
#include <Python.h>

typedef struct {
    PyObject_HEAD
    /* Type-specific fields go here. */
    struct wcsprm* wcs;
    struct celprm* cel;
    
} PyWcsObject;

extern PyTypeObject PyWcs_Type;
