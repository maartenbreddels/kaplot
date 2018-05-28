#define KAPLOT_FONT_MODULE
#include "pyfont.h"
#include "cinterface.h"

#define F26_6_TO_D(x) (((double)x)/(1<<6))
#define D_TO_F26_6(x) ((int)(x*(1<<6)))

static int
pyfont_init(PyFont *self, PyObject *args, PyObject *kwargs)
{
	char* filename;
	int error;

    if (!PyArg_ParseTuple(args, "s:PyFont.__init__", &filename))
    {
	    PyErr_SetString(PyExc_TypeError,"PyFont.__init__ takes 1 arguments");
		return -1;
	}
	self->face = NULL;
	self->ft_library = NULL;
	error = FT_Init_FreeType(&self->ft_library);
	if(error)
	{
	    PyErr_SetString(PyExc_TypeError,"Can't initialise FreeType2");
		return -1;
	}
	error = FT_New_Face(self->ft_library, filename, 0, &self->face);
	if(self->face == NULL)
	{
	    PyErr_Format(PyExc_Exception, "Can't load font: %s", filename);
		return -1;
	}


	return 0;
}
static void
pyfont_dealloc(PyFont *self)
{
    if (self->ob_type->tp_free)
		self->ob_type->tp_free((PyObject *)self);
    else
		PyObject_Del(self);
}

typedef struct _outline_info_t {
	kaplot_cinterface_t *cinterface;
	double lx, ly;
} outline_info_t;


static int
_cinterface_move_to (FT_Vector *to, void *closure)
{
	outline_info_t *info = (outline_info_t*)closure;
	kaplot_cinterface_t *cinterface = info->cinterface;
	info->lx = to->x / 64.0;
	info->ly = to->y / 64.0;
	//printf("m %i %i\n",  to->x, to->y);
	return cinterface->move_to(cinterface, to->x/64.0, to->y/64.0) != 1;
}

static int
_cinterface_line_to (FT_Vector *to, void *closure)
{
	outline_info_t *info = (outline_info_t*)closure;
	kaplot_cinterface_t *cinterface = info->cinterface;
	info->lx = to->x / 64.0;
	info->ly = to->y / 64.0;
	return cinterface->line_to(cinterface, to->x/64.0, to->y/64.0) != 1;
}

static int
_cinterface_conic_to (FT_Vector *control, FT_Vector *to, void *closure)
{
	int result;
	outline_info_t *info = (outline_info_t*)closure;
	kaplot_cinterface_t *cinterface = info->cinterface;
	result = cinterface->curve_to(cinterface, info->lx + 2.0/3.0*(control->x/64.0 - info->lx),
											info->ly + 2.0/3.0*(control->y/64.0 - info->ly),
											to->x/64.0 + 2.0/3.0*(control->x/64.0 - to->x/64.0),
											to->y/64.0 + 2.0/3.0*(control->y/64.0 - to->y/64.0),
											to->x/64.0,
											to->y/64.0) != 1;
	info->lx = to->x / 64.0;
	info->ly = to->y / 64.0;
	return result;
}

static int
_cinterface_cubic_to (FT_Vector *control1, FT_Vector *control2, FT_Vector *to, void *closure)
{
	outline_info_t *info = (outline_info_t*)closure;
	kaplot_cinterface_t *cinterface = info->cinterface;
	info->lx = to->x / 64.0;
	info->ly = to->y / 64.0;
	return cinterface->curve_to(cinterface, control1->x/64.0, control1->y/64.0, control2->x/64.0, control2->y/64.0, to->x/64.0, to->y/64.0) != 1;
}


static FT_Outline_Funcs cinterface_outline_funcs = {
	_cinterface_move_to,
	_cinterface_line_to,
	_cinterface_conic_to,
	_cinterface_cubic_to,
	0, /* shift */
	0, /* delta */
};


int drawMissingGlyph(PyObject *missingGlyphCallable, PyObject *missingGlyphArgs,
		Py_UNICODE unichar, FT_Int32 load_flags, FT_Matrix *matrix, int tx, int ty,
		int* new_tx, int* new_ty, char** otherFontName)
{
	PyObject *arglist;
    PyObject *result;
    Py_UNICODE unistring[2];
    PyObject* unicodeObject;

	unistring[0] = unichar;
	unistring[1] = 0;
	unicodeObject = PyUnicode_FromUnicode(unistring, 1) ;

	arglist = Py_BuildValue("(OOiiiiiii)", missingGlyphArgs, unicodeObject,
				matrix->xx, matrix->xy,
				matrix->yx, matrix->yy, tx, ty, load_flags);
	result = PyEval_CallObject(missingGlyphCallable, arglist);
	Py_DECREF(arglist);
	Py_DECREF(unicodeObject);
	if(result != NULL && result != Py_None &&
			PyArg_ParseTuple(result, "(ii)s", new_tx, new_ty, otherFontName))
	{
		Py_XDECREF(result);
		return 1;
	}
	else
	{
		Py_XDECREF(result);
		return 0;
	}
}

static PyObject *
pyfont_draw_path(PyFont *self, PyObject *args)
{
	Py_UNICODE* string;
	int length;
	int i, error;
	int glyph_index;
	FT_GlyphSlot glyph;
	FT_Int32 load_flags = FT_LOAD_DEFAULT;
	PyObject *cinterface_object;
	kaplot_cinterface_t *cinterface;
	outline_info_t outline_info;
	PyObject *ptype, *pvalue, *ptraceback;
	PyObject *missingGlyphCallable = NULL;
	PyObject *missingGlyphArgs = NULL;
	FT_Matrix matrix;
	char *otherFontName;
	long int a,b,c,d;

	long int tx0=0, ty0=0;
	long int tx, ty;
	long int advance_x, advance_y;

	glyph = self->face->glyph;
	matrix.xx = 1<<16;
	matrix.xy = 0;
	matrix.yx = 0;
	matrix.yy = 1<<16;

    /*
	if (!PyArg_ParseTuple(args, "u#O!|iiiiiiiOO:PyFont.draw_path", &string, &length,
    		 &PyCObject_Type, &cinterface_object,
    		 &matrix.xx, &matrix.xy, &matrix.yx, &matrix.yy, &tx0, &ty0,
    		 &load_flags, &missingGlyphCallable, &missingGlyphArgs))
		return NULL;
	/*/
    if (!PyArg_ParseTuple(args, "u#O!|lllliiiOO:PyFont.draw_path", &string, &length,
    		 &PyCObject_Type, &cinterface_object,
    		 &a, &b, &c, &d, &tx0, &ty0,
    		 &load_flags, &missingGlyphCallable, &missingGlyphArgs))
		return NULL;
	//printf("abcd, %li %li %li %li\n", a, b, c, d);
	/**/
	//length = strlen(string);

	//printf("sizes %li %li %li", sizeof(int), sizeof(FT_Pos), sizeof(long long));
	tx = tx0;
	ty = ty0;
	matrix.xx = a;
	matrix.xy = b;
	matrix.yx = c;
	matrix.yy = d;
	//printf("lenght=%i\n", length);
	//printf("[[% 10li % 10li] [% 10li % 10li]] % 10li % 10li\n", matrix.xx, matrix.xy, matrix.yx, matrix.yy, tx0, ty0);
	cinterface = PyCObject_AsVoidPtr(cinterface_object);
	outline_info.cinterface = cinterface;
	outline_info.lx = 0;
	outline_info.ly = 0;

	for(i = 0; i < length; i++)
	{
		//printf("char index: %c/%i/0x%x\n", (char)(string[i]), (FT_ULong)(string[i]), (FT_ULong)(string[i]));
		glyph_index = FT_Get_Char_Index(self->face, (FT_ULong)string[i]);
		advance_x = 0;
		advance_y = 0;
		error = 0;
		/*if(glyph_index == 0 && missingGlyphCallable != NULL && missingGlyphArgs != NULL &&
				drawMissingGlyph(missingGlyphCallable, missingGlyphArgs,
					string[i], load_flags, &matrix, tx, ty, &tx,
					&ty, &otherFontName))
		{
			//printf("glyph for character %c/%i/0x%x in font '%s' substituted with glyph from font '%s'\n",
			//		string[i], string[i], string[i], self->face->family_name, otherFontName);
			//Py_DECREF(otherFontName);
		}
		else*/
		{
			if(glyph_index == 0)
			{
				//printf("glyph for character %c/%i/0x%x in font '%s' not found",
				//	string[i], string[i], string[i], self->face->family_name);
				glyph_index = FT_Get_Char_Index(self->face, (FT_ULong)'?');
			}
			error = FT_Load_Glyph(self->face, glyph_index, load_flags);
			if(error)
			{
				printf("error loading glyph for char: %c, error %i/0x%x\n", string[i], error, error);
			}
			else
			{
				FT_Outline_Transform(&glyph->outline, &matrix);
				FT_Outline_Translate(&glyph->outline, tx, ty);
				FT_Outline_Decompose(&glyph->outline, &cinterface_outline_funcs, &outline_info);
				/* kerning support would be nice */
				advance_x = glyph->advance.x;
				advance_y = glyph->advance.y;
			}
			tx += 	(int)(
						(((double)advance_x) / (1<<6) * ((double)matrix.xx) / (1<<16) +
						((double)advance_y)  / (1<<6) * ((double)matrix.xy) / (1<<16)) * (1<<6)
						);
			ty += 	(int)(
						(((double)advance_x) / (1<<6) * ((double)matrix.yx) / (1<<16) +
						((double)advance_y)  / (1<<6) * ((double)matrix.yy) / (1<<16)) * (1<<6)
						);
			//printf("x,y = % 10i, % 10i\n", tx, ty);
		}
	}
	if(PyErr_Occurred())
	{
		PyErr_Fetch(&ptype, &pvalue, &ptraceback);
		PyErr_Restore(ptype, pvalue, ptraceback);
		return NULL;
	}
	else
	{
		//Py_INCREF(Py_None);
		return Py_BuildValue("ii", tx-tx0, ty-ty0);
	}
}

void PyKaplot_Font_Outline(PyFont *font, Py_UNICODE* string, int length,
	int xx, int xy, int yx, int yy, int tx, int ty, font_callback_t *callback, void* userdata)
{
	printf("PyKaplot_Font_Outline\n");
}

static PyObject *
pyfont_set_char_size(PyFont *self, PyObject *args)
{
	int width;
	int height;

    if (!PyArg_ParseTuple(args, "ii:PyFont.set_char_size", &width, &height))
		return NULL;
	FT_Set_Char_Size(self->face, width, height, 0,0);
	Py_INCREF(Py_None);
	return Py_None;
}

int getMissingGlyphTextMetrics(PyObject *missingGlyphCallable, PyObject *missingGlyphArgs,
		Py_UNICODE unichar, FT_Int32 load_flags,
		int* width, int* height, int* advance,
		int* bearingx, int* bearingy, char** otherFontName)
{
	PyObject *arglist;
    PyObject *result;
    Py_UNICODE unistring[2];
    PyObject* unicodeObject;
    double fwidth, fheight, fadvance, fbearingx, fbearingy;

	unistring[0] = unichar;
	unistring[1] = 0;
	unicodeObject = PyUnicode_FromUnicode(unistring, 1) ;

	arglist = Py_BuildValue("(OOi)", missingGlyphArgs, unicodeObject, load_flags);
	result = PyEval_CallObject(missingGlyphCallable, arglist);
	Py_DECREF(arglist);
	Py_DECREF(unicodeObject);
	if(result != NULL && result != Py_None &&
		//#PyArg_ParseTuple(result, "(ddddd)s", &fwidth, &fheight, &fadvance, &fbearingx, &fbearingy, otherFontName))
		PyArg_ParseTuple(result, "(iiiii)s", width, height, advance, bearingx, bearingy, otherFontName))
	{
		/*printf("%f %f %f %f %f\n", fwidth, fheight, fadvance, fbearingx, fbearingy);
		*width = D_TO_F26_6(fwidth);
		*height = D_TO_F26_6(fheight);
		*advance = D_TO_F26_6(fadvance);
		*bearingx = D_TO_F26_6(fbearingx);
		*bearingy = D_TO_F26_6(fbearingy);*/
		Py_XDECREF(result);
		return 1;
	}
	else
	{
		Py_XDECREF(result);
		return 0;
	}

}

static PyObject *
pyfont_get_text_metrics(PyFont *self, PyObject *args)
{
	Py_UNICODE* string;
	PyObject *missingGlyphCallable = NULL;
	PyObject *missingGlyphArgs = NULL;
	int length;
	int i, error;
	int glyph_index;
	FT_Int32 load_flags = FT_LOAD_DEFAULT;
	FT_GlyphSlot glyph;
	int other_width=0;
	int other_height=0;
	int other_advance=0;
	int other_bearingx=0;
	int other_bearingy=0;

	char* otherFontName;

	int width=0;
	int height=0;
	int advance=0;
	int bearingx=0;
	int bearingy=0;
	int leftoverx=0; // the part between the last glyph and the last advance point
	int ymin=0;
	int ymax=0;
	int floating=1;
	glyph = self->face->glyph;

    if (!PyArg_ParseTuple(args, "u#|iiOO:PyFont.get_text_metrics", &string,
    		&length, &load_flags, &floating, &missingGlyphCallable, &missingGlyphArgs))
		return NULL;
	if(length == 0)
	{
		PyErr_SetString(PyExc_Exception, "length of string should be >= 1");
		return NULL;
	}

#define MAX(a, b) (((a) > (b)) ? (a) : (b))
#define MIN(a, b) (((a) < (b)) ? (a) : (b))
	for(i = 0; i < length; i++)
	{
		glyph_index = FT_Get_Char_Index(self->face, (FT_ULong)string[i]);

		if(glyph_index == 0 && missingGlyphCallable &&
			 getMissingGlyphTextMetrics(missingGlyphCallable,
					missingGlyphArgs, string[i], load_flags,
					&other_width, &other_height, &other_advance,
					&other_bearingx, &other_bearingy, &otherFontName ))
		{
			//printf("glyph for character %c/%i/0x%x in font '%s' substituted with glyph from font '%s'\n",
			//		string[i], string[i], string[i], self->face->family_name, otherFontName);
			//printf("%i %i %i %i %i\n", other_width, other_height, other_advance,
			//	other_bearingx, other_bearingy);
			advance += other_advance;
			bearingy = MAX(bearingy, other_bearingy);
			ymax = bearingy;
			ymin = MIN(ymin, -(other_height - other_bearingy));
			if(i == 0)
			{
				bearingx = other_bearingx;
			}
			if(i == (length - 1))
			{
				leftoverx = other_advance - other_bearingx - other_width;
			}
		}
		else
		{
			if(glyph_index == 0)
			{
				printf("glyph for character %c/%i/0x%x not found", string[i], string[i], string[i]);
				glyph_index = FT_Get_Char_Index(self->face, (FT_ULong)'?');
			}
			error = FT_Load_Glyph(self->face, glyph_index, load_flags);
			if(error)
			{
				printf("error loading glyph for char: %c, error %i/0x%x\n", string[i], error, error);
			}
			else
			{
				advance += glyph->metrics.horiAdvance;
				bearingy = MAX(bearingy, glyph->metrics.horiBearingY);
				ymax = bearingy;
				ymin = MIN(ymin, -(glyph->metrics.height - bearingy));

				if(i == 0)
				{
					bearingx = glyph->metrics.horiBearingX;
				}
				if(i == (length - 1))
				{
					leftoverx = glyph->metrics.horiAdvance-glyph->metrics.horiBearingX-glyph->metrics.width;
				}
				/* kerning support would be nice */
			}
		}
	}
	width = advance - leftoverx - bearingx;
	height = ymax - ymin;
	//printf("% 10i % 10i % 10i % 10i % 10i\n", width, height ,advance, bearingx, bearingy);
	if(floating)
	return Py_BuildValue("ddddd",	F26_6_TO_D(width),		F26_6_TO_D(height),
									F26_6_TO_D(advance),	F26_6_TO_D(bearingx),
									F26_6_TO_D(bearingy));
	else
	return Py_BuildValue("iiiii",	(width),	(height),
									(advance),	(bearingx),
									(bearingy));
}

static PyObject *
pyfont_has_char(PyFont *self, PyObject *args)
{
	Py_UNICODE* string;
	int length;
    if (!PyArg_ParseTuple(args, "u#|i:PyFont.has_char", &string, &length))
		return NULL;
	if(length != 1)
	{
		PyErr_Format(PyExc_Exception, "length of string should be 1, not %i", length);
		return NULL;
	}
	if(FT_Get_Char_Index(self->face, (FT_ULong)string[0]) == 0)
	{
		Py_INCREF(Py_False);
		return Py_False;
	}
	else
	{
		Py_INCREF(Py_True);
		return Py_True;
	}
}

static PyObject *
pyfont_get_ascender(PyFont *self, PyObject *args)
{
	//return PyFloat_FromDouble((double)self->face->size->metrics.ascender / (1<<6));
	return PyFloat_FromDouble(
		(
			(double)self->face->ascender
		)
		* ((double)self->face->size->metrics.y_ppem / (double)self->face->units_per_EM)
	);
}

static PyObject *
pyfont_get_descender(PyFont *self, PyObject *args)
{
	//return PyFloat_FromDouble((double)self->face->size->metrics.descender / (1<<6));
	return PyFloat_FromDouble(
		(
			(double)self->face->descender
		)
		* ((double)self->face->size->metrics.y_ppem / (double)self->face->units_per_EM)
	);
}

static PyObject *
pyfont_get_height(PyFont *self, PyObject *args)
{
	//return PyFloat_FromDouble(((double)self->face->size->metrics.height) / (1<<6));
	return PyFloat_FromDouble(
		(
			(double)self->face->height
		)
		* ((double)self->face->size->metrics.y_ppem / (double)self->face->units_per_EM)
	);
}

static PyObject *
pyfont_get_line_gap(PyFont *self, PyObject *args)
{
	/*return PyFloat_FromDouble((double)(
			self->face->size->metrics.height -
			self->face->size->metrics.ascender +
			self->face->size->metrics.descender
			) / (1<<6));*/
	return PyFloat_FromDouble(
		(
			(double)self->face->height
			-(double)self->face->ascender
			+(double)self->face->descender
		)
		* ((double)self->face->size->metrics.y_ppem / (double)self->face->units_per_EM)
	);
}

static PyObject *
pyfont_get_units_per_EM(PyFont *self, PyObject *args)
{
	return PyInt_FromLong(self->face->units_per_EM);
}

static PyObject *
pyfont_get_underline_position(PyFont *self, PyObject *args)
{
	return PyFloat_FromDouble(
		(double)self->face->underline_position
		* ((double)self->face->size->metrics.y_ppem / (double)self->face->units_per_EM)
	);
}

static PyObject *
pyfont_get_underline_thickness(PyFont *self, PyObject *args)
{
	return PyFloat_FromDouble(
		(double)self->face->underline_thickness
		* ((double)self->face->size->metrics.y_ppem / (double)self->face->units_per_EM)
	);
}


static PyObject *
pyfont_get_family_name(PyFont *self, PyObject *args)
{
	return PyString_FromString(self->face->family_name);
}

static PyObject *
pyfont_get_style_name(PyFont *self, PyObject *args)
{
	return PyString_FromString(self->face->style_name);
}

static PyObject *
pyfont_get_is_bold(PyFont *self, PyObject *args)
{
	return PyInt_FromLong(self->face->style_flags & FT_STYLE_FLAG_BOLD);
}

static PyObject *
pyfont_get_is_italic(PyFont *self, PyObject *args)
{
	return PyInt_FromLong(self->face->style_flags & FT_STYLE_FLAG_ITALIC);
}

static PyMethodDef pyfont_methods[] = {
    { "draw_path", (PyCFunction)pyfont_draw_path, METH_VARARGS },
    { "get_text_metrics", (PyCFunction)pyfont_get_text_metrics, METH_VARARGS },
    { "set_char_size", (PyCFunction)pyfont_set_char_size, METH_VARARGS },
    { "has_char", (PyCFunction)pyfont_has_char, METH_VARARGS },
    { NULL, NULL, 0 }
};

static PyGetSetDef pyfont_getseters[] = {
    {"ascender", (getter)pyfont_get_ascender, NULL, NULL, NULL},
    {"descender", (getter)pyfont_get_descender, NULL, NULL, NULL},
    {"height", (getter)pyfont_get_height, NULL, NULL, NULL},
    {"line_gap", (getter)pyfont_get_line_gap, NULL, NULL, NULL},
    {"units_per_EM", (getter)pyfont_get_units_per_EM, NULL, NULL, NULL},
    {"underline_position", (getter)pyfont_get_underline_position, NULL, NULL, NULL},
    {"underline_thickness", (getter)pyfont_get_underline_thickness, NULL, NULL, NULL},


    {"family_name", (getter)pyfont_get_family_name, NULL, NULL, NULL},
    {"style_name", (getter)pyfont_get_style_name, NULL, NULL, NULL},
    {"is_bold", (getter)pyfont_get_is_bold, NULL, NULL, NULL},
    {"is_italic", (getter)pyfont_get_is_italic, NULL, NULL, NULL},




    {NULL}  /* Sentinel */
};

static PyMethodDef pyfont_functions[] = {
    { NULL, NULL, 0 }
};



PyTypeObject PyFont_Type = {
    PyObject_HEAD_INIT(NULL)
    0,                                  /* ob_size */
    "kaplot.cext.PyFont",                    /* tp_name */
    sizeof(PyFont),             /* tp_basicsize */
    0,                                  /* tp_itemsize */
    /* methods */
    (destructor)pyfont_dealloc, /* tp_dealloc */
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
    pyfont_methods,            /* tp_methods */
    0,                                  /* tp_members */
    pyfont_getseters,              /* tp_getset */
    (PyTypeObject *)0,                  /* tp_base */
    (PyObject *)0,                      /* tp_dict */
    0,                                  /* tp_descr_get */
    0,                                  /* tp_descr_set */
    0,                                  /* tp_dictoffset */
    (initproc)pyfont_init,                        /* tp_init */
    (allocfunc)0,                       /* tp_alloc */
    (newfunc)0,                         /* tp_new */
    (freefunc)0,                        /* tp_free */
    (inquiry)0,                         /* tp_is_gc */
    (PyObject *)0,                      /* tp_bases */
};

//pyfont_functions

#define INIT_TYPE(tp) \
    if (!tp.ob_type) tp.ob_type = &PyType_Type; \
    if (!tp.tp_alloc) tp.tp_alloc = PyType_GenericAlloc; \
    if (!tp.tp_new) tp.tp_new = PyType_GenericNew; \
    if (PyType_Ready(&tp) < 0) \
        return;

static PyKaplotFont_API_t api = {
	PyKaplot_Font_Outline,
	&PyFont_Type
};


PyMODINIT_FUNC
init_pyfont(void)
{
	PyObject *mod;
	PyObject *c_api_object;

	mod = Py_InitModule("kaplot.cext._pyfont", pyfont_functions);
	INIT_TYPE(PyFont_Type);
	PyModule_AddObject(mod, "Font",  (PyObject *)&PyFont_Type);

#define CONSTANT(x) PyModule_AddIntConstant( mod , # x , x )
	CONSTANT(FT_LOAD_DEFAULT);
	CONSTANT(FT_LOAD_NO_SCALE);
	CONSTANT(FT_LOAD_NO_HINTING);
	CONSTANT(FT_LOAD_RENDER);
	CONSTANT(FT_LOAD_NO_BITMAP);
	CONSTANT(FT_LOAD_VERTICAL_LAYOUT);
	CONSTANT(FT_LOAD_FORCE_AUTOHINT);
	CONSTANT(FT_LOAD_CROP_BITMAP);
	CONSTANT(FT_LOAD_PEDANTIC);
	CONSTANT(FT_LOAD_IGNORE_GLOBAL_ADVANCE_WIDTH);
	CONSTANT(FT_LOAD_NO_RECURSE);
	CONSTANT(FT_LOAD_IGNORE_TRANSFORM);
	CONSTANT(FT_LOAD_MONOCHROME);
	CONSTANT(FT_LOAD_LINEAR_DESIGN);
#undef CONSTANT
	//PyKaplotFont_API[0] = (void *)PyKaplot_Font_Outline;
	c_api_object = PyCObject_FromVoidPtr((void *)&api, NULL);
	if (c_api_object != NULL)
		PyModule_AddObject(mod, "_C_API", c_api_object);
}

