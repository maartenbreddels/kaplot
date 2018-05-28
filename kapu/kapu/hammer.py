from math import *

class HammerProjection(object):
	"""
	See http://en.wikipedia.org/wiki/Hammer_projection
	phi: latitude
	theta: longitude
	
	"""
	def __init__(self):
		#self.theta0 = float(theta0)
		#self.phi0 = float(phi0)
		#self.radius = float(radius)
		pass
		
		
	def to_pixel(self, theta, phi):
		phi = float(phi)
		theta = float(theta)
		z = acos(cos(phi)*cos(theta/2))
		f = sqrt(2) / sqrt(1 + cos(phi)*cos(theta/2))
		x = f*2*cos(phi)*sin(theta/2)
		y = f*sin(phi)
		return x, y
		

if __name__ == "__main__":
	#p = sgp()
	#print p.to_pixel(radians(0), radians(179.99))
	pass