/* pgcont.f -- translated by f2c (version 20020208).
   You must link the resulting object file with the libraries:
	-lf2c -lm   (in that order)
*/

#include "f2c.h"

/* Common Block Declarations */

struct {
    integer pgid, pgdevs[8], pgadvs[8], pgnx[8], pgny[8], pgnxc[8], pgnyc[8];
    real pgxpin[8], pgypin[8], pgxsp[8], pgysp[8], pgxsz[8], pgysz[8], pgxoff[
	    8], pgyoff[8], pgxvp[8], pgyvp[8], pgxlen[8], pgylen[8], pgxorg[8]
	    , pgyorg[8], pgxscl[8], pgyscl[8], pgxblc[8], pgxtrc[8], pgyblc[8]
	    , pgytrc[8], trans[6];
    logical pgprmp[8];
    integer pgclp[8], pgfas[8];
    real pgchsz[8];
    integer pgblev[8];
    logical pgrows[8];
    integer pgahs[8];
    real pgaha[8], pgahv[8];
    integer pgtbci[8], pgmnci[8], pgmxci[8], pgcint, pgcmin;
    logical pgpfix[8];
    integer pgitf[8];
    real pghsa[8], pghss[8], pghsp[8];
} pgplt1_;

#define pgplt1_1 pgplt1_

struct {
    char pgclab[32];
} pgplt2_;

#define pgplt2_1 pgplt2_

/* *PGCONT -- contour map of a 2D data array (contour-following) */
/* %void cpgcont(const float *a, int idim, int jdim, int i1, int i2, \ */
/* % int j1, int j2, const float *c, int nc, const float *tr); */
/* + */
/* Subroutine */ int pgcont_(a, idim, jdim, i1, i2, j1, j2, c__, nc, tr)
real *a;
integer *idim, *jdim, *i1, *i2, *j1, *j2;
real *c__;
integer *nc;
real *tr;
{
    /* System generated locals */
    integer a_dim1, a_offset;

    /* Local variables */
    extern /* Subroutine */ int pgcp_();
    static integer i__;
    extern /* Subroutine */ int pgconx_();
    extern logical pgnoto_();


/* Draw a contour map of an array.  The map is truncated if */
/* necessary at the boundaries of the viewport.  Each contour line */
/* is drawn with the current line attributes (color index, style, and */
/* width); except that if argument NC is positive (see below), the line */
/* style is set by PGCONT to 1 (solid) for positive contours or 2 */
/* (dashed) for negative contours. */

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
/*  TR     (input) : array defining a transformation between the I,J */
/*                   grid of the array and the world coordinates. */
/*                   The world coordinates of the array point A(I,J) */
/*                   are given by: */
/*                     X = TR(1) + TR(2)*I + TR(3)*J */
/*                     Y = TR(4) + TR(5)*I + TR(6)*J */
/*                   Usually TR(3) and TR(5) are zero - unless the */
/*                   coordinate transformation involves a rotation or */
/*                   shear. */
/* -- */
/* (7-Feb-1983) */
/* (24-Aug-1984) Revised to add the option of not automatically */
/*       setting the line-style. Sorry about the ugly way this is */
/*       done (negative NC); this is the least incompatible way of doing */
/*       it (TJP). */
/* (21-Sep-1989) Changed to call PGCONX instead of duplicating the code */
/*       [TJP]. */
/* ----------------------------------------------------------------------- */
/* ----------------------------------------------------------------------- */
/* PGPLOT: common block definition. */
/* ----------------------------------------------------------------------- */
/* Maximum number of concurrent devices (should match GRIMAX). */
/* ----------------------------------------------------------------------- */
/* ----------------------------------------------------------------------- */
/* Indentifier of currently selected device. */
/* ----------------------------------------------------------------------- */
/* ----------------------------------------------------------------------- */
/* Device status (indexed by device identifier). */
/* ----------------------------------------------------------------------- */
/* PGDEVS  =0 if device is not open; 1 if device is open. */
/* PGADVS  Set to 0 by PGBEGIN, set to 1 by PGPAGE; used to suppress */
/*         the prompt for the first page. */
/* PROMPT  If .TRUE., ask user before clearing page; set by PGASK */
/*         and (indirectly) by PGBEGIN, used in PGENV. */
/* PGBLEV  Buffering level: incremented by PGBBUF, decremented by */
/*         PGEBUF. */
/* PGPFIX  TRUE if PGPAP has been called, FALSE otherwise. */

/* ----------------------------------------------------------------------- */
/* Panel parameters (indexed by device identification). */
/* ----------------------------------------------------------------------- */
/* NX      Number of panels in x direction */
/* NY      Number of panels in y direction */
/* NXC     Ordinal number of current X panel */
/* NYC     Ordinal number of current Y panel */
/* XSZ     X dimension of panel (device units) */
/* YSZ     Y dimension of panel (device units) */
/* PGROWS  TRUE if panels are used in row order, FALSE for column */
/*         order. */

/* ----------------------------------------------------------------------- */
/* Attributes (indexed by device identification). */
/* ----------------------------------------------------------------------- */
/* PGCLP   clipping enabled/disabed */
/* PGFAS   fill-area style */
/* PGCHSZ  character height */
/* PGAHS   arrow-head fill style */
/* PGAHA   arrow-head angle */
/* PGAHV   arrow-head vent */
/* PGTBCI  text background color index */
/* PGMNCI  lower range of color indices available to PGGRAY/PGIMAG */
/* PGMXCI  upper range of color indices available to PGGRAY/PGIMAG */
/* PGITF   type of transfer function used by PGGRAY/PGIMAG */
/* PGHSA   hatching line angle */
/* PGHSS   hatching line separation */
/* PGHSP   hatching line phase */

/* ----------------------------------------------------------------------- */
/* Viewport parameters (indexed by device identification); all are device */
/* coordinates: */
/* ----------------------------------------------------------------------- */
/* PGXOFF  X coordinate of blc of viewport. */
/* PGYOFF  Y coordinate of blc of viewport. */
/* PGXVP   X coordinate of blc of viewport, relative to blc of subpage. */
/* PGYVP   Y coordinate of blc of viewport, relative to blc of subpage. */
/* PGXLEN  Width of viewport. */
/* PGYLEN  Height of viewport. */

/* ----------------------------------------------------------------------- */
/* Scaling parameters (indexed by device identification): */
/* ----------------------------------------------------------------------- */
/* PGXORG  device coordinate value corresponding to world X=0 */
/* PGYORG  device coordinate value corresponding to world Y=0 */
/* PGXSCL  scale in x (device units per world coordinate unit) */
/* PGYSCL  scale in y (device units per world coordinate unit) */
/* PGXPIN  device x scale in device units/inch */
/* PGYPIN  device y scale in device units/inch */
/* PGXSP   Character X spacing (device units) */
/* PGYSP   Character Y spacing (device units) */

/* ----------------------------------------------------------------------- */
/* Window parameters (indexed by device identification); all are world */
/* coordinate values: */
/* ----------------------------------------------------------------------- */
/* PGXBLC  world X at bottom left corner of window */
/* PGXTRC  world X at top right corner of window */
/* PGYBLC  world Y at bottom left corner of window */
/* PGYTRC  world Y at top right corner of window */

/* ----------------------------------------------------------------------- */
/* The following parameters are used in the contouring routines to pass */
/* information to the action routine. They do not need to be indexed. */
/* ----------------------------------------------------------------------- */
/* TRANS   Transformation matrix for contour plots; copied */
/*         from argument list by PGCONT and used by PGCP. */

/* ----------------------------------------------------------------------- */
/* ----------------------------------------------------------------------- */
/* ----------------------------------------------------------------------- */

    /* Parameter adjustments */
    a_dim1 = *idim;
    a_offset = 1 + a_dim1 * 1;
    a -= a_offset;
    --c__;
    --tr;

    /* Function Body */
    if (pgnoto_("PGCONT", (ftnlen)6)) {
	return 0;
    }

/* Save TRANS matrix. */

    for (i__ = 1; i__ <= 6; ++i__) {
	pgplt1_1.trans[i__ - 1] = tr[i__];
/* L10: */
    }

/* Use PGCONX with external function PGCP, which applies the TRANS */
/* scaling. */

    pgconx_(&a[a_offset], idim, jdim, i1, i2, j1, j2, &c__[1], nc, pgcp_);

} /* pgcont_ */

