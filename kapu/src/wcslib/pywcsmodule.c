//#include "pywcs.h"
#include "reproj.h"
//#include <libnumpy.h>

#include "reproj.h"
#include "pywcs.h"
#include <math.h>
#include <float.h>
//#include <libnumpy.h>
//#include <arrayobject.h>
#include <libnumarray.h>

static PyObject* PyReproj(PyObject* self, PyObject *args)
{
	PyObject* result = NULL;
	PyWcsObject *source_wcs;
	PyWcsObject *dest_wcs;
	PyObject *image_object;
	PyObject *new_image_object;
	PyArrayObject *image_array;
	int width, height;
	int new_width, new_height;
	double blank = DBL_MAX*2; // hopefully this is NaN, it's not, it's +INF, TODO
	double *image;
	double *new_image;
	double *pixcrd;
	double *imgcrd;
	double *phi, *theta;
	double *world;
	int *stat;
	int x, y;
	double xmin, ymin, xmax, ymax;
	double px, py;
	int pxi, pyi;
	int dims[2];
	int error;

#define PTR_CHECK(ptr) if(!ptr) return PyErr_Format(PyExc_MemoryError, "couldn't allocate memory, possibly a wrong wcs transformation");
	printf("begin");
	if(PyArg_ParseTuple(args, "OO!O!|d:reproj", &image_object, &PyWcs_Type, &source_wcs, &PyWcs_Type, &dest_wcs, &blank))
	{
		printf("-1\n");
		image_array = NA_InputArray(image_object, tFloat64, C_ARRAY);
		printf("-2\n");
		if(image_array == NULL)
			return PyErr_Format(PyExc_TypeError, "can't convert image data into numpy");
		if(image_array->nd != 2)
			return PyErr_Format(PyExc_TypeError, "image isn't 2 dimensional");
		printf("-3\n");
		width = image_array->dimensions[1];
		height = image_array->dimensions[0];
		image = (double*)NA_OFFSETDATA(image_array);

		pixcrd = (double*)malloc(width*height*sizeof(double) * 2);
		imgcrd = (double*)malloc(width*height*sizeof(double) * 2);
		phi = (double*)malloc(width*height*sizeof(double));
		theta = (double*)malloc(width*height*sizeof(double));
		world = (double*)malloc(width*height*sizeof(double)*2);
		stat = (int*)malloc(width*height*sizeof(int));

		pixcrd[0] = 1;
		pixcrd[1] = 1;
		error = wcsp2s(source_wcs->wcs, 1, 2, pixcrd, imgcrd, phi, theta, world, stat);
		error = wcss2p(dest_wcs->wcs,   1, 2, world, phi, theta, imgcrd, pixcrd, stat);
		printf("1) %f %f %f %f %i %i\n", pixcrd[0], pixcrd[1], world[0], world[1], error, stat[0]);
		pixcrd[0] = width;
		pixcrd[1] = 1;
		error = wcsp2s(source_wcs->wcs, 1, 2, pixcrd, imgcrd, phi, theta, world, stat);
		error = wcss2p(dest_wcs->wcs,   1, 2, world, phi, theta, imgcrd, pixcrd, stat);
		printf("2) %f %f %f %f %i %i\n", pixcrd[0], pixcrd[1], world[0], world[1], error, stat[0]);
		pixcrd[0] = width;
		pixcrd[1] = height;
		error = wcsp2s(source_wcs->wcs, 1, 2, pixcrd, imgcrd, phi, theta, world, stat);
		error = wcss2p(dest_wcs->wcs,   1, 2, world, phi, theta, imgcrd, pixcrd, stat);
		printf("3) %f %f %f %f %i %i\n", pixcrd[0], pixcrd[1], world[0], world[1], error, stat[0]);
		pixcrd[0] = 1;
		pixcrd[1] = height;
		error = wcsp2s(source_wcs->wcs, 1, 2, pixcrd, imgcrd, phi, theta, world, stat);
		error = wcss2p(dest_wcs->wcs,   1, 2, world, phi, theta, imgcrd, pixcrd, stat);
		printf("4) %f %f %f %f %i %i\n", pixcrd[0], pixcrd[1], world[0], world[1], error, stat[0]);

		for(x = 0; x < width; x++)
		{
			for(y = 0; y < height; y++)
			{
				pixcrd[(x + y * width)*2+0] = x + 1; // fits images start at 1,1
				pixcrd[(x + y * width)*2+1] = y + 1; //
			}
		}

		printf("-4\n");
		error = wcsp2s(source_wcs->wcs, width*height, 2, pixcrd, imgcrd, phi, theta, world, stat);
		printf("-5 %i\n", error);
		error = wcss2p(dest_wcs->wcs,   width*height, 2, world, phi, theta, imgcrd, pixcrd, stat);
		printf("-6 %i\n", error);

		xmin = pixcrd[0];
		ymin = pixcrd[1];
		xmax = pixcrd[0];
		ymax = pixcrd[1];
		for(x = 0; x < width; x++)
		{
			for(y = 0; y < height; y++)
			{
				//printf("%i ", stat[x + y * width]);
				if(pixcrd[(x + y * width)*2+0] > xmax)
					xmax = pixcrd[(x + y * width)*2+0];
				if(pixcrd[(x + y * width)*2+0] < xmin)
					xmin = pixcrd[(x + y * width)*2+0];
				if(pixcrd[(x + y * width)*2+1] > ymax)
					ymax = pixcrd[(x + y * width)*2+1];
				if(pixcrd[(x + y * width)*2+1] < ymin)
					ymin = pixcrd[(x + y * width)*2+1];
			}
		}
		printf("<%f %f %f %f>\n", xmin, ymin, xmax, ymax);
		printf("-7\n");
		new_width = (int)ceil(xmax - xmin);
		new_height = (int)ceil(ymax - ymin);

		free(pixcrd);
		free(imgcrd);
		free(phi);
		free(theta);
		free(world);
		free(stat);

		pixcrd = (double*)	malloc(new_width*new_height*sizeof(double) * 2);
		PTR_CHECK(pixcrd);
		imgcrd = (double*)	malloc(new_width*new_height*sizeof(double) * 2);
		PTR_CHECK(imgcrd);
		phi = (double*)		malloc(new_width*new_height*sizeof(double));
		PTR_CHECK(phi);
		theta = (double*)	malloc(new_width*new_height*sizeof(double));
		PTR_CHECK(theta);
		world = (double*)	malloc(new_width*new_height*sizeof(double)*2);
		PTR_CHECK(world);
		stat = (int*)		malloc(new_width*new_height*sizeof(int));
		PTR_CHECK(stat);
		new_image = (double*)malloc(new_width * new_height * sizeof(double));
		PTR_CHECK(new_image);

		for(x = 0; x < new_width; x++)
		{
			for(y = 0; y < new_height; y++)
			{
				pixcrd[(x + y * new_width)*2+0] = xmin + x;
				pixcrd[(x + y * new_width)*2+1] = ymin + y;
			}
		}
		printf("-8\n");

		error = wcsp2s(dest_wcs->wcs,   new_width*new_height, 2, pixcrd, imgcrd, phi, theta, world, stat);
		printf("-8/1 %i\n", error);
		error = wcss2p(source_wcs->wcs, new_width*new_height, 2, world, phi, theta, imgcrd, pixcrd, stat);
		printf("-9   %i\n", error);
		for(x = 0; x < new_width; x++)
		{
			for(y = 0; y < new_height; y++)
			{
				px = pixcrd[(x + y * new_width)*2+0];
				py = pixcrd[(x + y * new_width)*2+1];
				pxi = (int)floor(px+0.5)-1; // round, and correct for the fits start at 1,1
				pyi = (int)floor(py+0.5)-1; // round, and correct for the fits start at 1,1
				if(pxi >= 0 && pxi < width && pyi >= 0 && pyi < height)
				{
					new_image[(x + y * new_width)] = image[pxi + pyi * width];
				}
				else
				{
					new_image[(x + y * new_width)] = blank;
				}
			}
		}
		printf("-10 %f %f %f %f\n", xmin, ymin, xmax, ymax);
		dims[0] = new_height;
		dims[1] = new_width;
		printf("-10/1\n");
		new_image_object = PyArray_FromDims(2, dims, tFloat64);
		printf("-10/2\n");
		memcpy((double*)NA_OFFSETDATA(((PyArrayObject*)new_image_object)), new_image, new_width * new_height * sizeof(double));
		printf("-11\n");

		free(new_image);

		free(pixcrd);
		free(imgcrd);
		free(phi);
		free(theta);
		free(world);
		free(stat);

		result = Py_BuildValue("(Oddd)", new_image_object, xmin, ymin, blank);

	}
	return result;
}


static PyMethodDef wcs_functions[] = {
		{"reproj", (PyCFunction)PyReproj, METH_VARARGS, "reprojects an image"},
		{NULL, NULL, 0, NULL}
};

PyMODINIT_FUNC
init_wcslib(void)
{
	PyObject *mod;
	PyWcs_Type.tp_new = PyType_GenericNew;
	if (PyType_Ready(&PyWcs_Type) < 0)
        return;
	import_libnumarray();
	import_array();
	//import_libnumpy();
	mod = Py_InitModule3("kapu._wcslib", wcs_functions, "Binding to wcslib");
    Py_INCREF(&PyWcs_Type);
    PyModule_AddObject(mod, "Wcs", (PyObject*)&PyWcs_Type);
}



