import numpy
from numpy import *
#from numpy.linear_algebra import *
import kaplot3d.vector3d
import math

class Matrix3d:
	def __init__(self, matrix=None):
		if matrix == None:
			self.matrix = array([[1, 0, 0, 0], [0,1,0,0], [0,0,1,0], [0,0,0,1]], float, copy=0)
		else:
			self.matrix = array(matrix, copy=0)

	def __mul__(self, other):
		if isinstance(other, kaplot3d.vector3d.Vector3d):
			v = other
			x, y, z, w = array(matrix(self.matrix) * array([v.x, v.y, v.z, v.w]))[0]
			return kaplot3d.vector3d.Vector3d(x, y, z, w).homogenize()
		return Matrix3d(matrix(self.matrix) * matrix(other.matrix))
		#return Matrix3d(matrixmultiply(self.matrix, other.matrix))
		#return Matrix3d(transpose(matrixmultiply(transpose(other.matrix), transpose(self.matrix))))

	def mulXYZ(self, x, y, z):
		data = matrix(self.matrix) * array([x,y,z, zeros(len(z))+1.0])
		#print data
		x, y, z, w = array(data)
		return x/w, y/w, z/w
		

	def __repr__(self):
		lines = [" ".join(["%.2f" % k for k in row]) for row in self.matrix]
		matrixstr = "\n".join(lines)
		return "<%s.%s instance at \n%s\n" % (Matrix3d.__module__, Matrix3d.__name__, matrixstr)

	def rotateX(angle):
		matrix = Matrix3d();
		matrix.matrix[0][0] = 1;
		matrix.matrix[1][1] = cos(angle);
		matrix.matrix[1][2] = -sin(angle);
		matrix.matrix[2][1] = sin(angle);
		matrix.matrix[2][2] = cos(angle);
		matrix.matrix[3][3] = 1;
		return matrix;
	rotateX = staticmethod(rotateX)

	def rotateY(angle):
		matrix = Matrix3d();
		matrix.matrix[0][0] =  cos(angle);
		matrix.matrix[0][2] =  sin(angle);
		matrix.matrix[1][1] = 1;
		matrix.matrix[2][0] = -sin(angle);
		matrix.matrix[2][2] =  cos(angle);
		matrix.matrix[3][3] = 1;
		return matrix;
	rotateY = staticmethod(rotateY)


	def rotateZ(angle):
		matrix = Matrix3d();
		matrix.matrix[0][0] =  cos(angle);
		matrix.matrix[0][1] = -sin(angle);
		matrix.matrix[1][0] =  sin(angle);
		matrix.matrix[1][1] =  cos(angle);
		matrix.matrix[2][2] = 1;
		matrix.matrix[3][3] = 1;
		return matrix;
	rotateZ = staticmethod(rotateZ)

	def translate(x, y=None, z=None):
		#if not isinstance(point, ishi.Vector):
		#	point = ishi.Vector(point[0], point[1], point[2])
		#x, y, z = point.x, point.y, point.z
		if (y == None) and (z == None):
			x, y, z = x.x, x.y, x.z
		return Matrix3d(numpy.array([[1,0,0,x],[0,1,0,y], [0,0,1,z], [0,0,0,1]], numpy.float))
	translate = staticmethod(translate)

	def scale(x, y, z):
		#x, y, z = point
		return Matrix3d(numpy.array([[x,0,0,0],[0,y,0,0], [0,0,z,0], [0,0,0,1]], numpy.float))
	scale = staticmethod(scale)

	def inverse(self):
		return Matrix3d(inverse(self.matrix))

	def projection(width, height, znear, zfar, fov):
		aspect = width/height
		h = tan(fov / 2);
		w = aspect * h;

		clip_near = znear;
		clip_far = zfar;
		clip_left = -w;
		clip_right = w;
		clip_top = h;
		clip_bottom = -h;

		x = (2.0*clip_near)/(clip_right-clip_left);
		y = (2.0*clip_near)/(clip_top-clip_bottom);
		a = (clip_right+clip_left)/(clip_right-clip_left);
		b = (clip_top+clip_bottom)/(clip_top-clip_bottom);
		c = -((clip_far+clip_near)/(clip_far-clip_near));
		d = -((2.0*clip_far*clip_near)/(clip_far-clip_near));
		q = (clip_far / (clip_far - clip_near));

		m = zeros((4,4), float);
		m[0][0] = x;
		m[1][1] = y;
		m[2][2] = q;
		m[3][2] = 1;
		m[2][3] = -q*clip_near;
		m[0][0] = x;
		m[1][1] = y;
		m[2][2] = q;
		m[2][3] = 1;
		m[3][2] = -q*clip_near;
		return Matrix3d(transpose(m))
	projection = staticmethod(projection)

	def _projection(d):
		matrix = Matrix3d();
		matrix.matrix[3][2] = 1.0 / d;
		matrix.matrix[3][3] = 0;
		return matrix;
	_projection = staticmethod(_projection)

	def isoprojection():
	#[cos(30)    -sin(30)    0
    #  0    1        0
    # -cos(30)    -sin(30)    1]

		matrix = Matrix3d();
		a = 30 * math.pi / 180
		b = 30 * math.pi / 180
		matrix.matrix[0][0] =  cos(a)
		matrix.matrix[0][2] =  sin(a)
		matrix.matrix[1][0] = sin(b) * cos(a)
		matrix.matrix[1][1] = cos(b)
		matrix.matrix[1][2] = -sin(b) * cos(a)
		matrix.matrix[2][2] = 1.0
		#matrix.matrix[0][1] = -sin(angle30)
		return matrix;
	isoprojection = staticmethod(isoprojection)


	def clearLocation(self):
		self.matrix[0][3] = 0
		self.matrix[1][3] = 0
		self.matrix[2][3] = 0


#from ext import Matrix
#from ext.ishic import Matrix, Matrix_scale, Matrix_translate, Matrix_rotateX
#from ext.ishic import Matrix_rotateX, Matrix_rotateY, Matrix_rotateZ, Matrix_projection
