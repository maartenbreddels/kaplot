from kaplot.objects import PlotObject
from kaplot.vector import Vector
from kaplot.matrix import Matrix
from math import sqrt, pi
from numarray import *
from kaplot.tools import *
import kaplot.context

class Timeformat:
	def __init__(self, inhours=1, diff=1, hours=1, minutes=1, seconds=1, mseconds=0):
		self.inhours = inhours
		self.diff = diff
		self.hours = hours
		self.minutes = minutes
		self.seconds = seconds
		self.mseconds = mseconds

	def start(self):
		self.first = True

	def end(self):
		pass

	def format(self, value):
		if self.inhours:
			value = ((value / 15) + 24) % 24
		return self.fulllabel(value)
		if self.first:
			self.first = False
			label = self.fulllabel(value)
		else:
			if self.diff:
				label = self.difflabel(value)
			else:
				label = self.fulllabel(value)

		self.prev = value
		if len(label) > 1:
			return label
		else:
			return "+0"

	def difflabel(self, value):
		def strsign(i):
			if i < 0:
				return "-"
			else:
				return "+"


		pn = abs(int(60*60*1000 * self.prev))
		n = int(60*60*1000 * value)

		timestr = ""
		phours = pn / (60*60*1000)
		hours = n / (60*60*1000)
		pn -= phours * (60*60*1000)
		n -= hours * (60*60*1000)
		if self.hours and phours != hours:
			#timestr = strsign(
			value = ((hours-phours)+24) %24
			timestr += "%0.2ih" % value

		pminutes = pn / (60*1000)
		minutes = n / (60*1000)
		pn -= pminutes * (60*1000)
		n -= minutes * (60*1000)
		if self.minutes and pminutes != minutes:
			#if len(timestr) == 0: timestr = sign
			timestr += "%0.2im" % (((minutes-pminutes)+60)%60)

		pseconds = pn / (1000)
		seconds = n / (1000)
		pn -= pseconds * (1000)
		n -= seconds * (1000)
		if self.seconds and pseconds != seconds:
			#if len(timestr) == 0: timestr = sign
			timestr += "%0.2is" % (((seconds-pseconds)+60)%60)

		pmseconds = pn
		mseconds = n
		if self.mseconds and pmseconds != mseconds:
			#if len(timestr) == 0: timestr = sign
			timestr += "%0.2ims" % (((mseconds-pmseconds)+1000)%1000)
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

class WcsAxis(PlotObject):
	#ticks = autoproperty(default=[])
	#ticklength = numberproperty(default=5)
	#subdivides = numberproperty(default=50)
	##minorticks = numberproperty(default=1)
	#labeloffset = numberproperty()
	#side = stringproperty()
	#color = colorproperty()
	#labelcolor = colorproperty()
	#linewidth = linewidthproperty()
	#intersect = stringproperty(docstring="interect with 'x' or 'y' element")
	#labelformatter = autoproperty()
    #
	#textangle = numberproperty(default=0)
	#units = stringproperty()
	#valign = stringproperty()
	#halign = stringproperty()


	def __init__(self, transformation, intersect, p1=None, p2=None, side=None, \
			ticks=[], subdivides=10, units="mm", lock=True, context=None, **kwargs):
		PlotObject.__init__(self, lock=False, context=kaplot.context.mergeDicts(context, kwargs), clipping=False)
		self.side = side
		self.subdivides = subdivides
		self.transformation = transformation
		self.ticks = []
		self.intersect = intersect
		self.units = units
		self.textangle = toradians(0)
		self.halign = None
		self.valign = None
		self.labelformatter = Timeformat()
		self.ticklength = 0.01
		self.labeloffset = 0.01
		if side == None:
			if p1 == None or p2 == None:
				raise Exception, "invalid arguments, use p1 and p2, or side"
			self.p1 = p1
			self.p2 = p2
		else:
			if side == "left":
				self.p1 = (0, 1)
				self.p2 = (0, 0)
			elif side == "bottom":
				self.p1 = (0, 0)
				self.p2 = (1, 0)
			elif side == "right":
				self.p1 = (1, 0)
				self.p2 = (1, 1)
			elif side == "top":
				self.p1 = (1, 1)
				self.p2 = (0, 1)
			else:
				raise Exception, "invalid side: " +str(side)
		#if self.labeloffset == None:
		#	self.labeloffset = self.ticklength * 1.2
		self.yformat = u"%(d1)i\xB0%(d2)02i'%(d3)02.2f''"
		self.xformat = u"%(hour)ih%(minute)02im%(second)02.2fs"
		if lock:
			self._lock()


	def ______plot(self, device):
		#return
		device.pushContext(self.context)
		ticks = self.ticks

		intersect = self.intersect

		worldmatrix = device.getWorldMatrix()
		invworldmatrix = worldmatrix.inverse()
		device.pushWorldMatrix(invworldmatrix)

		start = invworldmatrix * self.p1
		end = invworldmatrix * self.p2

		tickdir = Matrix.rotate(toradians(-90)) * (Vector(self.p2)-Vector(self.p1)).unit()

		device.plotLine(self.p1, self.p2)
		tickangle = tickdir.angle()
		scale = device.getUnitMatrix(self.units)

		x, y = subdiv(start, end, self.subdivides)
		tx, ty = self.transformation.reversearray(x, y)
		#import pdb
		#pdb.set_trace()
		#tx = (tx + 180) % 360 - 180

		tlines = []
		#tx = ((array(tx) + 180) % 360) - 180
		for i in range(len(tx)-1):
			tlines.append(TAxisLine(Vector(tx[i], ty[i]), Vector(tx[i+1], ty[i+1]) ))
			#print tx[i], ty[i], "-->", tx[i+1], ty[i+1]
		print "ticks", self.ticks

		angle = (tickdir.angle())
		print ">>> tickdir", angle, self.intersect

		self.labelformatter.start()
		self.ticklength = 0.01
		self.labeloffset = 0.01
		if self.intersect == "y":
			for tick in ticks:
				for line in tlines:
					pos = line.ytick(tick)
					if pos:
						posworld = self.transformation.forward(pos.x, pos.y)
						if posworld != None:
							pos1 = worldmatrix * posworld
							print "BLAATy", pos1, posworld
							#pos2 = worldmatrix * self.transformation.forward(pos.x-1, pos.y)

							#tickdir = (pos2 - pos1).unit()
							#print pos1, tickdir
							tickend = pos1 - tickdir.scale(self.ticklength)
							device.plotLine(pos1, tickend)
							self.label(tick, pos1 + tickdir.scale(self.labeloffset), device, angle)
		elif self.intersect == "x":
			for tick in ticks:
				for line in tlines:
					pos = line.xtick(tick)
					if pos:
						posworld = self.transformation.forward(pos.x, pos.y)
						if posworld != None:
							pos1 = worldmatrix * posworld
							print "BLAATx", pos1, posworld
							#pos2 = worldmatrix * self.transformation.forward(pos.x-1, pos.y)
							#tickdir = (pos2 - pos1).unit()
							#print pos1, tickdir
							tickend = pos1 - tickdir.scale(self.ticklength)
							device.plotLine(pos1, tickend)
							self.label(tick, pos1 + tickdir.scale(self.labeloffset), device, angle)
		else:
			raise Exception, "unknown intersect: " +str(intersect)

		self.labelformatter.end()
		device.popWorldMatrix()
		assert device.popContext() == self.context
		return

	def _doAxis(self, device, callback, drawAxis):
		device.pushContext(self.context)

		ticks = self.ticks
		intersect = self.intersect

		worldmatrix = device.getWorldMatrix()
		invworldmatrix = worldmatrix.inverse()
		device.pushWorldMatrix(invworldmatrix)

		start = invworldmatrix * self.p1
		end = invworldmatrix * self.p2

		tickdir = Matrix.rotate(toradians(-90)) * (Vector(self.p2)-Vector(self.p1)).unit()

		if drawAxis:
			device.plotLine(self.p1, self.p2)
		tickangle = tickdir.angle()
		scale = device.getUnitMatrix(self.units)

		x, y = subdiv(start, end, self.subdivides)
		tx, ty = self.transformation.reversearray(x, y)
		#import pdb
		#pdb.set_trace()
		#tx = (tx + 180) % 360 - 180

		#print "AXIS", x, y, tx, ty, self.transformation.forwardarray(tx, ty)
		tlines = []
		#tx = ((array(tx) + 180) % 360) - 180
		for i in range(len(tx)-1):
			tlines.append(TAxisLine(Vector(tx[i], ty[i]), Vector(tx[i+1], ty[i+1]) ))

		angle = (tickdir.angle())

		self.labelformatter.start()
		#self.ticklength = 0.01
		#self.labeloffset = 0.01
		if self.intersect == "y":
			for tick in ticks:
				for line in tlines:
					pos = line.ytick(tick)
					if pos:
						posworld = self.transformation.forward(pos.x, pos.y)
						if posworld != None:
							pos1 = worldmatrix * posworld
							#print "BLAATy", pos1, posworld
							#pos2 = worldmatrix * self.transformation.forward(pos.x-1, pos.y)

							#tickdir = (pos2 - pos1).unit()
							#print pos1, tickdir
							tickend = pos1 - tickdir.scale(self.ticklength)
							if drawAxis:
								device.plotLine(pos1, tickend)
							#self.label(tick, pos1 + tickdir.scale(self.labeloffset), device, angle)
							callback(tick, pos1 + tickdir.scale(self.labeloffset), angle)
		elif self.intersect == "x":
			for tick in ticks:
				for line in tlines:
					pos = line.xtick(tick)
					if pos:
						posworld = self.transformation.forward(pos.x, pos.y)
						if posworld != None:
							pos1 = worldmatrix * posworld
							#print "BLAATx", pos1, posworld
							#pos2 = worldmatrix * self.transformation.forward(pos.x-1, pos.y)
							#tickdir = (pos2 - pos1).unit()
							#print pos1, tickdir
							tickend = pos1 - tickdir.scale(self.ticklength)
							if drawAxis:
								device.plotLine(pos1, tickend)
							#self.label(tick, pos1 + tickdir.scale(self.labeloffset), device, angle)
							callback(tick, pos1 + tickdir.scale(self.labeloffset), angle)
		else:
			raise Exception, "unknown intersect: " +str(intersect)

		self.labelformatter.end()
		device.popWorldMatrix()
		device.popContext() == self.context
		return tickdir.scale(self.labeloffset)

	def plot(self, device):
		def labelCallback(tick, position, angle):
			self.label(tick, position, device, angle)
		self._doAxis(device, labelCallback, True)

	def getMargin(self, device):
		global minpoint, maxpoint
		#minpoint = None
		#maxpoint = None
		xpoints = [0.0, 1.0]
		ypoints = [0.0, 1.0]
		def xCallback(tick, position, angle):
			global minpoint, maxpoint
			p1, p2, p3, p4 = self.labelBBox(tick, position, device, angle)
			#if minpoint is None:
			#	minpoint = kaplot.vector.Vector(p1)
			#if maxpoint is None:
			#	maxpoint = kaplot.vector.Vector(p1)
			#minpoint.x = min(p1.x, p2.x, p3.x, p4.x, minpoint.x)
			#minpoint.y = min(p1.y, p2.y, p3.y, p4.y, minpoint.y)
			#maxpoint.x = max(p1.x, p2.x, p3.x, p4.x, maxpoint.x)
			#maxpoint.y = max(p1.y, p2.y, p3.y, p4.y, maxpoint.y)
			#self.label(tick, position, device, angle)
			#print p1
			#print p2
			#print p3
			#print p4
			xpoints.extend([p1.x, p2.x, p3.x, p4.x])
			ypoints.extend([p1.y, p2.y, p3.y, p4.y])
		labelvector = self._doAxis(device, xCallback, False)
		#if maxpoint is None:
		#	return kaplot.vector.Vector(0,0)
		#else:
		#	return maxpoint - minpoint + labelvector.abs()
		if len(xpoints) == 0:
			return kaplot.vector.Vector(0,0), kaplot.vector.Vector(1,1)
		else:
			return kaplot.vector.Vector(min(xpoints), min(ypoints)), kaplot.vector.Vector(max(xpoints), max(ypoints))


	def getXMargin(self, device):
		margin = self.getMargin(device)
		return margin.x

	def getYMargin(self, device):
		margin = self.getMargin(device)
		return margin.y

	def ______label(self, tick, position, device, angle):
		#textstr = self.labelformatter.format(tick)
		textstr = str(tick)
		textstr = self.defaultLabel(tick)


		textangle = self.textangle
		halign = self.halign
		if halign == None:
			halign = self.getHalign(angle, textangle)

		valign = self.valign
		if valign == None:
			valign = self.getValign(angle, textangle)

		#print "@", halign, valign
		#halign, valign = "center", "bottom"
		#halign = self.getHalign(angle)
		#valign = self.getValign()
		device.plotText(textstr, position, textangle=textangle, halign=halign, valign=valign)

	def _getLabelData(self, tick, tickangle):
		#if self.labeler == None:
		textstr = self.getDefaultLabel(tick)
		#e#lse:
		#	textstr = "..."
		#textstr = self.labelformatter.format(tick)

		textangle = self.textangle
		halign = self.halign
		if halign == None:
			halign = self.getHalign(tickangle, textangle)

		valign = self.valign
		if valign == None:
			valign = self.getValign(tickangle, textangle)
		return textstr, halign, valign

	def labelBBox(self, tick, position, device, tickangle):
		textstr, halign, valign = self._getLabelData(tick, tickangle)
		#text = Text(textstr, position, textangle=textangle, color=self.labelcolor, halign=halign, valign=valign)
		#text.plot(dev)
		return device.getTextBbox(textstr, position, halign=halign, valign=valign, textangle=self.textangle)


	def label(self, tick, position, device, tickangle):
		textstr, halign, valign = self._getLabelData(tick, tickangle)
		#text = Text(textstr, position, textangle=textangle, color=self.labelcolor, halign=halign, valign=valign)
		#text.plot(dev)
		device.plotText(textstr, position, halign=halign, valign=valign, textangle=self.textangle)

	def getDefaultLabel(self, tick):
		degree1 = int(tick)
		degree2 = int((tick * 100  - degree1 * 100))
		degree3 = ((tick * 10000 - degree1 * 10000 - degree2 * 100))
		tick = (tick + 360) % 360
		totalhours = float(tick * 24.0 / 360)
		hours = int(totalhours)
		minutes = int((totalhours*60 - hours*60))
		seconds = (totalhours * 3600 - hours * 3600 - minutes * 60)
		values = {"d1":degree1, "d2":degree2, "d3":degree3, "hour":hours, "minute":minutes, "second":seconds}
		if self.intersect == "y":
			return  self.yformat % values
		else:
			return self.xformat % values

	def getHalign(self, tickangle, textangle):
		"""
		Return the horizontal alignment based on the
		octant the angle between the tickangle and
		textangle

		"""


		tickangle = (todegrees(tickangle) + 360) % 360
		textangle = (todegrees(textangle) + 360) % 360
		angle = (textangle-tickangle + 360.0) % 360
		octant = (int((angle+22.5) / 45)%8) + 1
		#print tickangle, textangle, angle, octant

		#print "octant(h)", octant, tickangle, textangle
		if octant in [1,2,8]:
			return "left"
		elif octant in [3,7]:
			return "center"
		elif octant in [4,5,6]:
			return "right"
		return "center"


	def getValign(self, tickangle, textangle):
		"""
		Return the vertical alignment based on the
		octant the angle between the tickangle and
		textangle


		"""


		tickangle = (todegrees(tickangle) + 360) % 360
		textangle = (todegrees(textangle) + 360) % 360
		angle = (textangle-tickangle + 360.0) % 360
		octant = (int((angle+22.5) / 45)%8) + 1
		#print "valign", tickangle, textangle, octant
		#print "octant(v)", octant, tickangle, textangle
		if octant in [1,5]:
			return "center"
		elif octant in [2,3,4]:
			return "top"
		elif octant in [6,7,8]:
			return "bottom"
		return "center"

		if octant in [2,3,4]:
			return "center"
		elif octant in [1,5]:
			return "top"
		elif octant in [6,7,8]:
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







