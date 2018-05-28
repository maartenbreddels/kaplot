from matplotlib.axes import SubplotBase, Axes, _process_plot_var_args, \
	_process_plot_var_args, rcParams, Text, FontProperties, linspace,\
	Polygon, Interval, Value, ScalarFormatter, AutoLocator, Bbox, Point, \
	NonseparableTransformation, FuncXY, POLAR, LOG10, get_bbox_transform, unit_bbox,\
	popall, Line2D, IDENTITY
from matplotlib.axis import Axis, XAxis, YAxis,\
	XTick, YTick, \
	 NullLocator, AutoLocator, ScalarFormatter, NullFormatter
from matplotlib.artist import Artist
from matplotlib.ticker import Locator
from matplotlib.transforms import Interval, Value, \
	blend_xy_sep_transform

from kapu.stereographic import StereoGraphicProjection
from pylab import gcf
import math
from numpy import *
import kapu

def rnd(x):
	return ((x + 360+180) % 360) - 180

def r180(x):
	return ((x + 360+180) % 360) - 180

def r90(x):
	return ((x + 180+90) % 180) - 90

def rndv(v):
	x, y = v
	return kapu.Vector(rnd(x), rnd(y))

def gca_wcs(**kwargs):
	fig = gcf()#.gca(**kwargs)
	ax = fig._axstack()
	if ax is not None:
		return ax
	else:
    	# code dup from Figure.gca and Figure.add_subplot
		args = [111]
		key = fig._make_key(*args, **kwargs)
		if fig._seen.has_key(key):
			ax = fig._seen[key]
			fig.sca(ax)
			return ax
		
		
		if not len(args): return
		
		a = WcsSubPlot(fig, *args, **kwargs)
		
		fig.axes.append(a)
		fig._axstack.push(a)
		fig.sca(a)
		fig._seen[key] = a
		return a
    
    
def wcsplot(*args, **kwargs):
    """
    wcs()
    """
    ax = gca_wcs()
    return ax.plot(*args, **kwargs) 

def lineintersection(p1, p2, p3, p4):
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

	
class WcsLocator(Locator):
	def __init__(self, axis, slocator):
		self.axis = axis
		self.axes = self.axis.axes
		self.slocator = slocator
		self.N = 20
		self.locationMap = {}


class WcsXLocator(WcsLocator): # Theta
	def __call__(self):
		self.slocator.set_view_interval(self.viewInterval)
		self.slocator.set_data_interval(self.dataInterval)
		(theta1, phi1), (theta2, phi2) = self.axes.getWcsBbox()
		thetaInterval = Interval(Value(theta1), Value(theta2))
		#print "theta interval:", theta1, theta2
		self.slocator.set_view_interval(thetaInterval)
		self.slocator.set_data_interval(thetaInterval)
		thetaValues = self.slocator()
		
		xValues  = []
		step = (phi2-phi1)/self.N
		phiRange = arange(phi1, phi2+step/2., step)
		phiRangeZipped = zip(phiRange[:-1], phiRange[1:])
		#print phiRange
		#print thetaValues
		
		wcs = self.axes.wcs
		(x1, y1), (x2, y2) = self.axes.getWorld()
		
		axis_start = kapu.Vector(x1, y1)
		axis_end = kapu.Vector(x2, y1)
		
		self.locationMap = {}
		for theta in thetaValues:
			for phi1, phi2 in phiRangeZipped:
				#print "theta:", theta, phi1, phi2
				p1 = wcs.to_pixel(theta, phi1)
				p2 = wcs.to_pixel(theta, phi2)
				if p1 is not None and p2 is not None:
					w1 = kapu.Vector(p1)
					w2 = kapu.Vector(p2)
					p = lineintersection(axis_start, axis_end, w1, w2)
					#print w1.x, w1.y, w2.x, w2.y
					if p:
						#print p
						self.locationMap[p.x] = theta
						xValues.append(p.x)
		return array(xValues)

		
		
		
class WcsYLocator(WcsLocator):
	def __call__(self):
		self.slocator.set_view_interval(self.viewInterval)
		self.slocator.set_data_interval(self.dataInterval)
		(theta1, phi1), (theta2, phi2) = self.axes.getWcsBbox()
		phiInterval = Interval(Value(phi1), Value(phi2))
		#print "theta interval:", theta1, theta2
		self.slocator.set_view_interval(phiInterval)
		self.slocator.set_data_interval(phiInterval)
		phiValues = self.slocator()
		
		yValues  = []
		step = (theta2-theta1)/self.N
		thetaRange = arange(theta1, theta2+step/2., step)
		thetaRangeZipped = zip(thetaRange[:-1], thetaRange[1:])
		#print "theta", thetaRange
		#print "phi", phiValues
		
		wcs = self.axes.wcs
		(x1, y1), (x2, y2) = self.axes.getWorld()
		
		axis_start = kapu.Vector(x1, y1)
		axis_end = kapu.Vector(x1, y2)
		
		#self.locationMap = {}
		for phi in phiValues:
			if phi >= -90 and phi <= 90:
				print "phi =", phi
				for theta1, theta2 in thetaRangeZipped:
					#print "theta:", theta, phi1, phi2
					#if (theta1 <= 90 or theta1 >= -90) and (theta2 <= 90 or theta2 >= -90):
						p1 = wcs.to_pixel(r180(theta1), r90(phi))
						p2 = wcs.to_pixel(r180(theta2), r90(phi))
						if p1 is not None and p2 is not None:
							w1 = kapu.Vector(p1)
							w2 = kapu.Vector(p2)
							p = lineintersection(axis_start, axis_end, w1, w2)
							#print w1.x, w1.y, w2.x, w2.y
							if p:
								print p.y
								#self.locationMap[p.y] = phi
								yValues.append(p.y)
								break # we only want 1 label
		return array(yValues)


class WcsXAxis(XAxis):
	def cla(self):
		XAxis.cla(self)
		self.set_major_locator(WcsXLocator(self, AutoLocator()))
		self.set_major_formatter(ScalarFormatter())
		self.set_minor_locator(NullLocator())
		self.set_minor_formatter(NullFormatter())
		

class WcsYAxis(YAxis):
	def cla(self):
		YAxis.cla(self)
		self.set_major_locator(WcsYLocator(self, AutoLocator()))
		self.set_major_formatter(ScalarFormatter())
		self.set_minor_locator(NullLocator())
		self.set_minor_formatter(NullFormatter())

class NoTransformation(object):
		
	def forward(self, x, y):
		return x, y
		
	def reverse(self, x, y):
		return x, y

	def userstring(self):
		return ""

class WcsGrid(Artist):
	zorder = 3
	N = 30
	def __init__(self, axes):
		self.axes = axes
		
	def draw(self, renderer):

		phiValues = self.axes.yaxis.major.locator.slocator()
		thetaValues = self.axes.xaxis.major.locator.slocator()
		
		(theta1, phi1), (theta2, phi2) = self.axes.getWcsBbox()

		thetaStep = (theta2-theta1)/self.N
		thetaValuesSmall = arange(theta1, theta2+thetaStep/2., thetaStep)
		thetaValuesSmallZipped = zip(thetaValuesSmall[:-1], thetaValuesSmall[1:])

		phiStep = (phi2-phi1)/self.N
		phiValuesSmall = arange(phi1, phi2+phiStep/2., phiStep)
		phiValuesSmallZipped = zip(phiValuesSmall[:-1], phiValuesSmall[1:])

		wcs = self.axes.wcs
		
		# lines at constant phi (horizontal)
		for phi in phiValues:
			print "line phi =", phi
			for theta1, theta2 in thetaValuesSmallZipped:
				xData = []
				yData = []
				p1 = wcs.to_pixel(rnd(theta1), rnd(phi))
				p2 = wcs.to_pixel(rnd(theta2), rnd(phi))
				if p1 is not None and p2 is not None:
					x1, y1 = p1
					x2, y2 = p2
					xData.append(x1)
					xData.append(x2)
					yData.append(y1)
					yData.append(y2)
				self.drawLine(xData, yData, renderer)

		# lines at constant theta (vertical)
		
		for theta in thetaValues:
			xData = []
			yData = []
			print "line theta =", theta
			for phi, phi2 in phiValuesSmallZipped:
				p = wcs.to_pixel(rnd(theta), rnd(phi))
				if p is not None:
					x, y = p
					xData.append(x)
					yData.append(y)
			self.drawLine(xData, yData, renderer)

	def drawLine(self, xData, yData, renderer):
		line = Line2D( xdata=xData, ydata=yData,
					color=rcParams['grid.color'],
					#linestyle=rcParams['grid.linestyle'],
					linewidth=rcParams['grid.linewidth'],
					antialiased=True,
				)
		line.set_transform( blend_xy_sep_transform( self.axes.transData,
		                         self.axes.transData) )
		line.set_clip_box(self.axes.bbox)
		#self._set_artist_props(line)
		line.draw(renderer)

	def get_animated(self):
		return False
		
class WcsAxes(Axes):
	def __init__(self, *args, **kwargs):
		self.wcsBbox = (0, 0), (1, 1)
		ref = (0, 50)
		s = 1.0
		self.wcs = kapu.Wcs(ref, ["RA---AIT", "DEC--AIT"], [s,0,0, s], (1,1), (0, 0), (0,0), [1,0,0,1], 1|2|4, [(1,0,1), (2,1,1)] )
		#self.wcs = StereoGraphicProjection()
		self.transformation = NoTransformation()
		Axes.__init__(self, *args, **kwargs)
		#self.dirty = True
		#self.xbounds = (0, 1)
		#self.ybounds = (0, 1)
		#self.range = self.getWcsBbox()
		#self.set_aspect('auto')
		#self.cla() 
		self.wcsgrid = WcsGrid(self)
		self.collections.append(self.wcsgrid)
		
	def autoscale_view(self, scalex=True, scaley=True):
		Axes.autoscale_view(self, scalex=scalex, scaley=scaley)
		self.calcWcsBbox()
		#print self.getWcsBbox()

	def draw_(self, renderer):
		#(theta1, phi1), (theta2, phi2) = self.axes.getWcsBbox()
		pass

	def setXInterval(self, interval):
		#print "xinterval", interval.get_bounds()
		self.xbounds = interval.get_bounds()
		self.setDirty()

	def setYInterval(self, interval):
		#print "yinterval", interval.get_bounds()
		self.ybounds = interval.get_bounds()
		self.setDirty()

	def setDirty(self):
		self.dirty = True

	def getWorld(self):		
		x1, x2 = self.xaxis.major.locator.viewInterval.get_bounds()
		y1, y2 = self.yaxis.major.locator.viewInterval.get_bounds()
		world = (x1, y1), (x2, y2)
		return world
		
	def getWcsBbox(self):
		return self.wcsBbox
			
	def calcWcsBbox(self):
		wcs = self.wcs
		transformation = self.transformation
		if True:
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
			if False:
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
			if True:
				(x1, y1), (x2, y2) = self.getWorld()
				stepx = (x2 - x1) / 10
				stepy = (x2 - x1) / 10
				for x in arange(x1, x2+stepx/2, stepx):
					p = wcs.from_pixel(x, y1)
					if p is not None:
						lon, lat = p
						longlist.append(lon)
						latlist.append(lat)
					p = wcs.from_pixel(x, y2)
					if p is not None:
						lon, lat = p
						longlist.append(lon)
						latlist.append(lat)
					
				for y in arange(y1, y2+stepy/2, stepy):
					p = wcs.from_pixel(x1, y)
					if p is not None:
						lon, lat = p
						longlist.append(lon)
						latlist.append(lat)
					p = wcs.from_pixel(x2, y)
					if p is not None:
						lon, lat = p
						longlist.append(lon)
						latlist.append(lat)
					
				for x, y in zip(arange(x1, x2+stepx/2, stepx), arange(y1, y2+stepy/2, stepy)):
					p = wcs.from_pixel(x, y)
					if p is not None:
						lon, lat = p
						longlist.append(lon)
						latlist.append(lat)

					
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
			#self.dirty = False
			self.wcsBbox = (lomin-lodiff*0.2, lamin-ladiff*0.2),\
							(lomax+lodiff*0.2, lamax+ladiff*0.2)
			#self.wcsBbox = (lomin, lamin), (lomax, lamax)
		#return self.wcsBox
			
	
	def format_coord(self, theta, r):
		return "coords..."

	def _init_axis(self):
		self.xaxis = WcsXAxis(self)
		self.yaxis = WcsYAxis(self)
		
	def cla_(self):
		self._get_lines = _process_plot_var_args()
		self._get_patches_for_fill = _process_plot_var_args('fill')
		
		#self._gridOn = rcParams['polaraxes.grid']
		self.thetagridlabels = []
		self.thetagridlines = []
		self.rgridlabels = []
		self.rgridlines = []
		
		self.lines = []
		self.images = []
		self.patches = []
		self.artists = []
		self.collections = []
		self.texts = []     # text in axis coords
		

class WcsSubPlot(SubplotBase, WcsAxes):
	def __init__(self, fig, *args, **kwargs):
		SubplotBase.__init__(self, fig, *args)
		WcsAxes.__init__(self, fig, [self.figLeft, self.figBottom, self.figW, self.figH], **kwargs) 	
		        