/*============================================================================
*
*   WCSLIB 3.6 - an implementation of the FITS WCS convention.
*   Copyright (C) 1995-2004, Mark Calabretta
*
*   This library is free software; you can redistribute it and/or modify it
*   under the terms of the GNU Library General Public License as published
*   by the Free Software Foundation; either version 2 of the License, or (at
*   your option) any later version.
*
*   This library is distributed in the hope that it will be useful, but
*   WITHOUT ANY WARRANTY; without even the implied warranty of
*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Library
*   General Public License for more details.
*
*   You should have received a copy of the GNU Library General Public License
*   along with this library; if not, write to the Free Software Foundation,
*   Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
*
*   Correspondence concerning WCSLIB may be directed to:
*      Internet email: mcalabre@atnf.csiro.au
*      Postal address: Dr. Mark Calabretta
*                      Australia Telescope National Facility, CSIRO
*                      PO Box 76
*                      Epping NSW 1710
*                      AUSTRALIA
*
*   Author: Mark Calabretta, Australia Telescope National Facility
*   http://www.atnf.csiro.au/~mcalabre/index.html
*   $Id: wcstrig.h,v 1.1 2007/02/19 16:30:12 breddels Exp $
*===========================================================================*/

#ifndef WCSLIB_TRIG
#define WCSLIB_TRIG

#ifdef __cplusplus
extern "C" {
#endif


#ifdef WCSTRIG_MACRO

/* Macro implementation of the trigd functions. */
#include "wcsmath.h"

#define cosd(X) cos((X)*D2R)
#define sind(X) sin((X)*D2R)
#define tand(X) tan((X)*D2R)
#define acosd(X) acos(X)*R2D
#define asind(X) asin(X)*R2D
#define atand(X) atan(X)*R2D
#define atan2d(Y,X) atan2(Y,X)*R2D

#else

/* Use WCSLIB wrappers or native trigd functions. */

double cosd(double);
double sind(double);
double tand(double);
double acosd(double);
double asind(double);
double atand(double);
double atan2d(double, double);

/* Domain tolerance for asin and acos functions. */
#define WCSTRIG_TOL 1e-10

#endif /* WCSTRIG_MACRO */


#ifdef __cplusplus
};
#endif

#endif /* WCSLIB_TRIG */
