#include <Python.h>
#include <stdio.h>
#include <string.h>
//#include <libnumarray.h>
#include <numpy/arrayobject.h>
#include "kaplot.h"
#include "cinterface.h"

extern PyTypeObject PyVector_Type;

#define MIN(X, Y) (((X) < (Y)) ? (X) : (Y))

int getVector(PyObject *args, double *x, double *y)
{
	PyVector *vector;
	if(PyObject_TypeCheck(args, &PyVector_Type))
	{
		vector = (PyVector*)args;
		*x = vector->x;
		*y = vector->y;
		return 0;
	}
	if (!PyArg_ParseTuple(args, "|dd:Vector.__init__", x, y))
    {
		PyErr_Clear();
	    if (!PyArg_ParseTuple(args, "(dd):Vector.__init__", x, y))
	    {
	    	return -1;
			//PyErr_Clear();
		    /*if (!PyArg_ParseTuple(args, "O!:Vector.__init__", &PyVector_Type, &vector))
		    {
		    	PyErr_Format(PyExc_TypeError, "vector arguments should be 2 numbers, a sequence of 2 numbers, or a Vector object");
	    		return -1;
	    	}
	    	*x = vector->x;
	    	*y = vector->y;*/
	    }
    }
    return 0;
}

static int
PyVector_init(PyVector *self, PyObject *args, PyObject *kwargs)
{
	/*PyVector *vector;
	self->x = 1;
	self->y = 1;
	if (!PyArg_ParseTuple(args, "|dd:Vector.__init__", &self->x, &self->y))
    {
		PyErr_Clear();
	    if (!PyArg_ParseTuple(args, "(dd):Vector.__init__", &self->x, &self->y))
	    {
			PyErr_Clear();
		    if (!PyArg_ParseTuple(args, "O!:Vector.__init__", &PyVector_Type, &vector))
	    		return -1;
	    	self->x = vector->x;
	    	self->y = vector->y;
	    }
    }*/
    return getVector(args, &self->x, &self->y);
	//return 0;
}

static void
PyVector_dealloc(PyVector *self)
{
    if (self->ob_type->tp_free)
		self->ob_type->tp_free((PyObject *)self);
    else
		PyObject_Del(self);
}


PyObject *
PyVector_new(double x, double y)
{
    PyVector *self;

    self = PyObject_New(PyVector, &PyVector_Type);
    if (!self) {
		return NULL;
    }

    self->x = x;
    self->y = y;
    return (PyObject *)self;
}


static PyObject *
PyVector_inverse(PyVector *self, PyObject *args)
{
	if(!PyArg_ParseTuple(args, ":inverse"))
		return NULL;
	else
		return PyVector_new(1/self->x, 1/self->y);
}

static PyObject *
PyVector_addMethod(PyVector *self, PyObject *args)
{
	double x, y;
	if(!(PyArg_ParseTuple(args, "(dd):translate", &x, &y)
		|| PyArg_ParseTuple(args, "dd:translate", &x, &y)))
		return NULL;
	else
		return PyVector_new(self->x + x, self->y + y);
}

static PyObject *
PyVector_scale(PyVector *self, PyObject *args)
{
	double sx, sy;
	if(!PyArg_ParseTuple(args, "dd:Vector.scale", &sx, &sy))
		return NULL;
	else
		return PyVector_new(self->x * sx, self->y * sy);
}

static PyObject *
PyVector_add(PyVector *self, PyVector *other)
{
	return PyVector_new(self->x+other->x, self->y+other->y);
}

static PyObject *
PyVector_substract(PyVector *self, PyVector *other)
{
	return PyVector_new(self->x-other->x, self->y-other->y);
}

static PyObject *
PyVector_multiply(PyVector *self, PyVector *other)
{
	return PyVector_new(self->x*other->x, self->y*other->y);
}

/*
static PyObject *
PyVector_get_translation(PyVector *self, PyObject *args)
{
	if(!PyArg_ParseTuple(args, ":get_translation"))
		return NULL;
	else
		return Py_BuildValue("dd", self->tx, self->ty);
}

static PyObject *
PyVector_no_translation(PyVector *self, PyObject *args)
{
	if(!PyArg_ParseTuple(args, ":no_translation"))
		return NULL;
	else
		return PyVector_new(self->xx, self->yy, 0, 0);
}
*/
/*
static int
PyVector_coerce(PyObject **a, PyObject **b)
{
	printf("a = %p\n", a);
	printf("b = %p\n", b);
	return 0;
}
static PyObject *
PyVector_multiply(PyVector *self, PyObject *args)
//PyVector_multiply(PyVector *self, PyVector *rhs)
{
	PyVector *rhs;
	rhs = (PyVector*)args;
	
	if(!(PyObject_TypeCheck(args, &PyVector_Type)||
		PyArg_ParseTuple(args, "O!:multiply", &PyVector_Type, &rhs)))
	{
		double x, y;
		if(!PyArg_ParseTuple(args, "dd:multiply", &x, &y)
			&& !PyArg_ParseTuple(args, "(dd):multiply", &x, &y))
		{
			PyErr_SetString(PyExc_TypeError, "multiply takes a Vector or vector(tuple or 2 doubles) as argument");
			return NULL;
		}
		else
		{
			return Py_BuildValue("dd",
					self->xx * x + self->tx, 
					self->yy * y + self->ty);
		}
	}
	else
		return PyVector_new(
							self->xx*rhs->xx,
							self->yy*rhs->yy,
							self->xx*rhs->tx+self->tx,
							self->yy*rhs->ty+self->ty
							);
}

static PyObject *
PyVector_scalebox(PyVector *self, PyObject *args)
{
	double x1, y1, x2, y2;
	if(!PyArg_ParseTuple(args, "(dd)(dd):scalebox", &x1, &y1, &x2, &y2))
		return NULL;
	else
	{
		double sx = x2 - x1;
		double sy = y2 - y1;
		return PyVector_new(1/sx, 1/sy, x1/sx, y1/sy);
	}
}

static PyObject *
PyVector_scalebox_inverse(PyVector *self, PyObject *args)
{
	double x1, y1, x2, y2;
	if(!PyArg_ParseTuple(args, "(dd)(dd):scalebox_inverse", &x1, &y1, &x2, &y2))
		return NULL;
	else
	{
		double sx = x2 - x1;
		double sy = y2 - y1;
		return PyVector_new(sx, sy, x1, y1);
	}
}
*/
static PyMethodDef PyVector_methods[] = {
    { "scale", (PyCFunction)PyVector_scale, METH_VARARGS},
    /*{ "inverse", (PyCFunction)PyVector_inverse, METH_VARARGS },
    { "translate", (PyCFunction)PyVector_translate, METH_VARARGS|METH_STATIC},
    { "get_translation", (PyCFunction)PyVector_get_translation, METH_VARARGS },
    { "no_translation", (PyCFunction)PyVector_no_translation, METH_VARARGS },
    { "multiply", (PyCFunction)PyVector_multiply, METH_VARARGS },
    { "scalebox", (PyCFunction)PyVector_scalebox, METH_VARARGS|METH_STATIC},
    { "scalebox_inverse", (PyCFunction)PyVector_scalebox_inverse, METH_VARARGS|METH_STATIC},
    */
    { NULL, NULL, 0 }
};


static PyObject *
PyVector_get_x(PyVector *self)
{
    return PyFloat_FromDouble(self->x);
}

static PyObject *
PyVector_get_y(PyVector *self)
{
    return PyFloat_FromDouble(self->y);
}

static PyObject *
PyVector_get_length(PyVector *self)
{
    return PyFloat_FromDouble(sqrt(self->x*self->x + self->y*self->y));
}

static PyGetSetDef PyVector_getseters[] = {
    { "x", (getter)PyVector_get_x, (setter)0 },
    { "y", (getter)PyVector_get_y, (setter)0 },
    { "length", (getter)PyVector_get_length, (setter)0 },
    { NULL, (getter)0, (setter)0 }
};

int PyVector_PySequence_length(PyVector *vector)
{
	return 2;
}

PyObject* PyVector_PySequence_item(PyVector *self, int item)
{
	if(item == 0)
		return PyFloat_FromDouble(self->x);
	else if(item == 1)
		return PyFloat_FromDouble(self->y);
	else
		return PyErr_Format(PyExc_IndexError, "Vector only has 2 elements");
}

static PySequenceMethods PyVector_PySequenceMethods = {
	PyVector_PySequence_length,
	0,0,
	PyVector_PySequence_item,
	0,0,0,0,0,0
	
};
/*
typedef struct {
	inquiry sq_length;
	binaryfunc sq_concat;
	intargfunc sq_repeat;
	intargfunc sq_item;
	intintargfunc sq_slice;
	intobjargproc sq_ass_item;
	intintobjargproc sq_ass_slice;
	objobjproc sq_contains;
	binaryfunc sq_inplace_concat;
	intargfunc sq_inplace_repeat;
} PySequenceMethods;
*/


static PyNumberMethods PyVector_as_number = {
  (binaryfunc)PyVector_add,
  (binaryfunc)PyVector_substract,
  (binaryfunc)PyVector_multiply,
  (binaryfunc)0,
  (binaryfunc)0,
  (binaryfunc)0,
  (ternaryfunc)0,
  (unaryfunc)0,
  (unaryfunc)0,
  (unaryfunc)0,
  (inquiry)0,
  (unaryfunc)0,
  (binaryfunc)0,
  (binaryfunc)0,
  (binaryfunc)0,
  (binaryfunc)0,
  (binaryfunc)0,
  (coercion)0, //PyVector_coerce,
  (unaryfunc)0,
  (unaryfunc)0,
  (unaryfunc)0,
  (unaryfunc)0,
  (unaryfunc)0,
  //(binaryfunc)0,
  //(binaryfunc)0,
  //(binaryfunc)PyVector_multiply
};

static PyObject *
PyVector_repr(PyVector *self)
{
    char buf[256];
    PyOS_snprintf(buf, sizeof(buf), "kaplot.Vector(%g, %g)",
		  self->x, self->y);
    return PyString_FromString(buf);
}

PyTypeObject PyVector_Type = {
    PyObject_HEAD_INIT(NULL)
    0,                                  /* ob_size */
    "Vector",                    			/* tp_name */
    sizeof(PyVector),          		   /* tp_basicsize */
    0,                                  /* tp_itemsize */
    /* methods */
    (destructor)PyVector_dealloc, /* tp_dealloc */
    (printfunc)0,                       /* tp_print */
    (getattrfunc)0,                     /* tp_getattr */
    (setattrfunc)0,                     /* tp_setattr */
    (cmpfunc)0,                         /* tp_compare */
    (reprfunc)PyVector_repr,                        /* tp_repr */
    &PyVector_as_number,                                  /* tp_as_number */
    &PyVector_PySequenceMethods,                                  /* tp_as_sequence */
    0,                                  /* tp_as_mapping */
    (hashfunc)0,                        /* tp_hash */
    (ternaryfunc)0,                     /* tp_call */
    (reprfunc)0,                        /* tp_str */
    (getattrofunc)0,                    /* tp_getattro */
    (setattrofunc)0,                    /* tp_setattro */
    0,                                  /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT|Py_TPFLAGS_BASETYPE|Py_TPFLAGS_CHECKTYPES,                 /* tp_flags */
    NULL, /* Documentation string */
    (traverseproc)0,                    /* tp_traverse */
    (inquiry)0,                         /* tp_clear */
    (richcmpfunc)0,                     /* tp_richcompare */
    0,                                  /* tp_weaklistoffset */
    (getiterfunc)0,                     /* tp_iter */
    (iternextfunc)0,                    /* tp_iternext */
    PyVector_methods,        			    /* tp_methods */
    0,                                  /* tp_members */
    PyVector_getseters,           		   /* tp_getset */
    (PyTypeObject*)0,                  /* tp_base */
    (PyObject *)0,                      /* tp_dict */
    0,                                  /* tp_descr_get */
    0,                                  /* tp_descr_set */
    0,                                  /* tp_dictoffset */
    (initproc)PyVector_init,                        /* tp_init */
    (allocfunc)0,                       /* tp_alloc */
    (newfunc)0,                         /* tp_new */
    (freefunc)0,                        /* tp_free */
    (inquiry)0,                         /* tp_is_gc */
    (PyObject *)0,                      /* tp_bases */
};

static PyMethodDef PyVector_functions[] = {
    { NULL, NULL, 0 }
};



/*

 MATRIX
 
*/

extern PyTypeObject PyMatrix_Type;

static int
PyMatrix_init(PyMatrix *self, PyObject *args, PyObject *kwargs)
{
	self->xx = 1;
	self->xy = 0;
	self->yx = 0;
	self->yy = 1;
	self->tx = 0;
	self->ty = 0;
    if (!PyArg_ParseTuple(args, "|dddd:Matrix.__init__", &self->xx, &self->yy, &self->tx, &self->ty))
    {
		return -1;
    }
	return 0;
}

static void
PyMatrix_dealloc(PyMatrix *self)
{
    if (self->ob_type->tp_free)
		self->ob_type->tp_free((PyObject *)self);
    else
		PyObject_Del(self);
}


PyObject *
PyMatrix_new(double xx, double xy, double yx, double yy, double tx, double ty)
{
    PyMatrix *self;

    self = PyObject_New(PyMatrix, &PyMatrix_Type);
    if (!self) {
		return NULL;
    }

    self->xx = xx;
    self->xy = xy;
    self->yx = yx;
    self->yy = yy;
    self->tx = tx;
    self->ty = ty;

    return (PyObject *)self;
}


static PyObject *
PyMatrix_inverse(PyMatrix *self, PyObject *args)
{
	double a,b,c,d, idet;
	if(!PyArg_ParseTuple(args, ":inverse"))
		return NULL;
	else {
		//return PyMatrix_new(1/self->xx, 1/self->yy, -self->tx/self->xx, -self->ty/self->yy);
		/*
		return PyMatrix_new(1/self->xx, 0, 0, 1/self->yy, -self->tx/self->xx, -self->ty/self->yy);
		/**/
		a = self->xx;
		b = self->xy;
		c = self->yx;
		d = self->yy;
		idet = 1/(a*d - b*c);
		return PyMatrix_new(idet*d, idet*-b, idet*-c, idet*a,
			idet*(c*self->ty - d*self->tx), idet*(b*self->tx - a*self->ty));
		/**/
	}
}


static PyObject *
PyMatrix_translate(PyMatrix *self, PyObject *args)
{
	double dx, dy;
	if(getVector(args, &dx, &dy))
		return NULL;
	else
		return PyMatrix_new(1, 0, 0, 1, dx, dy);
}

static PyObject *
PyMatrix_rotate(PyMatrix *self, PyObject *args)
{
	double angle;
	if(!PyArg_ParseTuple(args, "d:rotate", &angle))
		return NULL;
	else
		return PyMatrix_new(cos(angle), -sin(angle), sin(angle), cos(angle), 0, 0);
}

static PyObject *
PyMatrix_scale(PyMatrix *self, PyObject *args)
{
	double sx, sy;
	if(!PyArg_ParseTuple(args, "dd:scale", &sx, &sy))
		return NULL;
	else
		return PyMatrix_new(sx, 0, 0, sy, 0, 0);
}

static PyObject *
PyMatrix_get_translation(PyMatrix *self, PyObject *args)
{
	if(!PyArg_ParseTuple(args, ":get_translation"))
		return NULL;
	else
		return Py_BuildValue("dd", self->tx, self->ty);
}

static PyObject *
PyMatrix_no_translation(PyMatrix *self, PyObject *args)
{
	if(!PyArg_ParseTuple(args, ":no_translation"))
		return NULL;
	else
		return PyMatrix_new(self->xx, self->xy, self->yx, self->yy, 0, 0);
}

static int
PyMatrix_coerce(PyObject **a, PyObject **b)
{
	printf("a = %p\n", a);
	printf("b = %p\n", b);
	return 0;
}

static PyObject *
PyMatrix_mulXY(PyMatrix *self, PyObject *args)
{
	PyObject *x_array;
	PyObject *y_array;
	PyArrayObject *x_array_double;
	PyArrayObject *y_array_double;
	PyArrayObject *x_array_double_out;
	PyArrayObject *y_array_double_out;
	double *x;
	double *y;
	double *x_out;
	double *y_out;
	int length;
	int dims[1];
	int i;

	if(PyArg_ParseTuple(args, "OO", &x_array, &y_array))
	{
		//x_array_double = NA_InputArray(x_array, tFloat64, C_ARRAY);
		//y_array_double = NA_InputArray(y_array, tFloat64, C_ARRAY);
		x_array_double = (PyArrayObject*)PyArray_FromAny(x_array, NPY_FLOAT32, 1, 1, NPY_ARRAY_C_CONTIGUOUS, NULL);
		y_array_double = (PyArrayObject*)PyArray_FromAny(y_array, NPY_FLOAT32, 1, 1, NPY_ARRAY_C_CONTIGUOUS, NULL);
		if(x_array_double == NULL)
			return PyErr_Format(PyExc_TypeError, "can't convert x data into numpy array");
		if(x_array_double->nd != 1)
			return PyErr_Format(PyExc_TypeError, "x data isn't 1 dimensional");
		if(y_array_double == NULL)
			return PyErr_Format(PyExc_TypeError, "can't convert y data into numpy array");
		if(y_array_double->nd != 1)
			return PyErr_Format(PyExc_TypeError, "y data isn't 1 dimensional");
		length = MIN(x_array_double->dimensions[0], y_array_double->dimensions[0]);
		x = (double*)PyArray_DATA(x_array_double);
		y = (double*)PyArray_DATA(y_array_double);
		x_array_double_out = (PyArrayObject*)PyArray_FromDims(1, dims, NPY_FLOAT32);
		y_array_double_out = (PyArrayObject*)PyArray_FromDims(1, dims, NPY_FLOAT32);
		x_out = (double*)PyArray_DATA(x_array_double_out);
		y_out = (double*)PyArray_DATA(y_array_double_out);
		for(i = 0; i < length; i++)
		{
			x_out[i] = self->xx * x[i] + self->xy * y[i] + self->tx;
			y_out[i] = self->yx * x[i] + self->yy * y[i] + self->ty;
		}
		return Py_BuildValue("OO", x_array_double_out, y_array_double_out);
	}
	else
	{
		return NULL;
	}
	
}

static PyObject *
PyMatrix_multiply(PyMatrix *self, PyObject *args)
//PyMatrix_multiply(PyMatrix *self, PyMatrix *rhs)
{
	PyMatrix *rhs;
	rhs = (PyMatrix*)args;
	
	if(!(PyObject_TypeCheck(args, &PyMatrix_Type)||
		PyArg_ParseTuple(args, "O!:multiply", &PyMatrix_Type, &rhs)))
	{
		double x, y;
		PyErr_Clear();
		/*if(!PyArg_ParseTuple(args, "dd:multiply", &x, &y)
			&& !PyArg_ParseTuple(args, "(dd):multiply", &x, &y))
		{
			PyErr_SetString(PyExc_TypeError, "multiply takes a matrix or vector(tuple or 2 doubles) as argument");
			return NULL;
		}*/
		if(getVector(args, &x, &y) != 0)
		{
			PyObject_Print(args, stdout, 0);
			return NULL;
		}
		else
		{
			return PyVector_new(
					self->xx * x + self->xy * y + self->tx,
					self->yx * x + self->yy * y + self->ty);
		}
	}
	else
		/*
		return PyMatrix_new(
							self->xx*rhs->xx,
							0,
							0,
							self->yy*rhs->yy,
							self->xx*rhs->tx+self->tx,
							self->yy*rhs->ty+self->ty
							);
		/*/
		return PyMatrix_new(
							self->xx*rhs->xx + self->xy*rhs->yx,
							self->xx*rhs->xy + self->xy*rhs->yy,
							self->yx*rhs->xx + self->yy*rhs->yx,
							self->yx*rhs->xy + self->yy*rhs->yy,
							self->xx*rhs->tx + self->xy*rhs->ty + self->tx,
							self->yx*rhs->tx + self->yy*rhs->ty + self->ty
							);
		/**/
}

static PyObject *
PyMatrix_scalebox(PyMatrix *self, PyObject *args)
{
	double x1, y1, x2, y2;
	if(!PyArg_ParseTuple(args, "(dd)(dd):scalebox", &x1, &y1, &x2, &y2))
		return NULL;
	else
	{
		double sx = x2 - x1;
		double sy = y2 - y1;
		return PyMatrix_new(1/sx, 0, 0, 1/sy, x1/sx, y1/sy);
	}
}

static PyObject *
PyMatrix_scalebox_inverse(PyMatrix *self, PyObject *args)
{
	double x1, y1, x2, y2;
	if(!PyArg_ParseTuple(args, "(dd)(dd):scalebox_inverse", &x1, &y1, &x2, &y2))
		return NULL;
	else
	{
		double sx = x2 - x1;
		double sy = y2 - y1;
		return PyMatrix_new(sx, 0, 0, sy, x1, y1);
	}
}

static PyMethodDef PyMatrix_methods[] = {
    { "inverse", (PyCFunction)PyMatrix_inverse, METH_VARARGS },
    { "translate", (PyCFunction)PyMatrix_translate, METH_VARARGS|METH_STATIC},
    { "rotate", (PyCFunction)PyMatrix_rotate, METH_VARARGS|METH_STATIC},
    { "scale", (PyCFunction)PyMatrix_scale, METH_VARARGS|METH_STATIC},
    { "get_translation", (PyCFunction)PyMatrix_get_translation, METH_VARARGS },
    { "no_translation", (PyCFunction)PyMatrix_no_translation, METH_VARARGS },
    { "multiply", (PyCFunction)PyMatrix_multiply, METH_VARARGS },
    { "mulXY", (PyCFunction)PyMatrix_mulXY, METH_VARARGS },
    { "scalebox", (PyCFunction)PyMatrix_scalebox, METH_VARARGS|METH_STATIC},
    { "scalebox_inverse", (PyCFunction)PyMatrix_scalebox_inverse, METH_VARARGS|METH_STATIC},
    { NULL, NULL, 0 }
};

#define SET_GETTER(name) \
static PyObject * \
PyMatrix_get_##name (PyMatrix *self) \
{ \
    return PyFloat_FromDouble(self->name);\
}\
static int \
PyMatrix_set_##name (PyMatrix *self, PyObject *args, void *closure) \
{ \
	double value;\
	value = PyFloat_AsDouble(args); \
	self->name = value;\
	return 0;\
}

SET_GETTER(xx)
SET_GETTER(xy)
SET_GETTER(yx)
SET_GETTER(yy)
SET_GETTER(ty)
SET_GETTER(tx)



static PyGetSetDef PyMatrix_getseters[] = {
    { "xx", (getter)PyMatrix_get_xx, (setter)PyMatrix_set_xx },
    { "xy", (getter)PyMatrix_get_xy, (setter)PyMatrix_set_xy },
    { "yx", (getter)PyMatrix_get_yx, (setter)PyMatrix_set_yx },
    { "yy", (getter)PyMatrix_get_yy, (setter)PyMatrix_set_yy },
    { "tx", (getter)PyMatrix_get_tx, (setter)PyMatrix_set_tx },
    { "ty", (getter)PyMatrix_get_ty, (setter)PyMatrix_set_ty },
    { NULL, (getter)0, (setter)0 }
};

static PyNumberMethods PyMatrix_as_number = {
  (binaryfunc)0,
  (binaryfunc)0,
  (binaryfunc)PyMatrix_multiply,
  (binaryfunc)0,
  (binaryfunc)0,
  (binaryfunc)0,
  (ternaryfunc)0,
  (unaryfunc)0,
  (unaryfunc)0,
  (unaryfunc)0,
  (inquiry)0,
  (unaryfunc)0,
  (binaryfunc)0,
  (binaryfunc)0,
  (binaryfunc)0,
  (binaryfunc)0,
  (binaryfunc)0,
  (coercion)PyMatrix_coerce,
  (unaryfunc)0,
  (unaryfunc)0,
  (unaryfunc)0,
  (unaryfunc)0,
  (unaryfunc)0,
  //(binaryfunc)0,
  //(binaryfunc)0,
  //(binaryfunc)PyMatrix_multiply
};

static PyObject *
PyMatrix_repr(PyMatrix *self)
{
    char buf[256];
    PyOS_snprintf(buf, sizeof(buf), "kaplot.Matrix(%g, %g, %g, %g, %g, %g)",
		  self->xx, self->xy, self->yx, self->yy, self->tx, self->ty);
    return PyString_FromString(buf);
}

PyTypeObject PyMatrix_Type = {
    PyObject_HEAD_INIT(NULL)
    0,                                  /* ob_size */
    "Matrix",                    			/* tp_name */
    sizeof(PyMatrix),          		   /* tp_basicsize */
    0,                                  /* tp_itemsize */
    /* methods */
    (destructor)PyMatrix_dealloc, /* tp_dealloc */
    (printfunc)0,                       /* tp_print */
    (getattrfunc)0,                     /* tp_getattr */
    (setattrfunc)0,                     /* tp_setattr */
    (cmpfunc)0,                         /* tp_compare */
    (reprfunc)PyMatrix_repr,                        /* tp_repr */
    &PyMatrix_as_number,                                  /* tp_as_number */
    0,                                  /* tp_as_sequence */
    0,                                  /* tp_as_mapping */
    (hashfunc)0,                        /* tp_hash */
    (ternaryfunc)0,                     /* tp_call */
    (reprfunc)0,                        /* tp_str */
    (getattrofunc)0,                    /* tp_getattro */
    (setattrofunc)0,                    /* tp_setattro */
    0,                                  /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT|Py_TPFLAGS_BASETYPE|Py_TPFLAGS_CHECKTYPES,                 /* tp_flags */
    NULL, /* Documentation string */
    (traverseproc)0,                    /* tp_traverse */
    (inquiry)0,                         /* tp_clear */
    (richcmpfunc)0,                     /* tp_richcompare */
    0,                                  /* tp_weaklistoffset */
    (getiterfunc)0,                     /* tp_iter */
    (iternextfunc)0,                    /* tp_iternext */
    PyMatrix_methods,        			    /* tp_methods */
    0,                                  /* tp_members */
    PyMatrix_getseters,           		   /* tp_getset */
    (PyTypeObject*)0,                  /* tp_base */
    (PyObject *)0,                      /* tp_dict */
    0,                                  /* tp_descr_get */
    0,                                  /* tp_descr_set */
    0,                                  /* tp_dictoffset */
    (initproc)PyMatrix_init,                        /* tp_init */
    (allocfunc)0,                       /* tp_alloc */
    (newfunc)0,                         /* tp_new */
    (freefunc)0,                        /* tp_free */
    (inquiry)0,                         /* tp_is_gc */
    (PyObject *)0,                      /* tp_bases */
};

static PyMethodDef PyMatrix_functions[] = {
    { NULL, NULL, 0 }
};





typedef struct _kaplot_cinterface_wrap_t{
	kaplot_cinterface_t base;
	PyObject *move_to, *line_to, *curve_to, *fill, *stroke, *set_color_rgb;
} kaplot_cinterface_wrap_t;

int move_to_wrap(kaplot_cinterface_t *interface, double x, double y)
{
	kaplot_cinterface_wrap_t *real_interface = (kaplot_cinterface_wrap_t*)interface;
	PyObject *arglist, *result;
	arglist = Py_BuildValue("(dd)", x, y);
	result = PyEval_CallObject(real_interface->move_to, arglist);
	if(result == NULL)
		return 0;
	else
		return 1;
}

int line_to_wrap(kaplot_cinterface_t *interface, double x, double y)
{
	kaplot_cinterface_wrap_t *real_interface = (kaplot_cinterface_wrap_t*)interface;
	PyObject *arglist, *result;
	arglist = Py_BuildValue("(dd)", x, y);
	result = PyEval_CallObject(real_interface->line_to, arglist);
	if(result == NULL)
		return 0;
	else
		return 1;
}

int curve_to_wrap(kaplot_cinterface_t *interface, double x1, double y1, double x2, double y2, double x3, double y3)
{
	kaplot_cinterface_wrap_t *real_interface = (kaplot_cinterface_wrap_t*)interface;
	PyObject *arglist, *result;
	arglist = Py_BuildValue("(dddddd)", x1, y1, x2, y2, x3, y3);
	result = PyEval_CallObject(real_interface->curve_to, arglist);
	if(result == NULL)
		return 0;
	else
		return 1;
}

int fill_wrap(kaplot_cinterface_t *interface)
{
	kaplot_cinterface_wrap_t *real_interface = (kaplot_cinterface_wrap_t*)interface;
	PyObject *arglist, *result;
	arglist = Py_BuildValue("()");
	result = PyEval_CallObject(real_interface->fill, arglist);
	if(result == NULL)
		return 0;
	else
		return 1;
}

int stroke_wrap(kaplot_cinterface_t *interface)
{
	kaplot_cinterface_wrap_t *real_interface = (kaplot_cinterface_wrap_t*)interface;
	PyObject *arglist, *result;
	arglist = Py_BuildValue("()");
	result = PyEval_CallObject(real_interface->stroke, arglist);
	if(result == NULL)
		return 0;
	else
		return 1;
}

int set_color_rgb_wrap(kaplot_cinterface_t *interface, double r, double g, double b)
{
	kaplot_cinterface_wrap_t *real_interface = (kaplot_cinterface_wrap_t*)interface;
	PyObject *arglist, *result;
	arglist = Py_BuildValue("(ddd)", r, g, b);
	result = PyEval_CallObject(real_interface->set_color_rgb, arglist);
	if(result == NULL)
		return 0;
	else
		return 1;
}

void kaplot_cinterface_wrap_destr(void *base)
{
	kaplot_cinterface_wrap_t *real_interface = (kaplot_cinterface_wrap_t*)base;
	Py_DECREF(real_interface->move_to);
	Py_DECREF(real_interface->line_to);
	Py_DECREF(real_interface->curve_to);
	Py_DECREF(real_interface->fill);
	Py_DECREF(real_interface->stroke);
	Py_DECREF(real_interface->set_color_rgb);
	free(base);
}

PyObject* PyKaplot_CInterfaceWrap(PyObject* self, PyObject* args)
{
	PyObject *move_to, *line_to, *curve_to, *fill, *stroke, *set_color_rgb;
	kaplot_cinterface_wrap_t *c_interface;

	if(PyArg_ParseTuple(args, "OOOOOO:cinterface_wrap", &move_to, &line_to, &curve_to, &fill, &stroke, &set_color_rgb))
	{
		c_interface = (kaplot_cinterface_wrap_t*)malloc(sizeof(kaplot_cinterface_wrap_t));
		Py_INCREF(move_to);
		Py_INCREF(line_to);
		Py_INCREF(curve_to);
		Py_INCREF(fill);
		Py_INCREF(stroke);
		Py_INCREF(set_color_rgb);
		c_interface->base.move_to = move_to_wrap;
		c_interface->base.line_to = line_to_wrap;
		c_interface->base.curve_to = curve_to_wrap;
		c_interface->base.fill = fill_wrap;
		c_interface->base.stroke = stroke_wrap;
		c_interface->base.set_color_rgb = set_color_rgb_wrap;
		c_interface->move_to = move_to;
		c_interface->line_to = line_to;
		c_interface->curve_to = curve_to;
		c_interface->fill = fill;
		c_interface->stroke = stroke;
		c_interface->set_color_rgb = set_color_rgb;
		return PyCObject_FromVoidPtr(c_interface, kaplot_cinterface_wrap_destr);
	}
	else
	{
		return NULL;
	}

}

PyObject* PyKaplot_Polyline(PyObject* self, PyObject* args)
{
	PyObject *x_array;
	PyObject *y_array;
	PyArrayObject *x_array_double;
	PyArrayObject *y_array_double;
	PyObject *cinterface_object;
	kaplot_cinterface_t *cinterface;
	double *x;
	double *y;
	int length;
	int i;

	if(PyArg_ParseTuple(args, "O!OO", &PyCObject_Type, &cinterface_object, &x_array, &y_array))
	{
		//x_array_double = NA_InputArray(x_array, NPY_FLOAT32, C_ARRAY);
		//y_array_double = NA_InputArray(y_array, NPY_FLOAT32, C_ARRAY);
		x_array_double = (PyArrayObject*)PyArray_FromAny(x_array, NPY_FLOAT32, 1, 1, NPY_ARRAY_C_CONTIGUOUS, NULL);
		y_array_double = (PyArrayObject*)PyArray_FromAny(y_array, NPY_FLOAT32, 1, 1, NPY_ARRAY_C_CONTIGUOUS, NULL);
		if(x_array_double == NULL)
			return PyErr_Format(PyExc_TypeError, "can't convert x data into numpy");
		if(x_array_double->nd != 1)
			return PyErr_Format(PyExc_TypeError, "x data isn't 1 dimensional");
		if(y_array_double == NULL)
			return PyErr_Format(PyExc_TypeError, "can't convert y data into numpy");
		if(y_array_double->nd != 1)
			return PyErr_Format(PyExc_TypeError, "y data isn't 1 dimensional");

		length = MIN(x_array_double->dimensions[0], y_array_double->dimensions[0]);

		x = (double*)PyArray_DATA(x_array_double);
		y = (double*)PyArray_DATA(y_array_double);

		cinterface = PyCObject_AsVoidPtr(cinterface_object);

		if(length >= 2)
		{

			cinterface->move_to(cinterface, x[0], y[0]);
			for(i = 1; i < length; i++)
			{
				cinterface->line_to(cinterface, x[i], y[i]);
			}
		}

		Py_INCREF(Py_None);
		return Py_None;
	}
	else
	{
		return NULL;
	}


}


static PyMethodDef kaplot_ext_functions[] = {
		{"cinterface_wrap", (PyCFunction)PyKaplot_CInterfaceWrap, METH_VARARGS, "wraps a tuple of functions with a CObject containing a kaplot_cinterface_t"},
		{"polyline", (PyCFunction)PyKaplot_Polyline, METH_VARARGS, "creates a polyline path, without filling or stroking it"},
		{NULL, NULL, 0, NULL}
};

extern PyTypeObject PyMatrix_Type;
extern PyTypeObject PyVector_Type;
extern PyTypeObject PyVector4_Type;

PyMODINIT_FUNC
init_kaplot(void)
{
	PyObject *mod;
	//PyObject *c_api_object;


	//printf("import lib stuff\n");
	//import_array();
	//import_libnumarray();
	//printf("import lib stuff done\n");

	//mod = Py_InitModule("kaplot.cext._kaplot", kaplot_ext_functions);
	mod = Py_InitModule("kaplot.cext._kaplot", kaplot_ext_functions);

#define INIT_TYPE(tp) \
    if (!tp.ob_type) tp.ob_type = &PyType_Type; \
    if (!tp.tp_alloc) tp.tp_alloc = PyType_GenericAlloc; \
    if (!tp.tp_new) tp.tp_new = PyType_GenericNew; \
    if (PyType_Ready(&tp) < 0) \
        return;

	INIT_TYPE(PyMatrix_Type);
	INIT_TYPE(PyVector_Type);
	INIT_TYPE(PyVector4_Type);
	PyModule_AddObject(mod, "Matrix",  (PyObject *)&PyMatrix_Type);
	PyModule_AddObject(mod, "Vector",  (PyObject *)&PyVector_Type);
	PyModule_AddObject(mod, "Vector4",  (PyObject *)&PyVector4_Type);


	//PyKaplotContour_API[0] = (void *)PyKaplot_CInterfaceWrap;
	//c_api_object = PyCObject_FromVoidPtr((void *)PyKaplotContour_API, NULL);
	//if (c_api_object != NULL)
	//PyModule_AddObject(mod, "_C_API", c_api_object);

}

