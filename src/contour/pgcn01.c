/* pgcn01.f -- translated by f2c (version 20020208).
   You must link the resulting object file with the libraries:
	-lf2c -lm   (in that order)
*/

#include "f2c.h"

/* Table of constant values */

static integer c__0 = 0;
static integer c__1 = 1;

/* Subroutine */ int pgcn01_(z__, mx, my, ia, ib, ja, jb, z0, plot, flags, is,
	 js, sdir, userdata)
real *z__;
integer *mx, *my, *ia, *ib, *ja, *jb;
real *z0;
/* Subroutine */ int (*plot) ();
logical *flags;
integer *is, *js, *sdir;
void *userdata;
{
    /* System generated locals */
    integer z_dim1, z_offset;

    /* Local variables */
    static integer i__, j;
    static real x, y;
    static integer ii, jj;
    static real startx, starty;
    static integer dir;


/* Support routine for PGCNSC. This routine draws a continuous contour, */
/* starting at the specified point, until it either crosses the edge of */
/* the array or closes on itself. */
/* ----------------------------------------------------------------------- */

    /* Parameter adjustments */
    z_dim1 = *mx;
    z_offset = 1 + z_dim1 * 1;
    z__ -= z_offset;
    flags -= 10101;

    /* Function Body */
    i__ = *is;
    j = *js;
    dir = *sdir;
    ii = i__ + 1 - *ia;
    jj = j + 1 - *ja;
    if (dir == 1 || dir == 2) {
	x = (real) i__ + (*z0 - z__[i__ + j * z_dim1]) / (z__[i__ + 1 + j * 
		z_dim1] - z__[i__ + j * z_dim1]);
	y = (real) j;
    } else {
	x = (real) i__;
	y = (real) j + (*z0 - z__[i__ + j * z_dim1]) / (z__[i__ + (j + 1) * 
		z_dim1] - z__[i__ + j * z_dim1]);
    }
/* D    WRITE (*,*) 'SEGMENT' */

/* Move to start of contour and record starting point. */

    (*plot)(&c__0, &x, &y, z0, userdata);
    startx = x;
    starty = y;

/* We have reached grid-point (I,J) going in direction DIR (UP, DOWN, */
/* LEFT, or RIGHT). Look at the other three sides of the cell we are */
/* entering to decide where to go next. It is important to look to the */
/* two sides before looking straight ahead, in order to avoid self- */
/* intersecting contours. If all 3 sides have unused crossing-points, */
/* the cell is "degenerate" and we have to decide which of two possible */
/* pairs of contour segments to draw; at present we make an arbitrary */
/* choice. If we have reached the edge of the array, we have */
/* finished drawing an unclosed contour. If none of the other three */
/* sides of the cell have an unused crossing-point, we must have */
/* completed a closed contour, which requires a final segment back to */
/* the starting point. */

L100:
/* D    WRITE (*,*) I,J,DIR */
    ii = i__ + 1 - *ia;
    jj = j + 1 - *ja;
    switch ((int)dir) {
	case 1:  goto L110;
	case 2:  goto L120;
	case 3:  goto L130;
	case 4:  goto L140;
    }

/* DIR = UP */

L110:
    flags[ii + (jj + 100) * 100] = FALSE_;
    if (j == *jb) {
	return 0;
    } else if (flags[ii + (jj + 200) * 100]) {
	dir = 3;
	goto L200;
    } else if (flags[ii + 1 + (jj + 200) * 100]) {
	dir = 4;
	++i__;
	goto L200;
    } else if (flags[ii + (jj + 101) * 100]) {
/* !        DIR = UP */
	++j;
	goto L250;
    } else {
	goto L300;
    }

/* DIR = DOWN */

L120:
    flags[ii + (jj + 100) * 100] = FALSE_;
    if (j == *ja) {
	return 0;
    } else if (flags[ii + 1 + (jj + 199) * 100]) {
	dir = 4;
	++i__;
	--j;
	goto L200;
    } else if (flags[ii + (jj + 199) * 100]) {
	dir = 3;
	--j;
	goto L200;
    } else if (flags[ii + (jj + 99) * 100]) {
/* !        DIR = DOWN */
	--j;
	goto L250;
    } else {
	goto L300;
    }

/* DIR = LEFT */

L130:
    flags[ii + (jj + 200) * 100] = FALSE_;
    if (i__ == *ia) {
	return 0;
    } else if (flags[ii - 1 + (jj + 100) * 100]) {
	dir = 2;
	--i__;
	goto L250;
    } else if (flags[ii - 1 + (jj + 101) * 100]) {
	dir = 1;
	--i__;
	++j;
	goto L250;
    } else if (flags[ii - 1 + (jj + 200) * 100]) {
/* !        DIR = LEFT */
	--i__;
	goto L200;
    } else {
	goto L300;
    }

/* DIR = RIGHT */

L140:
    flags[ii + (jj + 200) * 100] = FALSE_;
    if (i__ == *ib) {
	return 0;
    } else if (flags[ii + (jj + 101) * 100]) {
	dir = 1;
	++j;
	goto L250;
    } else if (flags[ii + (jj + 100) * 100]) {
	dir = 2;
	goto L250;
    } else if (flags[ii + 1 + (jj + 200) * 100]) {
/* !        DIR = RIGHT */
	++i__;
	goto L200;
    } else {
	goto L300;
    }

/* Draw a segment of the contour. */

L200:
    x = (real) i__;
    y = (real) j + (*z0 - z__[i__ + j * z_dim1]) / (z__[i__ + (j + 1) * 
	    z_dim1] - z__[i__ + j * z_dim1]);
    (*plot)(&c__1, &x, &y, z0, userdata);
    goto L100;
L250:
    x = (real) i__ + (*z0 - z__[i__ + j * z_dim1]) / (z__[i__ + 1 + j * 
	    z_dim1] - z__[i__ + j * z_dim1]);
    y = (real) j;
    (*plot)(&c__1, &x, &y, z0, userdata);
    goto L100;

/* Close the contour and go look for another one. */

L300:
    (*plot)(&c__1, &startx, &starty, z0, userdata);
    return 0;

} /* pgcn01_ */

