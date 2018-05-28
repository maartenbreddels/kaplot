"""Matrix class for 2d geometry"""
import types
from numpy import *
import numpy
from numpy import linalg
import math
from vector import Vector
#from tools import issequence
import time
from pdb import set_trace
#from numpy import ArrayType

def issequence(obj):

	"""Tests if obj has the __getitem__ method or is of type ArrayType"""

	return hasattr(obj, "__getitem__") or type(obj) == ArrayType

if False:
	from kapu.cext._kaplot import Matrix # as mat
	#class Matrix(mat):
	#	def __mul__(self, *args):
	#		apply(Matrix, (self, )+args)
else:
	class Matrix(object):
		def __init__(self, sx=1, sy=1, tx=0, ty=0):
			"""Constructor
	
			If no arguments are given it will construct an identity matrix
	
			Matrix is in row-column format
	
			m1 = Matrix()
			m1[0][2] = 10
			m1[1][2] = 20
	
			m2 = Matrix.translate((10, 20))
	
			m1 == m2
	
			Optional arguments:
			matrix -- a 3x3 sequence
			"""
			if issequence(sx):
				self.matrix = numpy.array(sx)
			else:
				self.matrix = numpy.array([[sx, 0, tx],[0,sy,ty],[0,0,1]])
			if self.matrix == None:
				self.matrix = numpy.identity(3, numpy.Float)
	
		def inverse(self):
			"""Return the inverse of this matrix"""
			return Matrix(linear_algebra.inverse(self.matrix))
	
		def rotate(angle):
			"""Return a rotate matrix, angle in radians anticlockwise"""
			return Matrix(numpy.array([[math.cos(angle), -math.sin(angle),0],[math.sin(angle), math.cos(angle),0], [0,0,1]], numpy.Float))
	
		def translate(point):
			"""Return a translation matrix"""
			x, y = point
			return Matrix(numpy.array([[1,0,x],[0,1,y], [0,0,1]], numpy.Float))
	
		def scale(s):
			"""Returns a uniform scale matrix"""
			return Matrix(numpy.array([[s,0,0],[0,s,0], [0,0,1]], numpy.Float))
	
		def scaleXY(x, y):
			"""Returns a non-uniform scale matrix"""
			return Matrix(numpy.array([[x,0,0],[0,y,0], [0,0,1]], numpy.Float))
	
		def shear(x, y):
			"""Returns a shear matrix"""
			return Matrix(numpy.array([[1,x,0],[y,1,0], [0,0,1]], numpy.Float))
	
		def location(self):
			return Vector(self.matrix[0][2], self.matrix[1][2])
	
		def nolocation(self):
			matrix = numpy.array(self.matrix)
			matrix[0][2] = 0
			matrix[1][2] = 0
			return Matrix(matrix)
	
	
	
		def __mul__(self, other):
			"""Multiplies with a Matrix or point"""
			#if type(other) == types.TupleType:
			if issequence(other) and len(other) == 2:
				x, y = other
				if True:
					x, y = float(x), float(y)
					vec = array([x, y, 1])
					newvec = numpy.dot(self.matrix, vec)
					newx = newvec[0] / newvec[2]
					newy = newvec[1] / newvec[2]
					return Vector((newx, newy))
				else:
					m = self.matrix
					nx = m[0,0] * x + m[0,1] * y + m[0,2]
					ny = m[1,0] * x + m[1,1] * y + m[1,2]
					nw = m[2,0] * x + m[2,1] * y + m[2,2]
					return Vector((nx/nw, ny/nw))
			elif type(other) == Matrix:
				newmatrix = numpy.matrixmultiply(self.matrix, other.matrix)
				return Matrix(newmatrix[0,0], newmatrix[1,1], newmatrix[0,2], newmatrix[1,2])
			else:
				raise Exception, "can only multiply with 'point tuples', and Matrices"
	
		def mulXY(self, x, y):
			"""Muliplies the matrix with each x/y element
	
			Arguments:
			x -- a sequence with x elements
			y -- a sequence with y elements
			"""
			start = time.time()
			length = min(len(x), len(y))
			w = numpy.ones(length, Float)
	
			#print x, y
			#for i in xrange(length):
			#	point = numpy.matrixmultiply(self.matrix, points[i])
			#	newx[i] = point[0] / point[2]
			#	newy[i] = point[1] / point[2]
			#end = time.time()
			#if end - start > 1.0:
			#	set_trace()
			x = numpy.array(x, numpy.Float)
			y = numpy.array(y, numpy.Float)
			points = numpy.matrixmultiply(self.matrix, array([x,y,w]))
			newx = points[0] / points[2]
			newy = points[1] / points[2]
			return newx,newy
	
		def __eq__(self, other):
			"""Return self.equals(other)"""
			return self.equals(other)
	
		def __ne__(self, other):
			"""Return not self.equals(other)"""
			return not self.equals(other)
	
		def equals(self, other, sigma=1e-6):
			"""Compares 2 matrices
	
			Return false if the difference between 2 corresponding elements
			is larger than sigma
			"""
			if other == None:
				return 0
			error = max(abs(ravel(self.matrix) - ravel(other.matrix)))
			return error <= sigma
	
		def __repr__(self):
			"""Nice representation of the matrix"""
			return \
				self.__class__.__module__ +"." +\
				self.__class__.__name__ +"(" +repr(self.matrix.tolist()) +")"
	
	
		def __len__(self):
			"""Length is always 3, (3 rows)"""
			return 3
	
		def __getitem__(self, index):
			"""Return row"""
			return self.matrix[index]
	
		def __setitem__(self, index, value):
			"""Set row"""
			self.matrix[index] = value
	
		def scalebox(p1, p2):
			p1 = Vector(p1)
			p2 = Vector(p2)
			x1, y1 = p1
			x2, y2 = p2
			return (Matrix.translate(p1) * Matrix.scaleXY(x2-x1, y2-y1)).inverse()
			#m = [[1.0/(x2-x1), 0, 0], [0, 1.0/(y2-y1), 0], [-x1, -y1, 1]]
			#m = [[1.0/(x2-x1), 0, -1.0/x1], [0, 1.0/(y2-y1), -1.0/y1], [0, 0, 1]]
			return Matrix(m)
	
		scalebox = staticmethod(scalebox)
	
		def scaleboxInverse(p1, p2):
			#p1 = Vector(p1)
			#p2 = Vector(p2)
			x1, y1 = p1
			x2, y2 = p2
			#return (Matrix.translate(p1) * Matrix.scaleXY(x2-x1, y2-y1)).inverse()
			#m = [[(x2-x1), 0, 0], [0, (y2-y1), 0], [x1, y1, 1]]
			m = [[(x2-x1), 0, x1], [0, (y2-y1), y1], [0, 0, 1]]
			return Matrix(m)
	
		scaleboxInverse = staticmethod(scaleboxInverse)
	
		rotate = staticmethod(rotate)
		translate = staticmethod(translate)
		scale = staticmethod(scale)
		scaleXY = staticmethod(scaleXY)
		shear = staticmethod(shear)
	
