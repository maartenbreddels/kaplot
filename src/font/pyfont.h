#include <Python.h>
#include <ft2build.h>
#include FT_FREETYPE_H
#include FT_OUTLINE_H

extern PyTypeObject PyFont_Type;

typedef struct _font_callback {
	void (*move_to)(double, double, void* userdata);
	void (*line_to)(double, double, void* userdata);
	void (*conic_to)(double, double, double, double, void* userdata); /* if set to NULL, cubic_to will be called */
	void (*cubic_to)(double, double, double, double, double, double, void* userdata);
} font_callback_t;

typedef struct {
    PyObject_HEAD
    FT_Library ft_library;
    FT_Face face;
    char* filename;
} PyFont;

typedef struct _PyKaplotFont_API {
	 void (*_PyKaplot_Font_Outline)(PyFont *font, Py_UNICODE* string, int length, 
		int xx, int xy, int yx, int yy, int tx, int ty, font_callback_t *callback, void* userdata);
	PyTypeObject *_PyFont_Type;
	
} PyKaplotFont_API_t;

#ifdef KAPLOT_FONT_MODULE

void PyKaplot_Font_Outline(PyFont *font, Py_UNICODE* string, int length, 
	int xx, int xy, int yx, int yy, int tx, int ty, font_callback_t *callback, void* userdata);

#else

static PyKaplotFont_API_t *PyKaplotFont_API;

#define PyKaplot_Font_Outline (PyKaplotFont_API->_PyKaplot_Font_Outline)
#define PyFont_Type (PyKaplotFont_API->_PyFont_Type)

#define ___PyKaplot_Font_Outline \
 (*(void (*)(PyFont *font, Py_UNICODE* string, int length, \
	int xx, int xy, int yx, int yy, int tx, int ty, font_callback_t *callback, void* userdata)) PyKaplotFont_API[0]) 

static int
import_kaplot_font(void)
{
    PyObject *module = PyImport_ImportModule("kaplot.cext._pyfont");

    if (module != NULL) {
        PyObject *c_api_object = PyObject_GetAttrString(module, "_C_API");
        if (c_api_object == NULL)
            return -1;
        if (PyCObject_Check(c_api_object))
            PyKaplotFont_API = (PyKaplotFont_API_t*)PyCObject_AsVoidPtr(c_api_object);
        Py_DECREF(c_api_object);
    }
    else
    {
    	 return -1;
    }

    return 0;
}


#endif


