import kapu
import numpy
from kapu import *
from numpy import *
from matplotlib.ticker import Locator

def subdivide(v1, v2, ticks=4, subticks=None, interval=None, start=None, integer=False, logarithmic=False):
	def nextpow10(n):
		"""Return the next power of 10"""
		if n == 0:
			return 0
		else:
			return math.ceil(math.log10(abs(n)))
	
	def fround(value, mod):
		if mod == 0:
			return value
		else:
			return int(value/mod) *mod
	
	def magicnr(value, error):
		"""Return a number that looks 'nice', with a maximum error"""
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
	
	realinterval = interval
	if realinterval == None:
		diff = v2 - v1
		#ticks = 3
		tick = diff / ticks
		error = diff / 10.0
		realinterval = magicnr(tick, error)

	interval = realinterval

	if integer:
		interval = int(interval+0.5)
		if interval == 0 and realinterval > 0:
			interval = 1
		if interval == 0 and realinterval < 0:
			interval = -1

	if start == None:
		start = fround(v1, interval) -interval

	if integer:
		ticks = numpy.arange(start, int(v2+1) + interval*1, interval)
	else:
		ticks = numpy.arange(start, v2 + interval*1.5, interval)
	subticklist = []
	#import pdb;pdb.set_trace()

	if subticks is not None and subticks > 0:
		if logarithmic:
			sigma = 1.0e-9
			# ok, this looks weird, but take base 10, with 8 subticks as an example
			# and it will make sense :), or base 3, with 1 subtick
			offsets = log(numarray.arange(2, subticks+1+sigma))/log(subticks+2)
			length = len(ticks)
			for i in range(length-1):
				offset = ticks[i]
				width = ticks[i+1] - ticks[i]
				subticklist.extend(list(offset+offsets*width))
		else:
			#print float(interval), subticks
			subinterval = float(interval) / (1+subticks)
			length = len(ticks)
			for i in range(length-1):
				v1 = ticks[i]+subinterval
				v2 = ticks[i+1]
				subticklist.extend(numarray.arange(v1, v2-subinterval/2, subinterval))
	if subticks is not None:
		return ticks, numarray.array(subticklist)
	else:
		return ticks
	
	
def rnd(x):
	return ((x + 360+180) % 360) - 180

def rndv(v):
	x, y = v
	return kapu.Vector(rnd(x), rnd(y))

class NoTransformation(object):
		
	def forward(self, x, y):
		return x, y
		
	def reverse(self, x, y):
		return x, y

	def userstring(self):
		return ""
		
class WcsXLocator(Locator):
	def __init__(self, wcsLocators):
		self.wcsLocators = wcsLocators
		self.N = 20
		#self.ticks = 
		
	def set_view_interval(self, interval):
		Locator.set_view_interval(self, interval)
		self.wcsLocators.setXInterval(interval)
		
	def set_data_interval(self, interval):
		Locator.set_data_interval(self, interval)
		#self.wcsLocators.setXInterval(interval)
		#self.wcsLocators.setDirty()
	
		
	#def labelx(self, value):
	def _getXticks2(self, v1, v2):
		return subdivide(v1, v2) #, ticks=self.ticks, subticks=self.subticks, interval=self.interval,
					#start=self.start, integer=self.integer, logarithmic=self.logarithmic)		

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
				return p1 + (p2 - p1).scalexy(ua, ua)
			else:
				return None
					
	def _getXticks(self, world):
		#(wx1, wy1), (wx2, wy2) = self.container.getWorld()
		#world = self.container.getWorld()
		#x1, x2 = self.wcsLocators.xbounds
		#y1, y2 = self.wcsLocators.ybounds
		#world = (x1, y1), (x2, y2)
		matrix = kapu.Matrix.scaleboxInverse(*world)
		self.p1 = (0, 0)
		self.p2 = (1, 0)
		wp1 = matrix * self.p1
		wp2 = matrix * self.p2
		if True:
			(wcsx1, wcsy1), (wcsx2, wcsy2) = self.wcsLocators.getRange()
			print "range:", self.wcsLocators.getRange()
			#print self._getXticks2(wcsx1, wcsx2)
			wcsxlist = self._getXticks2(wcsx1, wcsx2)
			wcsylist_ = self._getXticks2(wcsy1, wcsy2)
			print "xlist:",wcsxlist
			xticks = []
			xvalues = []
			wcs = self.wcsLocators.wcs
			step = (wcsy2-wcsy1)/self.N
			wcsyrange = arange(wcsy1, wcsy2+step/2., step)
			r = lambda x, y: self.wcsLocators.transformation.reverse(x, y)
			for wcsx in wcsxlist:
				for wcsy1, wcsy2 in zip(wcsyrange[:-1], wcsyrange[1:]):
					p1 = wcs.to_pixel(*r(rnd(wcsx), rnd(wcsy1)))
					p2 = wcs.to_pixel(*r(rnd(wcsx), rnd(wcsy2)))
					print p1, p2
					if p1 is not None and p2 is not None:
						w1 = kapu.Vector(p1)
						w2 = kapu.Vector(p2)
						p = self.lineintersection(wp1, wp2, w1, w2)
						if p:
						#if (w1.y < wy1 and w2.y >= wy1) or (w2.y < wy1 and w1.y >= wy1):
							# todo, intersection
							print p.x
							xticks.append(p.x)
							xvalues.append(wcsx)
			
		#print xticks
		return array(xticks), array(xvalues), []

	def __call__(self):
		#return [0, 0.1, 1]
		p = self._getXticks(self.wcsLocators.getWorld())[0]
		print "%" * 70
		print p
		print "%" * 70
		return p

class WcsYLocator(Locator):
	def __init__(self, wcsLocators):
		self.wcsLocators = wcsLocators
		
	def set_view_interval(self, interval):
		Locator.set_view_interval(self, interval)
		self.wcsLocators.setYInterval(interval)
		
	def set_data_interval(self, interval):
		Locator.set_data_interval(self, interval)
		#self.wcsLocators.setXInterval(interval)
		#self.wcsLocators.setDirty()
		
	def __call__(self):
		return [0, 0.1, 1]
		
class WcsLocators(object):
	
	def __init__(self, wcs=None):
		if wcs is None:
			ref = (20, 20)
			self.wcs = Wcs(ref, ["RA---AIT", "DEC--AIT"], [1,0,0,1], (1,1), (0, 0), (0,0), [0.01,0,0,0.1], 1|2|4, [(1,0,1), (2,1,1)] )
		else:
			self.wcs = wcs
		self.transformation = NoTransformation()
		self.xmajor = WcsXLocator(self)
		self.ymajor = WcsYLocator(self)
		self.dirty = True
		self.xbounds = (0, 1)
		self.ybounds = (0, 1)
		self.range = self.getRange()
		
	def setXInterval(self, interval):
		print "xinterval", interval.get_bounds()
		self.xbounds = interval.get_bounds()
		self.setDirty()

	def setYInterval(self, interval):
		print "yinterval", interval.get_bounds()
		self.ybounds = interval.get_bounds()
		self.setDirty()
		
	def setDirty(self):
		self.dirty = True
		
	def init(self, axes):
		axes.xaxis.set_major_locator(self.xmajor)
		axes.yaxis.set_major_locator(self.ymajor)
		
	def getWorld(self):		
		x1, x2 = self.xbounds
		y1, y2 = self.ybounds
		world = (x1, y1), (x2, y2)
		return world
			
	def getRange(self):
		wcs = self.wcs
		transformation = self.transformation
		if self.dirty:
			ystart = -0.1
			yend = 1.1
			xstart = -0.1
			xend = 1.1
			step = (yend - ystart) / 10.0
	
			#matrix = self.getWorldMatrix().inverse()
			matrix = kapu.Matrix.scaleboxInverse(*self.getWorld())
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
					p2 = rndv(kapu.vector.Vector(pn))
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
			self.dirty = False
			self.range = ((lomin, lamin), (lomax, lamax))
		return self.range
			
	
