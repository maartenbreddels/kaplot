import kaplot
from kaplot.objects.decorators import Decorator
from kaplot.objects.plotobjects import PlotObject

import math
from numpy import *
def cut(a, a_min, a_max):
	if len(a) == 0:
		return a
	mask = logical_and(a >= a_min, a <= a_max);
	return a[mask]

def cut2(a, b, a_min, a_max):
	if len(a) == 0:
		return a, b
	mask = logical_and(a >= a_min, a <= a_max);
	return a[mask], b[mask]

class Axes2(Decorator):
	__fdoc__ = """Adds axes around the container

	Arguments:
	 * xinterval -- if specified, the major tick seperation for the x axis
	 * xinteger -- if True, x will always be an integer, so no floating point strings in your plot
	 * xstart -- if specified, the start value for the major ticks
	 * xsubticks -- the number of subticks (minor ticks) between mayor ticks
	 * xlogarithmic -- if True, the minor subticks will be seperated as on logarithmic paper.
	 		Note that you have to take the logarithm of your data yourself. Also, labels will
	 		be draws as the base (currently only 10 is supported) with the x-value as superscript
	 * yinterval and the rest -- same, but now for y
	 * ticklength -- length of the mayor ticks, if negative, ticks are drawn to the outside
	 * labeloffset -- length of the seperation between the label and the axis or tickmark (whichever is closer)
	 * linestyle and linewidth -- are added so that axes always look normal, ie your change the default
	 		linewidth of the page
	 		
	 TODO: example and explain how to do custom labeling and tick locations
	"""
	def __init__(self, container, linestyle="normal", linewidth="1px", **kwargs):
			#)
			#ticklength="3mm", labeloffset="1mm",
			#**kwargs):
		#super(Axes, self).__init__(container, viewport=viewport, linestyle=linestyle, linewidth=linewidth, **kwargs)
		#if not isinstance(container, kaplot.objects.Box2):
		#	raise TypeError, "Axes parent should be a box, (not '%r')" % (container)
		super(Axes2, self).__init__(container, linestyle=linestyle, linewidth=linewidth, **kwargs)
		self.parent = container

		self.leftaxes = []
		self.rightaxes = []
		self.topaxes = []
		self.bottomaxes = []
		
	def getBounds(self):
		left = sum([axis.getWidth() for axis in self.leftaxes])
		right = sum([axis.getWidth() for axis in self.rightaxes])
		bottom = sum([axis.getHeight() for axis in self.bottomaxes])
		top = sum([axis.getHeight() for axis in self.topaxes])
		self.axesviewport = (left, bottom), (1-right, 1-top)
		return self.axesviewport
		
	def draw(self, device):
		for axis in self.leftaxes + self.bottomaxes + self.topaxes + self.rightaxes:
			axis.draw(device, self.axesviewport)
		
	def addAxis(self, location, interval=None, integer=False, start=None, subticks=4, logarithmic=False,
			ticklength="3mm", labeloffset="1mm"):
		axis = None
		axis = Axis(self.container, self, location=location, interval=interval, integer=integer, start=start, subticks=subticks,
			logarithmic=logarithmic)
		if location == "left":
			self.leftaxes.append(axis)
		elif location == "bottom":
			self.bottomaxes.append(axis)
		elif location == "right":
			self.rightaxes.append(axis)
		elif location == "top":
			self.topaxes.append(axis)
		else:
			raise ValueError, "location should be 'left', 'right', 'top' or 'bottom'"
		return axis
		

class Axis(Decorator):
	def __init__(self, container, location="left", 
			interval=None, integer=False, start=None, ticks=4, subticks=3, logarithmic=False,
			ticklength="3mm", labeloffset="1mm", linestyle="normal", linewidth="1px",
			intersects=None, halign=None, valign=None, intersection=None,
			spacing="1mm",
			**kwargs):
		super(Axis, self).__init__(container, linestyle=linestyle, linewidth=linewidth, **kwargs)
		self.interval = interval
		self.integer = integer
		self.start = start 
		self.ticks = ticks
		self.subticks = subticks
		self.logarithmic = logarithmic
		self.intersection = intersection
		if location == "bottom":
			self.p1 = kaplot.Vector(0, 0)
			self.p2 = kaplot.Vector(1, 0)
			self.halign = "center"
			self.valign = "top"
			self.tickdir = kaplot.Vector(0, -1)
			if intersection is None:
				self.intersection = "x"
		elif location == "right":
			self.p1 = kaplot.Vector(1, 0)
			self.p2 = kaplot.Vector(1, 1)
			self.halign = "left"
			self.valign = "center"
			self.tickdir = kaplot.Vector(1)
			if intersection is None:
				self.intersection = "y"
		elif location == "top":
			self.p1 = kaplot.Vector(1, 1)
			self.p2 = kaplot.Vector(0, 1)
			self.halign = "center"
			self.valign = "bottom"
			self.tickdir = kaplot.Vector(0, 1)
			if intersection is None:
				self.intersection = "x"
		elif location == "left":
			self.p1 = kaplot.Vector(0, 1)
			self.p2 = kaplot.Vector(0, 0)
			self.halign = "right"
			self.valign = "center"
			self.tickdir = kaplot.Vector(-1, 0)
			if intersection is None:
				self.intersection = "y"
		else:
			raise Exception, "unkown location", location
		self.location = location
		self.ticklength = ticklength
		self.labeloffset = labeloffset
		self.spacing = spacing
		self.bounds = (0., 0.), (0., 0.)
		self.drawLabels = True
		
	def label(self, value):
		if self.logarithmic:
			return "10<sup>%s</sup>" % str(value)
		else:
			if abs(value) < 1e-14:
				return "0"
			else:
				return str(value)

	def _getTextBounds(self, text, font, fontname, fontsize, document):
		textObject = kaplot.textmod.parseText(text, font, fontsize, fontname, document.dpi)
		valign, halign = "center", "center"
		points = textObject.getBBoxTransformed(0, 0, 0, valign, halign)
		#width = (points[1] - points[0]).x
		#height = (points[-1] - points[0]).y
		
		xlist = [document.sizeToViewport("%fpx" % k.x).x for k in points]
		ylist = [document.sizeToViewport("%fpx" % k.y).y for k in points]
		#y = document.sizeToViewport("%fpx" % height, self.viewport).y
		return xlist, ylist
		
	def getWidth(self):
		width, height = self.getSize()
		return width
		
	def getHeight(self):
		width, height = self.getSize()
		return height
		
	def layout(self):
		fontname = self.getContextValue("fontname")
		fontsize = self.getContextValue("fontsize")
		font = kaplot.textmod.findFont(fontname, False, False)

		world = self.container.getWorld()
		worldMatrix = self.container.getWorldMatrix()
		document = self.getDocument()
		#viewportMatrix = kaplot.Matrix.scalebox_inverse(*self.viewport)
		
		ticks, tickvalues, subticks = self.getTicks(world)
		
		(wx1, wy1), (wx2, wy2) = world
		space = document.sizeToViewport(self.spacing)
		ticksizevp = document.sizeToViewport(self.ticklength).scale(-1, -1)
		labeloffsetvp = document.sizeToViewport(self.labeloffset)
		#ticksizevp = viewportMatrix.no_translation() * ticksizevp
		#labeloffsetvp = viewportMatrix.no_translation() * labeloffsetvp
		height = 0
		xvalues = []
		yvalues = []
		if self.drawLabels:
			for tick, value in zip(ticks, tickvalues):
				label = self.label(value)
				xlist, ylist = self._getTextBounds(label, font, fontname, fontsize, document)
				xvalues.extend(xlist)
				yvalues.extend(ylist)

		#if self.location == "left":
			if xvalues:
				width = max(xvalues) - min(xvalues)
			else:
				width = 0
			if yvalues:
				height = max(yvalues) - min(yvalues)
			else:
				height = 0
		else:
			width = 0
			height = 0
		if 1: #width >= 0:
			width += max(ticksizevp.x, 0)
			width += labeloffsetvp.x
			width += space.x
		if 1: #height >= 0:
			height += max(ticksizevp.y, 0)
			height += labeloffsetvp.y
			height += space.y
		#vp1, vp2 = self.viewport
		#vp1, vp2 = kaplot.Vector(vp1), kaplot.Vector(vp2)
		if 0:
			print "###", self.location, width, height
		if self.location == "left":
			self.bounds = (width, 0), (0, 0)
		elif self.location == "right":
			self.bounds = (0, 0), (width, 0)
		elif self.location == "bottom":
			self.bounds = (0, height), (0, 0)
		elif self.location == "top":
			self.bounds = (0, 0), (0, height)

	def draw(self, device, bounds):
		device.pushContext(self.context)
		document = self.getDocument()

		(left, bottom), (right, top) = bounds
		ndev2n = kaplot.Matrix.scalebox(*self.container.borderViewport).no_translation()
		if self.location == "left":
			offset = ndev2n * (-left, 0)
		elif self.location == "right":
			offset = ndev2n * (right, 0)
		elif self.location == "bottom":
			offset = ndev2n * (0, -bottom)
		elif self.location == "top":
			offset = ndev2n * (0, top)
		
		vp2 = kaplot.Matrix.scalebox_inverse(*self.container.borderViewport)
		#m = vp2 * vp1
		m = vp2
		viewport = m * (0, 0), m * (1, 1)
		device.pushViewport(viewport)
		
		worldMatrix = device.getWorldMatrix()
		viewportMatrix = device.getViewportMatrix()
		world = self.container.getWorld()
		(wx1, wy1), (wx2, wy2) = world
		iWorld = kaplot.Matrix.scalebox_inverse(*world)
		
		ticks, tickvalues, subticks = self.getTicks(world)

		ticksizevp = document.sizeToViewport(self.ticklength, device.getViewport()).scale(-1, -1)
		labeloffsetvp = document.sizeToViewport(self.labeloffset, device.getViewport())
		#labeloffsetvp = kaplot.Vector(abs(labeloffsetvp.x), abs(labeloffsetvp.y))
		#labeloffsetvp = labeloffsetvp.scale(-1, -1)
		
		ticksize = worldMatrix.no_translation().inverse() * ticksizevp
		labeloffset = worldMatrix.no_translation().inverse() * labeloffsetvp
		

		device.pushWorld(((0, 0), (1, 1)))
		device.popWorld()
		wp1 = iWorld * (self.p1 + offset)
		wp2 = iWorld * (self.p2 + offset)
		device.drawLine(wp1.x, wp1.y, wp2.x, wp2.y, gridsnap=True)
		v1, v2 = self.getEdgeValues(world)
		#print "Start", v1, "at", wp1, "to", wp2
		if True:
			x1 = []
			x2 = []
			y1 = []
			y2 = []
			for tickpos, value in zip(ticks, tickvalues):
				label = self.label(value)
				s = (tickpos-v1)/(v2-v1)
				tickPos = (wp1 + (wp2 - wp1).scale(s, s))
				tickLength = self.tickdir.scale(ticksize.x, ticksize.y)
				labelOffset = self.tickdir.scale(labeloffset.x, labeloffset.y)
				if labeloffsetvp.x > 0:
					labelOffset += (self.tickdir.x * ticksize.x, 0)
				if labeloffsetvp.y > 0:
					#print "DSADSADAS", labeloffsetvp.x, self.tickdir
					labelOffset += (0, abs(self.tickdir.y) * ticksize.y)
					#print "labeloffset", labelOffset
				#labelOffset = self.tickdir.scale(labeloffset.x, labeloffset.y) +\
				#			kaplot.Vector(self.tickdir.x * ticksize.x,
				#						  self.tickdir.y * ticksize.y)
				#if self.location == "bottom":
				#	print self.tickdir.scale(labeloffset.x, labeloffset.y)
				#	print kaplot.Vector(self.tickdir.x * ticksize.x,
				#						  self.tickdir.y * ticksize.y)
				tickStart = tickPos
				tickEnd = tickPos + tickLength
				labelPos = tickPos + labelOffset
				#print self.halign, self.valign, labelOffset
				if self.drawLabels:
					#if label == "4.0":
					#		print labelPos
					#		print tickPos
					#		print tickLength
					#		print labelOffset
					device.drawText(label, labelPos.x, labelPos.y, self.halign, self.valign)
				x1.append(tickStart.x)
				x2.append(tickEnd.x)
				y1.append(tickStart.y)
				y2.append(tickEnd.y)
				#device.drawLine(tickStart.x, tickStart.y, tickEnd.x, tickEnd.y, gridsnap=True)
				#device.drawLine(x, wy2, x, wy2+ticksize.y, gridsnap=True)

			ticksize = ticksize.scale(0.5, 0.5)
			for tickpos in subticks:
				s = (tickpos-v1)/(v2-v1)
				tickPos = (wp1 + (wp2 - wp1).scale(s, s))
				tickLength = self.tickdir.scale(ticksize.x, ticksize.y)
				tickStart = tickPos
				tickEnd = tickPos + tickLength
				x1.append(tickStart.x)
				x2.append(tickEnd.x)
				y1.append(tickStart.y)
				y2.append(tickEnd.y)
				#device.drawLine(tickStart.x, tickStart.y, tickEnd.x, tickEnd.y, gridsnap=True)
			device.drawLines(x1, y1, x2, y2, gridsnap=True)
		device.popViewport()
		device.popContext()
		
	def getEdgeValues(self, world):
		matrix = kaplot.Matrix.scalebox_inverse(*world)
		wp1 = kaplot.Vector(matrix * self.p1)
		wp2 = kaplot.Vector(matrix * self.p2)
		if self.intersection == "x":
			return wp1.x, wp2.x
		else:
			return wp1.y, wp2.y
	
	def getTicks(self, world):
		if self.intersection == "x":
			return self.getXticks(world)
		else:
			return self.getYticks(world)
			
	def getXticks(self, world):
		(wx1, wy1), (wx2, wy2) = world
		xticks, xtickvalues, xsubticks = self._getXticks(world)
		xticks, xtickvalues = cut2(xticks, xtickvalues, min(wx1, wx2), max(wx1, wx2))
		return xticks, xtickvalues, cut(xsubticks, min(wx1, wx2), max(wx1, wx2))
		
	def getYticks(self, world):
		(wx1, wy1), (wx2, wy2) = world
		yticks, ytickvalues, ysubticks = self._getYticks(world)
		yticks, ytickvalues = cut2(yticks, ytickvalues, min(wy1, wy2), max(wy1, wy2))
		return yticks, ytickvalues, cut(ysubticks, min(wy1, wy2), max(wy1, wy2))
		
		
	def _getXticks(self, world):
		matrix = kaplot.Matrix.scalebox_inverse(*world)
		v1 = kaplot.Vector(matrix * (0,0)).x
		v2 = kaplot.Vector(matrix * (1,0)).x
		t, sub = self._getXticks2(v1, v2)
		return t, t, sub
		
	def _getXticks2(self, v1, v2):
		return kaplot.utils.subdivide(v1, v2, ticks=self.ticks, subticks=self.subticks, interval=self.interval,
					start=self.start, integer=self.integer, logarithmic=self.logarithmic)		

	def _getYticks(self, world):
		matrix = kaplot.Matrix.scalebox_inverse(*world) #.inverse()
		v1 = kaplot.Vector(matrix * (0,0)).y
		v2 = kaplot.Vector(matrix * (0,1)).y
		t, sub = self._getYticks2(v1, v2)
		return t, t, sub

	def _getYticks2(self, v1, v2):
		t, sub = kaplot.utils.subdivide(v1, v2, ticks=self.ticks, subticks=self.subticks, interval=self.interval,
					start=self.start, integer=self.integer, logarithmic=self.logarithmic)
		return t, sub


