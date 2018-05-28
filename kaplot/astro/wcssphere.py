import kaplot
from kaplot.objects import Container, PlotObject
from kaplot.astro.projection import Projection
#from kaplot.cext._wcslib import Wcs
import numpy

class WcsText(PlotObject):
	def __init__(self, container, text, position, textangle=0, valign="center", halign="center",
						wcs=None, transformation=None, **kwargs):
		if not isinstance(container, kaplot.astro.WcsBox):
			raise Exception, "Wcs PlotObjects should have a WcsBox as container"
		if wcs is None:
			self.wcs = self.container.wcs
		else:
			self.wcs = wcs
		if transformation is None:
			self.transformation = self.container.transformation
		else:
			self.transformation = transformation
		self.text = text
		self.position = position
		self.textangle = textangle
		self.valign = valign
		self.halign = halign
		PlotObject.__init__(self, container, **kwargs)

	def plot(self, device):
		device.pushContext(self.context)
		x, y = self.position
		x, y = self.transformation.reverse(x, y)
		result = self.wcs.to_pixel(x, y)
		if result:
			phx, phy = result
			device.drawText(self.text, phx, phy, valign=self.valign, halign=self.halign, textangle=self.textangle)
		device.popContext()

class WcsSymbols(PlotObject):
	def __init__(self, container, x, y, symbolName="x", wcs=None, transformation=None, **kwargs):
		PlotObject.__init__(self, container, **kwargs)
		if not isinstance(container, kaplot.astro.WcsBox):
			raise Exception, "Wcs PlotObjects should have a WcsBox as container"
		if wcs is None:
			self.wcs = self.container.wcs
		else:
			self.wcs = wcs
		if transformation is None:
			self.transformation = self.container.transformation
		else:
			self.transformation = transformation
		self.x, self.y = x, y
		self.symbolName = symbolName

	def draw(self, device):
		device.pushContext(self.context)
		xlist = []
		ylist = []
		for x, y in zip(self.x, self.y):
			xt, yt = self.transformation.reverse(x, y)
			result = self.wcs.to_pixel(xt, yt)
			if result:
				xp, yp = result
				xlist.append(xp)
				ylist.append(yp)
		device.drawSymbol(xlist, ylist, self.symbolName)
		device.popContext()

class WcsSphere(PlotObject):
	def __init__(self, container, ref=None, wcs=None, transformation=None, **kwargs):
		PlotObject.__init__(self, container, **kwargs)
		if not isinstance(container, kaplot.astro.WcsBox):
			raise Exception, "Wcs PlotObjects should have a WcsBox as container"
		if wcs is None:
			self.wcs = self.container.wcs
		else:
			self.wcs = wcs
		if transformation is None:
			self.transformation = self.container.transformation
		else:
			self.transformation = transformation
		self.ref = ref
		#self.ref = (60, 40)
		self.ref = (0, 0)
		#import pdb
		#pdb.set_trace()
		#	[80.0, 80.0], [1.0,0.0,0.0,1.0], [0.1, 0.1], [0.0,0.0])
		
	def getBBox(self):
		return (-185, -95), (185, 95)

	def draw(self, device):
		device.pushContext(self.context)
		granularity = 2

		# 'horizontal' lines
		breakra = []
		if self.wcs.divergent:
			declist = range(-90+15-1, 92-15+1, 15)
			#ralist = range(-180, 181, 1) # +?
		else:
			declist = range(-90, 92, 15)
		ralist = range(-180, 180+granularity+1, granularity) # +?
		#declist = range(-90, 90, 15)
		sigma = 0.0001
		cracklimit = 5.0
		cracklimitlarge = 30.0
		for dec in declist:
			#break
			xlist = []
			ylist = []
			decorg = dec
			for ra1org, ra2org in zip(ralist[:-1], ralist[1:]):
				if self.transformation:
					ra1, dec1 = self.transformation.reverse(ra1org, decorg)
					ra2, dec2 = self.transformation.reverse(ra2org, decorg)
				else:
					dec1 = decorg
					dec2 = decorg
					ra1 = ra1org
					ra2 = ra2org
				p1 = self.wcs.to_pixel(ra1, dec1)
				p2 = self.wcs.to_pixel(ra1+sigma, dec1)
				p3 = self.wcs.to_pixel(ra2-sigma, dec2)
				p4 = self.wcs.to_pixel(ra2, dec2)
				if not(p1 and p2 and p3 and p4):
					device.drawPolyLine(xlist, ylist)
					xlist, ylist = [], []
				else:
					#if False and self.transformation:
					#	p1 = self.transformation(p1[0], p1[1])
					#	p2 = self.transformation(p2[0], p2[1])
					#	p3 = self.transformation(p3[0], p3[1])
					#	p4 = self.transformation(p4[0], p4[1])
					p1 = kaplot.Vector(p1)
					p2 = kaplot.Vector(p2)
					p3 = kaplot.Vector(p3)
					p4 = kaplot.Vector(p4)
					xlist.append(p1.x)
					ylist.append(p1.y)

					if (p2-p1).length > cracklimit: # crack in the first bit
						device.drawPolyLine(xlist, ylist)
						xlist, ylist = [], []
						breakra.append(ra1org)
					elif (p4-p3).length > cracklimit: # crack at the end
						xlist.append(p3.x)
						ylist.append(p3.y)
						device.drawPolyLine(xlist, ylist)
						xlist, ylist = [p4.x], [p4.y]
						breakra.append(ra1org)
						breakra.append(ra2org)
					elif (p1-p4).length > cracklimitlarge:
						device.drawPolyLine(xlist, ylist)
						xlist, ylist = [p4.x], [p4.y]
						breakra.append(ra1org)
						breakra.append(ra2org)


			device.drawPolyLine(xlist, ylist)

		# 'vertical' lines
		if self.wcs.divergent:
			declist = range(-90+15, 92-15+granularity, granularity)
			#ralist = range(-180, 181, 1) # +?
		else:
			declist = range(-90, 90+granularity, granularity)
		#declist = range(-90, 90+1, 1)
		ralist = range(-180, 180+1, 15) # +?
		lines = []
		for ra in ralist:
			xlist = []
			ylist = []
			#ra = ((ra +180) % 360) - 180
			raorg = ra

			# we don't want to draw the same line twice, so we do a
			# check to see if it's on the same location
			# this happens because we go from -180 to 180, which mostly
			# overlaps, but not always!
			line = []
			for dec in [-80, 45, 0, 45, 80]:
				if self.transformation:
					ra, dec = self.transformation.reverse(raorg, dec)
				result = self.wcs.to_pixel(ra, dec)
				if result:
					x, y = result
					line.append(x)
					line.append(y)
			line = numpy.array(line, numpy.Float)
			found = False
			for prevline in lines:
				if len(line) > 0 and \
					len(line) == len(prevline) and \
					max(abs(prevline - line)) < 0.01:
					found = True
					break
			if found:
				continue
			lines.append(line)
			# end of line check

			for dec1, dec2 in zip(declist[:-1], declist[1:]):
				if self.transformation:
					ra1, dec1 = self.transformation.reverse(raorg, dec1)
					ra2, dec2 = self.transformation.reverse(raorg, dec2)
				else:
					ra1 = raorg
					ra2 = raorg

				p1 = self.wcs.to_pixel(ra1, dec1)
				p2 = self.wcs.to_pixel(ra1, dec1+sigma)
				p3 = self.wcs.to_pixel(ra2, dec2-sigma)
				p4 = self.wcs.to_pixel(ra2, dec2)
				if not(p1 and p2 and p3 and p4):
					device.drawPolyLine(xlist, ylist)
					xlist, ylist = [], []
				else:
					#if False and self.transformation:
					#	p1 = self.transformation(p1[0], p1[1])
					#	p2 = self.transformation(p2[0], p2[1])
					#	p3 = self.transformation(p3[0], p3[1])
					#	p4 = self.transformation(p4[0], p4[1])
					p1 = kaplot.Vector(p1)
					p2 = kaplot.Vector(p2)
					p3 = kaplot.Vector(p3)
					p4 = kaplot.Vector(p4)
					xlist.append(p1.x)
					ylist.append(p1.y)

					if (p2-p1).length > cracklimit: # crack in the first bit
						device.drawPolyLine(xlist, ylist)
						xlist, ylist = [], []
					elif (p4-p3).length > cracklimit: # crack at the end
						xlist.append(p3.x)
						ylist.append(p3.y)
						device.drawPolyLine(xlist, ylist)
						xlist, ylist = [p4.x], [p4.y]
						xlist, ylist = [], []
					elif (p1-p4).length > cracklimitlarge:
						device.drawPolyLine(xlist, ylist)
						xlist, ylist = [p4.x], [p4.y]
						xlist, ylist = [], []
			device.drawPolyLine(xlist, ylist)
		device.popContext()




	def _plot(self, device):
		device.pushContext(self.context)

		ralist = range(-180, 181, 15)
		declist = range(-90, 91, 15)
		import numpy
		for ra1, ra2 in zip(ralist[:-1], ralist[1:]):
			for dec1, dec2 in zip(declist[:-1], declist[1:]):
				sigma = 0.0001
				def subdiv(p1, p2, n=10):
					p1 = self.wcs.from_pixel(p1[0], p1[1])
					p2 = self.wcs.from_pixel(p2[0], p2[1])
					if not(p1 and p2):
						return [], []
					p1 = kaplot.Vector(p1)
					p2 = kaplot.Vector(p2)
					x = numpy.zeros(n) + 0.0
					y = numpy.zeros(n) + 0.0
					v = kaplot.Vector(p2) - kaplot.Vector(p1)
					nminus1 = n - 1
					for i in xrange(n):
						p = p1 + v.scale(float(i)/nminus1)
						pp = self.wcs.to_pixel(p.x, p.y)
						x[i] = pp[0]
						y[i] = pp[1]
					return (x, y)
				p1 = self.wcs.to_pixel(ra1+sigma, dec1+sigma)
				p2 = self.wcs.to_pixel(ra2-sigma, dec1+sigma)
				p3 = self.wcs.to_pixel(ra2-sigma, dec2-sigma)
				p4 = self.wcs.to_pixel(ra1+sigma, dec2-sigma)
				if p1 and p2:
					x, y = subdiv(p1, p2)
					device.drawPolyLine(x, y)
				if p2 and p3:
					x, y = subdiv(p2, p3)
					device.drawPolyLine(x, y)
					#device.plotLine(p2, p3)
				if p3 and p4:
					x, y = subdiv(p3, p4)
					device.drawPolyLine(x, y)
					#device.plotLine(p3, p4)
				if p4 and p1:
					x, y = subdiv(p4, p1)
					device.drawPolyLine(x, y)
					#device.plotLine(p4, p1)

		if False:
				p1 = self.projection.forward(ra1+sigma, dec1+sigma)
				p2 = self.projection.forward(ra1+sigma, dec2-sigma)
				if p1 and p2:
					device.plotLine(p1, p2)
					v1 = kaplot.Vector(p1)
					v2 = kaplot.Vector(p2)
					if (v1-v2).length > 120:
						print "jump down", ra1, dec1, "to", ra1, dec2
						import pdb
						#pdb.set_trace()
				p1 = self.projection.forward(ra1-sigma, dec1-sigma)
				p2 = self.projection.forward(ra1-sigma, dec2-sigma)
				if p1 and p2:
					device.plotLine(p1, p2)
				p1 = self.projection.forward(ra1+sigma, dec1+sigma)
				p2 = self.projection.forward(ra2-sigma, dec1+sigma)
				if p1 and p2:
					device.plotLine(p1, p2)
					if (v1-v2).length() > 120:
						print "jump right", ra1, dec1, "to", ra2, dec1
						import pdb
						#pdb.set_trace()
		device.popContext()

	def _plot(self, device):
		#device.pushContext({"color":"black"})
		#device.plotPolygon([0,1,1,0,0], [0,0,1,1,0])
		#device.popContext()
		device.pushContext(self.context)
		raRef, decRef = self.ref

		for ra in range(-180, 180, 10):
			xlist = []
			ylist = []
			xlist = []
			ylist = []
			xlistlist = [xlist]
			ylistlist = [ylist]
			for dec in range(-90, 91, 10):
				result = self.projection.forward(ra, dec)
				if (dec) in [-180, -90, 0, 90, 180]: # we might get a jump here
					sigma = 0.1
					result = self.projection.forward(ra, dec-sigma)
					if result:
						xlist.append(result[0])
						ylist.append(result[1])
					xlist = []
					ylist = []
					xlistlist.append(xlist)
					ylistlist.append(ylist)
					result = self.projection.forward(ra, dec+sigma)
					if result:
						xlist.append(result[0])
						ylist.append(result[1])
				else:
					result = self.projection.forward(ra, dec)
					if result:
						xlist.append(result[0])
						ylist.append(result[1])
			for xlist, ylist in zip(xlistlist, ylistlist):
				for p1, p2 in zip(zip(xlist[:-1], ylist[:-1]),zip(xlist[1:], ylist[1:])):
					#print p1, p2
					device.plotLine(p1, p2)
					#pass

		raList = range(-180, 181, 10)
		for dec in range(-90, 91, 10):
			xlist = []
			ylist = []
			xlistlist = [xlist]
			ylistlist = [ylist]
			for ra in raList:
				if (ra-raRef) in [-360, -180, 0, 180, 360]: # we might get a jump here
					sigma = 0.001
					result = self.projection.forward(ra-sigma, dec)
					if result:
						xlist.append(result[0])
						ylist.append(result[1])
					xlist = []
					ylist = []
					xlistlist.append(xlist)
					ylistlist.append(ylist)
					result = self.projection.forward(ra+sigma, dec)
					if result:
						xlist.append(result[0])
						ylist.append(result[1])
				else:
					result = self.projection.forward(ra, dec)
					if result:
						xlist.append(result[0])
						ylist.append(result[1])
			#print xlist

			for xlist, ylist in zip(xlistlist, ylistlist):
				for p1, p2 in zip(zip(xlist[:-1], ylist[:-1]),zip(xlist[1:], ylist[1:])):
					#print p1, p2
					device.plotLine(p1, p2)

		#for i, (xlist, ylist) in enumerate(zip(self.xlist, self.ylist)):
		#	xlistsymbol = []
		#	ylistsymbol = []
		#	for x, y in zip(xlist, ylist):
		#		result = self.projection.forward(x, y)
		#		if result:
		#			xlistsymbol.append(result[0])
		#			ylistsymbol.append(result[1])
		#	if i < len(self.contexts):
		#		device.pushContext(self.contexts[i])
		#	device.plotSymbol(xlistsymbol, ylistsymbol, "dot")
		#	if i < len(self.contexts):
		#		device.popContext()
        #
		#device.pushContext(self.childContext)
		#self.plotChildren(device)
		#device.popContext()

		device.popContext()
