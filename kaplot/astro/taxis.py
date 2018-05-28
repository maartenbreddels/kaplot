from plotobject import PlotObject
from properties import *
from plotobjects import Line
from math import sqrt, pi
from Kplot import Vector
#from axis import Axis
import plotobjects
from Kplot.transformations import NoTransformation
from Numeric import *
from Kplot.tools import *


#def transform(point, trans, ytrans):
#	x = xtrans.transform(point.x)
#	y = ytrans.transform(point.y)
#	return Vector((x,y))

class Timeformat:
	def __init__(self, inhours=1, diff=1, hours=1, minutes=1, seconds=1, mseconds=0):
		self.inhours = inhours
		self.diff = diff
		self.hours = hours
		self.minutes = minutes
		self.seconds = seconds
		self.mseconds = mseconds

	def start(self):
		self.first = 1

	def end(self):
		pass

	def format(self, value):
		if self.inhours:
			value = ((value / 15) + 24) % 24
		if self.first:
			self.first = 0
			label = self.fulllabel(value)
		else:
			if self.diff:
				label = self.difflabel(value)
			else:
				label = self.fulllabel(value)

		self.prev = value
		return label

	def difflabel(self, value):
		pn = abs(int(60*60*1000 * self.prev))
		n = int(60*60*1000 * value)
		timestr  = ""

		phours = pn / (60*60*1000)
		hours = n / (60*60*1000)
		pn -= phours * (60*60*1000)
		n -= hours * (60*60*1000)
		if self.hours and phours != hours:
			timestr += "%0.2ih" % hours

		pminutes = pn / (60*1000)
		minutes = n / (60*1000)
		pn -= pminutes * (60*1000)
		n -= minutes * (60*1000)
		if self.minutes and pminutes != minutes:
			timestr += "%0.2im" % minutes

		pseconds = pn / (1000)
		seconds = n / (1000)
		pn -= pseconds * (1000)
		n -= seconds * (1000)
		if self.seconds and pseconds != seconds:
			timestr += "%0.2is" % seconds

		pmseconds = pn
		mseconds = n
		if self.mseconds and pmseconds != mseconds:
			timestr += "%0.2ims" % mseconds
		#print "diff[%s]" % timestr
		return timestr

	def fulllabel(self, value):
		n = int(60*60*1000 * value)
		timestr  = ""

		hours = n / (60*60*1000)
		n -= hours * (60*60*1000)
		if self.hours:
			timestr += "%0.2ih" % hours

		minutes = n / (60*1000)
		n -= minutes * (60*1000)
		if self.minutes:
			timestr += "%0.2im" % minutes

		seconds = n / (1000)
		n -= seconds * (1000)
		if self.seconds:
			timestr += "%0.2is" % seconds

		mseconds = n
		n -= mseconds * (1000)
		if self.mseconds:
			timestr += "%0.2ims" % mseconds

		return timestr







def timeformat(value):
	n = int(60*60*1000 * value)
	mseconds = n % 1000
	n = n / 1000
	seconds = n % 60
	n = n / 60
	minutes = n % 60
	n = n / 60
	hours = n
	#timestr = "hh:mm:ss:ms %0.2i:%0.2i:%0.2i:%0.3i" % (hours,  minutes, seconds, mseconds)
	timestr = "%0.2i:%0.2i:%0.2i:%0.3i" % (hours,  minutes, seconds, mseconds)
	timestr = "%0.2i:%0.2i:%0.2i" % (hours,  minutes, seconds)
	return timestr

def timeformathours(value):
	value = ((value / 15.0) + 24) % 24
	n = int(60*60*1000 * value)
	mseconds = n % 1000
	n = n / 1000
	seconds = n % 60
	n = n / 60
	minutes = n % 60
	n = n / 60
	hours = n
	#timestr = "hh:mm:ss:ms %0.2i:%0.2i:%0.2i:%0.3i" % (hours,  minutes, seconds, mseconds)
	timestr = "%0.2i:%0.2i:%0.2i:%0.3i" % (hours,  minutes, seconds, mseconds)
	timestr = "%0.2i:%0.2i:%0.2i" % (hours,  minutes, seconds)
	return timestr

def defaultformat(value):
	return str(value)

def defaultformatfunc():
	return defaultformat
class TAxisLine:
	def __init__(self, p1, p2):
		self.p1 = p1
		self.p2 = p2

	def ytick(self, tick):
		height = self.p2.y - self.p1.y
		if height != 0.0:
			scale = (tick - self.p1.y) / height
			if scale != None and scale >= 0.0 and scale < 1.0:
				return self.p1 + (self.p2 - self.p1).scale(scale)
			else:
				return None
		else:
			return None

	def xtick(self, tick):
		width = self.p2.x - self.p1.x
		if width != 0.0:
			scale = (tick - self.p1.x) / width
			if scale != None and scale >= 0.0 and scale < 1.0:
				return self.p1 + (self.p2 - self.p1).scale(scale)
			else:
				return None
		else:
			return None

def subdiv(p1, p2, n):
	x = zeros(n) + 0.0
	y = zeros(n) + 0.0
	v = p2 - p1
	nminus1 = n - 1
	for i in xrange(n):
		p = p1 + v.scale(float(i)/nminus1)
		x[i] = p.x
		y[i] = p.y
	return (x, y)

class TAxis(PlotObject):
	ticks = autoproperty(default=[])
	ticklength = numberproperty(default=5)
	subdivides = numberproperty(default=50)
	#minorticks = numberproperty(default=1)
	labeloffset = numberproperty()
	side = stringproperty()
	color = colorproperty()
	labelcolor = colorproperty()
	linewidth = linewidthproperty()
	intersect = stringproperty(docstring="interect with 'x' or 'y' element")
	labelformatter = autoproperty()

	textangle = numberproperty(default=0)
	units = stringproperty()
	valign = stringproperty()
	halign = stringproperty()


	def __init__(self, side, labelformatter, defaults=None, **properties):
		PlotObject.__init__(self, defaults=defaults, properties=properties)
		self.side = side
		self.labelformatter = labelformatter
		if self.intersect == None:
			if self.side in ["left", "right"]:
				self.intersect = "y"
			elif self.side in ["top", "bottom"]:
				self.intersect = "x"
			else:
				raise Exception, "side must be 'left', 'right', 'top' or 'bottom'"
		if self.labeloffset == None:
			self.labeloffset = self.ticklength * 1.2


	def plot(self, dev):
		dev.setClipping(0)
		ticks = self.ticks
		matrix = (dev.getWorldMatrix()).inverse()
		if self.side == "left":
			start = matrix * (0, 1)
			end = matrix * (0, 0)
		elif self.side == "right":
			start = matrix * (1, 0)
			end = matrix * (1, 1)
		elif self.side == "top":
			start = matrix * (1, 1)
			end = matrix * (0, 1)
		elif self.side == "bottom":
			start = matrix * (0, 0)
			end = matrix * (1, 0)
		else:
			raise Exception, "side must be 'left', 'right', 'top' or 'bottom'"

		intersect = self.intersect

		#direction = end - start
		#length = direction.length()
		#unitdirection = direction.unit()
		#tickdir = Matrix.rotate(-90.0*pi/180.0) * unitdirection
		transformation = dev.transformation
		dev.transformation = NoTransformation()

		world = dev.getWorldMatrix().nolocation() #translate(-dev.getWorldMatrix().location())
		viewport = dev.getViewportMatrix().nolocation() #translate(-dev.getViewportMatrix().location())
		#scale = (viewport * world).inverse() * dev.getUnitMatrix(self.units)
		scale = (dev.getUnitMatrix(self.units).inverse() * viewport * world).inverse()

		direction = (scale * end) - (scale * start)

		#print self.side, start, end, direction, end-start
		#length = direction.length()
		unitdirection = direction.unit()
		tickdir = Matrix.rotate(-90.0*pi/180.0) * unitdirection
		#print tickdir
		#tickdir = scale.inverse() * tickdir
		tickdir = tickdir.unit()

		x, y = subdiv(start, end, self.subdivides)
		tx, ty = transformation.inverse().transform(x, y)
		tx = (tx + 180) % 360 - 180
		#print tx, ty
		#print min(tx), max(tx)


		#tpoints = []
		#for point in points:
		#	tpoints.append(dev.transformation.transformPoint((point.x, point.y)))

		#tlines = [AxisLine(start, end) for point
		tlines = []
		for i in range(len(tx)-1):
			tlines.append(TAxisLine(Vector(tx[i], ty[i]), Vector(tx[i+1], ty[i+1]) ))

		gfxline = plotobjects.Line(start, end, color=self.color, linestyle="normal", linewidth=self.linewidth)
		gfxline.plot(dev)
		angle = tickdir.angle()

		self.labelformatter.start()

		if intersect == "y":
			for tick in ticks:
				for line in tlines:
					pos = line.ytick(tick)
					if pos:
						pos = transformation.transformPoint(pos)
						tickend = pos + tickdir.scale(self.ticklength)
						gfxline = plotobjects.Line(pos, tickend, color=self.color, linestyle="normal", linewidth=self.linewidth)
						gfxline.plot(dev)
						self.label(tick, pos + tickdir.scale(self.labeloffset), dev, angle)
		elif intersect == "x":
			for tick in ticks:
				for line in tlines:
					pos = line.xtick(tick)
					#print line.p1, line.p2, pos
					if pos:
						pos = transformation.transformPoint(pos)
						tickend = pos + tickdir.scale(self.ticklength)
						gfxline = plotobjects.Line(pos, tickend, color=self.color, linestyle="normal", linewidth=self.linewidth)
						gfxline.plot(dev)
						self.label(tick, pos + tickdir.scale(self.labeloffset), dev, angle)
		else:
			raise Exception, "unknown intersect: " +str(intersect)

		self.labelformatter.end()
		dev.transformation = transformation
		dev.setClipping(1)
		return

	def label(self, tick, position, dev, angle):
		textstr = self.labelformatter.format(tick)

		textangle = self.textangle
		halign = self.halign
		if halign == None:
			halign = self.getHalign(angle, textangle)

		valign = self.valign
		if valign == None:
			valign = self.getValign(angle, textangle)

		print "@", halign, valign
		text = plotobjects.Text(textstr, position, textangle=textangle, color=self.labelcolor, halign=halign, valign=valign)
		text.plot(dev)

	def getHalign(self, tickangle, textangle):
		"""
		Return the horizontal alignment based on the
		octant the angle between the tickangle and
		textangle

		 \2,3/
		  \ /
		4,5x1,8
		  / \
		 /6,7\

		octant:
			1,8:		"right"
			2,3,6,7:	"center"
			4,5:		"left"

		"""
		tickangle = (todegrees(tickangle) + 360) % 360
		textangle = (todegrees(textangle) + 360) % 360
		angle = (tickangle-textangle + 360.0) % 360
		octant = int(angle / 45) + 1
		#print tickangle, textangle, angle, octant
		if octant in [1,8]:
			return "left"
		elif octant in [2,3,6,7]:
			return "center"
		elif octant in [4,5]:
			return "right"
		return "center"


	def getValign(self, tickangle, textangle):
		"""
		Return the vertical alignment based on the
		octant the angle between the tickangle and
		textangle

		 \2,3/
		  \ /
		4,5x  1,8
		  / \
		 /6,7\

		octant:
			1,8,4,5:	"center"
			6,7:		"top"
			2,3:		"bottom"

		"""
		tickangle = (todegrees(tickangle) + 360) % 360
		textangle = (todegrees(textangle) + 360) % 360
		angle = (tickangle-textangle + 360.0) % 360
		octant = int(angle / 45) + 1
		#print "valign", tickangle, textangle, octant
		if octant in [1,8,4,5]:
			return "center"
		elif octant in [6,7]:
			return "top"
		elif octant in [2,3]:
			return "bottom"
		return "center"



	#def label(self, tick, position, dev, angle):
	#	tick = int(tick * 100) / 100.0
	#	textstr = self.labelformatter.format(tick)
#
#		if angle > 90+45 and angle <= 180+45: # left
#			textangle=0
#			halign = "right"
#			valign = "center"
#		elif angle > 180+45 and angle <= 270+45: # bottom
#			textangle=0
#			halign = "center"
#			valign = "top"
#		text = plotobjects.Text(textstr, position, color=self.labelcolor, textangle=0, halign=halign, valign=valign)
#		text.plot(dev)







