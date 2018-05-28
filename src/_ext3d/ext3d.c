#define KAPLOT_EXT3D_MODULE
#include <ext3d.h>
#include <Python.h>
#include <libnumarray.h>
#include "cinterface.h"

#define TRUE 1
#define FALSE 0

void _line(void* userdata, line_callback callback, double* xvalues, double* yvalues, double* zvalues, int width, int height, int xi1, int yi1, int xi2, int yi2)
{
	double rx1 = xvalues[xi1+yi1*width];
	double ry1 = yvalues[xi1+yi1*width];
	double rz1 = zvalues[xi1+yi1*width];
	double rx2 = xvalues[xi2+yi2*width];
	double ry2 = yvalues[xi2+yi2*width];
	double rz2 = zvalues[xi2+yi2*width];
	double x1, y1, z1, x2, y2, z2;
	int rest = 1;
	double su[4], sv[4];
	double svmin, svmax;
	double svminon, svmaxon;
	double vx, vy;
	double ux, uy;
	double uxt[4], uyt[4];
	double tempx, tempy;
	double dx, dy;
	int clipped = 0;
	int hidden = 0;
	int x, z, i;
	double d1[4];
	double d2[4];
	double zavg;
	double distancesign;
	int done = 0;
	//printf("%i %i %i %i\n", x1, y1, x2, y2);
	int debug = 0;
	double xt[4];
	double yt[4];
	int count = 0;
	int intersections;

	while(rest)
	{
		hidden = FALSE;
		x1 = rx1;
		y1 = ry1;
		z1 = rz1;
		x2 = rx2;
		y2 = ry2;
		z2 = rz2;
		rest = FALSE;
		/*if(count > 0)
		{
			printf("repeat for %i %i %i %i\n
		}*/

		count++;
		done = FALSE;
		for(z = 0; z < height-1 && !done; z++)
		{
			for(x = 0; x < width-1 && !done; x++)
			{
				//if(zvalues[xi1+yi1*width]

				if(
					(yi1 == yi2 && !((z == yi1 || z == (yi1-1)) && x == xi1)) ||
					(xi1 == xi2 && !((x == xi1 || x == (xi1-1)) && z == yi1))
				)
				{
					if((xi1 == 8 && yi1 == 9 && yi1 == yi2) && x == 8 && z ==7)
						printf("HOEBAHOEBAHOEBAHOEBAHOEBAHOEBAHOEBAHOEBAHOEBA");
					vx = x2-x1;
					vy = y2-y1;
					//clipped = 1;
					// hor line
					// right
					ux = xvalues[(x+1)+z*width] - xvalues[x+z*width];
					uy = yvalues[(x+1)+z*width] - yvalues[x+z*width];
					xt[0] = xvalues[x+z*width];
					yt[0] = yvalues[x+z*width];
					su[0] = (-yvalues[x+z*width]*vx + y1*vx + xvalues[x+z*width]*vy-x1*vy) / (uy*vx-ux*vy);
					sv[0] = ( yvalues[x+z*width]*ux - y1*ux - xvalues[x+z*width]*uy+x1*uy) / (-uy*vx+ux*vy);
					d1[0] = ((ux * (yvalues[x+z*width] - y1) - (xvalues[x+z*width] - x1) * uy)) / sqrt(ux*ux + uy*uy);
					d2[0] = ((ux * (yvalues[x+z*width] - y2) - (xvalues[x+z*width] - x2) * uy)) / sqrt(ux*ux + uy*uy);
					uxt[0] = ux;
					uyt[0] = uy;
					//d1[0] = (uy * x1 - ux*y1 + (xvalues[x+z*width]*yvalues[(x+1)+z*width] - xvalues[(x+1)+z*width]*yvalues[x+z*width]))/ sqrt(ux*ux + uy*uy);
					//d2[0] = (uy * x2 - ux*y2 + (xvalues[x+z*width]*yvalues[(x+1)+z*width] - xvalues[(x+1)+z*width]*yvalues[x+z*width]))/ sqrt(ux*ux + uy*uy);

					// up
					ux = xvalues[(x+1)+(z+1)*width] - xvalues[(x+1)+z*width];
					uy = yvalues[(x+1)+(z+1)*width] - yvalues[(x+1)+z*width];
					xt[1] = xvalues[(x+1)+z*width];
					yt[1] = yvalues[(x+1)+z*width];
					su[1] = (-yvalues[(x+1)+z*width]*vx + y1*vx + xvalues[(x+1)+z*width]*vy-x1*vy) / (uy*vx-ux*vy);
					sv[1] = ( yvalues[(x+1)+z*width]*ux - y1*ux - xvalues[(x+1)+z*width]*uy+x1*uy) / (-uy*vx+ux*vy);
					d1[1] = ((ux * (yvalues[(x+1)+z*width] - y1) - (xvalues[(x+1)+z*width] - x1) * uy)) / sqrt(ux*ux + uy*uy);
					d2[1] = ((ux * (yvalues[(x+1)+z*width] - y2) - (xvalues[(x+1)+z*width] - x2) * uy)) / sqrt(ux*ux + uy*uy);
					uxt[1] = ux;
					uyt[1] = uy;
					//d1[1] = (uy * x1 - ux*y1 + (xvalues[(x+1)+z*width]*yvalues[(x+1)+(z+1)*width] - xvalues[(x+1)+(z+1)*width]*yvalues[(x+1)+z*width]))/ sqrt(ux*ux + uy*uy);
					//d2[1] = (uy * x2 - ux*y2 + (xvalues[(x+1)+z*width]*yvalues[(x+1)+(z+1)*width] - xvalues[(x+1)+(z+1)*width]*yvalues[(x+1)+z*width]))/ sqrt(ux*ux + uy*uy);

					// left
					ux = xvalues[x+(z+1)*width] - xvalues[(x+1)+(z+1)*width];
					uy = yvalues[x+(z+1)*width] - yvalues[(x+1)+(z+1)*width];
					xt[2] = xvalues[(x+1)+(z+1)*width];
					yt[2] = yvalues[(x+1)+(z+1)*width];
					su[2] = (-yvalues[(x+1)+(z+1)*width]*vx + y1*vx + xvalues[(x+1)+(z+1)*width]*vy-x1*vy) / (uy*vx-ux*vy);
					sv[2] = ( yvalues[(x+1)+(z+1)*width]*ux - y1*ux - xvalues[(x+1)+(z+1)*width]*uy+x1*uy) / (-uy*vx+ux*vy);
					d1[2] = ((ux * (yvalues[(x+1)+(z+1)*width] - y1) - (xvalues[(x+1)+(z+1)*width] - x1) * uy)) / sqrt(ux*ux + uy*uy);
					d2[2] = ((ux * (yvalues[(x+1)+(z+1)*width] - y2) - (xvalues[(x+1)+(z+1)*width] - x2) * uy)) / sqrt(ux*ux + uy*uy);
					uxt[2] = ux;
					uyt[2] = uy;
					//d1[2] = (uy * x1 - ux*y1 + (xvalues[(x+1)+(z+1)*width]*yvalues[x+(z+1)*width] - xvalues[x+(z+1)*width]*yvalues[(x+1)+(z+1)*width]))/ sqrt(ux*ux + uy*uy);
					//d2[2] = (uy * x2 - ux*y2 + (xvalues[(x+1)+(z+1)*width]*yvalues[x+(z+1)*width] - xvalues[x+(z+1)*width]*yvalues[(x+1)+(z+1)*width]))/ sqrt(ux*ux + uy*uy);

					// down
					ux = xvalues[x+z*width] - xvalues[x+(z+1)*width];
					uy = yvalues[x+z*width] - yvalues[x+(z+1)*width];
					xt[3] = xvalues[x+(z+1)*width];
					yt[3] = yvalues[x+(z+1)*width];
					su[3] = (-yvalues[x+(z+1)*width]*vx + y1*vx + xvalues[x+(z+1)*width]*vy-x1*vy) / (uy*vx-ux*vy);
					sv[3] = ( yvalues[x+(z+1)*width]*ux - y1*ux - xvalues[x+(z+1)*width]*uy+x1*uy) / (-uy*vx+ux*vy);
					d1[3] = ((ux * (yvalues[x+(z+1)*width] - y1) - (xvalues[x+(z+1)*width] - x1) * uy)) / sqrt(ux*ux + uy*uy);
					d2[3] = ((ux * (yvalues[x+(z+1)*width] - y2) - (xvalues[x+(z+1)*width] - x2) * uy)) / sqrt(ux*ux + uy*uy);
					uxt[3] = ux;
					uyt[3] = uy;
					//d1[3] = (uy * x1 - ux*y1 + (xvalues[x+(z+1)*width]*yvalues[x+z*width] - xvalues[x+z*width]*yvalues[x+(z+1)*width]))/ sqrt(ux*ux + uy*uy);
					//d2[3] = (uy * x2 - ux*y2 + (xvalues[x+(z+1)*width]*yvalues[x+z*width] - xvalues[x+z*width]*yvalues[x+(z+1)*width]))/ sqrt(ux*ux + uy*uy);
					zavg = (zvalues[x+z*width] + zvalues[(x+1)+z*width] + zvalues[x+(z+1)*width] + zvalues[(x+1)+(z+1)*width])/4.0;
					if(xi1 == 11 && yi1 == 11 && xi2 == 12 && yi2 == 11)// && x == 12 && z == 8)
					{
						//printf("%i %i\n", x, z);
						//printf("%f %f %f %f %f %f %f %f\n", d1[0], d1[1], d1[2], d1[3], d2[0], d2[1], d2[2], d2[3]);
					}
					if(	(xvalues[(x+0)+(z+1)*width]-xvalues[(x+1)+(z+0)*width]) *
						(yvalues[(x+1)+(z+1)*width]-yvalues[(x+1)+(z+0)*width]) >=
						(yvalues[(x+0)+(z+1)*width]-yvalues[(x+1)+(z+0)*width]) *
						(xvalues[(x+1)+(z+1)*width]-xvalues[(x+1)+(z+0)*width]))
						distancesign = -1;
					else
						distancesign = 1;


					#define epsilon 1.0e-5
					//distancesign = 1;
		//if(!(xi1 == 17 && yi1 == 11 && yi1 == yi2))
					/*if(xi1 == 0 && yi1 == 10 && yi1 == yi2 && x == 2 && z == 7)
					{
						printf("! %f %f / %i %i\n", svmin, svmax, x, z);
						printf("%f %f %f %f %f %f %f %f\n", sv[0], sv[1], sv[2], sv[3], su[0], su[1], su[2], su[3]);
						printf("%g %f %f %f %f %f %f %f\n", d1[0], d1[1], d1[2], d1[3], d2[0], d2[1], d2[2], d2[3]);
						printf("%f %f %f %i %i %i %i %i\n", distancesign, (z1+z2)/2, zavg, (distancesign*d1[0] <= 0.0 && distancesign*d1[1] <= 0 && distancesign*d1[2] <= 0 && distancesign*d1[3] <= 0),
							distancesign*d1[0] <= 0.0, distancesign*d1[1] <= 0, distancesign*d1[2] <= 0, distancesign*d1[3] <= 0);
					}*/

					if((z1+z2)/2 > zavg)
					{
						svmin = 10.0;
						svminon = 10.0;
						svmax = -10.0;
						svmaxon = -10.0;
						intersections = 0;
						for(i = 0; i < 4; i++)
						{
							dx = (xt[i] + su[i] * uxt[i]) - (x1 + sv[i] * vx);
							dy = (yt[i] + su[i] * uyt[i]) - (y1 + sv[i] * vy);
							if(sqrt(dx*dx + dy*dy) < sqrt(vx*vx + vy * vy) / 10.0)
							{
								if(sv[i] < svminon && sv[i] >= -epsilon && sv[i] <= 1 && su[i] >= -epsilon && su[i] <= 1) // && (uy*vx-ux*vy) > 0.01)
									svminon = sv[i];
								if(sv[i] > svmaxon && sv[i] >= -epsilon && sv[i] <= 1 && su[i] >= -epsilon && su[i] <= 1) // && (uy*vx-ux*vy) > 0.01)
									svmaxon = sv[i];
								if(sv[i] > svmax && su[i] >= 0 && su[i] <= 1)
									svmax = sv[i];
								if(sv[i] < svmin && su[i] >= 0 && su[i] <= 1)
									svmin = sv[i];
								intersections++;
							}
						}

						/*
						if((xi1 == 8 && yi1 == 9 && yi1 == yi2) && (svmin < svmax))// && x == 15 && z < 1)
						{
								printf("\n*** %f %f %f %f / %i %i (%f, %f, %f)\n", svmin, svmax, svminon, svmaxon, x, z, sqrt(vx*vx + vy * vy) / 10.0, vx, vy);
								printf("%f %f %f %f %f %f %f %f\n", sv[0], sv[1], sv[2], sv[3], su[0], su[1], su[2], su[3]);
								printf("%f %f %f %f %f %f %f %f\n\n", d1[0], d1[1], d1[2], d1[3], d2[0], d2[1], d2[2], d2[3]);
						}
						else if((xi1 == 8 && yi1 == 9 && yi1 == yi2))
							printf("--> %f %f %f %f - %i %i\n", svmin, svmax, svminon, svmaxon, x, z);
						*/

						//if((xi1 == 0 && yi1 == 8 && xi1 == xi2) && x == 0 && z ==7)
						//if((xi1 == 8 && yi1 == 6) && xi1 == xi2 && x == 9)


						//if(xi1 == 7 && yi1 == 9 && xi1 == xi2 && (svmin < svmax))
						//if((xi1 == 0 && yi1 == 9 && xi1 == xi2) && x == 0 && z ==7)
						//if((xi1 == 1 && yi1 == 1 && xi1 == xi2))// && x == 0 && z ==7)
						//if((xi1 == 4 && yi1 >= 10 && yi2 <= 10 && yi1 == yi2) && x == 5 && z ==7)
						if((xi1 == 10 && yi1 >= 9 && yi2 <= 9		 && xi1 == xi2))
						{
							hidden = 1;
							printf("dsadsadsadsadsadsa\n\n\n\n\n[%i]", intersections);
							printf("\n!!! %f %f %f %f / %i %i (%f, %f, %f)\n", svmin, svmax, svminon, svmaxon, x, z, sqrt(vx*vx + vy * vy) / 10.0, vx, vy);
							printf("%f %f %f %f %f %f %f %f\n", sv[0], sv[1], sv[2], sv[3], su[0], su[1], su[2], su[3]);
							printf("%f %f %f %f %f %f %f %f\n\n", d1[0], d1[1], d1[2], d1[3], d2[0], d2[1], d2[2], d2[3]);
							printf("%i %i %i %i %i\n", intersections > 0, svmin < svmax, svmin < epsilon, svmax > -epsilon,((svmin < epsilon && svmaxon < (1+epsilon)) ||
									(svmin < (1+epsilon))) && svmax > (1-epsilon));
						}



						if(intersections > 0)
						if(svmin < svmax)
						if(svmin < epsilon) // there are lines behind, inclusive
						{
							if(svmax > -epsilon) // there are lines in front, inclusive
							{
								// if the first intersection point is in range [0,1],  the whole line is hidden
								//if(svminon >= svmin && svmaxon <= svmax && (svminon > (1-epsilon) || svminon < epsilon))
								//if(svminon >= -epsilon && svmaxon <= (1+epsilon) && svminon < (svmaxon-epsilon))
								//if(svmax > epsilon && (svminon < epsilon || svminon > (1-epsilon)) && svmaxon > (1-epsilon))
								if( ((svmin < epsilon && svmaxon < (1+epsilon)) ||
									(svmin < (1+epsilon))) && svmax > (1-epsilon)
								)
								{
									//printf("%f %f\n", svminon, svmaxon);
									/*printf("***************************\n");
									printf("%i %i / %i %i / %i %i\n", x, z, xi1, yi1, xi2, yi2);
									printf("%f %f %f %f %f %f %f %f\n", sv[0], sv[1], sv[2], sv[3], su[0], su[1], su[2], su[3]);
									*/
									hidden = 1;
									done = TRUE;
									printf("1");
								}
								else // the first part is hidden
								if(svminon <= (1+epsilon))
								{
									if(svminon < epsilon && svmaxon < (1+epsilon))
									{
										x1 = x1 + svmaxon * vx;
										y1 = y1 + svmaxon * vy;
									}
									else
									{
										x1 = x1 + svminon * vx;
										y1 = y1 + svminon * vy;
									}

									/*
									printf("2 --> ");
									printf("%f %f\n", svminon, svmaxon);
									printf("%i %i / %i %i / %i %i\n", x, z, xi1, yi1, xi2, yi2);
									printf("%f %f %f %f %f %f %f %f\n", sv[0], sv[1], sv[2], sv[3], su[0], su[1], su[2], su[3]);
									printf("***************************\n");
									*/
								}
								else
								{
									printf("N");
								}

							}
							else
							{
								// just visible
								printf(".");
								/*printf("impossible: ");
								printf(" %f %f %f %f / %i %i (%f, %f, %f)\n", svmin, svmax, svminon, svmaxon, x, z, sqrt(vx*vx + vy * vy) / 10.0, vx, vy);
								printf("%f %f %f %f %f %f %f %f\n", sv[0], sv[1], sv[2], sv[3], su[0], su[1], su[2], su[3]);
								*/
							}

						}
						else
						{
							if(svmax > epsilon) // there are lines in front
							{
								 // the middle part is hidden
								if(svmaxon > svminon && svmaxon < (1-epsilon))// && svmaxon > epsilon && svminon < (1.0-epsilon) && svminon > epsilon)
								{
									if(rest)
										printf("REST!");
									if(!rest)
									{
										rx1 = x1 + (svmaxon+0.1) * vx;
										ry1 = y1 + (svmaxon+0.1) * vy;
										rx2 = x2;
										ry2 = y2;
										rest = TRUE;
									}
									x2 = x1 + (svminon) * vx;
									y2 = y1 + (svminon) * vy;
									//printf("\n** %f %f **\n", svminon, svmaxon);
									printf("+");
								}
								else
								if(svminon < (1.0-epsilon)) // the end is hidden
								{
									x2 = x1 + svminon * vx;
									y2 = y1 + svminon * vy;
									printf("3");
								}
								else // no intersection
								{
									printf("4");
								}
							}
							else
							{
								printf("impossible\n");
							}
						}
					}
				}
			}
		}
		if(!hidden)
		//if(!(xi1 > 8 && xi1 < 10 && yi1 > 9 && yi2 < 11))
		//if(!(xi1 == 9 && yi1 == 10 && yi1 == yi2))
		//if(!(xi1 == 16 && yi1 == 9 && yi1 == yi2))
		//if(!(xi1 == 9 && yi1 == 0 && yi1 == yi2))
		//if(!(xi1 == 1 && yi1 == 12 && yi1 == yi2))
		//if(!(xi1 == 14 && yi1 == 1 && yi1 == yi2))
		//if(!(xi1 == 14 && yi1 == 1 && yi1 == yi2))
		//if(!(xi1 == 18 && yi1 == 12 && xi1 == xi2))
		//if(!(xi1 >= 9 && xi1 <= 9 && yi1 >= 10 && yi2 <= 12))
		//if(!(xi1 == 9 && yi1 == 10 && yi1 == yi2))
		//if(!(xi1 == 8 && yi1 == 9 && yi1 == yi2))
			callback(userdata, x1, y1, x2, y2);
	}
}

void PyKaplot_Wireframe(double* data2d, int width, int height, double matrix[4][4], line_callback callback, void* userdata)
{
	//callback(userdata, 0, 1, 2,3, 4,5);
	int x, z;
	double *xvalues;
	double *yvalues;
	double *zvalues;
	//double *wvalues;
	double w;

	xvalues = (double*)malloc(sizeof(double) * width * height);
	yvalues = (double*)malloc(sizeof(double) * width * height);
	zvalues = (double*)malloc(sizeof(double) * width * height);
	//wvalues = (double*)malloc(sizeof(double) * width * height);

	for(z = 0; z < height; z++)
	{
		for(x = 0; x < width; x++)
		{
			w =						matrix[3][0] * x +
									matrix[3][1] * data2d[x + z*width] +
									matrix[3][2] * z +
									matrix[3][3];
			xvalues[x+z*width] =(	matrix[0][0] * x +
									matrix[0][1] * data2d[x + z*width] +
									matrix[0][2] * z +
									matrix[0][3]) / w;
			yvalues[x+z*width] =(	matrix[1][0] * x +
									matrix[1][1] * data2d[x + z*width] +
									matrix[1][2] * z +
									matrix[1][3]) / w;
			zvalues[x+z*width] =(	matrix[2][0] * x +
									matrix[2][1] * data2d[x + z*width] +
									matrix[2][2] * z +
									matrix[2][3]) / w;
		}
	}

	for(z = 0; z < height-1; z++)
	{
		for(x = 0; x < width-1; x++)
		{
				_line(userdata, callback, xvalues, yvalues, zvalues, width, height,
						(x+0),(z+0),
						(x+1),(z+0));
				_line(userdata, callback, xvalues, yvalues, zvalues, width, height,
						(x+0),(z+0),
						(x+0),(z+1));
		}
		_line(userdata, callback, xvalues, yvalues, zvalues, width, height ,
				(width-1),(z+0),
				(width-1),(z+1));
	}
	for(x = 0; x < width-1; x++)
	{
			_line(userdata, callback, xvalues, yvalues, zvalues, width, height,
					(x+0),(height-1),
					(x+1),(height-1));
	}

	free(xvalues);
	free(yvalues);
	free(zvalues);
	//free(wvalues);
}

int pytriangle_wrapper(void* userdata, double x1, double y1, double x2, double y2)
{
	PyObject *arglist;
    PyObject *result;
	arglist = Py_BuildValue("(dd)(dd)", x1, y1, x2, y2);
	result = PyEval_CallObject((PyObject*)userdata, arglist);
	Py_DECREF(arglist);
	if(result != NULL)
	{
		Py_DECREF(result);
		return 1;
	}
	else
	{
		return 0;
	}
}


PyObject* PyWireframe(PyObject* self, PyObject *args)
{
	PyObject *result = NULL;
	PyObject *data2d;
	PyArrayObject *dataArray;
	PyArrayObject *matrixArray;
	PyObject *pymatrix;
	PyObject *pyline_callback;
	double matrix[4][4];
	long int width, height;
	int i, j;

	if(PyArg_ParseTuple(args, "OOO:wireframe", &data2d, &pymatrix, &pyline_callback))
	{
		dataArray = NA_InputArray(data2d, tFloat64, C_ARRAY);
		if(dataArray == NULL)
			return PyErr_Format(PyExc_TypeError, "can't convert data2d into numarray");
		if(dataArray->nd != 2)
			return PyErr_Format(PyExc_TypeError, "data isn't 2 dimensional");
		width = dataArray->dimensions[1];
		height = dataArray->dimensions[0];

		matrixArray= NA_InputArray(pymatrix, tFloat64, C_ARRAY);
		if(matrixArray == NULL)
			return PyErr_Format(PyExc_TypeError, "can't convert matrixinto numarray");
		if(matrixArray->nd != 2)
			return PyErr_Format(PyExc_TypeError, "matrix isn't 2 dimensional");
		if(matrixArray->dimensions[1] != 4 || matrixArray->dimensions[0] != 4)
			return PyErr_Format(PyExc_TypeError, "matrix isn't 4x4");
		if(!PyCallable_Check(pyline_callback))
			return PyErr_Format(PyExc_TypeError, "line_callback isn't callable");

		for(i = 0; i < 4; i++)
		{
			for(j = 0; j < 4; j++)
			{
				matrix[i][j] = *((double*)NA_OFFSETDATA(matrixArray) + i + j * 4);
			}
		}
		PyKaplot_Wireframe((double*)NA_OFFSETDATA(dataArray), width, height, matrix, pytriangle_wrapper, pyline_callback);
		Py_INCREF(Py_None);
		result = Py_None;
	}
	return result;
}
/*
#############################################################################
*/

typedef struct flat3dinfo_t_ {
	PyObject *colorfunction;
	PyObject *shadefunction;
	int solid;		/* draw polygons? */
	int wireframe;	/* draw wireframe? */
	int shading;	/* shade the polygons? */
	double wirecolor_r, wirecolor_g, wirecolor_b;
	double data2dmin, data2dmax;
	double *data2d;
	double* xt;
	double* yt;
	double* zt;
	int width;
	int height;
	kaplot_cinterface_t *cinterface;
} flat3dinfo_t;


void quad_normal(flat3dinfo_t *flat3dinfo, int x, int z, double *nx, double *ny, double *nz)
{
	/*
	outerproduct
	A x B = (	Ay*Bz - Az*By,
	 			Az*Bx - Ax*Bz,
	 			Ax*By - Ay*Bx)
	*/
	double nx1, ny1, nz1;
	double nx2, ny2, nz2;
	double nx3, ny3, nz3;
	double nx4, ny4, nz4;
	double nxa, nya, nza; // avg normal vector
	double Ax, Ay, Az;
	double Bx, By, Bz;
	double length;

	Ax = flat3dinfo->xt[(x+0)+(z+0)*flat3dinfo->width] - flat3dinfo->xt[(x+0)+(z+1)*flat3dinfo->width];
	Ay = flat3dinfo->yt[(x+0)+(z+0)*flat3dinfo->width] - flat3dinfo->yt[(x+0)+(z+1)*flat3dinfo->width];
	Az = flat3dinfo->zt[(x+0)+(z+0)*flat3dinfo->width] - flat3dinfo->zt[(x+0)+(z+1)*flat3dinfo->width];
	Bx = flat3dinfo->xt[(x+0)+(z+0)*flat3dinfo->width] - flat3dinfo->xt[(x+1)+(z+0)*flat3dinfo->width];
	By = flat3dinfo->yt[(x+0)+(z+0)*flat3dinfo->width] - flat3dinfo->yt[(x+1)+(z+0)*flat3dinfo->width];
	Bz = flat3dinfo->zt[(x+0)+(z+0)*flat3dinfo->width] - flat3dinfo->zt[(x+1)+(z+0)*flat3dinfo->width];
	nx1 = Ay*Bz - Az*By;
	ny1 = Az*Bx - Ax*Bz;
	nz1 = Ax*By - Ay*Bx;

	Ax = flat3dinfo->xt[(x+1)+(z+0)*flat3dinfo->width] - flat3dinfo->xt[(x+0)+(z+0)*flat3dinfo->width];
	Ay = flat3dinfo->yt[(x+1)+(z+0)*flat3dinfo->width] - flat3dinfo->yt[(x+0)+(z+0)*flat3dinfo->width];
	Az = flat3dinfo->zt[(x+1)+(z+0)*flat3dinfo->width] - flat3dinfo->zt[(x+0)+(z+0)*flat3dinfo->width];
	Bx = flat3dinfo->xt[(x+1)+(z+0)*flat3dinfo->width] - flat3dinfo->xt[(x+1)+(z+1)*flat3dinfo->width];
	By = flat3dinfo->yt[(x+1)+(z+0)*flat3dinfo->width] - flat3dinfo->yt[(x+1)+(z+1)*flat3dinfo->width];
	Bz = flat3dinfo->zt[(x+1)+(z+0)*flat3dinfo->width] - flat3dinfo->zt[(x+1)+(z+1)*flat3dinfo->width];
	nx2 = Ay*Bz - Az*By;
	ny2 = Az*Bx - Ax*Bz;
	nz2 = Ax*By - Ay*Bx;

	Ax = flat3dinfo->xt[(x+1)+(z+1)*flat3dinfo->width] - flat3dinfo->xt[(x+1)+(z+0)*flat3dinfo->width];
	Ay = flat3dinfo->yt[(x+1)+(z+1)*flat3dinfo->width] - flat3dinfo->yt[(x+1)+(z+0)*flat3dinfo->width];
	Az = flat3dinfo->zt[(x+1)+(z+1)*flat3dinfo->width] - flat3dinfo->zt[(x+1)+(z+0)*flat3dinfo->width];
	Bx = flat3dinfo->xt[(x+1)+(z+1)*flat3dinfo->width] - flat3dinfo->xt[(x+0)+(z+1)*flat3dinfo->width];
	By = flat3dinfo->yt[(x+1)+(z+1)*flat3dinfo->width] - flat3dinfo->yt[(x+0)+(z+1)*flat3dinfo->width];
	Bz = flat3dinfo->zt[(x+1)+(z+1)*flat3dinfo->width] - flat3dinfo->zt[(x+0)+(z+1)*flat3dinfo->width];
	nx3 = Ay*Bz - Az*By;
	ny3 = Az*Bx - Ax*Bz;
	nz3 = Ax*By - Ay*Bx;

	Ax = flat3dinfo->xt[(x+0)+(z+1)*flat3dinfo->width] - flat3dinfo->xt[(x+1)+(z+1)*flat3dinfo->width];
	Ay = flat3dinfo->yt[(x+0)+(z+1)*flat3dinfo->width] - flat3dinfo->yt[(x+1)+(z+1)*flat3dinfo->width];
	Az = flat3dinfo->zt[(x+0)+(z+1)*flat3dinfo->width] - flat3dinfo->zt[(x+1)+(z+1)*flat3dinfo->width];
	Bx = flat3dinfo->xt[(x+0)+(z+1)*flat3dinfo->width] - flat3dinfo->xt[(x+0)+(z+0)*flat3dinfo->width];
	By = flat3dinfo->yt[(x+0)+(z+1)*flat3dinfo->width] - flat3dinfo->yt[(x+0)+(z+0)*flat3dinfo->width];
	Bz = flat3dinfo->zt[(x+0)+(z+1)*flat3dinfo->width] - flat3dinfo->zt[(x+0)+(z+0)*flat3dinfo->width];
	nx4 = Ay*Bz - Az*By;
	ny4 = Az*Bx - Ax*Bz;
	nz4 = Ax*By - Ay*Bx;

	nxa = nx1 + nx2 + nx3 + nx4;
	nya = ny1 + ny2 + ny3 + ny4;
	nza = nz1 + nz2 + nz3 + nz4;
	length = sqrt(nxa*nxa + nya*nya + nza*nza);
	*nx = (nxa / length);
	*ny = (nya / length);
	*nz = (nza / length);
}

int pygetcolor(PyObject *callable, double y, double *r, double *g, double *b)
{
	PyObject *arglist;
    PyObject *result;
	arglist = Py_BuildValue("(d)", y);
	result = PyEval_CallObject(callable, arglist);
	Py_DECREF(arglist);
	if(result != NULL && PyArg_ParseTuple(result, "ddd", r, g, b))
	{
		Py_XDECREF(result);
		return 1;
	}
	else
	{
		Py_XDECREF(result);
		return 0;
	}
}

int pyshade(PyObject *callable, double y, double *r, double *g, double *b)
{
	PyObject *arglist;
    PyObject *result;
	arglist = Py_BuildValue("dddd", y, *r, *g, *b);
	result = PyEval_CallObject(callable, arglist);
	Py_DECREF(arglist);
	Py_XDECREF(result);
	return result != NULL; // return 1 if successful
}

int line(flat3dinfo_t *flat3dinfo, int x1, int z1, int x2, int z2)
{
	kaplot_cinterface_t *cinterface = flat3dinfo->cinterface;
	cinterface->move_to(cinterface, flat3dinfo->xt[x1+z1*flat3dinfo->width],
									flat3dinfo->yt[x1+z1*flat3dinfo->width]);
	cinterface->line_to(cinterface, flat3dinfo->xt[x2+z2*flat3dinfo->width],
									flat3dinfo->yt[x2+z2*flat3dinfo->width]);
	cinterface->stroke(cinterface);
	return 1;
}

int quad(flat3dinfo_t *flat3dinfo, int x, int z)
{
	double vx = 0, vy = 0, vz = 1; // viewing direction
	double shade=1;
	double nx, ny, nz; // quad normal
	double data2davg;
	double r=0.5, g=0.5, b=0.5;
	kaplot_cinterface_t *cinterface = flat3dinfo->cinterface;

	data2davg = (flat3dinfo->data2d[(x+0)+(z+0)*flat3dinfo->width] + flat3dinfo->data2d[(x+1)+(z+0)*flat3dinfo->width]
			 + flat3dinfo->data2d[(x+0)+(z+1)*flat3dinfo->width] + flat3dinfo->data2d[(x+1)+(z+1)*flat3dinfo->width]) / 4.0;


	if(flat3dinfo->colorfunction)
	{
		if(!pygetcolor(flat3dinfo->colorfunction,
			(data2davg-flat3dinfo->data2dmin) / (flat3dinfo->data2dmax-flat3dinfo->data2dmin), &r, &g, &b))
		{
			return 0;
		}
	}

	if(flat3dinfo->shading)
	{
		quad_normal(flat3dinfo, x, z, &nx, &ny, &nz);
		shade = vx * nx + vy * ny + vz * nz; // innerproduct
		if(flat3dinfo->shadefunction)
		{
			if(!pyshade(flat3dinfo->shadefunction, shade, &r, &g, &b))
			{
				return 0;
			}
		}
		else
		{
			r *= fabs(shade);
			g *= fabs(shade);
			b *= fabs(shade);
		}
	}


	//if(shade > 0)
	{
		//printf("set color\n");
		cinterface->set_color_rgb(cinterface, r, g, b);
		//printf("x/z: %i %i\n", x, z);
		//printf("-> %f %f\n", flat3dinfo->xt[(x+0)+(z+0)*flat3dinfo->width], flat3dinfo->yt[(x+0)+(z+0)*flat3dinfo->width]);
		//printf("-> %f %f\n", flat3dinfo->xt[(x+1)+(z+0)*flat3dinfo->width], flat3dinfo->yt[(x+1)+(z+0)*flat3dinfo->width]);
		//printf("-> %f %f\n", flat3dinfo->xt[(x+1)+(z+1)*flat3dinfo->width], flat3dinfo->yt[(x+1)+(z+1)*flat3dinfo->width]);
		//printf("-> %f %f\n", flat3dinfo->xt[(x+0)+(z+1)*flat3dinfo->width], flat3dinfo->yt[(x+0)+(z+1)*flat3dinfo->width]);
		cinterface->move_to(cinterface, flat3dinfo->xt[(x+0)+(z+0)*flat3dinfo->width], flat3dinfo->yt[(x+0)+(z+0)*flat3dinfo->width]);
		cinterface->line_to(cinterface, flat3dinfo->xt[(x+1)+(z+0)*flat3dinfo->width], flat3dinfo->yt[(x+1)+(z+0)*flat3dinfo->width]);
		cinterface->line_to(cinterface, flat3dinfo->xt[(x+1)+(z+1)*flat3dinfo->width], flat3dinfo->yt[(x+1)+(z+1)*flat3dinfo->width]);
		cinterface->line_to(cinterface, flat3dinfo->xt[(x+0)+(z+1)*flat3dinfo->width], flat3dinfo->yt[(x+0)+(z+1)*flat3dinfo->width]);
		//printf("fill\n");
		cinterface->fill(cinterface);
		/*

		when wireframe is true, set the color, and draw it, otherwise we
		have to fill in the gaps between the polygons using the same color.
		TODO: when wireframe is false, set linewidth to 0, so it draws a
			really small line
		*/

		if(flat3dinfo->wireframe)
		{
			cinterface->set_color_rgb(cinterface, flat3dinfo->wirecolor_r, flat3dinfo->wirecolor_g, flat3dinfo->wirecolor_b);
		}
		cinterface->move_to(cinterface, flat3dinfo->xt[(x+0)+(z+0)*flat3dinfo->width], flat3dinfo->yt[(x+0)+(z+0)*flat3dinfo->width]);
		cinterface->line_to(cinterface, flat3dinfo->xt[(x+1)+(z+0)*flat3dinfo->width], flat3dinfo->yt[(x+1)+(z+0)*flat3dinfo->width]);
		cinterface->line_to(cinterface, flat3dinfo->xt[(x+1)+(z+1)*flat3dinfo->width], flat3dinfo->yt[(x+1)+(z+1)*flat3dinfo->width]);
		cinterface->line_to(cinterface, flat3dinfo->xt[(x+0)+(z+1)*flat3dinfo->width], flat3dinfo->yt[(x+0)+(z+1)*flat3dinfo->width]);
		cinterface->line_to(cinterface, flat3dinfo->xt[(x+0)+(z+0)*flat3dinfo->width], flat3dinfo->yt[(x+0)+(z+0)*flat3dinfo->width]);
		cinterface->stroke(cinterface);
		/**/
	}
	//printf("-> %i,%i: %f %f\n", x,z, flat3dinfo->xt[(x+0)+(z+0)*flat3dinfo->width], flat3dinfo->yt[(x+0)+(z+0)*flat3dinfo->width]);
	return 1;
}

/* needs to be in one struct for qsort */
typedef struct  {
	double zavg;	// avg z of a quad
	int index;		// quad indices, so we can sort them
} zavg_and_index_t;

int cmpzavg(const zavg_and_index_t *e1, const zavg_and_index_t *e2)
{
	if(e1->zavg < e2->zavg)
		return 1;
	else if(e1->zavg > e2->zavg)
		return -1;
	else
		return 0;
}

int flat3d(double* data2d, double matrix[4][4], flat3dinfo_t *flat3dinfo)
{
	int x, z, i, j;
	double *xvalues;
	double *yvalues;
	double *zvalues;
	//double *wvalues;
	double w;
	//int indextemp;
	//int *indices;
	//double *zavg;
	//double ztemp;
	zavg_and_index_t *zavg_and_index;
	int result = 1; // return value

	//indices = (int*)malloc(sizeof(int) * (flat3dinfo->width-1) * (flat3dinfo->height-1)); // quad indices, so we can sort them
	//zavg = (double*)malloc(sizeof(double) * (flat3dinfo->width-1) * (flat3dinfo->height-1)); // avg z of a quad
	zavg_and_index = (zavg_and_index_t*)malloc(sizeof(zavg_and_index_t) *
		 (flat3dinfo->width-1) * (flat3dinfo->height-1));

	for(z = 0; z < flat3dinfo->height; z++)
	{
		for(x = 0; x < flat3dinfo->width; x++)
		{
			w =						matrix[3][0] * x +
									matrix[3][1] * data2d[x + z*flat3dinfo->width] +
									matrix[3][2] * z +
									matrix[3][3];
			flat3dinfo->xt[x+z*flat3dinfo->width] =(	matrix[0][0] * x +
									matrix[0][1] * data2d[x + z*flat3dinfo->width] +
									matrix[0][2] * z +
									matrix[0][3]) / w;
			flat3dinfo->yt[x+z*flat3dinfo->width] =(	matrix[1][0] * x +
									matrix[1][1] * data2d[x + z*flat3dinfo->width] +
									matrix[1][2] * z +
									matrix[1][3]) / w;
			flat3dinfo->zt[x+z*flat3dinfo->width] =(	matrix[2][0] * x +
									matrix[2][1] * data2d[x + z*flat3dinfo->width] +
									matrix[2][2] * z +
									matrix[2][3]) / w;
		}
	}

	flat3dinfo->data2dmin = data2d[0];
	flat3dinfo->data2dmax = data2d[0];
	for(z = 0; z < flat3dinfo->height; z++)
	{
		for(x = 0; x < flat3dinfo->width; x++)
		{
			if(flat3dinfo->data2dmin < data2d[x+z*flat3dinfo->width])
				flat3dinfo->data2dmin = data2d[x+z*flat3dinfo->width];
			if(flat3dinfo->data2dmax > data2d[x+z*flat3dinfo->width])
				flat3dinfo->data2dmax = data2d[x+z*flat3dinfo->width];
		}
	}

	if(flat3dinfo->solid) /* draw solid, with possible wireframe, don't care about HLR */
	{
		for(z = 0; z < flat3dinfo->height-1; z++)
		{
			for(x = 0; x < flat3dinfo->width-1; x++)
			{
				zavg_and_index[x+z*(flat3dinfo->width-1)].index = x+z*(flat3dinfo->width-1);
				zavg_and_index[x+z*(flat3dinfo->width-1)].zavg = (
							flat3dinfo->zt[x+z*flat3dinfo->width] +
							flat3dinfo->zt[x+1+z*flat3dinfo->width] +
							flat3dinfo->zt[x+(z+1)*flat3dinfo->width] +
							flat3dinfo->zt[x+1+(z+1)*flat3dinfo->width]
						) / 4.0;

			}
		}

		// quicksort from front to back;
		printf("quicksorting...\n");
		qsort(zavg_and_index, (flat3dinfo->width-1)*(flat3dinfo->height-1),
			sizeof(zavg_and_index_t), cmpzavg);
		/*for(i = 0; i < (flat3dinfo->width-1)*(flat3dinfo->height-1)-1; i++)
		{
			for(j = (i+1); j < (flat3dinfo->width-1)*(flat3dinfo->height-1); j++)
			{
				if(zavg[i] < zavg[j])
				{
					ztemp = zavg[j];
					zavg[j] = zavg[i];
					zavg[i] = ztemp;
					indextemp = indices[j];
					indices[j] = indices[i];
					indices[i] = indextemp;
				}
			}
		}*/
		printf("quicksorting done...\n");
		printf("drawing quads...\n");

		for(i = 0; i < (flat3dinfo->width-1)*(flat3dinfo->height-1); i++)
		{
			//printf("%i,%i,%i ", indices[i], indices[i] % (flat3dinfo->width-1), indices[i] / (flat3dinfo->width-1));
			if(!quad(flat3dinfo, zavg_and_index[i].index % (flat3dinfo->width-1), zavg_and_index[i].index / (flat3dinfo->width-1)))
			{
				result = 0;
				break;
			}
		}
	}
	else if(flat3dinfo->wireframe) /* only draw wireframe, TODO: HLR */
	{
		flat3dinfo->cinterface->set_color_rgb(flat3dinfo->cinterface,
				flat3dinfo->wirecolor_r, flat3dinfo->wirecolor_g, flat3dinfo->wirecolor_b);
		for(z = 0; z < flat3dinfo->height-1; z++)
		{
			for(x = 0; x < flat3dinfo->width-1; x++)
			{
					if(!line(flat3dinfo, (x+0),(z+0), (x+1),(z+0)) ||
						!line(flat3dinfo, (x+0),(z+0), (x+0),(z+1)))
					{
						result = 0;
						break;
					}

			}
			line(flat3dinfo, (flat3dinfo->width-1),(z+0), (flat3dinfo->width-1),(z+1));
		}
		for(x = 0; x < flat3dinfo->width-1; x++)
		{
				if(!line(flat3dinfo, (x+0), (flat3dinfo->height-1), (x+1), (flat3dinfo->height-1)))
				{
					result = 0;
					break;
				}
		}
	}
	printf("drawing quads done...\n");
	//free(indices);
	//free(zavg);
	free(zavg_and_index);
	return result;
}

PyObject* PyFlat3d(PyObject* self, PyObject *args, PyObject *kwargs)
{
	static char *kwlist[] = {"data2d", "matrix", "cinterface", "colorfunction",
			"shading", "shadefunction", "wireframe", "wirecolor",
			"solid", NULL};
	PyObject *result = NULL;
	PyObject *data2d;
	PyArrayObject *dataArray;
	PyArrayObject *matrixArray;
	PyObject *pymatrix;
	PyObject *cinterface_object = NULL;
	kaplot_cinterface_t *cinterface;
	double matrix[4][4];
	long int width, height;
	int i, j;
	flat3dinfo_t flat3dinfo;
	double wirecolor_r = 0;
	double wirecolor_g = 0;
	double wirecolor_b = 0;

	PyObject *colorfunction = NULL;
	PyObject *shading = NULL;
	PyObject *shadefunction = NULL;
	PyObject *wireframe = NULL;
	PyObject *wirecolor = NULL;
	PyObject *solid = NULL;

	/* WARNING: I don't inc the ref count to Py_False */
	shading = Py_False;
	wireframe = Py_False;
	solid = Py_True;

	if(PyArg_ParseTupleAndKeywords(args, kwargs, "OOO!|OO!OOOO:flat3d", kwlist, &data2d, &pymatrix,
			&PyCObject_Type, &cinterface_object,
			&colorfunction, &PyBool_Type, &shading, &shadefunction,
			&wireframe, &wirecolor, &solid))
	{
		dataArray = NA_InputArray(data2d, tFloat64, C_ARRAY);
		if(dataArray == NULL)
			return PyErr_Format(PyExc_TypeError, "can't convert data2d into numarray");
		if(dataArray->nd != 2)
			return PyErr_Format(PyExc_TypeError, "data isn't 2 dimensional");
		width = dataArray->dimensions[1];
		height = dataArray->dimensions[0];

		matrixArray= NA_InputArray(pymatrix, tFloat64, C_ARRAY);
		if(matrixArray == NULL)
			return PyErr_Format(PyExc_TypeError, "can't convert matrixinto numarray");
		if(matrixArray->nd != 2)
			return PyErr_Format(PyExc_TypeError, "matrix isn't 2 dimensional");
		if(matrixArray->dimensions[1] != 4 || matrixArray->dimensions[0] != 4)
			return PyErr_Format(PyExc_TypeError, "matrix isn't 4x4");
		cinterface = PyCObject_AsVoidPtr(cinterface_object);

		if(wirecolor != NULL)
		{
			if(PySequence_Check(wirecolor) && PySequence_Length(wirecolor) == 3)
			{
				wirecolor_r = PyFloat_AsDouble(PySequence_GetItem(wirecolor, 0));
				wirecolor_g = PyFloat_AsDouble(PySequence_GetItem(wirecolor, 1));
				wirecolor_b = PyFloat_AsDouble(PySequence_GetItem(wirecolor, 2));
			}
			else
			{
				return PyErr_Format(PyExc_TypeError, "wirecolor should be a sequence of length 3");
			}
		}

		for(i = 0; i < 4; i++)
		{
			for(j = 0; j < 4; j++)
			{
				matrix[i][j] = *((double*)NA_OFFSETDATA(matrixArray) + j + i * 4);
			}
		}

		flat3dinfo.cinterface = cinterface;
		flat3dinfo.shadefunction = shadefunction;
		flat3dinfo.colorfunction = colorfunction;
		flat3dinfo.data2d = (double*)NA_OFFSETDATA(dataArray);
		flat3dinfo.width = width;
		flat3dinfo.height = height;
		flat3dinfo.solid = (solid == Py_True);
		flat3dinfo.shading = (shading == Py_True);
		flat3dinfo.wireframe = (wireframe == Py_True);
		flat3dinfo.wirecolor_r = wirecolor_r;
		flat3dinfo.wirecolor_g = wirecolor_g;
		flat3dinfo.wirecolor_b = wirecolor_b;

		flat3dinfo.xt = (double*)malloc(sizeof(double) * flat3dinfo.width * flat3dinfo.height);
		flat3dinfo.yt = (double*)malloc(sizeof(double) * flat3dinfo.width * flat3dinfo.height);
		flat3dinfo.zt = (double*)malloc(sizeof(double) * flat3dinfo.width * flat3dinfo.height);

		flat3d(flat3dinfo.data2d, matrix, &flat3dinfo);

		free(flat3dinfo.xt);
		free(flat3dinfo.yt);
		free(flat3dinfo.zt);

		if(!PyErr_Occurred())
		{
			Py_INCREF(Py_None);
			result = Py_None;
		}
	}
	return result;
}

static PyMethodDef pyext3d_functions[] = {
	//{"wireframe", (PyCFunction)PyWireframe, METH_VARARGS, "draws a wireframe surface"},
	{"flat3d", (PyCFunction)PyFlat3d, METH_VARARGS|METH_KEYWORDS, "draws a flat shaded surface"},
    { NULL, NULL, 0 }
};



PyMODINIT_FUNC
init_ext3d(void)
{
	static void *PyKaplotExt3d_API[1];
	PyObject *mod;
	PyObject *c_api_object;

	import_libnumarray();

	mod = Py_InitModule("_ext3d", pyext3d_functions);

	PyKaplotExt3d_API[0] = (void *)PyKaplot_Wireframe;
	c_api_object = PyCObject_FromVoidPtr((void *)PyKaplotExt3d_API, NULL);
	if (c_api_object != NULL)
		PyModule_AddObject(mod, "_C_API", c_api_object);
}

