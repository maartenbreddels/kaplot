from math import sqrt

class Vector3d:
	def __init__(self, x, y, z, w=1.0):
		self.x = float(x)
		self.y = float(y)
		self.z = float(z)
		self.w = float(w)

	def cross(self, other):
		x = self.y*other.z - self.z*other.y
		y = self.z*other.x - self.x*other.z
		z = self.x*other.y - self.y*other.x
		return Vector3d(x,y,z)

	def dot(self, other):
		return self.x*other.x + self.y*other.y + self.z*other.z

	def scale(self, s):
		return Vector3d(self.x * s, self.y *s, self.z * s)
		
	def homogenize(self):
		return Vector3d(self.x/self.w, self.y/self.w, self.z/self.w)

	def norm(self):
		return self.scale(1.0/self.length())
	unit = norm
	normalise = norm

	def length(self):
		return sqrt(self.x*self.x + self.y*self.y + self.z*self.z)
	abs = length

	def __sub__(self, other):
		return Vector3d(self.x-other.x, self.y-other.y, self.z-other.z)

	def __neg__(self):
		return Vector3d(-self.x, -self.y, -self.z)

	def __add__(self, other):
		return Vector3d(self.x+other.x, self.y+other.y, self.z+other.z)

	def __repr__(self):
		return "<%s.%s instance at 0x%x %f %f %f>" % (Vector3d.__module__, Vector3d.__name__, hash(self), self.x, self.y, self.z)
		
	def __len__(self):
		return 3
	
	def __getitem__(self, val):
		if val == 0:
			return self.x
		elif val == 1:
			return self.y
		elif val == 2:
			return self.z
		else:
			raise IndexError, "blaat"
		#elif val == 3:
		#	return self.w

