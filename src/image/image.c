/* -*- mode: C; c-basic-offset: 4 -*- */
#include <Python.h>
//#include <libnumarray.h>
//#include <arrayobject.h>
#include <numpy/arrayobject.h>

extern PyTypeObject PyKaplotImage_Type;

PyObject *pykaplot_image_new(int width, int height);

typedef struct {
    PyObject_HEAD
    //cairo_surface_t *surface;
    char* image_data;
    int width;
    int height;
    int owns_data;
} PyKaplotImage;

void write32to24(unsigned char* source, unsigned char* dest, int width, int height, int red_index, int green_index, int blue_index)
{
	int length, i;
	length = width * height;
	for(i = 0; i < length; i++)
	{
		dest[i*3+0] = source[i*4+red_index];
		dest[i*3+1] = source[i*4+green_index];
		dest[i*3+2] = source[i*4+blue_index];
	}
}

void write24to32(unsigned char* source, unsigned char* dest, int width, int height, int red_index, int green_index, int blue_index, unsigned char alpha)
{
	int length, i;
	length = width * height;
	for(i = 0; i < length; i++)
	{
		dest[i*4+0] = source[i*3+red_index];
		dest[i*4+1] = source[i*3+green_index];
		dest[i*4+2] = source[i*3+blue_index];
		dest[i*4+3] = alpha;
	}
}

void write32to24blend(unsigned char* source, unsigned char* dest, int width, int height, int red_index, int green_index, int blue_index, int alpha_index)
{
	int length, i;
	length = width * height;
	for(i = 0; i < length; i++)
	{
		dest[i*3+0] = (((unsigned int)source[i*4+red_index]) * source[i*4+alpha_index]) / 255;
		dest[i*3+1] = (((unsigned int)source[i*4+green_index]) * source[i*4+alpha_index]) / 255;
		dest[i*3+2] = (((unsigned int)source[i*4+blue_index]) * source[i*4+alpha_index]) / 255;
	}
}

void write32to32(unsigned char* source, unsigned char* dest, int width, int height, int red_index, int green_index, int blue_index, int alpha_index)
{
	int length, i;
	length = width * height;
	for(i = 0; i < length; i++)
	{
		dest[i*4+0] = source[i*4+red_index];
		dest[i*4+1] = source[i*4+green_index];
		dest[i*4+2] = source[i*4+blue_index];
		dest[i*4+3] = source[i*4+alpha_index];

	}
}


PyObject *
pykaplot_image_new(int width, int height)
{
    PyKaplotImage *self;

    self = PyObject_New(PyKaplotImage, &PyKaplotImage_Type);
    if (!self) {
		return NULL;
    }

    self->image_data = malloc(width*height*4);
    self->width = width;
    self->height = height;

    return (PyObject *)self;
}

static int
pykaplot_image_init(PyKaplotImage *self, PyObject *args, PyObject *kwargs)
{
	int width;
	int height;
	char* buffer = 0;
	int buffersize = 0;

    if (!PyArg_ParseTuple(args, "ii|w#:Image.__init__", &width, &height, &buffer, &buffersize))
    {
		return -1;
	}

	if(buffer != 0)
	{
		self->image_data = buffer;
	    if(width*height > buffersize)
	    {
	    	PyErr_SetString(PyExc_TypeError,"Image.__init__ buffer is not long enough");
			return -1;
		}
		self->owns_data = 0;
	}
	else
	{
		self->image_data = malloc(width*height*4);
		self->owns_data = 1;
	}
    self->width = width;
    self->height = height;
	return 0;
}

static void
pykaplot_image_dealloc(PyKaplotImage *self)
{
    if (self->image_data && self->owns_data)
		free(self->image_data);
    self->image_data = NULL;

    if (self->ob_type->tp_free)
	self->ob_type->tp_free((PyObject *)self);
    else
	PyObject_Del(self);
}

static PyObject *
pykaplot_image_get_argb_string(PyKaplotImage *self, PyObject *args)
{
    int red_index = 2, green_index = 1, blue_index = 0, alpha_index = 3;
    PyObject* result;
	char* temp;

    if (!PyArg_ParseTuple(args, "|iiii:Image.get_argb_string",
			  &red_index, &green_index, &blue_index, &alpha_index))
	return NULL;

	temp = malloc(self->width * self->height * 4);
	write32to32(self->image_data, temp, self->width, self->height, red_index, green_index, blue_index, alpha_index);
	result = PyString_FromStringAndSize(temp, self->width * self->height * 4);
	free(temp);
	return result;
}

static PyObject *
pykaplot_image_get_rgb_string(PyKaplotImage *self, PyObject *args)
{
    int red_index = 2, green_index = 1, blue_index = 0, alpha_index=3, blend = 0;
    PyObject* result;
	char* temp;

    if (!PyArg_ParseTuple(args, "|iiiii:Image.get_rgb_string",
			  &red_index, &green_index, &blue_index, &alpha_index, &blend))
	return NULL;

	temp = malloc(self->width * self->height * 3);
	if(blend)
		write32to24blend(self->image_data, temp, self->width, self->height, red_index, green_index, blue_index, alpha_index);
	else
		write32to24(self->image_data, temp, self->width, self->height, red_index, green_index, blue_index);
	result = PyString_FromStringAndSize(temp, self->width * self->height * 3);
	free(temp);
	return result;
}

static PyObject *
pykaplot_image_set_rgb_string(PyKaplotImage *self, PyObject *args)
{
    int red_index = 2, green_index = 1, blue_index = 0, alpha_index=3;
    PyObject *pystring;

    if (!PyArg_ParseTuple(args, "O|iiiii:Image.get_rgb_string", &pystring,
			  &red_index, &green_index, &blue_index, &alpha_index))
	return NULL;

	if(!PyString_Check(pystring))
	{
		PyErr_SetString(PyExc_TypeError,"Image.set_rgb_string expects string as first argument");
		return NULL;
	}
	if(PyString_Size(pystring) != (self->width * self->height * 3))
	{
		PyErr_Format(PyExc_Exception,"Image.set_rgb_string string argument is of wrong length: %i, should be %i", PyString_Size(pystring), self->width * self->height * 3);
		return NULL;
	}

	write24to32(PyString_AsString(pystring), self->image_data, self->width, self->height, red_index, green_index, blue_index, 0xff);
	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject *
pykaplot_image_set_argb_string(PyKaplotImage *self, PyObject *args)
{
    int red_index = 2, green_index = 1, blue_index = 0, alpha_index=3;
    PyObject *pystring;

    if (!PyArg_ParseTuple(args, "O|iiiii:Image.get_rgb_string", &pystring,
			  &red_index, &green_index, &blue_index, &alpha_index))
	return NULL;

	if(!PyString_Check(pystring))
	{
		PyErr_SetString(PyExc_TypeError,"Image.set_rgb_string expects string as first argument");
		return NULL;
	}
	if(PyString_Size(pystring) != (self->width * self->height * 4))
	{
		PyErr_Format(PyExc_Exception,"Image.set_rgb_string string argument is of wrong length: %i, should be %i", PyString_Size(pystring), self->width * self->height * 4);
		return NULL;
	}

	write32to32(PyString_AsString(pystring), self->image_data, self->width, self->height, red_index, green_index, blue_index, alpha_index);
	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject *
pykaplot_image_write_rgb_to_buffer(PyKaplotImage *self, PyObject *args)
{
    int red_index = 2, green_index = 1, blue_index = 0, alpha_index=3, blend = 0;
    char* buffer;
    int buffersize;

    if (!PyArg_ParseTuple(args, "w#|iiii:Image.write_rgb_to_buffer", &buffer, &buffersize,
			  &red_index, &green_index, &blue_index, &alpha_index))
	return NULL;

	if(buffersize < (self->width * self->height * 3))
	{
		PyErr_Format(PyExc_Exception,"Image.copy_rgb_to_buffer buffer is not long enough: is %i, should be %i", buffersize, self->width * self->height * 3);
		return NULL;
	}

	if(blend)
		write32to24blend(self->image_data, buffer, self->width, self->height, red_index, green_index, blue_index, alpha_index);
	else
		write32to24(self->image_data, buffer, self->width, self->height, red_index, green_index, blue_index);
	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject *
pykaplot_image_write_argb_to_buffer(PyKaplotImage *self, PyObject *args)
{
    int red_index = 2, green_index = 1, blue_index = 0, alpha_index=3;
    //PyObject *pystring;
    char* buffer;
    int buffersize;

    if (!PyArg_ParseTuple(args, "w#|iiii:Image.write_argb_to_buffer", &buffer, &buffersize,
			  &red_index, &green_index, &blue_index, &alpha_index))
	return NULL;

	if(buffersize < (self->width * self->height * 4))
	{
		PyErr_Format(PyExc_Exception,"Image.copy_argb_to_buffer buffer is not long enough: is %i, should be %i", buffersize, self->width * self->height * 4);
		return NULL;
	}

	write32to32(self->image_data, buffer, self->width, self->height, red_index, green_index, blue_index, alpha_index);
	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject * pykaplot_image_get_width(PyKaplotImage *self, void *closure)
{
	return PyInt_FromLong(self->width);
}

static PyObject * pykaplot_image_get_height(PyKaplotImage *self, void *closure)
{
	return PyInt_FromLong(self->height);
}

static PyObject*
PyPal2Rgb(PyObject* self, PyObject *args)
{
	PyObject *result = NULL;
	PyObject *image = NULL;
	PyObject *paletteObject = NULL;
	PyArrayObject *imageArray;
	int width, height;
	unsigned int palette[256];
	unsigned int r, g, b;
	unsigned int* buffer;
    int buffersize;
    double* imageData;
    double datamin, datamax;
    int i, x, y, index;

	if(PyArg_ParseTuple(args, "OOw#:contour", &image, &paletteObject, &buffer, &buffersize))
	{
		//imageArray = NA_InputArray(image, tFloat64, C_ARRAY);
		imageArray = (PyArrayObject*)PyArray_FromAny(image, PyArray_DescrFromType(NPY_FLOAT64), 2, 2, NPY_ARRAY_C_CONTIGUOUS, NULL);
		if(imageArray == NULL)
			return PyErr_Format(PyExc_TypeError, "can't convert image data into numpy");
		if(imageArray->nd != 2)
			return PyErr_Format(PyExc_TypeError, "data isn't 2 dimensional");
		imageData = (double*)PyArray_DATA(imageArray);
		width = imageArray->dimensions[1];
		height = imageArray->dimensions[0];
		if(width*height*3 != buffersize)
			return PyErr_Format(PyExc_TypeError, "buffersize isn't width*height*3(%i) bytes long(but %i)", width*height*3, buffersize);
		paletteObject = PySequence_Fast(paletteObject, "palette must be a sequence");
		if(paletteObject)
		{
			if(PySequence_Fast_GET_SIZE(paletteObject) != 256*3)
			{
				PyErr_Format(PyExc_ValueError, "palette must be a sequence of length 256*3(it is of length: %i)", PySequence_Fast_GET_SIZE(paletteObject));
			}
			else
			{
				for(i = 0; i < 256; i++)
				{
					r = PyInt_AsLong(PySequence_Fast_GET_ITEM(paletteObject, i*3+0));
					g = PyInt_AsLong(PySequence_Fast_GET_ITEM(paletteObject, i*3+1));
					b = PyInt_AsLong(PySequence_Fast_GET_ITEM(paletteObject, i*3+2));
					palette[i] = (r<<16) + (g<< 8) + b;
				}
				datamin = imageData[0];
				datamax = imageData[0];
				for(y = 0; y < height; y++)
				{
					for(x = 0; x < width; x++)
					{
						if(imageData[x+y*width] < datamin)
							datamin = imageData[x+y*width];
						if(imageData[x+y*width] > datamax)
							datamax = imageData[x+y*width];
					}
				}
				for(y = 0; y < height; y++)
				{
					for(x = 0; x < width; x++)
					{
						index = (int)((imageData[x+y*width] - datamin) / (datamax - datamin) * 255.0);
						//buffer[x+y*width] = palette[index];
						((char*)buffer)[(x+y*width)*3+2] = (palette[index]) & 255;
						((char*)buffer)[(x+y*width)*3+1] = (palette[index]>>8) & 255;
						((char*)buffer)[(x+y*width)*3+0] = (palette[index]>>16) & 255;
					}
				}
				Py_INCREF(Py_None);
        		result = Py_None;
			}
		}
	}
	return result;
}

static PyMethodDef pykaplot_image_methods[] = {
    { "get_rgb_string", (PyCFunction)pykaplot_image_get_rgb_string, METH_VARARGS, "docstring!" },
    { "get_argb_string", (PyCFunction)pykaplot_image_get_argb_string, METH_VARARGS },
    { "set_rgb_string", (PyCFunction)pykaplot_image_set_rgb_string, METH_VARARGS },
    { "set_argb_string", (PyCFunction)pykaplot_image_set_argb_string, METH_VARARGS },
    { "write_rgb_to_buffer", (PyCFunction)pykaplot_image_write_rgb_to_buffer, METH_VARARGS },
    { "write_argb_to_buffer", (PyCFunction)pykaplot_image_write_argb_to_buffer, METH_VARARGS },
    { NULL, NULL, 0 }
};

static PyGetSetDef pykaplot_image_getseters[] = {
    {"width", (getter)pykaplot_image_get_width, NULL, "width of image",  NULL},
    {"height", (getter)pykaplot_image_get_height, NULL, "height of image",  NULL},
    {NULL}  /* Sentinel */
};

static PyMethodDef pykaplot_image_functions[] = {
	{"pal2rgb", (PyCFunction)PyPal2Rgb, METH_VARARGS, "makes a rgb image from a palette image"},
    { NULL, NULL, 0 }
};

PyTypeObject PyKaplotImage_Type = {
    PyObject_HEAD_INIT(NULL)
    0,                                  /* ob_size */
    "kaplot.cext.Image",                    /* tp_name */
    sizeof(PyKaplotImage),             /* tp_basicsize */
    0,                                  /* tp_itemsize */
    /* methods */
    (destructor)pykaplot_image_dealloc, /* tp_dealloc */
    (printfunc)0,                       /* tp_print */
    (getattrfunc)0,                     /* tp_getattr */
    (setattrfunc)0,                     /* tp_setattr */
    (cmpfunc)0,                         /* tp_compare */
    (reprfunc)0,                        /* tp_repr */
    0,                                  /* tp_as_number */
    0,                                  /* tp_as_sequence */
    0,                                  /* tp_as_mapping */
    (hashfunc)0,                        /* tp_hash */
    (ternaryfunc)0,                     /* tp_call */
    (reprfunc)0,                        /* tp_str */
    (getattrofunc)0,                    /* tp_getattro */
    (setattrofunc)0,                    /* tp_setattro */
    0,                                  /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT,                 /* tp_flags */
    NULL, /* Documentation string */
    (traverseproc)0,                    /* tp_traverse */
    (inquiry)0,                         /* tp_clear */
    (richcmpfunc)0,                     /* tp_richcompare */
    0,                                  /* tp_weaklistoffset */
    (getiterfunc)0,                     /* tp_iter */
    (iternextfunc)0,                    /* tp_iternext */
    pykaplot_image_methods,            /* tp_methods */
    0,                                  /* tp_members */
    pykaplot_image_getseters,              /* tp_getset */
    (PyTypeObject *)0,                  /* tp_base */
    (PyObject *)0,                      /* tp_dict */
    0,                                  /* tp_descr_get */
    0,                                  /* tp_descr_set */
    0,                                  /* tp_dictoffset */
    (initproc)pykaplot_image_init,                        /* tp_init */
    (allocfunc)0,                       /* tp_alloc */
    (newfunc)0,                         /* tp_new */
    (freefunc)0,                        /* tp_free */
    (inquiry)0,                         /* tp_is_gc */
    (PyObject *)0,                      /* tp_bases */
};

#define INIT_TYPE(tp) \
    if (!tp.ob_type) tp.ob_type = &PyType_Type; \
    if (!tp.tp_alloc) tp.tp_alloc = PyType_GenericAlloc; \
    if (!tp.tp_new) tp.tp_new = PyType_GenericNew; \
    if (PyType_Ready(&tp) < 0) \
        return;

PyMODINIT_FUNC
init_image(void)
{
	PyObject *mod;
	//PyObject *c_api_object;

	//import_libnumarray();
	import_array();

	mod = Py_InitModule("kaplot.cext._image", pykaplot_image_functions);
	INIT_TYPE(PyKaplotImage_Type);
	PyModule_AddObject(mod, "Image",  (PyObject *)&PyKaplotImage_Type);

	//PyKaplotFont_API[0] = (void *)PyKaplot_Font_Outline;
	//c_api_object = PyCObject_FromVoidPtr((void *)&api, NULL);
	//if (c_api_object != NULL)
	//	PyModule_AddObject(mod, "_C_API", c_api_object);
}

