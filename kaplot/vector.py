"""Vector class for 2d geometry"""
from math import sqrt, acos, pi, atan2

if True:
	from kaplot.cext._kaplot import Vector
else:
	
	class Vector:
		"""Used for 2d math
	
		Vector acts like a sequence of length 2, therefore it
		can do sequence unpacking:
			v = Vector((10, 20)
			x, y = v			# x == 10, y == 20
	
			v = Vector((100, 200)).scale(0.1) # v.x == 10, v.y == 200
	
		The x and y elements can be accessed using the x or y member, or the the
		item getter and setter ([])
			v = Vector(10, 20)
			v.x += 30    equals    v[0] -= 30
			v.y += 50    equals    v[1] -= 50
	
		All methods return a new Vector, it does not change the current vector
		v1 = Vector(10, 20)
		v2 = v1.scale(2)
	
		'v1.scale(2)' returns a new Vector object, it doesn't alter the original
		Vector.
	
		"""
		def __init__(self, first, second=None):
			"""Constructor
	
			A Vector can be constructed using another sequence of length 2,
			or a x and y element.
			v1 = Vector(10, 20)
			v2 = Vector([10, 20])
			v3 = Vector((10, 20))
			v4 = Vector(v1)
			v5 = Vector(v1.x, v2.y)
			"""
			if second == None:
				self.x, self.y = first
			else:
				self.x, self.y = first, second
			self.x = float(self.x)
			self.y = float(self.y)
	
		def scale(self, s):
			"""Return a new Vector scaled by factor s"""
			return Vector((self.x * s, self.y * s))
	
		def abs(self):
			"""Return a new Vector withs abs(x) and abs(y)"""
			return Vector((abs(self.x), abs(self.y)))
	
		def length(self):
			"""Return the length of the Vector"""
			return sqrt(self.x * self.x + self.y * self.y)
	
		def unit(self):
			"""Return a new Vector scaled to length 1"""
			return self.scale(1/self.length())
	
		def dot(self, other):
			return self.x * other.x + self.y * other.y
	
		def angle(self):
			"""Returns the angle of the vector in a unit sphere"""
			return (atan2(self.y, self.x) + 2*pi) % (2*pi)
	
		def __add__(self, other):
			"""Adds two Vectors together"""
			return Vector((self.x + other.x, self.y + other.y))
	
		def __sub__(self, other):
			"""Subtract two vectors from eachother"""
			return Vector((self.x - other.x, self.y - other.y))
	
		def __neg__(self):
			"""Negates a new negated vector"""
			return self.scale(-1)
	
		def __getitem__(self, index):
			if index == 0:
				return self.x
			elif index == 1:
				return self.y
			else:
				raise IndexError, "Vector index out of range"
	
		def __setitem__(self, index, value):
			if index == 0:
				self.x = value
			elif index == 1:
				self.y = value
			else:
				raise IndexError, "Vector index out of range"
	
		def __len__(self):
			"""Always return 2"""
			return 2
	
		def __repr__(self):
			return "kaplot.Vector("+ str(self.x) +", " +str(self.y) +")"
	
		def __eq__(self, other):
			"""Return self.equals(other)"""
			return self.equals(other)
	
		def __ne__(self, other):
			"""Return not self.equals(other)"""
			return not self.equals(other)
	
		def equals(self, other, sigma=1e-6):
			"""Compares 2 vectors
	
			Return false if the difference between 2 corresponding elements
			is larger than sigma
	
			"""
			return abs(self.x - other.x) < sigma and abs(self.y - other.y) < sigma
	
	
	
	
