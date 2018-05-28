
typedef void (*contour_callback)(long int*, float*, float*, float*, void*);

#ifdef KAPLOT_CONTOUR_MODULE

void _PyKaplot_Contour (float* data, int width, int height, int beginx, int endx, 
						int beginy, int endy, float* levels, int levelcount, 
						contour_callback callback, void*);

#else

static void **PyKaplotContour_API;

#define PyKaplot_Contour \
 (*(void (*)(float* data, int width, int height, int beginx, int endx, \
 	int beginy, int endy, float* levels, int levelcount, \
 	contour_callback callback, void*)) PyKaplotContour_API[0]) 

static int
import_kaplot_contour(void)
{
    PyObject *module = PyImport_ImportModule("kaplot.cext._contour");

    if (module != NULL) {
        PyObject *c_api_object = PyObject_GetAttrString(module, "_C_API");
        if (c_api_object == NULL)
            return -1;
        if (PyCObject_Check(c_api_object))
            PyKaplotContour_API = (void **)PyCObject_AsVoidPtr(c_api_object);
        Py_DECREF(c_api_object);
    }
    else
    {
    	 return -1;
    }

    return 0;
}


#endif


