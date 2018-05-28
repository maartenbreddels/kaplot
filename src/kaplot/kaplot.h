

#ifndef _KAPLOT_H_
#define _KAPLOT_H_

#include <Python.h>


typedef struct {
    PyObject_HEAD
    double xx, xy, yx, yy, tx, ty;
} PyMatrix;

typedef struct {
    PyObject_HEAD
    double x, y;
} PyVector;

typedef struct {
    PyObject_HEAD
    double x, y, z, w;
} PyVector4;

int getVector(PyObject *args, double *x, double *y);
PyObject *PyVector_new(double x, double y);

int getVector4(PyObject *args, double *x, double *y, double *z, double *w);
PyObject *PyVector_new4(double x, double y, double z, double w);


#endif
