from math import *

class AitoffProjection(object):
	"""
	See http://en.wikipedia.org/wiki/Aitoff_projection
	phi: latitude
	theta: longitude
	
	"""
	def __init__(self):
		#self.theta0 = float(theta0)
		#self.phi0 = float(phi0)
		#self.radius = float(radius)
		pass
		
		
	def to_pixel(self, theta, phi):
		phi = radians(phi)
		theta = radians(theta)
		z = acos(cos(phi)*cos(theta/2))
		x = 2*z*cos(phi)*sin(theta/2)/sin(z)
		y = z * sin(phi)/sin(z)
		return x, y
		

if __name__ == "__main__":
	#p = sgp()
	#print p.to_pixel(radians(0), radians(179.99))
	pass