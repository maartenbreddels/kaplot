#include <Python.h>
#include <stdio.h>
#include <string.h>
#include <numpy/arrayobject.h>
#include "kaplot.h"

extern PyTypeObject PyVector4_Type;

int getVector4(PyObject *args, double *x, double *y, double *z, double *w)
{
	PyVector4 *vector;
	if(PyObject_TypeCheck(args, &PyVector4_Type))
	{
		vector = (PyVector4*)args;
		*x = vector->x;
		*y = vector->y;
		*z = vector->z;
		*w = vector->w;
		return 0;
	}
	*x = *y = *z = 0;
	*w = 1;
	if (!PyArg_ParseTuple(args, "ddd|d:Vector4.__init__", x, y, z, w))
    {
		PyErr_Clear();
	    if (!PyArg_ParseTuple(args, "(dddd):Vector4.__init__", x, y, z, w))
	    {
	    	return -1;
			//PyErr_Clear();
		    /*if (!PyArg_ParseTuple(args, "O!:Vector4.__init__", &PyVector4_Type, &vector))
		    {
		    	PyErr_Format(PyExc_TypeError, "vector arguments should be 2 numbers, a sequence of 2 numbers, or a Vector4 object");
	    		return -1;
	    	}
	    	*x = vector->x;
	    	*y = vector->y;*/
	    }
    }
    return 0;
}

static int
PyVector4_init(PyVector4 *self, PyObject *args, PyObject *kwargs)
{
	/*PyVector4 *vector;
	self->x = 1;
	self->y = 1;
	if (!PyArg_ParseTuple(args, "|dd:Vector4.__init__", &self->x, &self->y))
    {
		PyErr_Clear();
	    if (!PyArg_ParseTuple(args, "(dd):Vector4.__init__", &self->x, &self->y))
	    {
			PyErr_Clear();
		    if (!PyArg_ParseTuple(args, "O!:Vector4.__init__", &PyVector4_Type, &vector))
	    		return -1;
	    	self->x = vector->x;
	    	self->y = vector->y;
	    }
    }*/
    return getVector4(args, &self->x, &self->y, &self->z, &self->w);
	//return 0;
}

static void
PyVector4_dealloc(PyVector4 *self)
{
    if (self->ob_type->tp_free)
		self->ob_type->tp_free((PyObject *)self);
    else
		PyObject_Del(self);
}


PyObject *
PyVector4_new(double x, double y, double z, double w)
{
    PyVector4 *self;

    self = PyObject_New(PyVector4, &PyVector4_Type);
    if (!self) {
		return NULL;
    }

    self->x = x;
    self->y = y;
    self->z = z;
    self->w = w;
    return (PyObject *)self;
}


static PyObject *
PyVector4_inverse(PyVector4 *self, PyObject *args)
{
	if(!PyArg_ParseTuple(args, ":inverse"))
		return NULL;
	else
		return PyVector4_new(1/self->x, 1/self->y, 1/self->z, 1/self->w);
}

static PyObject *
PyVector4_addMethod(PyVector4 *self, PyObject *args)
{
	double x, y, z, w;
	//if(!(PyArg_ParseTuple(args, "(dddd):translate", &x, &y, &z, &w)
	//	|| PyArg_ParseTuple(args, "dddd:translate", &x, &y, &z, &w)))
	//	return NULL;
	//else
	//	return PyVector4_new(self->x + x, self->y + y, self->z + z, self->w + w);
	if(getVector4(args, &x, &y, &z, &w) == 0)
		return PyVector4_new(self->x + x, self->y + y, self->z + z, 1);
	else
		return NULL;
}

static PyObject *
PyVector4_scale(PyVector4 *self, PyObject *args)
{
	double sx, sy, sz, sw = 1;
	if(!PyArg_ParseTuple(args, "ddd|d:Vector4.scale", &sx, &sy, &sz, &sw))
		return NULL;
	else
		return PyVector4_new(self->x * sx, self->y * sy, self->z * sz, self->w * sw);
}

static PyObject *
PyVector4_cross(PyVector4 *self, PyObject *args)
{
	double x, y, z, w;
	if(getVector4(args, &x, &y, &z, &w) == 0)
		return PyVector4_new(self->y*z - self->z*y, self->z*x - self->x*z, self->x*y - self->y*x, 1);
	else
		return NULL;
}

static PyObject *
PyVector4_dot(PyVector4 *self, PyObject *args)
{
	double x, y, z, w;
	if(getVector4(args, &x, &y, &z, &w) == 0)
		return PyFloat_FromDouble(self->x*x + self->y*y + self->z*z);
	else
		return NULL;
}

static PyObject *
PyVector4_normalize(PyVector4 *self, PyObject *args)
{
	double length = sqrt(self->x*self->x + self->y*self->y + self->z*self->z);
	return PyVector4_new(self->x/length, self->y/length, self->z/length, 1);
}

static PyObject *
PyVector4_add(PyVector4 *self, PyVector4 *other)
{
	return PyVector4_new(self->x+other->x, self->y+other->y, self->z+other->z, 1);
}

static PyObject *
PyVector4_substract(PyVector4 *self, PyVector4 *other)
{
	return PyVector4_new(self->x-other->x, self->y-other->y, self->z-other->z, 1);
}

static PyObject *
PyVector4_multiply(PyVector4 *self, PyVector4 *other)
{
	return PyVector4_new(self->x*other->x, self->y*other->y, self->z*other->z, 1);
}

/*
static PyObject *
PyVector4_get_translation(PyVector4 *self, PyObject *args)
{
	if(!PyArg_ParseTuple(args, ":get_translation"))
		return NULL;
	else
		return Py_BuildValue("dd", self->tx, self->ty);
}

static PyObject *
PyVector4_no_translation(PyVector4 *self, PyObject *args)
{
	if(!PyArg_ParseTuple(args, ":no_translation"))
		return NULL;
	else
		return PyVector4_new(self->xx, self->yy, 0, 0);
}
*/
/*
static int
PyVector4_coerce(PyObject **a, PyObject **b)
{
	printf("a = %p\n", a);
	printf("b = %p\n", b);
	return 0;
}
static PyObject *
PyVector4_multiply(PyVector4 *self, PyObject *args)
//PyVector4_multiply(PyVector4 *self, PyVector4 *rhs)
{
	PyVector4 *rhs;
	rhs = (PyVector4*)args;
	
	if(!(PyObject_TypeCheck(args, &PyVector4_Type)||
		PyArg_ParseTuple(args, "O!:multiply", &PyVector4_Type, &rhs)))
	{
		double x, y;
		if(!PyArg_ParseTuple(args, "dd:multiply", &x, &y)
			&& !PyArg_ParseTuple(args, "(dd):multiply", &x, &y))
		{
			PyErr_SetString(PyExc_TypeError, "multiply takes a Vector4 or vector(tuple or 2 doubles) as argument");
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
		return PyVector4_new(
							self->xx*rhs->xx,
							self->yy*rhs->yy,
							self->xx*rhs->tx+self->tx,
							self->yy*rhs->ty+self->ty
							);
}

static PyObject *
PyVector4_scalebox(PyVector4 *self, PyObject *args)
{
	double x1, y1, x2, y2;
	if(!PyArg_ParseTuple(args, "(dd)(dd):scalebox", &x1, &y1, &x2, &y2))
		return NULL;
	else
	{
		double sx = x2 - x1;
		double sy = y2 - y1;
		return PyVector4_new(1/sx, 1/sy, x1/sx, y1/sy);
	}
}

static PyObject *
PyVector4_scalebox_inverse(PyVector4 *self, PyObject *args)
{
	double x1, y1, x2, y2;
	if(!PyArg_ParseTuple(args, "(dd)(dd):scalebox_inverse", &x1, &y1, &x2, &y2))
		return NULL;
	else
	{
		double sx = x2 - x1;
		double sy = y2 - y1;
		return PyVector4_new(sx, sy, x1, y1);
	}
}
*/
static PyMethodDef PyVector4_methods[] = {
    { "scale", (PyCFunction)PyVector4_scale, METH_VARARGS},
    { "normalize", (PyCFunction)PyVector4_normalize, METH_VARARGS},
    { "cross", (PyCFunction)PyVector4_cross, METH_VARARGS},
    { "dot", (PyCFunction)PyVector4_dot, METH_VARARGS},
    /*{ "inverse", (PyCFunction)PyVector4_inverse, METH_VARARGS },
    { "translate", (PyCFunction)PyVector4_translate, METH_VARARGS|METH_STATIC},
    { "get_translation", (PyCFunction)PyVector4_get_translation, METH_VARARGS },
    { "no_translation", (PyCFunction)PyVector4_no_translation, METH_VARARGS },
    { "multiply", (PyCFunction)PyVector4_multiply, METH_VARARGS },
    { "scalebox", (PyCFunction)PyVector4_scalebox, METH_VARARGS|METH_STATIC},
    { "scalebox_inverse", (PyCFunction)PyVector4_scalebox_inverse, METH_VARARGS|METH_STATIC},
    */
    { NULL, NULL, 0 }
};


static PyObject *
PyVector4_get_x(PyVector4 *self)
{
    return PyFloat_FromDouble(self->x);
}

static PyObject *
PyVector4_get_y(PyVector4 *self)
{
    return PyFloat_FromDouble(self->y);
}

static PyObject *
PyVector4_get_z(PyVector4 *self)
{
    return PyFloat_FromDouble(self->z);
}

static PyObject *
PyVector4_get_w(PyVector4 *self)
{
    return PyFloat_FromDouble(self->w);
}

static PyObject *
PyVector4_get_length(PyVector4 *self)
{
    return PyFloat_FromDouble(sqrt(self->x*self->x + self->y*self->y + self->z*self->z));
}

static PyGetSetDef PyVector4_getseters[] = {
    { "x", (getter)PyVector4_get_x, (setter)0 },
    { "y", (getter)PyVector4_get_y, (setter)0 },
    { "z", (getter)PyVector4_get_z, (setter)0 },
    { "w", (getter)PyVector4_get_w, (setter)0 },
    { "length", (getter)PyVector4_get_length, (setter)0 },
    { NULL, (getter)0, (setter)0 }
};

int PyVector4_PySequence_length(PyVector4 *vector)
{
	return 4;
}

PyObject* PyVector4_PySequence_item(PyVector4 *self, int item)
{
	if(item == 0)
		return PyFloat_FromDouble(self->x);
	else if(item == 1)
		return PyFloat_FromDouble(self->y);
	else if(item == 2)
		return PyFloat_FromDouble(self->z);
	else if(item == 3)
		return PyFloat_FromDouble(self->w);
	else
		return PyErr_Format(PyExc_IndexError, "Vector4 only has 4 elements");
}

static PySequenceMethods PyVector4_PySequenceMethods = {
	PyVector4_PySequence_length,
	0,0,
	PyVector4_PySequence_item,
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


static PyNumberMethods PyVector4_as_number = {
  (binaryfunc)PyVector4_add,
  (binaryfunc)PyVector4_substract,
  (binaryfunc)PyVector4_multiply,
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
  (coercion)0, //PyVector4_coerce,
  (unaryfunc)0,
  (unaryfunc)0,
  (unaryfunc)0,
  (unaryfunc)0,
  (unaryfunc)0,
  //(binaryfunc)0,
  //(binaryfunc)0,
  //(binaryfunc)PyVector4_multiply
};

static PyObject *
PyVector4_repr(PyVector4 *self)
{
	char buf[256];
	if(self->w == 1)
		PyOS_snprintf(buf, sizeof(buf), "kaplot.Vector4(%g, %g, %g)",
		  self->x, self->y, self->z);
	else
		PyOS_snprintf(buf, sizeof(buf), "kaplot.Vector4(%g, %g, %g, %g)",
		  self->x, self->y, self->z, self->w);
    return PyString_FromString(buf);
}

PyTypeObject PyVector4_Type = {
    PyObject_HEAD_INIT(NULL)
    0,                                  /* ob_size */
    "Vector4",                    			/* tp_name */
    sizeof(PyVector4),          		   /* tp_basicsize */
    0,                                  /* tp_itemsize */
    /* methods */
    (destructor)PyVector4_dealloc, /* tp_dealloc */
    (printfunc)0,                       /* tp_print */
    (getattrfunc)0,                     /* tp_getattr */
    (setattrfunc)0,                     /* tp_setattr */
    (cmpfunc)0,                         /* tp_compare */
    (reprfunc)PyVector4_repr,                        /* tp_repr */
    &PyVector4_as_number,                                  /* tp_as_number */
    &PyVector4_PySequenceMethods,                                  /* tp_as_sequence */
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
    PyVector4_methods,        			    /* tp_methods */
    0,                                  /* tp_members */
    PyVector4_getseters,           		   /* tp_getset */
    (PyTypeObject*)0,                  /* tp_base */
    (PyObject *)0,                      /* tp_dict */
    0,                                  /* tp_descr_get */
    0,                                  /* tp_descr_set */
    0,                                  /* tp_dictoffset */
    (initproc)PyVector4_init,                        /* tp_init */
    (allocfunc)0,                       /* tp_alloc */
    (newfunc)0,                         /* tp_new */
    (freefunc)0,                        /* tp_free */
    (inquiry)0,                         /* tp_is_gc */
    (PyObject *)0,                      /* tp_bases */
};

static PyMethodDef PyVector4_functions[] = {
    { NULL, NULL, 0 }
};



