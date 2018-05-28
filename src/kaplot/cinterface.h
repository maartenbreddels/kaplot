#ifndef KAPLOT_C_INTERFACE
#define KAPLOT_C_INTERFACE

struct _kaplot_cinterface_t;
//typedef struct _kaplot_cinterface_t kaplot_cinterface_t;

typedef struct _kaplot_cinterface_t{
	int (*move_to)(void*, double, double);
	int (*line_to)(void*, double, double);
	int (*curve_to)(void*, double, double, double, double, double, double);
	int (*fill)(void*);
	int (*stroke)(void*);
	int (*set_color_rgb)(void*, double, double, double);
} kaplot_cinterface_t;
#endif KAPLOT_C_INTERFACE

