/* pgconx.f -- translated by f2c (version 20020208).
   You must link the resulting object file with the libraries:
	-lf2c -lm   (in that order)
*/

#include "f2c.h"

/* Table of constant values */

static integer c__1 = 1;
static integer c__2 = 2;

/* *PGCONX -- contour map of a 2D data array (non rectangular) */
/* + */
/* Subroutine */ int pgconx_(a, idim, jdim, i1, i2, j1, j2, c__, nc, plot, userdata)
real *a;
integer *idim, *jdim, *i1, *i2, *j1, *j2;
real *c__;
integer *nc;
/* Subroutine */ int (*plot) ();
void *userdata;
{
    /* System generated locals */
    integer a_dim1, a_offset, i__1, i__2, i__3, i__4;

    /* Local variables */
    static integer i__;
    extern /* Subroutine */ int pgqls_(), pgsls_();
    static logical style;
    static integer ia, ib, ja, jb, ki, kj, ls, kx, ky;
    extern /* Subroutine */ int pgbbuf_();
    static integer px, py;
    extern /* Subroutine */ int pgebuf_(), pgcnsc_(), grwarn_();
    extern logical pgnoto_();
    static integer nnx, nny;


/* Draw a contour map of an array using a user-supplied plotting */
/* routine.  This routine should be used instead of PGCONT when the */
/* data are defined on a non-rectangular grid.  PGCONT permits only */
/* a linear transformation between the (I,J) grid of the array */
/* and the world coordinate system (x,y), but PGCONX permits any */
/* transformation to be used, the transformation being defined by a */
/* user-supplied subroutine. The nature of the contouring algorithm, */
/* however, dictates that the transformation should maintain the */
/* rectangular topology of the grid, although grid-points may be */
/* allowed to coalesce.  As an example of a deformed rectangular */
/* grid, consider data given on the polar grid theta=0.1n(pi/2), */
/* for n=0,1,...,10, and r=0.25m, for m=0,1,..,4. This grid */
/* contains 55 points, of which 11 are coincident at the origin. */
/* The input array for PGCONX should be dimensioned (11,5), and */
/* data values should be provided for all 55 elements.  PGCONX can */
/* also be used for special applications in which the height of the */
/* contour affects its appearance, e.g., stereoscopic views. */

/* The map is truncated if necessary at the boundaries of the viewport. */
/* Each contour line is drawn with the current line attributes (color */
/* index, style, and width); except that if argument NC is positive */
/* (see below), the line style is set by PGCONX to 1 (solid) for */
/* positive contours or 2 (dashed) for negative contours. Attributes */
/* for the contour lines can also be set in the user-supplied */
/* subroutine, if desired. */

/* Arguments: */
/*  A      (input) : data array. */
/*  IDIM   (input) : first dimension of A. */
/*  JDIM   (input) : second dimension of A. */
/*  I1, I2 (input) : range of first index to be contoured (inclusive). */
/*  J1, J2 (input) : range of second index to be contoured (inclusive). */
/*  C      (input) : array of NC contour levels; dimension at least NC. */
/*  NC     (input) : +/- number of contour levels (less than or equal */
/*                   to dimension of C). If NC is positive, it is the */
/*                   number of contour levels, and the line-style is */
/*                   chosen automatically as described above. If NC is */
/*                   negative, it is minus the number of contour */
/*                   levels, and the current setting of line-style is */
/*                   used for all the contours. */
/*  PLOT   (input) : the address (name) of a subroutine supplied by */
/*                   the user, which will be called by PGCONX to do */
/*                   the actual plotting. This must be declared */
/*                   EXTERNAL in the program unit calling PGCONX. */

/* The subroutine PLOT will be called with four arguments: */
/*      CALL PLOT(VISBLE,X,Y,Z) */
/* where X,Y (input) are real variables corresponding to */
/* I,J indices of the array A. If  VISBLE (input, integer) is 1, */
/* PLOT should draw a visible line from the current pen */
/* position to the world coordinate point corresponding to (X,Y); */
/* if it is 0, it should move the pen to (X,Y). Z is the value */
/* of the current contour level, and may be used by PLOT if desired. */
/* Example: */
/*       SUBROUTINE PLOT (VISBLE,X,Y,Z) */
/*       REAL X, Y, Z, XWORLD, YWORLD */
/*       INTEGER VISBLE */
/*       XWORLD = X*COS(Y) ! this is the user-defined */
/*       YWORLD = X*SIN(Y) ! transformation */
/*       IF (VISBLE.EQ.0) THEN */
/*           CALL PGMOVE (XWORLD, YWORLD) */
/*       ELSE */
/*           CALL PGDRAW (XWORLD, YWORLD) */
/*       END IF */
/*       END */
/* -- */
/* 14-Nov-1985 - new routine [TJP]. */
/* 12-Sep-1989 - correct documentation error [TJP]. */
/* 22-Apr-1990 - corrected bug in panelling algorithm [TJP]. */
/* 13-Dec-1990 - make errors non-fatal [TJP]. */
/* ----------------------------------------------------------------------- */

/* Check arguments. */

    /* Parameter adjustments */
    a_dim1 = *idim;
    a_offset = 1 + a_dim1 * 1;
    a -= a_offset;
    --c__;

    /* Function Body */
    if (pgnoto_("PGCONX", (ftnlen)6)) {
	return 0;
    }
    if (*i1 < 1 || *i2 > *idim || *i1 >= *i2 || *j1 < 1 || *j2 > *jdim || *j1 
	    >= *j2) {
	grwarn_("PGCONX: invalid range I1:I2, J1:J2", (ftnlen)34);
	printf("%i %i %i %i %i %i\n", i1, i2, j1, j2, idim, jdim);
	return 0;
    }
    if (*nc == 0) {
	return 0;
    }
    style = *nc > 0;
    //pgqls_(&ls);
    //pgbbuf_();

/* Divide arrays into panels not exceeding MAXEMX by MAXEMY for */
/* contouring by PGCNSC. */

/* D    write (*,*) 'PGCONX window:',i1,i2,j1,j2 */
    nnx = *i2 - *i1 + 1;
    nny = *j2 - *j1 + 1;
/* Computing MAX */
    i__1 = 1, i__2 = (nnx + 98) / 99;
    kx = max(i__1,i__2);
/* Computing MAX */
    i__1 = 1, i__2 = (nny + 98) / 99;
    ky = max(i__1,i__2);
    px = (nnx + kx - 1) / kx;
    py = (nny + ky - 1) / ky;
    i__1 = kx;
    for (ki = 1; ki <= i__1; ++ki) {
	ia = *i1 + (ki - 1) * px;
/* Computing MIN */
	i__2 = *i2, i__3 = ia + px;
	ib = min(i__2,i__3);
	i__2 = ky;
	for (kj = 1; kj <= i__2; ++kj) {
	    ja = *j1 + (kj - 1) * py;
/* Computing MIN */
	    i__3 = *j2, i__4 = ja + py;
	    jb = min(i__3,i__4);

/*             Draw the contours in one panel. */

/* D            write (*,*) 'PGCONX panel:',ia,ib,ja,jb */
	    if (style) {
		//pgsls_(&c__1);
	    }
	    i__3 = abs(*nc);
	    for (i__ = 1; i__ <= i__3; ++i__) {
		if (style && c__[i__] < (float)0.) {
		    //pgsls_(&c__2);
		}
		pgcnsc_(&a[a_offset], idim, jdim, &ia, &ib, &ja, &jb, &c__[
			i__], plot, userdata);
		if (style) {
		    //pgsls_(&c__1);
		}
/* L40: */
	    }
/* L50: */
	}
/* L60: */
    }

    //pgsls_(&ls);
    //pgebuf_();
} /* pgconx_ */

