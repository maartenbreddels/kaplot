//----------------------------------------------------------------------------
// Anti-Grain Geometry - Version 2.2
// Copyright (C) 2002-2004 Maxim Shemanarev (http://www.antigrain.com)
//
// Permission to copy, use, modify, sell and distribute this software 
// is granted provided this copyright notice appears in all copies. 
// This software is provided "as is" without express or implied
// warranty, and with no claim as to its suitability for any purpose.
//
//----------------------------------------------------------------------------
// Contact: mcseem@antigrain.com
//          mcseemagg@yahoo.com
//          http://www.antigrain.com
//----------------------------------------------------------------------------

#ifndef AGG_PIXFMT_RGBA32_PRE_INCLUDED
#define AGG_PIXFMT_RGBA32_PRE_INCLUDED

#include <string.h>
#include "agg_basics.h"
#include "agg_color_rgba8.h"
#include "agg_rendering_buffer.h"

namespace agg
{


    //=================================================pixel_formats_rgba32_pre
    template<class Order> class pixel_formats_rgba32_pre
    {
    public:
        typedef rgba8 color_type;
        typedef Order order_type;
        typedef rendering_buffer::row_data row_data;


    private:
        //--------------------------------------------------------------------
        static inline void copy_pix(int8u* p, const color_type& c)
        {
            p[Order::R] = (int8u)c.r;
            p[Order::G] = (int8u)c.g;
            p[Order::B] = (int8u)c.b;
            p[Order::A] = (int8u)c.a;
        }

        //--------------------------------------------------------------------
        static inline void blend_pix(int8u* p, const color_type& c, 
                                     unsigned cover, unsigned alpha)
        {
            p[Order::R] = (int8u)((p[Order::R] * alpha + ((c.r * cover) << 8)) >> 16);
            p[Order::G] = (int8u)((p[Order::G] * alpha + ((c.g * cover) << 8)) >> 16);
            p[Order::B] = (int8u)((p[Order::B] * alpha + ((c.b * cover) << 8)) >> 16);
            p[Order::A] = (int8u)(255 - ((alpha * (255 - p[Order::A])) >> 16));
        }

        //--------------------------------------------------------------------
        static inline void copy_or_blend_pix(int8u* p, const color_type& c, unsigned cover)
        {
            unsigned alpha = 65535 - cover * c.a;

            if(alpha < 65535)
            {
                if(alpha <= 65535-255*255)
                {
                    copy_pix(p, c);
                }
                else
                {
                    blend_pix(p, c, cover, alpha);
                }
            }
        }

        //--------------------------------------------------------------------
        static inline void copy_or_blend_pix(int8u* p, const color_type& c)
        {
            unsigned alpha = 255 - c.a;
            if(alpha < 255)
            {
                if(alpha == 0)
                {
                    copy_pix(p, c);
                }
                else
                {
                    p[Order::R] = (int8u)((p[Order::R] * alpha + (c.r << 8)) >> 8);
                    p[Order::G] = (int8u)((p[Order::G] * alpha + (c.g << 8)) >> 8);
                    p[Order::B] = (int8u)((p[Order::B] * alpha + (c.b << 8)) >> 8);
                    p[Order::A] = (int8u)(255 - ((alpha * (255 - p[Order::A])) >> 8));
                }
            }
        }



    public:
        //--------------------------------------------------------------------
        pixel_formats_rgba32_pre(rendering_buffer& rb)
            : m_rbuf(&rb)
        {
        }

        //--------------------------------------------------------------------
        unsigned width()  const { return m_rbuf->width();  }
        unsigned height() const { return m_rbuf->height(); }

        //--------------------------------------------------------------------
        color_type pixel(int x, int y) const
        {
            int8u* p = m_rbuf->row(y) + (x << 2);
            return color_type(p[Order::R], p[Order::G], p[Order::B], p[Order::A]);
        }

        //--------------------------------------------------------------------
        row_data span(int x, int y) const
        {
            return row_data(x, width() - 1, m_rbuf->row(y) + (x << 2));
        }

        //--------------------------------------------------------------------
        void copy_pixel(int x, int y, const color_type& c)
        {
            int8u* p = m_rbuf->row(y) + (x << 2);
            p[Order::R] = (int8u)c.r;
            p[Order::G] = (int8u)c.g;
            p[Order::B] = (int8u)c.b;
            p[Order::A] = (int8u)c.a;
        }

        //--------------------------------------------------------------------
        void blend_pixel(int x, int y, const color_type& c, int8u cover)
        {
            copy_or_blend_pix(m_rbuf->row(y) + (x << 2), c, cover);
        }

        //--------------------------------------------------------------------
        void copy_hline(int x, int y, unsigned len, const color_type& c)
        {
            int32u v;
            copy_pix((int8u*)&v, c);
            int32u* p32 = (int32u*)(m_rbuf->row(y)) + x;
            do
            {
                *p32++ = v;
            }
            while(--len);
        }

        //--------------------------------------------------------------------
        void copy_vline(int x, int y, unsigned len, const color_type& c)
        {
            int32u v;
            copy_pix((int8u*)&v, c);
            int8u* p = m_rbuf->row(y) + (x << 2);
            do
            {
                *(int32u*)p = v; 
                p += m_rbuf->stride();
            }
            while(--len);
        }

        //--------------------------------------------------------------------
        void blend_hline(int x, int y, unsigned len, 
                         const color_type& c, int8u cover)
        {
            unsigned alpha = unsigned(cover) * c.a;
            if(alpha == 255*255)
            {
                int32u v;
                copy_pix((int8u*)&v, c);
                int32u* p32 = (int32u*)(m_rbuf->row(y)) + x;
                do
                {
                    *p32++ = v;
                }
                while(--len);
            }
            else
            {
                int8u* p = m_rbuf->row(y) + (x << 2);
                alpha = 65535 - alpha;
                do
                {
                    blend_pix(p, c, cover, alpha);
                    p += 4;
                }
                while(--len);
            }
        }

        //--------------------------------------------------------------------
        void blend_vline(int x, int y, unsigned len, 
                         const color_type& c, int8u cover)
        {
            int8u* p = m_rbuf->row(y) + (x << 2);
            unsigned alpha = unsigned(cover) * c.a;
            if(alpha == 255*255)
            {
                int32u v;
                copy_pix((int8u*)&v, c);
                do
                {
                    *(int32u*)p = v; 
                    p += m_rbuf->stride();
                }
                while(--len);
            }
            else
            {
                alpha = 65535 - alpha;
                do
                {
                    blend_pix(p, c, cover, alpha);
                    p += m_rbuf->stride();
                }
                while(--len);
            }
        }


        //--------------------------------------------------------------------
        void copy_from(const rendering_buffer& from, 
                       int xdst, int ydst,
                       int xsrc, int ysrc,
                       unsigned len)
        {
            memmove(m_rbuf->row(ydst) + xdst * 4, 
                    (const void*)(from.row(ysrc) + xsrc * 4), len * 4);
        }


        //--------------------------------------------------------------------
        template<class SrcPixelFormatRenderer>
        void blend_from(const SrcPixelFormatRenderer& from, 
                        const int8u* psrc,
                        int xdst, int ydst,
                        int xsrc, int ysrc,
                        unsigned len)
        {
            typedef typename SrcPixelFormatRenderer::order_type src_order;

            int8u* pdst = m_rbuf->row(ydst) + (xdst << 2);
            int incp = 4;
            if(xdst > xsrc)
            {
                psrc += (len-1) << 2;
                pdst += (len-1) << 2;
                incp = -4;
            }
            do 
            {
                unsigned alpha = 255 - psrc[src_order::A];
                if(alpha < 255)
                {
                    if(alpha == 0)
                    {
                        pdst[Order::R] = psrc[src_order::R];
                        pdst[Order::G] = psrc[src_order::G];
                        pdst[Order::B] = psrc[src_order::B];
                        pdst[Order::A] = psrc[src_order::A];
                    }
                    else
                    {
                        pdst[Order::R] = (int8u)((pdst[Order::R] * alpha + (psrc[src_order::R] << 8)) >> 8);
                        pdst[Order::G] = (int8u)((pdst[Order::G] * alpha + (psrc[src_order::G] << 8)) >> 8);
                        pdst[Order::B] = (int8u)((pdst[Order::B] * alpha + (psrc[src_order::B] << 8)) >> 8);
                        pdst[Order::A] = (int8u)(255 - ((alpha * (255 - pdst[Order::A])) >> 8));
                    }
                }
                psrc += incp;
                pdst += incp;
            }
            while(--len);
        }



        //--------------------------------------------------------------------
        void blend_solid_hspan(int x, int y, unsigned len, 
                               const color_type& c, const int8u* covers)
        {
            int8u* p = m_rbuf->row(y) + (x << 2);
            do 
            {
                copy_or_blend_pix(p, c, *covers++);
                p += 4;
            }
            while(--len);
        }



        //--------------------------------------------------------------------
        void blend_solid_vspan(int x, int y, unsigned len, 
                               const color_type& c, const int8u* covers)
        {
            int8u* p = m_rbuf->row(y) + (x << 2);
            do 
            {
                copy_or_blend_pix(p, c, *covers++);
                p += m_rbuf->stride();
            }
            while(--len);
        }


        //--------------------------------------------------------------------
        void blend_color_hspan(int x, int y, unsigned len, 
                               const color_type* colors, 
                               const int8u* covers, 
                               int8u cover)
        {
            int8u* p = m_rbuf->row(y) + (x << 2);
            do 
            {
                copy_or_blend_pix(p, *colors++, covers ? *covers++ : cover);
                p += 4;
            }
            while(--len);
        }


        //--------------------------------------------------------------------
        void blend_color_vspan(int x, int y, unsigned len, 
                               const color_type* colors, 
                               const int8u* covers,
                               int8u cover)
        {
            int8u* p = m_rbuf->row(y) + (x << 2);
            do 
            {
                copy_or_blend_pix(p, *colors++, covers ? *covers++ : cover);
                p += m_rbuf->stride();
            }
            while(--len);
        }

    private:
        rendering_buffer* m_rbuf;
    };

    typedef pixel_formats_rgba32_pre<order_rgba32> pixfmt_rgba32_pre; //----pixfmt_rgba32_pre
    typedef pixel_formats_rgba32_pre<order_argb32> pixfmt_argb32_pre; //----pixfmt_argb32_pre
    typedef pixel_formats_rgba32_pre<order_abgr32> pixfmt_abgr32_pre; //----pixfmt_abgr32_pre
    typedef pixel_formats_rgba32_pre<order_bgra32> pixfmt_bgra32_pre; //----pixfmt_bgra32_pre
}


#endif
