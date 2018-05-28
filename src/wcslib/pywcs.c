#include "pywcs.h"
#include <Python.h>
#include <wcs.h>

static void
Wcs_dealloc(PyWcsObject* self)
{
	/*if(self->image_buffer != NULL)
		free(self->image_buffer);
	gsapi_exit(self->gs_instance);
	gsapi_delete_instance(self->gs_instance);*/
	wcsfree(self->wcs);
	free(self->wcs);
    self->ob_type->tp_free((PyObject*)self);
}

static int
Wcs_init(PyWcsObject *self, PyObject *args, PyObject *kwds)
{
	double crval1, crval2;
	double crpix1, crpix2;
	double cdelt1, cdelt2;
	double crota1, crota2;
	double pcmatrix[4];
	double cdmatrix[4];
	char *ctype1, *ctype2;
	int result;
	int i;
	int altlin;

	PyObject* pvlist;
	int pvlistCount;
	pvlist = NULL;
	if(!PyArg_ParseTuple(args, "(dd)(ss)(dddd)(dd)(dd)(dd)(dddd)i|O", &crval1, &crval2, &ctype1, &ctype2, \
			&pcmatrix[0], &pcmatrix[1], &pcmatrix[2], &pcmatrix[3], &cdelt1, &cdelt2, &crpix1, &crpix2, &crota1, &crota2,
			&cdmatrix[0], &cdmatrix[1], &cdmatrix[2], &cdmatrix[3], &altlin, &pvlist))
		return -1;

	self->wcs = (struct wcsprm*)malloc(sizeof(struct wcsprm));
	result = wcsini(1, 2, self->wcs);
	if(result != 0)
	{
		PyErr_Format(PyExc_Exception, "Error allocating wcs struct, (%s)", wcs_errmsg[result]);
		return -1;
	}
	// TODO, read wcs.h, if pcmatrix presents, crota and cdelt aren't needed

	self->wcs->altlin = altlin; // flags, PC matrix present etc..
	self->wcs->naxis = 2;
	self->wcs->crpix[0] = crpix1;
	self->wcs->crpix[1] = crpix2;
	self->wcs->pc[0] = pcmatrix[0];
	self->wcs->pc[1] = pcmatrix[1];
	self->wcs->pc[2] = pcmatrix[2];
	self->wcs->pc[3] = pcmatrix[3];
	self->wcs->cd[0] = cdmatrix[0];
	self->wcs->cd[1] = cdmatrix[1];
	self->wcs->cd[2] = cdmatrix[2];
	self->wcs->cd[3] = cdmatrix[3];
	self->wcs->cdelt[0] = cdelt1;
	self->wcs->cdelt[1] = cdelt2;
	self->wcs->crota[0] = crota1;
	self->wcs->crota[1] = crota2;
	//printf("########### crota: %f %f\n", crota1, crota2);
	strncpy(self->wcs->ctype[0], ctype1, 9);
	strncpy(self->wcs->ctype[1], ctype2, 9);

	self->wcs->crval[0] = crval1;
	self->wcs->crval[1] = crval2;
	self->wcs->lonpole = 999.0;
	self->wcs->latpole = 999.0;

	if(pvlist != NULL)
	{
		if(!PySequence_Check(pvlist))
		{
			PyErr_SetString(PyExc_TypeError, "pvlist must be a sequence");
			return -1;
		}
		pvlistCount = PySequence_Length(pvlist);
		for(i = 0; i < pvlistCount; i++)
		{
			PyObject* pv;
			int i_, m;
			double value;

			pv = PySequence_GetItem(pvlist, i);
			if(!PyArg_ParseTuple(pv, "iid", &i_, &m, &value))
				return -1;
			self->wcs->pv[i].i = i_;
			self->wcs->pv[i].m = m;
			self->wcs->pv[i].value = value;
		}
		self->wcs->npv = pvlistCount;
	}

	result = wcsset(self->wcs);
	if(result != 0)
	{
		PyErr_Format(PyExc_Exception, "Error initialising wcs struct, (%s)", wcs_errmsg[result]);
		return -1;
	}
	/*if(!PySequence_Check(optionsList))
	{
		PyErr_SetString(PyExc_TypeError, "options must be a list");
		return -1;
	}*/
	return 0;
}

static PyObject*
Wcs_to_pixel(PyWcsObject *self, PyObject *args)
{
	int result;
	double pixcrd[2];
	double imgcrd[2];
	double phi[1], theta[1];
	double world[2];
	int stat[1];
    if (!PyArg_ParseTuple(args, "dd:Wcs.to_pixel", &world[0], &world[1]))
		return NULL;

	result = 0;
	result = wcss2p(self->wcs, 1, 2, world, phi, theta, imgcrd, pixcrd, stat);
	/*if(result != 0)
	{
		PyErr_Format(PyExc_Exception, "wcs forward error(%s)", wcs_errmsg[result]);
		return NULL;
	}*/
	if(result != 0)
	{
		Py_INCREF(Py_None);
		return Py_None;
	}
	else
	{
		return Py_BuildValue("(dd)", pixcrd[0], pixcrd[1]);
	}
}

static PyObject*
Wcs_from_pixel(PyWcsObject *self, PyObject *args)
{
	int result;
	double pixcrd[2];
	double imgcrd[2];
	double phi[1], theta[1];
	double world[2];
	int stat[1];
    if (!PyArg_ParseTuple(args, "dd:Wcs.from_pixel", &pixcrd[0], &pixcrd[1]))
		return NULL;

	result = 0;
	result = wcsp2s(self->wcs, 1, 2, pixcrd, imgcrd, phi, theta, world, stat);
	//printf("reverse done");
	/*if(result != 0)
	{
		PyErr_Format(PyExc_Exception, "wcs reverse error(%s)", wcs_errmsg[result]);
		return NULL;
	}*/
	if(result != 0)
	{
		Py_INCREF(Py_None);
		return Py_None;
	}
	else
	{
		return Py_BuildValue("(dd)", world[0], world[1]);
	}
}
static PyObject*
Wcs_print(PyWcsObject *self, PyObject *args)
{
	wcsprt(self->wcs);
	Py_INCREF(Py_None);
	return Py_None;
}

static PyMethodDef Wcs_methods[] = {
    {"to_pixel", (PyCFunction)Wcs_to_pixel, METH_VARARGS, "world -> pixel"},
    {"from_pixel", (PyCFunction)Wcs_from_pixel, METH_VARARGS, "pixel -> world"},
    {"print_", (PyCFunction)Wcs_print, METH_VARARGS, "prints information about the projection to stdout"},
    /*{"begin", (PyCFunction)Ghostscript_begin, METH_VARARGS, "Execute string"},
    {"execute_continue", (PyCFunction)Ghostscript_execute_continue, METH_VARARGS, "Execute string"},
    {"end", (PyCFunction)Ghostscript_end, METH_VARARGS, "Execute string"},
    {"lines", (PyCFunction)Ghostscript_lines, METH_VARARGS, "sets a path"},
    { "get_rgb_string", (PyCFunction)Ghostscript_get_rgb_string, METH_VARARGS },
    { "get_argb_string", (PyCFunction)Ghostscript_get_argb_string, METH_VARARGS },*/
    {NULL}  /* Sentinel */
};

static PyObject*
PyWcs_get_simplezen(PyWcsObject *self, void *closure)
{
	PyObject* result = self->wcs->cel.prj.simplezen ? Py_True : Py_False;
	Py_INCREF(result);
	return result;
}

static PyObject*
PyWcs_get_equiareal(PyWcsObject *self, void *closure)
{
	PyObject* result = self->wcs->cel.prj.equiareal ? Py_True : Py_False;
	Py_INCREF(result);
	return result;
}

static PyObject*
PyWcs_get_conformal(PyWcsObject *self, void *closure)
{
	PyObject* result = self->wcs->cel.prj.conformal ? Py_True : Py_False;
	Py_INCREF(result);
	return result;
}

static PyObject*
PyWcs_get_global(PyWcsObject *self, void *closure)
{
	PyObject* result = self->wcs->cel.prj.global ? Py_True : Py_False;
	Py_INCREF(result);
	return result;
}

static PyObject*
PyWcs_get_divergent(PyWcsObject *self, void *closure)
{
	PyObject* result = self->wcs->cel.prj.divergent ? Py_True : Py_False;
	Py_INCREF(result);
	return result;
}

static PyObject*
PyWcs_get_name(PyWcsObject *self, void *closure)
{
	return PyString_FromString(self->wcs->cel.prj.name);
}

static PyObject*
PyWcs_get_code(PyWcsObject *self, void *closure)
{
	return PyString_FromString(self->wcs->cel.prj.code);
}

static PyObject*
PyWcs_get_category(PyWcsObject *self, void *closure)
{
	return PyString_FromString(prj_categories[self->wcs->cel.prj.category]);
}


/* doc string taken from wcslib source */
static PyGetSetDef Wcs_getseters[] = {
    {"simplezen",	(getter)PyWcs_get_simplezen, NULL, "True is the projection is a simple zenithal projection",  NULL},
    {"equiareal",	(getter)PyWcs_get_equiareal, NULL, "True is the projection is equal area",  NULL},
    {"conformal",	(getter)PyWcs_get_conformal, NULL, "True is the projection is conformal",  NULL},
    {"global",		(getter)PyWcs_get_global, NULL, "True is the projection can represent the whole sphere in a finite, non-overlapped mapping",  NULL},
    {"divergent",	(getter)PyWcs_get_divergent, NULL, "True is the projection diverges in latitude",  NULL},
    {"name",	(getter)PyWcs_get_name, NULL, "Name of the projection",  NULL},
    {"category",	(getter)PyWcs_get_category, NULL, "Name of the projection category",  NULL},
    {"code",	(getter)PyWcs_get_code, NULL, "The 3 letter projection code",  NULL},
    /*{"width", (getter)Ghostscript_get_width, NULL, "width of image",  NULL},
    {"height", (getter)Ghostscript_get_height, NULL, "height of image",  NULL},*/
    {NULL}
};

PyTypeObject PyWcs_Type = {
    PyObject_HEAD_INIT(NULL)
    0,                         /*ob_size*/
    "wcs.Wcs",             /*tp_name*/
    sizeof(PyWcsObject), /*tp_basicsize*/
    0,                         /*tp_itemsize*/
    (destructor)Wcs_dealloc,       /*tp_dealloc*/
    0,                         /*tp_print*/
    0,                         /*tp_getattr*/
    0,                         /*tp_setattr*/
    0,                         /*tp_compare*/
    0,                         /*tp_repr*/
    0,                         /*tp_as_number*/
    0,                         /*tp_as_sequence*/
    0,                         /*tp_as_mapping*/
    0,                         /*tp_hash */
    0,                         /*tp_call*/
    0,                         /*tp_str*/
    0,                         /*tp_getattro*/
    0,                         /*tp_setattro*/
    0,                         /*tp_as_buffer*/
    Py_TPFLAGS_DEFAULT,        /*tp_flags*/
    "Wcs objects",           /* tp_doc */
    0,		               /* tp_traverse */
    0,		               /* tp_clear */
    0,		               /* tp_richcompare */
    0,		               /* tp_weaklistoffset */
    0,		               /* tp_iter */
    0,		               /* tp_iternext */
    Wcs_methods,             /* tp_methods */
    0,           	  /* tp_members */
    Wcs_getseters,                         /* tp_getset */
    0,                         /* tp_base */
    0,                         /* tp_dict */
    0,                         /* tp_descr_get */
    0,                         /* tp_descr_set */
    0,                         /* tp_dictoffset */
    (initproc)Wcs_init,      /* tp_init */
    0,                         /* tp_alloc */
    0,                 /* tp_new */
};
