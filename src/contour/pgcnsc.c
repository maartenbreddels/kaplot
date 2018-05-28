/* pgcnsc.f -- translated by f2c (version 20020208).
   You must link the resulting object file with the libraries:
	-lf2c -lm   (in that order)
*/

#include "f2c.h"

/* Table of constant values */

static integer c__1 = 1;
static integer c__3 = 3;
static integer c__2 = 2;
static integer c__4 = 4;

/* Subroutine */ int pgcnsc_(z__, mx, my, ia, ib, ja, jb, z0, plot, userdata)
real *z__;
integer *mx, *my, *ia, *ib, *ja, *jb;
real *z0;
/* Subroutine */ int (*plot) ();
void *userdata;
{
    /* System generated locals */
    integer z_dim1, z_offset, i__1, i__2;

    /* Local variables */
    static integer i__, j;
    extern /* Subroutine */ int pgcn01_();
    static logical flags[20000]	/* was [100][100][2] */;
    static real z1, z2, z3;
    static integer ii, jj;
    extern /* Subroutine */ int grwarn_();
    static integer dir;


/* PGPLOT (internal routine): Draw a single contour.  This routine is */
/* called by PGCONT, but may be called directly by the user. */

/* Arguments: */

/* Z (real array dimension MX,MY, input): the array of function values. */
/* MX,MY (integer, input): actual declared dimension of Z(*,*). */
/* IA,IB (integer, input): inclusive range of the first index of Z to be */
/*       contoured. */
/* JA,JB (integer, input): inclusive range of the second index of Z to */
/*       be contoured. */
/* Z0 (real, input): the contour level sought. */
/* PLOT (the name of a subroutine declared EXTERNAL in the calling */
/*       routine): this routine is called by PGCNSC to do all graphical */
/*       output. The calling sequence is CALL PLOT(K,X,Y,Z) where Z is */
/*       the contour level, (X,Y) are the coordinates of a point (in the */
/*       inclusive range I1<X<I2, J1<Y<J2, and if K is 0, the routine is */
/*       to move then pen to (X,Y); if K is 1, it is to draw a line from */
/*       the current position to (X,Y). */

/* NOTE:  the intervals (IA,IB) and (JA,JB) must not exceed the */
/* dimensions of an internal array. These are currently set at 100. */
/* -- */
/* 17-Sep-1989 - Completely rewritten [TJP]. The algorithm is my own, */
/*               but it is probably not original. It could probably be */
/*               coded more briefly, if not as clearly. */
/*  1-May-1994 - Modified to draw contours anticlockwise about maxima, */
/*               to prevent contours at different levels from */
/*               crossing in degenerate cells [TJP]. */
/* ----------------------------------------------------------------------- */


/* The statement function RANGE decides whether a contour at level P */
/* crosses the line between two gridpoints with values P1 and P2. It is */
/* important that a contour cannot cross a line with equal endpoints. */


/* Check for errors. */

    /* Parameter adjustments */
    z_dim1 = *mx;
    z_offset = 1 + z_dim1 * 1;
    z__ -= z_offset;

    /* Function Body */
    if (*ib - *ia + 1 > 100 || *jb - *ja + 1 > 100) {
	grwarn_("PGCNSC - array index range exceeds built-in limit of 100", (
		ftnlen)56);
	return 0;
    }

/* Initialize the flags. The first flag for a gridpoint is set if */
/* the contour crosses the line segment to the right of the gridpoint */
/* (joining [I,J] to [I+1,J]); the second flag is set if if it crosses */
/* the line segment above the gridpoint (joining [I,J] to [I,J+1]). */
/* The top and right edges require special treatment. (For purposes */
/* of description only, we assume I increases horizontally to the right */
/* and J increases vertically upwards.) */

    i__1 = *ib;
    for (i__ = *ia; i__ <= i__1; ++i__) {
	ii = i__ - *ia + 1;
	i__2 = *jb;
	for (j = *ja; j <= i__2; ++j) {
	    jj = j - *ja + 1;
	    z1 = z__[i__ + j * z_dim1];
	    flags[ii + (jj + 100) * 100 - 10101] = FALSE_;
	    flags[ii + (jj + 200) * 100 - 10101] = FALSE_;
	    if (i__ < *ib) {
		z2 = z__[i__ + 1 + j * z_dim1];
		if (*z0 > dmin(z1,z2) && *z0 <= dmax(z1,z2) && z1 != z2) {
		    flags[ii + (jj + 100) * 100 - 10101] = TRUE_;
		}
	    }
	    if (j < *jb) {
		z3 = z__[i__ + (j + 1) * z_dim1];
		if (*z0 > dmin(z1,z3) && *z0 <= dmax(z1,z3) && z1 != z3) {
		    flags[ii + (jj + 200) * 100 - 10101] = TRUE_;
		}
	    }
/* L10: */
	}
/* L20: */
    }

/* Search the edges of the array for the start of an unclosed contour. */
/* Note that (if the algorithm is implemented correctly) all unclosed */
/* contours must begin and end at the edge of the array. When one is */
/* found, call PGCN01 to draw the contour, telling it the correct */
/* starting direction so that it follows the contour into the array */
/* instead of out of it. A contour is only started if the higher */
/* ground lies to the left: this is to enforce the direction convention */
/* that contours are drawn anticlockwise around maxima. If the high */
/* ground lies to the right, we will find the other end of the contour */
/* and start there. */

/* Bottom edge. */

    j = *ja;
    jj = j - *ja + 1;
    i__1 = *ib - 1;
    for (i__ = *ia; i__ <= i__1; ++i__) {
	ii = i__ - *ia + 1;
	if (flags[ii + (jj + 100) * 100 - 10101] && z__[i__ + j * z_dim1] > 
		z__[i__ + 1 + j * z_dim1]) {
	    pgcn01_(&z__[z_offset], mx, my, ia, ib, ja, jb, z0, plot, flags, &
		    i__, &j, &c__1, userdata);
	}
/* L26: */
    }

/* Right edge. */

    i__ = *ib;
    ii = i__ - *ia + 1;
    i__1 = *jb - 1;
    for (j = *ja; j <= i__1; ++j) {
	jj = j - *ja + 1;
	if (flags[ii + (jj + 200) * 100 - 10101] && z__[i__ + j * z_dim1] > 
		z__[i__ + (j + 1) * z_dim1]) {
	    pgcn01_(&z__[z_offset], mx, my, ia, ib, ja, jb, z0, plot, flags, &
		    i__, &j, &c__3, userdata);
	}
/* L27: */
    }

/* Top edge. */

    j = *jb;
    jj = j - *ja + 1;
    i__1 = *ia;
    for (i__ = *ib - 1; i__ >= i__1; --i__) {
	ii = i__ - *ia + 1;
	if (flags[ii + (jj + 100) * 100 - 10101] && z__[i__ + 1 + j * z_dim1] 
		> z__[i__ + j * z_dim1]) {
	    pgcn01_(&z__[z_offset], mx, my, ia, ib, ja, jb, z0, plot, flags, &
		    i__, &j, &c__2, userdata);
	}
/* L28: */
    }

/* Left edge. */

    i__ = *ia;
    ii = i__ - *ia + 1;
    i__1 = *ja;
    for (j = *jb - 1; j >= i__1; --j) {
	jj = j - *ja + 1;
	if (flags[ii + (jj + 200) * 100 - 10101] && z__[i__ + (j + 1) * 
		z_dim1] > z__[i__ + j * z_dim1]) {
	    pgcn01_(&z__[z_offset], mx, my, ia, ib, ja, jb, z0, plot, flags, &
		    i__, &j, &c__4, userdata);
	}
/* L29: */
    }

/* Now search the interior of the array for a crossing point, which will */
/* lie on a closed contour (because all unclosed contours have been */
/* eliminated). It is sufficient to search just the horizontal crossings */
/* (or the vertical ones); any closed contour must cross a horizontal */
/* and a vertical gridline. PGCN01 assumes that when it cannot proceed */
/* any further, it has reached the end of a closed contour. Thus all */
/* unclosed contours must be eliminated first. */

    i__1 = *ib - 1;
    for (i__ = *ia + 1; i__ <= i__1; ++i__) {
	ii = i__ - *ia + 1;
	i__2 = *jb - 1;
	for (j = *ja + 1; j <= i__2; ++j) {
	    jj = j - *ja + 1;
	    if (flags[ii + (jj + 100) * 100 - 10101]) {
		dir = 1;
		if (z__[i__ + 1 + j * z_dim1] > z__[i__ + j * z_dim1]) {
		    dir = 2;
		}
		pgcn01_(&z__[z_offset], mx, my, ia, ib, ja, jb, z0, plot, 
			flags, &i__, &j, &dir, userdata);
	    }
/* L30: */
	}
/* L40: */
    }

/* We didn't find any more crossing points: we're finished. */

    return 0;
} /* pgcnsc_ */

