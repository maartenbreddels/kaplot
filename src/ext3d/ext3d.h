// return 0 on error
typedef int (*line_callback)(void* userdata, double x1, double y1, double x2, double y2);

#ifdef KAPLOT_EXT3D_MODULE

void PyKaplot_Wireframe(double* data2d, int width, int height, double matrix[4][4],
						line_callback callback, void* userdata);

#else

static void **PyKaplotExt3d_API;

#define PyKaplot_Wireframe \
 (*(void (*)(double* data2d, int width, int height, double matrix[4][4], \
						line_callback callback, void* userdata)) PyKaplotExt3d_API[0])

static int
import_kaplot_ext3d(void)
{
    PyObject *module = PyImport_ImportModule("kaplot.cext._ext3d");

    if (module != NULL) {
        PyObject *c_api_object = PyObject_GetAttrString(module, "_C_API");
        if (c_api_object == NULL)
            return -1;
        if (PyCObject_Check(c_api_object))
            PyKaplotExt3d_API = (void **)PyCObject_AsVoidPtr(c_api_object);
        Py_DECREF(c_api_object);
    }
    return 0;
}


#endif


