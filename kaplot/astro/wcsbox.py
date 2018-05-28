from kaplot.objects import Decorator, Axis, Container, PlotObject
#from kaplot.astro.wcsgrid import WcsGrid
#from kaplot.astro.wcsaxis import WcsAxis
#from kaplot.objects.box import Labels
#from kaplot.cext._gipsy import *
from numpy import *
#from kaplot.astro import projection
import kaplot
import kapu
#import kaplot.context
#import kaplot.vector
#from kaplot.cext._wcslib import Wcs
#import kaplot.cext._gipsy as gipsy

#from kaplot.astro.taxis import TAxis, Timeformat
#from grid import Grid
#from math import *
#from Numeric import *

def nextpow10(n):
	if n == 0:
		return 0
	else:
		return ceil(log(abs(n))/log(10))

def fround(value, mod):
	if mod == 0:
		return value
	else:
		return int(value/mod) *mod

def magicnr(value, error):
	magics = [	(10 ** (nextpow10(error))),
				(10 ** (nextpow10(error))) / 2.0,
				(10 ** (nextpow10(error))) / 4.0,
				(10 ** (nextpow10(error))) / 10.0,
				(10 ** (nextpow10(error))) / 20.0,
				(10 ** (nextpow10(error))) / 40.0,
				(10 ** (nextpow10(error))) / 100.0,
				]
	magics.sort()
	magics.reverse()
	magic = magics[-1]
	for n in magics:
		if n < abs(value):
			magic = n
			break
	return fround(value, magic)
	
def rnd(x):
	return ((x + 360+180) % 360) - 180
def rndv(v):
	x, y = v
	return kaplot.Vector(rnd(x), rnd(y))
	
def degreeformat(value):
	degrees = int(value)

	value -= degrees
	value *= 60
	minutes = int(value)

	value -= minutes
	value *= 60
	seconds = int(value)

	value -= seconds
	value *= 1000
	mseconds = int(value)
	return "%+i:%02i:%02i.%i" % (degrees, minutes, seconds, mseconds/100)

def timeformat(degree):
	value = ((degree + 360) % 360) * 24 / 360
	hours = int(value)

	value -= hours
	value *= 60
	minutes = int(value)

	value -= minutes
	value *= 60
	seconds = int(value)

	value -= seconds
	value *= 1000
	mseconds = int(value)
	return "%i:%02i:%02i.%i" % (hours, minutes, seconds, mseconds/100)

class WcsGrid(PlotObject):
	def __init__(self, container, wcs=None, transformation=None,
			xinterval=None, xinteger=False, xstart=None, 
			yinterval=None, yinteger=False, ystart=None, 
			**kwargs):
		super(WcsGrid, self).__init__(container, **kwargs)
		if not isinstance(container, WcsBox):
			raise Exception, "Wcs PlotObjects should have a WcsBox as container"
		if wcs is None:
			self.wcs = self.container.wcs
		else:
			self.wcs = wcs
		if transformation is None:
			self.transformation = self.container.transformation
		else:
			self.transformation = transformation
		self.xinterval = xinterval
		self.xinteger = xinteger
		self.xstart = xstart
		self.yinterval = yinterval
		self.yinteger = yinteger
		self.ystart = ystart
		self.N = 10

	def getWcsRange(self):
		ystart = -0.1
		yend = 1.1
		xstart = -0.1
		xend = 1.1
		step = (yend - ystart) / 10.0

		#matrix = self.getWorldMatrix().inverse()
		matrix = kaplot.Matrix.scalebox_inverse(*self.container.getWorld())
		#tinv = trans.inverse()
		longlist = []
		latlist = []
		for y in arange(ystart, yend+step/2, step):
			for x in arange(xstart, xend+step/2, step):
				p = (x, y)
				p1 = matrix * p
				pn = self.wcs.from_pixel(p1.x, p1.y)
				if pn == None:
					continue
				pn = self.transformation.forward(*pn)
				p2 = rndv(kaplot.vector.Vector(pn))
				longlist.append(p2.x)
				latlist.append(p2.y)
		lomin, lomax = min(longlist), max(longlist)
		lamin, lamax = min(latlist), max(latlist)

		lodiff = lomax - lomin
		ladiff = lamax - lamin

		return ((lomin, lamin), (lomax, lamax))


	def draw(self, device):
		device.pushContext(self.context)
		(wx1, wy1), (wx2, wy2) = self.container.getWorld()
		(wcsx1, wcsy1), (wcsx2, wcsy2) = self.getWcsRange()
		wcsxlist = kaplot.utils.subdivide(wcsx1, wcsx2, interval=self.xinterval,
			integer=self.xinteger, start=self.xstart)
		wcsylist = kaplot.utils.subdivide(wcsy1, wcsy2, interval=self.yinterval,
			integer=self.yinteger, start=self.ystart)
		#wcsxlist = range(-10, 10)
		#wcsylist = range(-10, 10)
		wcs = self.container.wcs
		step = (wcsx2-wcsx1)/self.N
		wcsxrange = arange(wcsx1, wcsx2+step/2., step)
		step = (wcsy2-wcsy1)/self.N
		wcsyrange = arange(wcsy1, wcsy2+step/2., step)
		r = lambda x, y: self.transformation.reverse(x, y)
		for wcsy in wcsylist:
			for wcsx1, wcsx2 in zip(wcsxrange[:-1], wcsxrange[1:]):
				p1 = wcs.to_pixel(*r(rnd(wcsx1), rnd(wcsy)))
				p2 = wcs.to_pixel(*r(rnd(wcsx2), rnd(wcsy)))
				if p1 is not None and p2 is not None:
					w1 = kaplot.Vector(p1)
					w2 = kaplot.Vector(p2)
					device.drawLine(w1.x, w1.y, w2.x, w2.y)
				#print (w1 + w2).length
		for wcsx in wcsxlist:
			for wcsy1, wcsy2 in zip(wcsyrange[:-1], wcsyrange[1:]):
				p1 = wcs.to_pixel(*r(rnd(wcsx), rnd(wcsy1)))
				p2 = wcs.to_pixel(*r(rnd(wcsx), rnd(wcsy2)))
				if p1 is not None and p2 is not None:
					w1 = kaplot.Vector(p1)
					w2 = kaplot.Vector(p2)
					#device.drawLine(rnd(w1.x), rnd(w1.y), rnd(w2.x), rnd(w2.y))
					device.drawLine(w1.x, w1.y, w2.x, w2.y)
				#print rnd(w1.x), rnd(w1.y), rnd(w2.x), rnd(w2.y)
				#print wcsx, wcsy1, wcsy2
				#print 
				
		device.popContext()
				
class WcsAxis(Axis):
	def __init__(self, container, location, wcs=None, transformation=None, 
			format="%(value).2f", ticklength="-3mm", **kwargs):
		Axis.__init__(self, container, location, ticklength=ticklength, **kwargs)
		if not isinstance(container, WcsBox):
			raise Exception, "Wcs PlotObjects should have a WcsBox as container"
		if wcs is None:
			self.wcs = self.container.wcs
		else:
			self.wcs = wcs
		if transformation is None:
			self.transformation = self.container.transformation
		else:
			self.transformation = transformation
		self.N = 15.
		self.format = format
		
	def label(self, value):
		valuemap = {}
		valuemap["degree"] = degreeformat(value)
		valuemap["time"] = timeformat(value)
		valuemap["value"] = value
		#return self.container.xformat(value)
		return self.format % valuemap
	
	def labely(self, value):
		#return degreeformat(value)
		return self.container.yformat(value)
		
	def lineintersection(self, p1, p2, p3, p4):
		# from http://astronomy.swin.edu.au/~pbourke/geometry/lineline2d/
		numa = (p4.x - p3.x)*(p1.y-p3.y) - (p4.y-p3.y)*(p1.x-p3.x)
		numb = (p2.x - p1.x)*(p1.y-p3.y) - (p2.y-p1.y)*(p1.x-p3.x)
		denom = (p4.y - p3.y)*(p2.x-p1.x) - (p4.x-p3.x)*(p2.y-p1.y)
		if abs(denom) < 1e-6:
			return None
		else:
			ua = numa/denom
			ub = numb/denom
			if ua >= 0 and ua < 1 and ub >= 0 and ub < 1:
				return p1 + (p2 - p1).scale(ua, ua)
			else:
				return None
		

	def _getYticks(self, world):
		#(wx1, wy1), (wx2, wy2) = self.container.getWorld()
		world = self.container.getWorld()
		matrix = kaplot.Matrix.scalebox_inverse(*world)
		wp1 = matrix * self.p1
		wp2 = matrix * self.p2
		(wcsx1, wcsy1), (wcsx2, wcsy2) = self.container.getRange(self.wcs, self.transformation)
		wcsxlist, _ = self._getXticks2(wcsx1, wcsx2)
		wcsylist, __ = self._getXticks2(wcsy1, wcsy2)
		yticks = []
		yvalues = []
		wcs = self.wcs
		step = (wcsx2-wcsx1)/self.N
		wcsxrange = arange(wcsx1, wcsx2+step/2., step)
		#print self.container.getWorld()
		#print self.container.getRange()
		r = lambda x, y: self.transformation.reverse(x, y)
		for wcsy in wcsylist:
			for wcsx1, wcsx2 in zip(wcsxrange[:-1], wcsxrange[1:]):
				p1 = wcs.to_pixel(*r(rnd(wcsx1), rnd(wcsy)))
				p2 = wcs.to_pixel(*r(rnd(wcsx2), rnd(wcsy)))
				if p1 is not None and p2 is not None:
					w1 = kaplot.Vector(p1)
					w2 = kaplot.Vector(p2)
				#sprint w1.x, w2.x, wx1
					p = self.lineintersection(wp1, wp2, w1, w2)
					if p:
					#if (w1.x < wx1 and w2.x >= wx1) or (w2.x < wx1 and w1.x >= wx1):
						# todo, intersection
						#import pdb; pdb.set_trace()
						#print "tick", w1.y, rnd(w1.y), wcsx1, wcsx2
						yticks.append(p.y) #+(w2.x-w1.x)/2)
						yvalues.append(wcsy)
			
		#print "yticks", yticks
		return array(yticks), array(yvalues), []
		
	#def labelx(self, value):
	def _getXticks(self, world):
		(wx1, wy1), (wx2, wy2) = self.container.getWorld()
		world = self.container.getWorld()
		matrix = kaplot.Matrix.scalebox_inverse(*world)
		wp1 = matrix * self.p1
		wp2 = matrix * self.p2
		(wcsx1, wcsy1), (wcsx2, wcsy2) = self.container.getRange(self.wcs, self.transformation)
		wcsxlist, _ = self._getXticks2(wcsx1, wcsx2)
		wcsylist, __ = self._getXticks2(wcsy1, wcsy2)
		xticks = []
		xvalues = []
		wcs = self.wcs
		step = (wcsy2-wcsy1)/self.N
		wcsyrange = arange(wcsy1, wcsy2+step/2., step)
		r = lambda x, y: self.transformation.reverse(x, y)
		for wcsx in wcsxlist:
			for wcsy1, wcsy2 in zip(wcsyrange[:-1], wcsyrange[1:]):
				p1 = wcs.to_pixel(*r(rnd(wcsx), rnd(wcsy1)))
				p2 = wcs.to_pixel(*r(rnd(wcsx), rnd(wcsy2)))
				if p1 is not None and p2 is not None:
					w1 = kaplot.Vector(p1)
					w2 = kaplot.Vector(p2)
					p = self.lineintersection(wp1, wp2, w1, w2)
					if p:
					#if (w1.y < wy1 and w2.y >= wy1) or (w2.y < wy1 and w1.y >= wy1):
						# todo, intersection
						xticks.append(p.x)
						xvalues.append(wcsx)
			
		#print xticks
		return array(xticks), array(xvalues), []

class Transformation(object):
	def forward(self, x, y):
		pass

	def reverse(self, x, y):
		pass

class EpochTransformation(Transformation):
	def __init__(self, epoch_in, epoch_out):
		self.epoch_in = epoch_in
		self.epoch_out = epoch_out
		
	def forward(self, x, y):
		xa, ya = gipsy.epoco([x], [y], self.epoch_in, self.epoch_out)
		return xa[0], ya[0]
		
	def reverse(self, x, y):
		xa, ya = gipsy.epoco([x], [y], self.epoch_out, self.epoch_in)
		return xa[0], ya[0]
		
	def __str__(self):
		return "epoch %s -> %s" % (self.epoch_in, self.epoch_out)

	def userstring(self):
		return "%i" % (self.epoch_out)


class SkySystemTransformation(Transformation):
	smap = {kapu.EQUATORIAL_1950:"B1950", kapu.GALACTIC:"Gal", kapu.ECLIPTIC:"Ecliptic",
			kapu.SUPERGALACTIC:"SGal", kapu.EQUATORIAL_2000:"J2000"}

	def __init__(self, skysystem_in, skysystem_out):
		self.skysystem_in = skysystem_in
		self.skysystem_out = skysystem_out
		
	def forward(self, x, y):
		xa, ya = gipsy.skyco([x], [y], self.skysystem_in, self.skysystem_out)
		return xa[0], ya[0]
		
	def reverse(self, x, y):
		xa, ya = gipsy.skyco([x], [y], self.skysystem_out, self.skysystem_in)
		return xa[0], ya[0]

	def __str__(self):
		return "%s -> %s" % (self.smap[skysystem_in], self.smap[self.skysystem_out])

	def userstring(self):
		return self.smap[self.skysystem_out]

class CascaseTransformation(Transformation):
	def __init__(self, t1, t2):
		self.t1 = t1
		self.t2 = t2
	
	def forward(self, x, y):
		x1, y1 = self.t1.forward(x, y)
		return self.t2.forward(x1, y1)

	def reverse(self, x, y):
		x2, y2 = self.t2.reverse(x, y)
		return self.t1.reverse(x2, y2)

	def userstring(self):
		return "%s %s" % (t1.userstring(), t2.userstring())
		
	
class NoTransformation(object):
		
	def forward(self, x, y):
		return x, y
		
	def reverse(self, x, y):
		return x, y

	def userstring(self):
		return ""
		
def transformation(epoch_in=None, epoch_out=None, skysystem_in=kapu.EQUATORIAL_2000, skysystem_out=None):
	transformation = None
	if epoch_in is not None and epoch_out is not None:
		transformation = EpochTransformation(epoch_in, epoch_out)
	
	if skysystem_out is not None:
		skytrans = SkySystemTransformation(skysystem_in, skysystem_out)
		if transformation is not None:
			transformation = CascaseTransformation(transformation, skytrans)
		else:
			transformation = skytrans
			
	
	if transformation is None:
		transformation = NoTransformation()
	return transformation

transformationFunction = transformation # alias

class WcsBox(Container):
	def __init__(self, page, xformat=None, yformat=None, transformation=None, wcs=None, **kwargs):
		if xformat is None:
			self.xformat = timeformat
		else:
			self.xformat = xformat
		if yformat is None:
			self.yformat = degreeformat
		else:
			self.yformat = yformat
		super(WcsBox, self).__init__(page, **kwargs)
		self.border = kaplot.objects.Border(self)
		if transformation is None:
			self.transformation = NoTransformation()
		else:
			self.transformation = transformation
		self.tinfos = []
		if wcs is None:
			ref = (0, 0)
			self.wcs = Wcs(ref, ["RA---AIT", "DEC--AIT"], [1,0,0,1], (1,1), (0, 0), (0,0), [0.01,0,0,0.1], 1|2|4, [(1,0,1), (2,1,1)] )
		else:
			self.wcs = wcs

	def addTransformationInfo(self, name, transformation, xformat=None, yformat=None):
		if xformat is None:
			xformat = timeformat
		if yformat is None:
			yformat = degreeformat
		self.tinfos.append((name, transformation, xformat, yformat))

	def getMouseMoveText(self, x, y):
		vx, vy = self.getDocument().windowToViewport(x, y, self.innerViewport)
		px = kaplot.utils.convertPixelsTo(x, "cm")
		py = kaplot.utils.convertPixelsTo(y, "cm")
		wx, wy = self.windowToWorld(x, y)
		text = super(WcsBox, self).getMouseMoveText(x, y)
		result = self.wcs.from_pixel(wx, wy)
		if result:
			phx, phy = result
			phxt, phyt = self.transformation.forward(phx, phy)
			text += "\nphysical: %s %s" % (self.xformat(phxt), self.yformat(phyt))
		else:
			text += "\ninvalid coordinate"
		for name, trans, xformat, yformat in self.tinfos:
			phxt, phyt = trans.forward(phx, phy)
			text += "\n%s: %s %s" % (name, xformat(phxt), yformat(phyt))
		return text


	def getXticks(self, dev):
		matrix = dev.getWorldMatrix().inverse()
		v1 = (matrix * (0,0)).x
		v2 = (matrix * (1,0)).x
		#print "x %f %f" % (v1, v2)

		interval = self.xinterval
		if interval == None:
			diff = v2 - v1
			ticks = 3
			tick = diff / 4
			error = diff / 8.0
			interval = magicnr(tick, error)

		start = self.xstart
		if start == None:
			start = fround(v1, interval)

		ticks = arange(start-interval,v2+interval*1.5, interval)
		subticks = []

		if self.xsubticks > 0:
			subinterval = interval / (1+self.xsubticks)
			length = len(ticks)
			for i in range(length-1):
				v1 = ticks[i]+subinterval
				v2 = ticks[i+1]
				subticks += arange(v1, v2-subinterval/2, subinterval)


		return ticks, subticks

	def getYticks(self, dev):
		matrix = dev.getWorldMatrix().inverse()
		v1 = (matrix * (0,0)).y
		v2 = (matrix * (0,1)).y
		#print "y %f %f" % (v1, v2)

		interval = self.yinterval
		if interval == None:
			diff = v2 - v1
			ticks = 3
			tick = diff / 4
			error = diff / 10.0
			interval = magicnr(tick, error)

		start = self.ystart
		if start == None:
			start = fround(v1, interval)

		ticks = arange(start-interval,v2+interval*1.5, interval)
		subticks = []

		if self.ysubticks > 0:
			subinterval = interval / (1+self.ysubticks)
			length = len(ticks)
			for i in range(length-1):
				v1 = ticks[i]+subinterval
				v2 = ticks[i+1]
				subticks += arange(v1, v2-subinterval/2, subinterval)

		return ticks, subticks

	def getRange(self, wcs, transformation):
		ystart = -0.1
		yend = 1.1
		xstart = -0.1
		xend = 1.1
		step = (yend - ystart) / 10.0

		#matrix = self.getWorldMatrix().inverse()
		matrix = kaplot.Matrix.scalebox_inverse(*self.getWorld())
		#tinv = trans.inverse()
		longlist = []
		latlist = []
		for y in arange(ystart, yend+step/2, step):
			for x in arange(xstart, xend+step/2, step):
				p = (x, y)
				p1 = matrix * p
				pn = wcs.from_pixel(p1.x, p1.y)
				if pn == None:
					continue
				pn = transformation.forward(*pn)
				p2 = rndv(kaplot.vector.Vector(pn))
				#print pn, p2
				#print p1
				#print p1, p2, trans.forward(p2.x, p2.y)

				#p.x = (p.x + 180) % 360 - 180
				#p.x = (p.x + 0) % 360
				#p = trans.transformPoint(p)
				longlist.append(p2.x)
				latlist.append(p2.y)
		#print matrix, self.getWorld()
		lomin, lomax = min(longlist), max(longlist)
		lamin, lamax = min(latlist), max(latlist)
		#print lomin, lomax,lamin, lamax
		import pdb
		#pdb.set_trace()

		lodiff = lomax - lomin
		ladiff = lamax - lamin

		#lomin = max(lomin, -180)
		#print "lomax", lomax
		#lomax = min(lomax, 179.99)
		#lomin = max(lomin - lodiff * 0.5, -360)
		#lomax = min(lomax + lodiff * 0.5, 360)
		#lamin = max(lamin - ladiff * 0.5, -90)
		#lamax = min(lamax + ladiff * 0.5, 90)
		#print "laminmax", lamin, lamax, lomin, lomax
		#lamin = max(lamin, -80)
		#lamax = min(lamax, 80)
		#lomin = max(lomin - abs(lodiff) * 1.1, -179.9999)
		#lomax = min(lomax + abs(lodiff) * 1.1, 179.9999)
		#lomin = max(lomin - abs(lodiff) * 0.1, 0.0001)
		#lomax = min(lomax + abs(lodiff) * 0.1, 359.9999)
		#print "laminmax", lamin, lamax, lomin, lomax
		#lomin = max(lomin - lodiff * 0.5, 0.99)
		#lomax = min(lomax + lodiff * 0.5, 359.99)
		#print ((lomin, lamin), (lomax, lamax))

		return ((lomin, lamin), (lomax, lamax))


