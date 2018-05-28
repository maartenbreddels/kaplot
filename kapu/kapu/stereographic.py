from math import *

class StereoGraphicProjection(object):
	"""
	See http://mathworld.wolfram.com/StereographicProjection.html
	phi: latitude (phi in eq 1,2)
	theta: longitude (lambda in eq 1,2)
	
	"""
	def __init__(self, theta0=0, phi0=0, radius=1.):
		self.theta0 = radians(theta0)
		self.phi0 = radians(phi0)
		self.radius = float(radius)
		
		
	def _calc_k(self, theta, phi):
		d = 1 + sin(self.phi0) * sin(phi) + cos(self.phi0) * cos(phi) * cos(theta-self.theta0)
		return self.radius * 2. / d

	def to_pixel(self, theta, phi):
		phi = radians(phi)
		theta = radians(theta)
		k = self._calc_k(theta, phi)
		x = k * cos(phi) * sin(theta - self.theta0)
		y = k * (cos(self.phi0) * sin(phi) - sin(self.phi0) * cos(phi) * cos(theta-self.theta0))
		return x, y
		
	def from_pixel(self, x, y):
		ro = sqrt(x**2+y**2)
		c = 2 * atan(ro/2 * self.radius)
		phi = asin(cos(c) * sin(self.phi0) + y * sin(c) * cos(self.phi0) / ro)
		d = ro * cos(self.phi0) * cos(c) - y * sin(self.phi0)*sin(c)
		theta = self.theta0 + atan(x * sin(c) / d)
		return degrees(theta), degrees(phi)
		

sgp = StereoGraphicProjection

if __name__ == "__main__":
	p = sgp()
	print p.to_pixel(radians(0), radians(179.99))