/*
TODO:
 * control filtering, it's inconsistent now, draw_rgba does without, draw_bgra with
 * try to make the code more generic(templates)
 * cleanups/checks of clipping, pixel order
*/
#undef _DEBUG
#include <Python.h>
#define _DEBUG
#include <stdio.h>
#include <string.h>
#include <numpy/arrayobject.h>
#include "cinterface.h"
#include "agg_basics.h"
#include "agg_rendering_buffer.h"
#include "agg_rasterizer_scanline_aa.h"
#include "agg_path_storage.h"
#include "agg_renderer_scanline.h"
#include "agg_pixfmt_rgb.h"
//#include "agg_pixfmt_rgba_pre.h"
#include "agg_pixfmt_gray.h"
#include "agg_alpha_mask_u8.h"
#include "agg_scanline_u.h"
#include "agg_scanline_p.h"
#include "agg_span_image_filter_rgba.h"
#include "agg_trans_affine.h"
#include "agg_span_interpolator_linear.h"
#include "agg_span_pattern_filter_rgba.h"

#include "agg_span_pattern_rgba.h"
#include "agg_conv_dash.h"
#include "agg_conv_stroke.h"
#include "agg_conv_transform.h"

#include "agg_renderer_primitives.h"
#include "agg_pixfmt_rgba.h"
#include "agg_renderer_primitives.h"
#include "agg_rasterizer_scanline_aa.h"
#include "agg_rasterizer_outline.h"
#include "agg_scanline_p.h"
#include "agg_scanline_bin.h"
#include "agg_renderer_scanline.h"
#include "agg_renderer_primitives.h"
#include <iostream>

#define MIN(X, Y) (((X) < (Y)) ? (X) : (Y))

using namespace std;

class Agg;
extern PyTypeObject PyAgg_Type;

typedef agg::pixfmt_bgra32								pixel_format;
typedef agg::renderer_base<pixel_format>				renderer_base;
typedef agg::renderer_scanline_aa_solid<renderer_base>	renderer_aa;
typedef agg::renderer_scanline_bin_solid<renderer_base>	renderer_bin;
typedef agg::renderer_primitives<renderer_base>			renderer_primitives;

template<class pixfmt_pre, class pixorder=agg::order_bgra>
class ImageDraw
{
public:
	renderer_base			&rb;
	agg::rendering_buffer	&rbuffer;
	agg::alpha_mask_gray8	&alpha_mask;

	ImageDraw(renderer_base &rb, agg::rendering_buffer &rbuffer, agg::alpha_mask_gray8 &alpha_mask) :
		rb(rb), rbuffer(rbuffer), alpha_mask(alpha_mask)
	{
	}

	void draw_image(unsigned char* data, int image_width, int image_height, int stride, agg::trans_affine transformation)
	{
		//typedef pixfmt                         				pixfmt_pre;
		typedef agg::renderer_base<pixfmt_pre>                 renderer_base_pre;
		typedef agg::renderer_scanline_aa_solid<renderer_base> renderer_solid;
		typedef agg::span_allocator<agg::rgba8> span_alloc_type;
		typedef agg::span_interpolator_linear<> interpolator_type;
		typedef agg::span_image_filter_rgba_nn<agg::rgba8, pixorder, interpolator_type> span_gen_type;
		typedef agg::renderer_scanline_aa<renderer_base_pre, span_gen_type> renderer_type;

		agg::path_storage		quad;
		agg::rendering_buffer	rbuf_image(data, image_width, image_height, stride);
		pixfmt_pre				pixf_pre(rbuffer);
		renderer_base_pre		rb_pre(pixf_pre);
		//renderer_solid			rs(rb);

		interpolator_type interpolator(~transformation);

		span_alloc_type sa;

		span_gen_type sg(sa, rbuf_image, agg::rgba_pre(1, 1, 1, 0), interpolator);
		quad.move_to(0, 0);
		quad.line_to(image_width, 0);
		quad.line_to(image_width, image_height);
		quad.line_to(0, image_height);
		quad.line_to(0, 0);
		agg::conv_transform<agg::path_storage> quad_trans(quad, transformation);

		renderer_type ri(rb_pre, sg);
		agg::rasterizer_scanline_aa<> pf;
		pf.add_path(quad_trans);
		agg::scanline_u8 sl;
		agg::scanline_u8_am<agg::alpha_mask_gray8> sl_clip(alpha_mask);
		//rb_pre.clip_box(0, 0, rbuffer.width(), rbuffer.height());
		agg::render_scanlines(pf, sl_clip, ri);
	}

	void draw_image_bilinear(unsigned char* data, int image_width, int image_height, int stride, agg::trans_affine transformation)
	{
		//typedef pixfmt                         				pixfmt_pre;
		typedef agg::renderer_base<pixfmt_pre>                 renderer_base_pre;
		typedef agg::renderer_scanline_aa_solid<renderer_base> renderer_solid;
		typedef agg::span_allocator<agg::rgba8> span_alloc_type;
		typedef agg::span_interpolator_linear<> interpolator_type;
		typedef agg::span_image_filter_rgba_bilinear<agg::rgba8, pixorder, interpolator_type> span_gen_type;
		typedef agg::renderer_scanline_aa<renderer_base_pre, span_gen_type> renderer_type;

		agg::path_storage		quad;
		agg::rendering_buffer	rbuf_image(data, image_width, image_height, stride);
		pixfmt_pre				pixf_pre(rbuffer);
		renderer_base_pre		rb_pre(pixf_pre);
		//renderer_solid			rs(rb);

		interpolator_type interpolator(~transformation);

		span_alloc_type sa;

		span_gen_type sg(sa, rbuf_image, agg::rgba_pre(1, 1, 1, 0), interpolator);
		quad.move_to(0, 0);
		quad.line_to(image_width, 0);
		quad.line_to(image_width, image_height);
		quad.line_to(0, image_height);
		quad.line_to(0, 0);
		agg::conv_transform<agg::path_storage> quad_trans(quad, transformation);

		renderer_type ri(rb_pre, sg);
		agg::rasterizer_scanline_aa<> pf;
		pf.add_path(quad_trans);
		agg::scanline_u8 sl;
		agg::scanline_u8_am<agg::alpha_mask_gray8> sl_clip(alpha_mask);
        agg::render_scanlines(pf, sl_clip, ri);
	}


};


class Agg
{
public:
	int width, height;
	unsigned char *buffer;
	agg::rendering_buffer rbuffer;
	pixel_format pixf;
	agg::rasterizer_scanline_aa<> rasterizer;
	agg::scanline_bin             m_sl_bin;

	agg::scanline_p8 sl_p8;
	renderer_base rb;
	renderer_aa ren_aa;
	double matrix[6];

	unsigned char *alphabuffer;
	agg::rendering_buffer alpha_mask_rbuf;
	agg::alpha_mask_gray8 alpha_mask;

	agg::path_storage current_path; // used for cinterface

	// 'state' variables
	agg::rgba					color;
	double						linewidth;
	double						*dashes;
	int							dashes_length;
	agg::line_cap_e				line_cap;
	agg::line_join_e 			line_join;
	Agg							*pattern;


	Agg(unsigned char* buffer, int width, int height) : width(width), height(height),
		buffer(buffer),
		rbuffer(buffer, width, height, -width*4),
		pixf(rbuffer),
		rb(pixf),
		ren_aa(rb),
		alpha_mask(alpha_mask_rbuf),
		color(0, 0, 0, 1),
		linewidth(1),
		dashes(NULL),
		dashes_length(0),
		line_cap(agg::butt_cap),
		line_join(agg::miter_join),
		pattern(NULL)
	{
		alphabuffer = (unsigned char*)malloc(width * height);
		alpha_mask_rbuf.attach(alphabuffer, width, height, width); // - width for stride?

		memset(buffer, 0xff, width * height * 4);
		memset(alphabuffer, 0xff, width * height);

		matrix[1] = matrix[2] = matrix[4] = matrix[5] = 0;
		matrix[0] = matrix[3] = 1;
		rasterizer.clip_box(0, 0, width, height);
		//clip_box
	}

	~Agg()
	{
		free(alphabuffer);
	}

	void set_linedash(const double* dashes, int length)
	{
		if(this->dashes != NULL)
			free(this->dashes);
		this->dashes_length = length;
		if(length > 0)
		{
			this->dashes = (double*)malloc(sizeof(double) * length);
			memcpy(this->dashes, dashes, length * sizeof(double));
		}
		else
		{
			this->dashes = NULL;
		}
	}

	void transform(double x, double y, double& ox, double &oy)
	{
		/*
		ox = matrix[0] * x + matrix[1] * y + matrix[4];
		oy = matrix[2] * x + matrix[3] * y + matrix[5];
		/*/
		ox = matrix[0] * x + matrix[2] * y + matrix[4];
		oy = matrix[1] * x + matrix[3] * y + matrix[5];
		/**/
	}

	agg::trans_affine get_agg_trans()
	{
		/*
		return agg::trans_affine(matrix[0], matrix[2], matrix[1], matrix[3], matrix[4], matrix[5]);
		/*/
		return agg::trans_affine(matrix[0], matrix[1], matrix[2], matrix[3], matrix[4], matrix[5]);
		/**/
	}

	void _clip(double x1, double y1, double x2, double y2, double x3, double y3, double x4, double y4)
	{
		typedef agg::renderer_base<agg::pixfmt_gray8> ren_base;
		typedef agg::renderer_scanline_aa_solid<ren_base> renderer;

		agg::path_storage polypath;
		polypath.move_to(x1, y1);
		polypath.line_to(x2, y2);
		polypath.line_to(x3, y3);
		polypath.line_to(x4, y4);
		polypath.close_polygon();
		agg::conv_transform<agg::path_storage> polypath_trans(polypath, get_agg_trans());

		agg::pixfmt_gray8 pixf(alpha_mask_rbuf);
		ren_base rbase(pixf);
		renderer rend(rbase);
		agg::scanline_p8 scanline;

		rbase.clear(agg::gray8(0x0));

		rasterizer.add_path(polypath_trans);
		rend.color(0xff);
		agg::render_scanlines(rasterizer, scanline, rend);
		rasterizer.reset();
	}

	void clip(double x1, double y1, double x2, double y2, double x3, double y3, double x4, double y4)
	{
		typedef agg::renderer_base<agg::pixfmt_gray8> ren_base;
		typedef agg::renderer_scanline_aa_solid<ren_base> renderer;

		agg::path_storage polypath;
		polypath.move_to(x1, y1);
		polypath.line_to(x2, y2);
		polypath.line_to(x3, y3);
		polypath.line_to(x4, y4);
		polypath.close_polygon();
		/*
		agg::trans_affine trans = get_agg_trans();
		agg::conv_transform<agg::path_storage> polypath_trans(polypath, trans);
		/*/
		agg::conv_transform<agg::path_storage> polypath_trans(polypath, get_agg_trans());
		/**/

		agg::pixfmt_gray8 pixf(alpha_mask_rbuf);
		ren_base rbase(pixf);
		renderer rend(rbase);
		agg::scanline_p8 scanline;

		rbase.clear(agg::gray8(0x0));

		rasterizer.add_path(polypath_trans);
		rend.color(0xff);
		agg::render_scanlines(rasterizer, scanline, rend);
		rasterizer.reset();
	}

	void clear(double r, double g, double b, double a)
	{
		rb.clear(agg::rgba(r,g,b,a));
	}

	void draw_agg(Agg* other, bool filter)
	{
		ImageDraw<agg::pixfmt_bgra32_pre, agg::order_bgra> id(rb, rbuffer, alpha_mask);
		if(filter)
			id.draw_image_bilinear(other->buffer, other->width, other->height, -other->width*4,
				other->get_agg_trans() * this->get_agg_trans());
		else
			id.draw_image(other->buffer, other->width, other->height, -other->width*4,
				other->get_agg_trans() * this->get_agg_trans());
	}

	void blit_agg(Agg* other, int x, int y)
	{
		rb.copy_from(other->rbuffer, 0, x, y);
	}

	void polyline(double *x, double *y, int length)
	{
		current_path.move_to(x[0], y[0]);
		for(int i = 1; i < length; i++)
		{
			current_path.line_to(x[i], y[i]);
		}
		//agg::conv_transform<agg::path_storage> trans_path(polypath, get_agg_trans());
		//stroke(trans_path);

	}

	void close()
	{
		current_path.end_poly();
		//agg::conv_transform<agg::path_storage> trans_path(polypath, get_agg_trans());
		//fill(trans_path);
	}

	template<class path_type>
	void fill(path_type &path)
	{
		agg::scanline_u8_am<agg::alpha_mask_gray8> sl_clip(alpha_mask);

		if(pattern != NULL)
		{
			typedef agg::pixfmt_bgra32_pre                         pixfmt_pre;
			typedef agg::renderer_base<pixfmt_pre>                 renderer_base_pre;
			typedef agg::renderer_scanline_aa_solid<renderer_base> renderer_solid;
			typedef agg::span_allocator<agg::rgba8> span_alloc_type;
			typedef agg::span_interpolator_linear<> interpolator_type;
			typedef agg::wrap_mode_repeat_auto_pow2 wrap_type_x;
    			typedef agg::wrap_mode_repeat_auto_pow2 wrap_type_y;
			typedef agg::span_pattern_filter_rgba_bilinear<agg::rgba8, agg::order_bgra, interpolator_type, wrap_type_x, wrap_type_y> span_gen_type;
			typedef agg::renderer_scanline_aa<renderer_base_pre, span_gen_type> renderer_type;

			agg::path_storage		quad;
			pixfmt_pre				pixf_pre(rbuffer);
			renderer_base_pre		rb_pre(pixf_pre);
			//renderer_solid			rs(rb);

			interpolator_type interpolator(pattern->get_agg_trans());

			span_alloc_type sa;

			span_gen_type sg(sa, pattern->rbuffer, interpolator);
			renderer_type ri(rb_pre, sg);
			agg::rasterizer_scanline_aa<> pf;
			pf.add_path(path);
			agg::scanline_u8_am<agg::alpha_mask_gray8> sl_clip(alpha_mask);
			agg::render_scanlines(pf, sl_clip, ri);

		}
		else
		{
			ren_aa.color(color);
			rasterizer.add_path(path);
			agg::render_scanlines(rasterizer, sl_clip, ren_aa);
		}
		rasterizer.reset();
	}

	template<class path_type>
	void stroke(path_type &path)
	{
		if(dashes_length > 0)
		{
			agg::scanline_u8_am<agg::alpha_mask_gray8> sl_clip(alpha_mask);
			ren_aa.color(color);
			agg::conv_dash<path_type> dash(path);
			agg::conv_stroke<agg::conv_dash<path_type> > dash_stroke(dash);
			for(int i = 0; i < dashes_length/2; i++)
				dash.add_dash(dashes[i*2], dashes[i*2+1]);
			dash_stroke.width(linewidth);
			dash_stroke.line_cap(line_cap);
			dash_stroke.line_join(line_join);
			rasterizer.add_path(dash_stroke);
			agg::render_scanlines(rasterizer, sl_clip, ren_aa);
			rasterizer.reset();
		}
		else
		{
			agg::scanline_u8_am<agg::alpha_mask_gray8> sl_clip(alpha_mask);
			ren_aa.color(color);
			agg::conv_stroke<path_type> stroke(path);
			stroke.width(linewidth);
			stroke.line_cap(line_cap);
			stroke.line_join(line_join);
			rasterizer.add_path(stroke);
			agg::render_scanlines(rasterizer, sl_clip, ren_aa);
			rasterizer.reset();
		}

	}

	void move_to(double x, double y)
	{
		current_path.move_to(x, y);
	}

	void line_to(double x, double y)
	{
		current_path.line_to(x, y);
	}

	void curve_to(double x1, double y1, double x2, double y2, double x3, double y3)
	{
		current_path.curve4(x1, y1, x2, y2, x3, y3);
	}

	void fill()
	{
		agg::conv_transform<agg::path_storage> trans_path(current_path, get_agg_trans());
		fill(trans_path);
		current_path.remove_all();
	}

	void stroke()
	{
		agg::conv_transform<agg::path_storage> trans_path(current_path, get_agg_trans());
		stroke(trans_path);
		current_path.remove_all();
	}

	bool fill_repeat(double *x, double *y, double *scale_x, double *scale_y, double *angle, double* intensity, PyObject *colormap, int length)
	{
		PyObject *ret;
		PyObject *args, *value;
		double r, g, b;
		agg::rgba original_color = color;
		/*for(int i = 0; i < length; i++)
		{
			agg::conv_transform<agg::path_storage> trans_path(current_path,
				agg::trans_affine_translation(x[i], y[i]) * get_agg_trans() );
			fill(trans_path);
		}*/
		if(scale_x == NULL && scale_y == NULL && angle == NULL)
		{
			for(int i = 0; i < length; i++)
			{
				agg::conv_transform<agg::path_storage> trans_path(current_path,
					agg::trans_affine_translation(x[i], y[i]) * get_agg_trans() );
				if(colormap != NULL && intensity != NULL) {
					//ret = PyObject_Call(colormap, Py_BuildValue("d", intensity[i]), NULL);
					//ret = PyObject_CallObject(colormap, Py_BuildValue("d", intensity[i]));
					//ret = PyObject_CallFunction(colormap, "d", 
					
					args = PyList_New(1);
					value = PyFloat_FromDouble(intensity[i]);
					PyList_SET_ITEM(args, 0, value);
					//ret = PyObject_Call(colormap, args, NULL);
					ret = PyObject_CallFunction(colormap, "d", intensity[i]);
					Py_DECREF(value);
					Py_DECREF(args);
					if(ret == NULL)
						return false;
					if(!PyArg_ParseTuple(ret, "ddd", &color.r, &color.g, &color.b)) {
						return false;
					}
				}
				fill(trans_path);
			}
		}
		else
		{
			for(int i = 0; i < length; i++)
			{
				agg::conv_transform<agg::path_storage> trans_path(current_path,
					agg::trans_affine_scaling(scale_x != NULL ? scale_x[i] : 1, 1) * 
					agg::trans_affine_scaling(1, scale_y != NULL ? scale_y[i] : 1) * 
					agg::trans_affine_rotation(angle != NULL ? angle[i] : 1) * 
					agg::trans_affine_translation(x[i], y[i]) * get_agg_trans());
				fill(trans_path);
			}
		}
		current_path.remove_all();
		current_path.remove_all();
		color = original_color;
		return true;
	}

	void stroke_repeat(double *x, double *y, double *scale_x, double *scale_y, double *angle, int length)
	{
		if(scale_x == NULL && scale_y == NULL && angle == NULL)
		{
			for(int i = 0; i < length; i++)
			{
				agg::conv_transform<agg::path_storage> trans_path(current_path,
					agg::trans_affine_translation(x[i], y[i]) * get_agg_trans() );
				stroke(trans_path);
			}
		}
		else
		{
			for(int i = 0; i < length; i++)
			{
				agg::conv_transform<agg::path_storage> trans_path(current_path,
					agg::trans_affine_scaling(scale_x != NULL ? scale_x[i] : 1, 1) * 
					agg::trans_affine_scaling(1, scale_y != NULL ? scale_y[i] : 1) * 
					agg::trans_affine_rotation(angle != NULL ? angle[i] : 1) * 
					agg::trans_affine_translation(x[i], y[i]) * get_agg_trans());
				stroke(trans_path);
			}
		}
		current_path.remove_all();
	}

};


/*                         Python code below                          */

typedef struct _kaplot_cinterface_agg_t {
	kaplot_cinterface_t base;
	Agg* agg;
} kaplot_cinterface_agg_t;

typedef struct {
    PyObject_HEAD
    Agg *agg;
    unsigned char* buffer;
    PyObject* pybuffer;
    PyObject* pyclipbuffer;
    kaplot_cinterface_agg_t cinterface;
    PyObject *pycinterface;
} PyAgg;

int agg_move_to(void* closure, double x, double y)
{
	kaplot_cinterface_agg_t* cinterface = (kaplot_cinterface_agg_t*)closure;
	cinterface->agg->move_to(x, y);
	//cout << "moveto " << x << ", " << y << endl; 
	return 1;
}

int agg_line_to(void* closure, double x, double y)
{
	kaplot_cinterface_agg_t* cinterface = (kaplot_cinterface_agg_t*)closure;
	cinterface->agg->line_to(x, y);
	//cout << "lineto " << x << ", " << y << endl; 
	return 1;
}

int agg_curve_to(void* closure, double x1, double y1, double x2, double y2, double x3, double y3)
{
	kaplot_cinterface_agg_t* cinterface = (kaplot_cinterface_agg_t*)closure;
	cinterface->agg->curve_to(x1, y1, x2, y2, x3, y3);
	//cout << "curveto " << x1 << ", " << y1 << ", " << x2 << ", " << y2 << ", " << x3 << ", " << y3 << ", " << endl; 
	return 1;
}

int agg_fill(void* closure)
{
	kaplot_cinterface_agg_t* cinterface = (kaplot_cinterface_agg_t*)closure;
    cinterface->agg->fill();
	//cout << "fill" << endl; 
	return 1;
}

int agg_stroke(void* closure)
{
	kaplot_cinterface_agg_t* cinterface = (kaplot_cinterface_agg_t*)closure;
    cinterface->agg->stroke();
	//cout << "stroke" << endl; 
	return 1;
}

int agg_set_color_rgb(void* closure, double r, double g, double b)
{
	kaplot_cinterface_agg_t* cinterface = (kaplot_cinterface_agg_t*)closure;
	cinterface->agg->color.r = r;
	cinterface->agg->color.g = g;
	cinterface->agg->color.b = b;
	return 1;
}

static int
pyagg_init(PyAgg *self, PyObject *args, PyObject *kwargs)
{
	int width, height;
    if (!PyArg_ParseTuple(args, "ii:PyAgg.__init__", &width, &height))
    {
		return -1;
    }
	self->buffer = (unsigned char*)malloc(sizeof(unsigned char) * width * height * 4);
	self->pybuffer = PyBuffer_FromReadWriteMemory(self->buffer, width * height * 4);
	self->pycinterface = PyCObject_FromVoidPtr(&self->cinterface, NULL);
    self->agg = new Agg(self->buffer, width, height);
	self->pyclipbuffer = PyBuffer_FromReadWriteMemory(self->agg->alphabuffer, width * height);
    self->cinterface.base.move_to = agg_move_to;
    self->cinterface.base.line_to = agg_line_to;
    self->cinterface.base.curve_to = agg_curve_to;
    self->cinterface.base.fill = agg_fill;
    self->cinterface.base.stroke = agg_stroke;
    self->cinterface.base.set_color_rgb = agg_set_color_rgb;
    self->cinterface.agg = self->agg;
	return 0;
}


static void
pyagg_dealloc(PyAgg *self)
{
	Py_DECREF(self->pybuffer);
	Py_DECREF(self->pyclipbuffer);
	free(self->buffer);
	delete self->agg;
    if (self->ob_type->tp_free)
		self->ob_type->tp_free((PyObject *)self);
    else
		PyObject_Del(self);
}

static PyObject *
pyagg_clip(PyAgg *self, PyObject *args)
{
	double x1, y1, x2, y2, x3, y3, x4, y4;
	if(!PyArg_ParseTuple(args, "(dd)(dd)(dd)(dd):clip", &x1, &y1, &x2, &y2, &x3, &y3, &x4, &y4))
		return NULL;
	else
		self->agg->clip(x1, y1, x2, y2, x3, y3, x4, y4);
	Py_INCREF(Py_None);
	return Py_None;
}


static PyObject *
pyagg_polyline(PyAgg *self, PyObject *args)
{
	PyObject *x_array;
	PyObject *y_array;
	PyArrayObject *x_array_double;
	PyArrayObject *y_array_double;
	int length;
	double *x;
	double *y;

	if(PyArg_ParseTuple(args, "OO:polyline", &x_array, &y_array))
	{
		//x_array_double = NA_InputArray(x_array, tFloat64, C_ARRAY);
		//y_array_double = NA_InputArray(y_array, tFloat64, C_ARRAY);
		x_array_double = (PyArrayObject*)PyArray_FromAny(x_array, PyArray_DescrFromType(NPY_FLOAT64), 1, 1, NPY_ARRAY_C_CONTIGUOUS, NULL);
		y_array_double = (PyArrayObject*)PyArray_FromAny(y_array, PyArray_DescrFromType(NPY_FLOAT64), 1, 1, NPY_ARRAY_C_CONTIGUOUS, NULL);
		if(x_array_double == NULL)
			return PyErr_Format(PyExc_TypeError, "can't convert x data into numarray");
		if(x_array_double->nd != 1)
			return PyErr_Format(PyExc_TypeError, "x data isn't 1 dimensional");
		if(y_array_double == NULL)
			return PyErr_Format(PyExc_TypeError, "can't convert y data into numarray");
		if(y_array_double->nd != 1)
			return PyErr_Format(PyExc_TypeError, "y data isn't 1 dimensional");
		length = MIN(x_array_double->dimensions[0], y_array_double->dimensions[0]);
		x = (double*)PyArray_DATA(x_array_double);
		y = (double*)PyArray_DATA(y_array_double);
		self->agg->polyline(x, y, length);
		Py_INCREF(Py_None);
		return Py_None;
	}
	return NULL;
}

static PyObject *
pyagg_close(PyAgg *self, PyObject *args)
{
	self->agg->close();
	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject *
draw_rgba_image(PyAgg *self, PyObject *args)
{
	unsigned char* data;
	int length;
	int width, height;
	int filter=0;
	if(PyArg_ParseTuple(args, "s#ii|i:draw_rgba_image", &data, &length, &width, &height, &filter))
	{
		if(length != (width * height * 4))
		{
			PyErr_Format(PyExc_TypeError, "length of data != width * height * 4");
			return NULL;
		}

		agg::trans_affine t = agg::trans_affine_translation(0.5, 0.5);
		ImageDraw<agg::pixfmt_rgba32_pre> id(self->agg->rb,
			self->agg->rbuffer, self->agg->alpha_mask);
		if(filter)
			id.draw_image_bilinear(data, width, height, width*4, t * self->agg->get_agg_trans());
		else
			id.draw_image(data, width, height, width*4, t * self->agg->get_agg_trans());
		Py_INCREF(Py_None);
		return Py_None;
	}
	else

		return NULL;
}

static PyObject *
pyagg_draw_agg(PyAgg *self, PyObject *args)
{
	PyAgg* other;
	bool filter;
	if(!PyArg_ParseTuple(args, "O!|i:draw_agg", &PyAgg_Type, &other, &filter))
		return NULL;
	self->agg->draw_agg(other->agg, filter);
	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject *
pyagg_blit_agg(PyAgg *self, PyObject *args)
{
	PyAgg* other;
	int x, y;
	if(!PyArg_ParseTuple(args, "O!ii:blit_agg", &PyAgg_Type, &other, &x, &y))
		return NULL;
	self->agg->blit_agg(other->agg, x, y);
	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject *
pyagg_set_color(PyAgg *self, PyObject *args)
{
	if(!PyArg_ParseTuple(args, "ddd:set_color", &self->agg->color.r, &self->agg->color.g, &self->agg->color.b))
		return NULL;
	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject *
pyagg_set_alpha(PyAgg *self, PyObject *args)
{
	if(!PyArg_ParseTuple(args, "d:set_alpha", &self->agg->color.a))
		return NULL;
	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject *
pyagg_set_matrix(PyAgg *self, PyObject *args)
{
	double* m = self->agg->matrix;
	if(!PyArg_ParseTuple(args, "dddddd:set_matrix", m, m+1, m+2, m+3, m+4, m+5))
		return NULL;
	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject *
pyagg_set_linewidth(PyAgg *self, PyObject *args)
{
	if(!PyArg_ParseTuple(args, "d:set_linewidth", &self->agg->linewidth))
		return NULL;
	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject *
pyagg_set_linedash(PyAgg *self, PyObject *args)
{
	PyObject *sequence;
	double *dashes;
	int length;

	if(!PyArg_ParseTuple(args, "O:set_linedash", &sequence))
		return NULL;
	sequence = PySequence_Fast(sequence, "first argument should be a sequence");
	if(!sequence)
		return NULL;
	length = PySequence_Fast_GET_SIZE(sequence);
	dashes = (double*)malloc(sizeof(double) * length);
	for(int i = 0; i < length; i++)
	{
		dashes[i] = PyFloat_AsDouble(PySequence_Fast_GET_ITEM(sequence, i));
		if(PyErr_Occurred())
		{
			free(dashes);
			Py_DECREF(sequence);
			return NULL;
		}
	}
	Py_DECREF(sequence);
	self->agg->set_linedash(dashes, length);
	free(dashes);

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject *
pyagg_set_linecap(PyAgg *self, PyObject *args)
{
	agg::line_cap_e line_cap;
	if(!PyArg_ParseTuple(args, "i!:set_linecap", &line_cap))
		return NULL;
	self->agg->line_cap = line_cap;
	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject *
pyagg_set_linejoin(PyAgg *self, PyObject *args)
{
	agg::line_join_e line_join;
	if(!PyArg_ParseTuple(args, "i!:set_linejoin", &line_join))
		return NULL;
	self->agg->line_join = line_join;
	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject *
pyagg_set_pattern(PyAgg *self, PyObject *args)
{
	PyAgg* other;
	if(!PyArg_ParseTuple(args, "O!:set_pattern", &PyAgg_Type, &other))
		return NULL;
	self->agg->pattern = other->agg;
	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject *
pyagg_clear_pattern(PyAgg *self, PyObject *args)
{
	self->agg->pattern = NULL;
	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject *
pyagg_move_to(PyAgg *self, PyObject *args)
{
	double x, y;
	if(!PyArg_ParseTuple(args, "dd:move_to", &x, &y))
		return NULL;
	self->agg->move_to(x, y);
	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject *
pyagg_line_to(PyAgg *self, PyObject *args)
{
	double x, y;
	if(!PyArg_ParseTuple(args, "dd:line_to", &x, &y))
		return NULL;
	self->agg->line_to(x, y);
	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject *
pyagg_curve_to(PyAgg *self, PyObject *args)
{
	double x1, y1, x2, y2, x3, y3;
	if(!PyArg_ParseTuple(args, "dddddd:curve_to", &x1, &y1, &x2, &y2, &x3, &y3))
		return NULL;
	self->agg->curve_to(x1, y1, x2, y2, x3, y3);
	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject *
pyagg_fill(PyAgg *self, PyObject *args)
{
	self->agg->fill();
	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject *
pyagg_stroke(PyAgg *self, PyObject *args)
{
	self->agg->stroke();
	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject *
pyagg_fill_repeat(PyAgg *self, PyObject *args)
{
	PyObject *x_array;
	PyObject *y_array;
	PyObject *scale_x_array = NULL;
	PyObject *scale_y_array = NULL;
	PyObject *angle_array = NULL;
	PyObject *intensity_array = NULL;
	PyObject *colormap = NULL;
	PyArrayObject *x_array_double;
	PyArrayObject *y_array_double;
	PyArrayObject *scale_x_array_double = NULL;
	PyArrayObject *scale_y_array_double = NULL;
	PyArrayObject *angle_array_double = NULL;
	PyArrayObject *intensity_array_double = NULL;
	int length;
	double *x;
	double *y;
	double *scale_x = NULL;
	double *scale_y = NULL;
	double *angle = NULL;
	double *intensity = NULL;

	if(PyArg_ParseTuple(args, "OO|OOOOO:fill_repeat", &x_array, &y_array, &scale_x_array, &scale_y_array, &angle_array, &intensity_array, &colormap))
	{
		//x_array_double = NA_InputArray(x_array, tFloat64, C_ARRAY);
		//y_array_double = NA_InputArray(y_array, tFloat64, C_ARRAY);
		x_array_double = (PyArrayObject*)PyArray_FromAny(x_array, PyArray_DescrFromType(NPY_FLOAT64), 1, 1, NPY_ARRAY_C_CONTIGUOUS, NULL);
		y_array_double = (PyArrayObject*)PyArray_FromAny(y_array, PyArray_DescrFromType(NPY_FLOAT64), 1, 1, NPY_ARRAY_C_CONTIGUOUS, NULL);
		if(x_array_double == NULL)
			return PyErr_Format(PyExc_TypeError, "can't convert x data into numarray");
		if(x_array_double->nd != 1)
			return PyErr_Format(PyExc_TypeError, "x data isn't 1 dimensional");
		if(y_array_double == NULL)
			return PyErr_Format(PyExc_TypeError, "can't convert y data into numarray");
		if(y_array_double->nd != 1)
			return PyErr_Format(PyExc_TypeError, "y data isn't 1 dimensional");
		length = MIN(x_array_double->dimensions[0], y_array_double->dimensions[0]);
		x = (double*)PyArray_DATA(x_array_double);
		y = (double*)PyArray_DATA(y_array_double);
		if(scale_x_array != NULL && !(scale_x_array == Py_None))
		{
			//scale_x_array_double = NA_InputArray(scale_x_array, tFloat64, C_ARRAY);
			scale_x_array_double = (PyArrayObject*)PyArray_FromAny(scale_x_array, PyArray_DescrFromType(NPY_FLOAT64), 1, 1, NPY_ARRAY_C_CONTIGUOUS, NULL);
			if(scale_x_array_double == NULL)
				return PyErr_Format(PyExc_TypeError, "can't convert xscale data into numarray");
			if(scale_x_array_double->nd != 1)
				return PyErr_Format(PyExc_TypeError, "scale x data isn't 1 dimensional");
			length = MIN(length, scale_x_array_double->dimensions[0]);
			scale_x = (double*)PyArray_DATA(scale_x_array_double);
		}
		if(scale_y_array != NULL && !(scale_y_array == Py_None))
		{
			//scale_y_array_double = NA_InputArray(scale_y_array, tFloat64, C_ARRAY);
			scale_y_array_double = (PyArrayObject*)PyArray_FromAny(scale_y_array, PyArray_DescrFromType(NPY_FLOAT64), 1, 1, NPY_ARRAY_C_CONTIGUOUS, NULL);
			if(scale_y_array_double == NULL)
				return PyErr_Format(PyExc_TypeError, "can't convert yscale data into numarray");
			if(scale_y_array_double->nd != 1)
				return PyErr_Format(PyExc_TypeError, "scale y data isn't 1 dimensional");
			length = MIN(length, scale_y_array_double->dimensions[0]);
			scale_y = (double*)PyArray_DATA(scale_y_array_double);
		}
		if(angle_array != NULL && !(angle_array == Py_None))
		{
			//angle_array_double = NA_InputArray(angle_array, tFloat64, C_ARRAY);
			angle_array_double = (PyArrayObject*)PyArray_FromAny(angle_array, PyArray_DescrFromType(NPY_FLOAT64), 1, 1, NPY_ARRAY_C_CONTIGUOUS, NULL);
			if(angle_array_double == NULL)
				return PyErr_Format(PyExc_TypeError, "can't convert angle data into numarray");
			if(angle_array_double->nd != 1)
				return PyErr_Format(PyExc_TypeError, "angle data isn't 1 dimensional");
			length = MIN(length, angle_array_double->dimensions[0]);
			angle = (double*)PyArray_DATA(angle_array_double);
		}
		if(intensity_array != NULL && !(intensity_array == Py_None))
		{
			///intensity_array_double = NA_InputArray(intensity_array, tFloat64, C_ARRAY);
			intensity_array_double = (PyArrayObject*)PyArray_FromAny(intensity_array, PyArray_DescrFromType(NPY_FLOAT64), 1, 1, NPY_ARRAY_C_CONTIGUOUS, NULL);
			if(intensity_array_double == NULL)
				return PyErr_Format(PyExc_TypeError, "can't convert intensity data into numarray");
			if(intensity_array_double->nd != 1)
				return PyErr_Format(PyExc_TypeError, "intensity data isn't 1 dimensional");
			length = MIN(length, intensity_array_double->dimensions[0]);
			intensity = (double*)PyArray_DATA(intensity_array_double);
		}
		if(self->agg->fill_repeat(x, y, scale_x, scale_y, angle, intensity, colormap, length)) {
			Py_INCREF(Py_None);
			return Py_None;
		}	
	}
	return NULL;
}

static PyObject *
pyagg_stroke_repeat(PyAgg *self, PyObject *args)
{
	PyObject *x_array;
	PyObject *y_array;
	PyObject *scale_x_array = NULL;
	PyObject *scale_y_array = NULL;
	PyObject *angle_array = NULL;
	PyArrayObject *x_array_double;
	PyArrayObject *y_array_double;
	PyArrayObject *scale_x_array_double = NULL;
	PyArrayObject *scale_y_array_double = NULL;
	PyArrayObject *angle_array_double = NULL;
	int length;
	double *x;
	double *y;
	double *scale_x = NULL;
	double *scale_y = NULL;
	double *angle = NULL;

	if(PyArg_ParseTuple(args, "OO|OOO:stroke_repeat", &x_array, &y_array, &scale_x_array, &scale_y_array, &angle_array))
	{
		//x_array_double = NA_InputArray(x_array, tFloat64, C_ARRAY);
		//y_array_double = NA_InputArray(y_array, tFloat64, C_ARRAY);
		x_array_double = (PyArrayObject*)PyArray_FromAny(x_array, PyArray_DescrFromType(NPY_FLOAT64), 1, 1, NPY_ARRAY_C_CONTIGUOUS, NULL);
		y_array_double = (PyArrayObject*)PyArray_FromAny(y_array, PyArray_DescrFromType(NPY_FLOAT64), 1, 1, NPY_ARRAY_C_CONTIGUOUS, NULL);
		if(x_array_double == NULL)
			return PyErr_Format(PyExc_TypeError, "can't convert x data into numarray");
		if(x_array_double->nd != 1)
			return PyErr_Format(PyExc_TypeError, "x data isn't 1 dimensional");
		if(y_array_double == NULL)
			return PyErr_Format(PyExc_TypeError, "can't convert y data into numarray");
		if(y_array_double->nd != 1)
			return PyErr_Format(PyExc_TypeError, "y data isn't 1 dimensional");
		length = MIN(x_array_double->dimensions[0], y_array_double->dimensions[0]);
		x = (double*)PyArray_DATA(x_array_double);
		y = (double*)PyArray_DATA(y_array_double);
		if(scale_x_array != NULL && !(scale_x_array == Py_None))
		{
			//scale_x_array_double = NA_InputArray(scale_x_array, tFloat64, C_ARRAY);
			scale_x_array_double = (PyArrayObject*)PyArray_FromAny(scale_x_array, PyArray_DescrFromType(NPY_FLOAT64), 1, 1, NPY_ARRAY_C_CONTIGUOUS, NULL);
			if(scale_x_array_double == NULL)
				return PyErr_Format(PyExc_TypeError, "can't convert xscale data into numarray");
			if(scale_x_array_double->nd != 1)
				return PyErr_Format(PyExc_TypeError, "scale x data isn't 1 dimensional");
			length = MIN(length, scale_x_array_double->dimensions[0]);
			scale_x = (double*)PyArray_DATA(scale_x_array_double);
		}
		if(scale_y_array != NULL && !(scale_y_array == Py_None))
		{
			//scale_y_array_double = NA_InputArray(scale_y_array, tFloat64, C_ARRAY);
			scale_y_array_double = (PyArrayObject*)PyArray_FromAny(scale_y_array, PyArray_DescrFromType(NPY_FLOAT64), 1, 1, NPY_ARRAY_C_CONTIGUOUS, NULL);
			if(scale_y_array_double == NULL)
				return PyErr_Format(PyExc_TypeError, "can't convert yscale data into numarray");
			if(scale_y_array_double->nd != 1)
				return PyErr_Format(PyExc_TypeError, "scale y data isn't 1 dimensional");
			length = MIN(length, scale_y_array_double->dimensions[0]);
			scale_y = (double*)PyArray_DATA(scale_y_array_double);
		}
		if(angle_array != NULL && !(angle_array == Py_None))
		{
			//angle_array_double = NA_InputArray(angle_array, tFloat64, C_ARRAY);
			angle_array_double = (PyArrayObject*)PyArray_FromAny(angle_array, PyArray_DescrFromType(NPY_FLOAT64), 1, 1, NPY_ARRAY_C_CONTIGUOUS, NULL);
			if(angle_array_double == NULL)
				return PyErr_Format(PyExc_TypeError, "can't convert angle data into numarray");
			if(angle_array_double->nd != 1)
				return PyErr_Format(PyExc_TypeError, "angle data isn't 1 dimensional");
			length = MIN(length, angle_array_double->dimensions[0]);
			angle = (double*)PyArray_DATA(angle_array_double);
		}
		self->agg->stroke_repeat(x, y, scale_x, scale_y, angle, length);
		Py_INCREF(Py_None);
		return Py_None;
	}
	return NULL;
}

static PyObject *
pyagg_clear(PyAgg *self, PyObject *args)
{
	double r, g, b, a;
	if(!PyArg_ParseTuple(args, "dddd:clear", &r, &g, &b, &a))
		return NULL;
	self->agg->clear(r, g, b, a);
	Py_INCREF(Py_None);
	return Py_None;
}

static PyMethodDef pyagg_methods[] = {
    { "clip", (PyCFunction)pyagg_clip, METH_VARARGS },
    { "polyline", (PyCFunction)pyagg_polyline, METH_VARARGS },
    { "close", (PyCFunction)pyagg_close, METH_VARARGS },
    { "draw_rgba_image", (PyCFunction)draw_rgba_image, METH_VARARGS },
    { "draw_agg", (PyCFunction)pyagg_draw_agg, METH_VARARGS },
    { "blit_agg", (PyCFunction)pyagg_blit_agg, METH_VARARGS },
    { "set_color", (PyCFunction)pyagg_set_color, METH_VARARGS },
    { "set_alpha", (PyCFunction)pyagg_set_alpha, METH_VARARGS },
    { "set_matrix", (PyCFunction)pyagg_set_matrix, METH_VARARGS },
    { "set_linewidth", (PyCFunction)pyagg_set_linewidth, METH_VARARGS },
    { "set_linedash", (PyCFunction)pyagg_set_linedash, METH_VARARGS },
    { "set_linecap", (PyCFunction)pyagg_set_linecap, METH_VARARGS },
    { "set_linejoin", (PyCFunction)pyagg_set_linejoin, METH_VARARGS },
    { "set_pattern", (PyCFunction)pyagg_set_pattern, METH_VARARGS },
    { "clear_pattern", (PyCFunction)pyagg_clear_pattern, METH_VARARGS },
    { "move_to", (PyCFunction)pyagg_move_to, METH_VARARGS },
    { "line_to", (PyCFunction)pyagg_line_to, METH_VARARGS },
    { "curve_to", (PyCFunction)pyagg_curve_to, METH_VARARGS },
    { "fill", (PyCFunction)pyagg_fill, METH_VARARGS },
    { "stroke", (PyCFunction)pyagg_stroke, METH_VARARGS },
    { "fill_repeat", (PyCFunction)pyagg_fill_repeat, METH_VARARGS },
    { "stroke_repeat", (PyCFunction)pyagg_stroke_repeat, METH_VARARGS },
    { "clear", (PyCFunction)pyagg_clear, METH_VARARGS },
    { NULL, NULL, 0 }
};

static PyObject *
pyagg_get_buffer(PyAgg *self, PyObject *args)
{
	Py_INCREF(self->pybuffer);
	return self->pybuffer;
}
static PyObject *
pyagg_get_clipbuffer(PyAgg *self, PyObject *args)
{
	Py_INCREF(self->pyclipbuffer);
	return self->pyclipbuffer;
}


static PyObject *
pyagg_get_cinterface(PyAgg *self, void* closure)
{
	Py_INCREF(self->pycinterface);
	return self->pycinterface;
}


static PyGetSetDef pyagg_getseters[] = {
    {"buffer", (getter)pyagg_get_buffer, NULL, NULL, NULL},
    {"clipbuffer", (getter)pyagg_get_clipbuffer, NULL, NULL, NULL},
    {"cinterface", (getter)pyagg_get_cinterface, NULL, NULL, NULL},
    {NULL}
};


PyTypeObject PyAgg_Type = {
    PyObject_HEAD_INIT(NULL)
    0,                                  /* ob_size */
    "Agg",                    			/* tp_name */
    sizeof(PyAgg),          		   /* tp_basicsize */
    0,                                  /* tp_itemsize */
    /* methods */
    (destructor)pyagg_dealloc, /* tp_dealloc */
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
    pyagg_methods,        			    /* tp_methods */
    0,                                  /* tp_members */
    pyagg_getseters,           		   /* tp_getset */
    (PyTypeObject *)0,                  /* tp_base */
    (PyObject *)0,                      /* tp_dict */
    0,                                  /* tp_descr_get */
    0,                                  /* tp_descr_set */
    0,                                  /* tp_dictoffset */
    (initproc)pyagg_init,                        /* tp_init */
    (allocfunc)0,                       /* tp_alloc */
    (newfunc)0,                         /* tp_new */
    (freefunc)0,                        /* tp_free */
    (inquiry)0,                         /* tp_is_gc */
    (PyObject *)0,                      /* tp_bases */
};

static PyMethodDef pyagg_functions[] = {
    { NULL, NULL, 0 }
};


#define INIT_TYPE(tp) \
    if (!tp.ob_type) tp.ob_type = &PyType_Type; \
    if (!tp.tp_alloc) tp.tp_alloc = PyType_GenericAlloc; \
    if (!tp.tp_new) tp.tp_new = PyType_GenericNew; \
    if (PyType_Ready(&tp) < 0) \
        return;

PyMODINIT_FUNC
init_agg(void)
{
	PyObject *mod;
	import_array();

	mod = Py_InitModule("_agg", pyagg_functions);
	INIT_TYPE(PyAgg_Type);
	PyModule_AddObject(mod, "Agg",  (PyObject *)&PyAgg_Type);

#define AGG_CONSTANT(x, y) PyModule_AddIntConstant(mod, #y, x)
	AGG_CONSTANT(agg::butt_cap, butt_cap);
	AGG_CONSTANT(agg::square_cap, square_cap);
	AGG_CONSTANT(agg::round_cap, round_cap);
	AGG_CONSTANT(agg::miter_join, miter_join);
	AGG_CONSTANT(agg::miter_join_revert, miter_join_revert);
	AGG_CONSTANT(agg::round_join, round_join);
	AGG_CONSTANT(agg::bevel_join, bevel_join);
}

