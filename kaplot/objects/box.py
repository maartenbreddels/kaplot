from numarray import *
import kaplot.context
from kaplot.objects import Container

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
 

class Box(Container):
	def __init__(self, page=None, **kwargs):
		super(Box, self).__init__(page, **kwargs)
		self.xinterval = None
		self.xinteger = False
		self.xstart = None 
		self.xsubticks = 4
		self.xlogarithmic = False
		
		self.yinterval = None
		self.yinteger = False
		self.ystart = None 
		self.ysubticks = 4
		self.ylogarithmic = False
		self.ticklength = "5mm"
		
	def labelx(self, value):
		return str(value) #+ "[=--=!=--=]"
		#label = "e<sup>%s</sup>" % str(y)

	def labely(self, value):
		return "%g" % value
		return str(value)
		
	def draw(self, device):
		self.preDraw(device)
		if False:
			self.drawObjects(device)
			self.postDraw(device)
			return
		
		worldMatrix = device.getWorldMatrix()
		viewportMatrix = device.getViewportMatrix()
		plot = self.getPlot()
		
		#ticksize = "0.3cm"
		labeloffset = "0.1cm"
		#bordersize = "0.2cm"
		
		xticks, xsubticks = self.getXticks(device)
		yticks, ysubticks = self.getYticks(device)

		(wx1, wy1), (wx2, wy2) = device.getWorld()
		def cut(a, a_min, a_max):
			mask = logical_and(a >= a_min, a <= a_max);
			return a[mask]
		xticks = cut(xticks, min(wx1, wx2), max(wx1, wx2))
		xsubticks = cut(xsubticks, min(wx1, wx2), max(wx1, wx2))
		yticks = cut(yticks, min(wy1, wy2), max(wy1, wy2))
		ysubticks = cut(ysubticks, min(wy1, wy2), max(wy1, wy2))
		
		if True:
			ticksizevp = plot.sizeToViewport(self.ticklength, device.getViewport()).scale(-1, -1)
			labeloffsetvp = plot.sizeToViewport(labeloffset, device.getViewport())
			ticksizevp = viewportMatrix.no_translation() * ticksizevp
			labeloffsetvp = viewportMatrix.no_translation() * labeloffsetvp
			height = 0
			for x in xticks:
				label = self.labelx(x)
				bbox = device.getTextBbox(label, 0, 0, "center", "top")
				bbox = [viewportMatrix.no_translation() * worldMatrix*p for p in bbox]
				xlist = [p[0] for p in bbox]
				ylist = [p[1] for p in bbox]
				newheight = max(ylist) - min(ylist)
				height = max(newheight, height)

			width = 0
			for y in yticks:
				label = self.labely(y)
				bbox = device.getTextBbox(label, 0, 0, "right", "center")
				bbox = [viewportMatrix.no_translation() * worldMatrix*p for p in bbox]
				xlist = [p[0] for p in bbox]
				ylist = [p[1] for p in bbox]
				newwidth = max(xlist) - min(xlist)
				width = max(newwidth, width)
			width += max(ticksizevp.x, 0)
			height += max(ticksizevp.y, 0)
			width += labeloffsetvp.x
			height += labeloffsetvp.y
			vp1, vp2 = device.getViewport()
			vp1, vp2 = kaplot.Vector(vp1), kaplot.Vector(vp2)
			#bordersizevp = viewportMatrix.no_translation() * plot.sizeToViewport(labeloffset, device.getViewport())
			device.pushViewport(((vp1.x+width, vp1.y+height), (vp2.x, vp2.y)))
			#device.pushViewport(device.getViewport())

		ticksizevp = plot.sizeToViewport(self.ticklength, device.getViewport()).scale(-1, -1)
		labeloffsetvp = plot.sizeToViewport(labeloffset, device.getViewport())
		#cm1 = plot.sizeToViewport(ticksize, device.getViewport())
		ticksize = worldMatrix.no_translation().inverse() * ticksizevp
		labeloffset = worldMatrix.no_translation().inverse() * labeloffsetvp
		
		clipping = device.getClipping()
		device.setClipping(False)

		device.pushWorld(((0, 0), (1, 1)))
		device.drawPolyLine([0, 1, 1, 0, 0], [0, 0, 1, 1, 0], gridsnap=True)
		device.popWorld()

		if True:
			for x in xticks:
				label = self.labelx(x)
				labelx = x
				labely = wy1 - max(0, ticksize.y) - labeloffset.y
				device.drawText(label, labelx, labely, "center", "top")
				device.drawLine(x, wy1, x, wy1-ticksize.y, gridsnap=True)
				#device.drawLine(x, wy2, x, wy2+ticksize.y, gridsnap=True)
				#bbox = device.getTextBbox(label, labelx, labely, "center", "top")
				#p1, p2, p3, p4 = bbox
				#x = [p1[0], p2[0], p3[0], p4[0], p1[0]]
				#y = [p1[1], p2[1], p3[1], p4[1], p1[1]]
				#device.drawPolyLine(x, y)
			for y in yticks:
				label = self.labely(y)
				labelx = wx1 - max(0, ticksize.x) - labeloffset.x
				labely = y
				device.drawText(label, labelx, labely, "right", "center")
				device.drawLine(wx1, y, wx1-ticksize.x, y, gridsnap=True)
				#device.drawLine(wx2, y, wx2+ticksize.x, y, gridsnap=True)
				#bbox = device.getTextBbox(label, labelx, labely, "right", "center")
				#p1, p2, p3, p4 = bbox
				#x = [p1[0], p2[0], p3[0], p4[0], p1[0]]
				#y = [p1[1], p2[1], p3[1], p4[1], p1[1]]
				#device.drawPolyLine(x, y)

		color = device.getColor()
		s = 0.1
		device.setColor(color.scale(s,s,s))
		device.setColor("grey")
		linewidth = device.getLinewidth()
		linewidthNr, linewidthUnits = kaplot.utils.splitDimension(linewidth)
		device.setLinewidth("%f%s" % (linewidthNr*1./2, linewidthUnits))
		#device.setLinestyle("dash")
		for x in xsubticks:
			device.drawLine(x, wy1, x, wy2, gridsnap=True)
		for y in ysubticks:
			device.drawLine(wx1, y, wx2, y, gridsnap=True)
			
		device.restoreLinewidth()
		device.restoreLinestyle()
		device.restoreColor()


		for x in xticks:
			device.drawLine(x, wy1, x, wy2, gridsnap=True)
		for y in yticks:
			device.drawLine(wx1, y, wx2, y, gridsnap=True)

		device.setClipping(clipping)
		self.drawDecorators(device)
		self.drawObjects(device)
		device.setClipping(False)
		ticksize = ticksize.scale(0.5, 0.5)
		for x in xsubticks:
			device.drawLine(x, wy1, x, wy1-ticksize.y, gridsnap=True)
			#device.drawLine(x, wy2, x, wy2+ticksize.y, gridsnap=True)
		for y in ysubticks:
			device.drawLine(wx1, y, wx1-ticksize.x, y, gridsnap=True)
			#device.drawLine(wx2, y, wx2+ticksize.x, y, gridsnap=True)
		device.popViewport()
		device.setClipping(clipping)
		self.postDraw(device)
		
	def getXticks(self, dev):
		matrix = dev.getWorldMatrix().inverse()
		#import pdb; pdb.set_trace()
		v1 = kaplot.Vector(matrix * (0,0)).x
		v2 = kaplot.Vector(matrix * (1,0)).x

		realinterval = self.xinterval
		if realinterval == None:
			diff = v2 - v1
			ticks = 3
			tick = diff / 4
			error = diff / 8.0
			realinterval = magicnr(tick, error)

		interval = realinterval

		if self.xinteger:
			interval = int(interval+0.5)
			if interval == 0 and realinterval > 0:
				interval = 1
			if interval == 0 and realinterval < 0:
				interval = -1

		start = self.xstart
		if start == None:
			start = fround(v1, interval) - interval

		if self.xinteger:
			ticks = arange(start, int(v2+1)+interval*1, interval)
		else:
			ticks = arange(start, v2 + interval*1.5, interval)

		subticks = []

		if self.xsubticks > 0:
			if self.xlogarithmic:
				sigma = 1.0e-9
				# ok, this looks weird, but take base 10, with 8 subticks as an example
				# and it will make sense :), or base 3, with 1 subtick
				offsets = log(arange(2, self.xsubticks+1+sigma))/log(self.xsubticks+2)
				length = len(ticks)
				for i in range(length-1):
					offset = ticks[i]
					width = ticks[i+1] - ticks[i]
					subticks.extend(list(offset+offsets*width))
			else:
				subinterval = float(interval) / (1+self.xsubticks)
				length = len(ticks)
				for i in range(length-1):
					v1 = ticks[i]+subinterval
					v2 = ticks[i+1]
					subticks.extend(arange(v1, v2-subinterval*0.5, subinterval))


		return ticks, array(subticks)

	def getYticks(self, dev):
		matrix = dev.getWorldMatrix().inverse()
		v1 = kaplot.Vector(matrix * (0,0)).y
		v2 = kaplot.Vector(matrix * (0,1)).y

		realinterval = self.yinterval
		if realinterval == None:
			diff = v2 - v1
			ticks = 3
			tick = diff / 4
			error = diff / 10.0
			realinterval = magicnr(tick, error)

		interval = realinterval

		if self.yinteger:
			interval = int(interval+0.5)
			if interval == 0 and realinterval > 0:
				interval = 1
			if interval == 0 and realinterval < 0:
				interval = -1

		start = self.ystart
		if start == None:
			start = fround(v1, interval) -interval

		if self.yinteger:
			ticks = arange(start, int(v2+1) + interval*0, interval)
		else:
			ticks = arange(start, v2 + interval*1.5, interval)
		subticks = []
		#import pdb;pdb.set_trace()

		if self.ysubticks > 0:
			if self.ylogarithmic:
				sigma = 1.0e-9
				# ok, this looks weird, but take base 10, with 8 subticks as an example
				# and it will make sense :), or base 3, with 1 subtick
				offsets = log(arange(2, self.ysubticks+1+sigma))/log(self.ysubticks+2)
				length = len(ticks)
				for i in range(length-1):
					offset = ticks[i]
					width = ticks[i+1] - ticks[i]
					subticks.extend(list(offset+offsets*width))
			else:
				subinterval = float(interval) / (1+self.ysubticks)
				length = len(ticks)
				for i in range(length-1):
					v1 = ticks[i]+subinterval
					v2 = ticks[i+1]
					subticks.extend(arange(v1, v2-subinterval/2, subinterval))

		return ticks, array(subticks)
