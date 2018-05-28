# -*- coding: utf-8 -*-
"""shapes for the markers

plus - a plus shape
x - an x shape
star - a shape like the seastar, 5 arms
solidstart - like star, but solid
tristar - a star with 3 points, like the mercedes symbol, has no interior
square - a simple square
solidsquare - like square, but solid
circle - not a real circle, but a fine polygon
solidcircle - like circle, but solid

"""
import math
import kaplot.vector
import kaplot.utils

symbols = {}

class SimpleSymbol(object):
	def __init__(self, count, evenradius, oddradius, startangle, solid):
		self.count = count
		self.evenradius = float(evenradius)
		self.oddradius = float(oddradius)
		self.startangle = startangle
		self.solid = solid
		self.parts = 1

	def getXY(self, device, location, pointsize):
		location = kaplot.vector.Vector(location)

		value, units = kaplot.utils.splitDimension(pointsize)
		v = kaplot.vector.Vector(value, value)
		nv = device.getUnitMatrix(units) * v
		v = device.getUnitMatrix("normalised").inverse() * nv
		pointsize = min(v.x, v.y)

		x = []
		y = []
		#scale = dev.getUnitMatrix(units) * dev.getViewportMatrix().inverse() * dev.getWorldMatrix().inverse()
		scale = device.getWorldMatrix().inverse().nolocation()
		#scale = pointsize
		pointsize = pointsize
		print pointsize
		#pointsize *= 10
		vec = kaplot.vector.Vector(0,0)
		for i in range(self.count*2):
			angle = (i * math.pi*2) / (self.count*2)  + self.startangle
			if (i % 2) == 0: # even
				vec.x = math.cos(angle) * self.evenradius * pointsize
				vec.y = math.sin(angle) * self.evenradius * pointsize
			else: # odd
				vec.x = math.cos(angle) * self.oddradius * pointsize
				vec.y = math.sin(angle) * self.oddradius * pointsize
			vec = scale * vec
			x.append(location.x + vec.x)
			y.append(location.y + vec.y)
		if not self.solid:
			x.append(x[0])
			y.append(y[0])
		#dev.plotPolygon(x, y, color=color, linestyle=self.linestyle, fillstyle=self.fillstyle, linewidth=linewidth, units=units)
		return x, y

	def getXY(self, part):
		xlist = []
		ylist = []
		pointsize = 1.0
		for i in range(self.count*2):
			angle = (i * math.pi*2) / (self.count*2)  + self.startangle
			if (i % 2) == 0: # even
				x = math.cos(angle) * self.evenradius * pointsize
				y = math.sin(angle) * self.evenradius * pointsize
			else: # odd
				x = math.cos(angle) * self.oddradius * pointsize
				y = math.sin(angle) * self.oddradius * pointsize
			xlist.append(0.5 + x)
			ylist.append(0.5 + y)
		if not self.solid:
			xlist.append(xlist[0])
			ylist.append(ylist[0])
		return xlist, ylist

class VectorSymbol(object):
	def __init__(self):
		self.solid = False
		self.multipart = True
		self.parts = 2
		
	def getXY(self, part):
		xlist = []
		ylist = []
		if part == 0:
			xlist.extend([-0.5,0.5])
			ylist.extend([0,0])
		if part == 1:
			xlist.extend([0.25,0.5, 0.25])
			ylist.extend([-0.25,0, 0.25])
		return xlist, ylist

class HVectorSymbol(object):
	def __init__(self):
		self.solid = False
		self.multipart = True
		self.parts = 1
		
	def getXY(self, part):
		xlist = []
		ylist = []
		if part == 0:
			xlist.extend([-0.5,0.5])
			ylist.extend([0,0])
		return xlist, ylist

symbols["line"] = SimpleSymbol(1, 0.5, 0.5, 0, False)
symbols["vline"] = SimpleSymbol(1, 0.5, 0.5, 90 * math.pi/180, False)
symbols["plus"] = SimpleSymbol(4, 0.5, 0, 90 * math.pi/180, False)
symbols["x"] = SimpleSymbol(4, 0.5, 0, 45 * math.pi/180, False)
symbols["star"] = SimpleSymbol(5, 0.5, 0.2, 90 * math.pi/180, False)
symbols["starsolid"] = SimpleSymbol(5, 0.5, 0.2, 90 * math.pi/180, True)
symbols["tristar"] = SimpleSymbol(3, 0.5, 0, 90 * math.pi/180, False)
symbols["triangle"] = SimpleSymbol(3, 1, 0.5, 90 * math.pi/180, False)
symbols["trianglesolid"] = SimpleSymbol(3, 1, 0.5, 90 * math.pi/180, True)
symbols["square"] = SimpleSymbol(2, 0.5, 0.5, 45 * math.pi/180, False)
symbols["squaresolid"] = SimpleSymbol(2, 0.5, 0.5, 45 * math.pi/180, True)
symbols["circle"] = SimpleSymbol(12, 0.5, 0.5, 45 * math.pi/180, False)
symbols["dot"] = SimpleSymbol(12, 0.1, 0.1, 45 * math.pi/180, True)
symbols["circlesmall"] = SimpleSymbol(12, 0.1, 0.1, 45 * math.pi/180, False)
symbols["circlesolid"] = SimpleSymbol(12, 0.5, 0.5, 45 * math.pi/180, True)
symbols["diamond"] = SimpleSymbol(2, 0.5, 0.5, 45 * math.pi/45, False)
symbols["diamondsolid"] = SimpleSymbol(2, 0.5, 0.5, 45 * math.pi/45, True)
symbols["vector"] = VectorSymbol()
symbols["hvector"] = HVectorSymbol()



