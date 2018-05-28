#define KAPLOT_CONTOUR_MODULE
#include "contour.h"
#include "cinterface.h"
#include <Python.h>
//#define PY_ARRAY_UNIQUE_SYMBOL PyArrayHandle
//#include <numpy/libnumarray.h>
#include <numpy/arrayobject.h>
#include "f2c.h"

PyObject *labelelements;
PyObject *polylines;
float *xelements;
float *yelements;
int pointcount;
float prevx, prevy;
float distance_square;
float label_length = 2;
float label_length_square = 2*2;
float label_seperation = 10;
float label_seperation_square = 10*10;
int size;
int first;
int inlabel;
/*
*/

typedef int (*plotfunc)();

int pgcnsc_(real *z__, integer *mx, integer *my, integer *ia, integer *ib, integer *ja, integer *jb, integer *z0, int (*plot) ());
int pgconx_(real *a, integer *idim, integer *jdim, integer *i1, integer *i2, integer *j1, integer *j2, real *c__, integer *nc, int (*plot)(), void *userdata);
void grwarn_(char* s, int len)
{
	printf(s);
}
int pgnoto_(char* s, int len)
{
	/*printf(s);*/
	return 0;
}
void pgbbuf_()
{
}

void addPolyline()
{
	PyObject* tuple;
	PyObject* xArray;
	PyObject* yArray;
	int size;

	if(pointcount > 0)
	{
		size = pointcount;
		tuple = PyTuple_New(2);
		xArray = PyArray_FromDims(1, &size, NPY_FLOAT32);
		yArray = PyArray_FromDims(1, &size, NPY_FLOAT32);
		memcpy((float*)(PyArray_DATA(((PyArrayObject*)xArray))), (void*)xelements, size*sizeof(float));
		memcpy((float*)(PyArray_DATA(((PyArrayObject*)yArray))), (void*)yelements, size*sizeof(float));
		PyTuple_SET_ITEM(tuple, 0, xArray);
		PyTuple_SET_ITEM(tuple, 1, yArray);
		PyList_Append(polylines, tuple);
	}
	pointcount = 0;
}

void func(long int* visible_, float* x, float* y, float* z, void *userdata)
{
	kaplot_cinterface_t *cinterface = (kaplot_cinterface_t*)userdata;
	int visible = *visible_;
	float dx, dy;
	float distance_square_mod;
	
	if(!visible)
	{
		if(pointcount > 0)
		{
			if(cinterface != NULL)
				cinterface->stroke(cinterface);
			addPolyline();
		}
	}
	else
	{
		if(pointcount == 0)
		{
			if(cinterface != NULL)
				cinterface->move_to(cinterface, prevx, prevy);
			xelements[pointcount] = prevx;
			yelements[pointcount] = prevy;
			pointcount++;
		}
		dx = *x - prevx;
		dy = *y - prevy;
		distance_square += dx*dx + dy*dy;
		distance_square_mod = (float)fmod(distance_square, label_seperation_square);
		if(	!((distance_square_mod < label_seperation_square/2-label_length_square/2) ||
			(distance_square_mod > label_seperation_square/2+label_length_square/2))
			&& 0)
		{
			if(!inlabel)
			{
				addPolyline();
			}
			else
			{
				xelements[pointcount-1] = *x;
				yelements[pointcount-1] = *y;
			}
			inlabel = 1;
		}
		else
		{
			//if(!inlabel)
			{
				if(cinterface != NULL)
					cinterface->line_to(cinterface, *x, *y);
				xelements[pointcount] = *x;
				yelements[pointcount] = *y;
				pointcount++;
			}
			inlabel = 0;
		}
		//printf("%f %f %f %i\n", distance_square, distance_square_mod, label_seperation_square, inlabel);
	}
	prevx = *x;
	prevy = *y;
}
void func_(long int* visible, float* x, float* y, float* z, void *userdata)
{
	kaplot_cinterface_t *cinterface = (kaplot_cinterface_t*)userdata;
	float distance_square_mod = (float)fmod(distance_square, label_seperation_square);
	if(!first)
	{
		float dx = *x - prevx;
		float dy = *y - prevy;
		distance_square += dx*dx + dy*dy;
	}
	first = 0;
	prevx = *x;
	prevy = *y;
	if(	!(distance_square_mod < label_seperation_square/2-label_length_square/2) &&
		(distance_square_mod > label_seperation_square/2+label_length_square/2))
	{
		if(!inlabel)
		{
			if(pointcount > 1)
				addPolyline();
		}
			
		inlabel = 1;
		*visible = 0;
	}
	else
	{
		inlabel = 0;
	}

	//printf("%f %f %f %i\n", distance_square, distance_square_mod, label_seperation_square, inlabel);
	
	if(!(*visible))
	{
		if(cinterface != NULL)
		{
			cinterface->stroke(cinterface);
			cinterface->move_to(cinterface, *x, *y);
		}
		if(pointcount > 1)
			addPolyline();
		pointcount = 0;
		xelements[pointcount] = *x;
		yelements[pointcount] = *y;
		pointcount++;
	}
	else
	{
		//cairo_line_to(last_context, *x, *y);
		if(cinterface != NULL)
			cinterface->line_to(cinterface, *x, *y);
		xelements[pointcount] = *x;
		yelements[pointcount] = *y;
		if(pointcount > 1)
		{
		}
		pointcount++;
	}

}

void PyKaplot_Contour(float* data, int width, int height, int beginx, int endx,
						int beginy, int endy, float* levels, int levelcount, contour_callback callback, void *userdata)
{
	distance_square = 0;
	pointcount = 0;
	first = 1;
	inlabel = 0;
	//printf("%li %li %li %li %li %li %li\n", width, height, beginx, endx, beginy, endy, levelcount);
	pgconx_(data, &width, &height, &beginx, &endx, &beginy, &endy, levels, &levelcount, (plotfunc)callback, userdata);
}


PyObject* PyContour(PyObject* self, PyObject *args)
{
	PyObject *result = NULL;
    PyObject *image;
	PyArrayObject *dataArray;
	PyObject *cinterface_object = NULL;
	kaplot_cinterface_t *cinterface;
	//PyObject *xArray, *yArray;
	float level1;
	long int width, height, beginx, endx, beginy, endy, zero;
	integer levelCount;
	real levels[1];

	if (PyArg_ParseTuple(args, "Of|O!:contour", &image, &level1, &PyCObject_Type, &cinterface_object))
	{
		dataArray = (PyArrayObject*)PyArray_FromAny(image, NPY_FLOAT32, 2, 2, NPY_ARRAY_C_CONTIGUOUS, NULL);
		//printf("dataArray = %x %x\n", dataArray, image);
		if(dataArray == NULL)
			return PyErr_Format(PyExc_TypeError, "can't convert image data into numpy");
		if(dataArray->nd != 2)
			return PyErr_Format(PyExc_TypeError, "data isn't 2 dimensional");

		width = dataArray->dimensions[1];
		height = dataArray->dimensions[0];
		beginx = 1;
		endx = width;
		beginy = 1;
		endy = height;
		zero = 0;
		levelCount = 1;
		levels[0] = level1;
		size = 0;
		pointcount = 0;
		polylines = PyList_New(0);
		//printf("..... %li %li %f %li %li\n", width, height, level1, sizeof(int), sizeof(long int));
		

		xelements = (float*)malloc(sizeof(float) * width * height);
		yelements = (float*)malloc(sizeof(float) * width * height);
		labelelements = PyList_New(0);
		if(cinterface_object != NULL)
			cinterface = PyCObject_AsVoidPtr(cinterface_object);
		else
			cinterface = NULL;
		PyKaplot_Contour((float*)PyArray_DATA(dataArray), width, height, beginx, endx, beginy, endy, levels, levelCount, func, cinterface);
		if(pointcount > 0)
		{
			addPolyline();
			if(cinterface != NULL)
				cinterface->stroke(cinterface);
		}

		//pgconx_((real*)NA_OFFSETDATA(dataArray), &width, &height, &beginx, &endx, &beginy, &endy, levels, &levelCount, (plotfunc)func);
		//if(pointcount > 0)
		//	addPolyline();
		//pgconx_((real*)NA_OFFSETDATA(dataArray), &width, &height, &beginx, &endx, &beginy, &endy, levels, &levelCount, (plotfunc)func);

		//xArray = PyArray_FromDimsAndData(1, &size, tFloat32, (char*)xelements);
		//yArray = PyArray_FromDimsAndData(1, &size, tFloat32, (char*)yelements);
		//printf("size: %i\n", size);

		free(xelements);
		free(yelements);

		//Py_XDECREF(dataArray);
		return Py_BuildValue("(OO)", polylines, labelelements);
        /*
		Py_INCREF(Py_None);
        result = Py_None;
		*/
    }
    return result;

}

static PyMethodDef kaplot_ext_functions[] = {
		{"contour", (PyCFunction)PyContour, METH_VARARGS, "draws a contour"},
		{NULL, NULL, 0, NULL}
};

PyMODINIT_FUNC
init_contour(void)
{
	static void *PyKaplotContour_API[1];
	PyObject *mod;
	PyObject *c_api_object;

	import_array();

	mod = Py_InitModule("kaplot.cext._contour", kaplot_ext_functions);
	PyKaplotContour_API[0] = (void *)PyKaplot_Contour;
	c_api_object = PyCObject_FromVoidPtr((void *)PyKaplotContour_API, NULL);
	if (c_api_object != NULL)
		PyModule_AddObject(mod, "_C_API", c_api_object);

}
