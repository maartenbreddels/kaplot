#include <Python.h>
#include <libnumarray.h>
//#include <libnumeric.h>

int skyco_c( double *xin,
              double *yin,
              int   *min,
              double *xou,
              double *you,
              int   *mou ) ;

PyObject* PyKaplot_Gipsy_Sky(PyObject* self, PyObject* args)
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
	int type_in, type_out;
	int ret;
	char* error_msg = "unknown error";

	if(PyArg_ParseTuple(args, "OOii", &x_array, &y_array, &type_in, &type_out))
	{
		x_array_double = NA_InputArray(x_array, tFloat64, C_ARRAY);
		y_array_double = NA_InputArray(y_array, tFloat64, C_ARRAY);
		if(x_array_double == NULL)
			return PyErr_Format(PyExc_TypeError, "can't convert x data into numarray");
		if(x_array_double->nd != 1)
			return PyErr_Format(PyExc_TypeError, "x data isn't 1 dimensional");
		if(y_array_double == NULL)
			return PyErr_Format(PyExc_TypeError, "can't convert y data into numarray");
		if(y_array_double->nd != 1)
			return PyErr_Format(PyExc_TypeError, "y data isn't 1 dimensional");
		length = MIN(x_array_double->dimensions[0], y_array_double->dimensions[0]);
		x = (double*)NA_OFFSETDATA(x_array_double);
		y = (double*)NA_OFFSETDATA(y_array_double);
		
		dims[0] = length;
		x_array_double_out = (PyArrayObject*)PyArray_FromDims(1, dims, tFloat64);
		y_array_double_out = (PyArrayObject*)PyArray_FromDims(1, dims, tFloat64);
		x_out = (double*)NA_OFFSETDATA(x_array_double_out);
		y_out = (double*)NA_OFFSETDATA(y_array_double_out);
		for(i = 0; i < length; i++)
		{
			ret = skyco_c(x+i, y+i, &type_in, x_out+i, y_out+i, &type_out);
			if(ret != 0)
			{
				switch(ret)
				{
					case 5: error_msg = "input sky system unknown"; break;
					case 6: error_msg = "output sky system unknown "; break;
					case 7: error_msg = "input and output sky system unknown "; break;
				}
				PyErr_Format(PyExc_ValueError, "Error in transforming skysystem coordinate: %s\n", error_msg);
				Py_DECREF(x_array_double_out);
				Py_DECREF(y_array_double_out);
			}
		}
		return Py_BuildValue("OO", x_array_double_out, y_array_double_out);
	}
	else
		return NULL;
}
void eclipco_c( double *lambdaI, double *betaI, double *epochIN, 
                double *lambdaO, double *betaO, double *epochOUT );
void epoco_c(double *a1, double *d1, double *t1, double *a2, double *d2, double *t2 );
typedef void (*epoch_function_t)(double*, double*, double*, double*, double*, double*);

PyObject* PyKaplot_Gipsy_Epoch_Generic(PyObject* self, PyObject* args, epoch_function_t epoch_function)
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
	double epoch_in, epoch_out;
	char* error_msg = "unknown error";

	if(PyArg_ParseTuple(args, "OOdd", &x_array, &y_array, &epoch_in, &epoch_out))
	{
		x_array_double = NA_InputArray(x_array, tFloat64, C_ARRAY);
		y_array_double = NA_InputArray(y_array, tFloat64, C_ARRAY);
		if(x_array_double == NULL)
			return PyErr_Format(PyExc_TypeError, "can't convert x data into numarray");
		if(x_array_double->nd != 1)
			return PyErr_Format(PyExc_TypeError, "x data isn't 1 dimensional");
		if(y_array_double == NULL)
			return PyErr_Format(PyExc_TypeError, "can't convert y data into numarray");
		if(y_array_double->nd != 1)
			return PyErr_Format(PyExc_TypeError, "y data isn't 1 dimensional");
		length = MIN(x_array_double->dimensions[0], y_array_double->dimensions[0]);
		x = (double*)NA_OFFSETDATA(x_array_double);
		y = (double*)NA_OFFSETDATA(y_array_double);
		
		dims[0] = length;
		x_array_double_out = (PyArrayObject*)PyArray_FromDims(1, dims, tFloat64);
		y_array_double_out = (PyArrayObject*)PyArray_FromDims(1, dims, tFloat64);
		x_out = (double*)NA_OFFSETDATA(x_array_double_out);
		y_out = (double*)NA_OFFSETDATA(y_array_double_out);
		for(i = 0; i < length; i++)
		{
			epoch_function(x+i, y+i, &epoch_in, x_out+i, y_out+i, &epoch_out);
		}
		return Py_BuildValue("OO", x_array_double_out, y_array_double_out);
	}
	else
		return NULL;
}


PyObject* PyKaplot_Gipsy_Epoch_Ecliptic(PyObject* self, PyObject* args)
{
	return PyKaplot_Gipsy_Epoch_Generic(self, args, eclipco_c);
}

PyObject* PyKaplot_Gipsy_Epoch(PyObject* self, PyObject* args)
{
	return PyKaplot_Gipsy_Epoch_Generic(self, args, epoco_c);
}

static PyMethodDef kaplot_gipsy_functions[] = {
		{"skyco", (PyCFunction)PyKaplot_Gipsy_Sky, METH_VARARGS, "does sky transformations"},
		{"epoco", (PyCFunction)PyKaplot_Gipsy_Epoch, METH_VARARGS, "does equatorial epoch transformations"},
		{"epoco_ecliptic", (PyCFunction)PyKaplot_Gipsy_Epoch_Ecliptic, METH_VARARGS, "does ecliptical epoch transformations"},
		//{"eclip", (PyCFunction)PyKaplot_Gipsy_Eclip, METH_VARARGS, ""},
		{NULL, NULL, 0, NULL}
};

PyMODINIT_FUNC
init_gipsy(void)
{
	PyObject *mod;
	import_libnumarray();
	import_libnumeric();
	mod = Py_InitModule("kaplot.cext._gipsy", kaplot_gipsy_functions);
	PyModule_AddIntConstant(mod, "EQUATORIAL_1950", 1);
	PyModule_AddIntConstant(mod, "GALACTIC", 2);
	PyModule_AddIntConstant(mod, "ECLIPTIC", 3);
	PyModule_AddIntConstant(mod, "SUPERGALACTIC", 4);
	PyModule_AddIntConstant(mod, "EQUATORIAL_2000", 5);

}