import kaplot
from kaplot.objects.containers import Container
from kaplot.objects import PlotBase


class Decorator(PlotBase):
	__fdoc__ = "A decorator 'decorates' a container, like axes add axes to it"
	def __init__(self, container, **kwargs):
		if not isinstance(container, Container):
			raise TypeError, "decorator parent should be a container"
		self.container = container
		self.container.decorators.append(self)
		self.context = kaplot.Context(**kwargs)
		self.bounds = (0, 0), (0, 0)
		
	def draw(self, device, offsets):
		pass
		
	def layout(self):
		pass
		
	def getDocument(self):
		return self.container.getDocument()

	def getContextValue(self, name):
		if name in self.context:
			return self.context[name]
		else:
			return self.container.getContextValue(name)
	
class Spacer(Decorator):
	__fdoc__ = """Adds some space around the container"""
	def __init__(self, container, space="0pt", bottom="0cm", right="0cm",
			top="0cm", left="0cm", **kwargs):
		super(Spacer, self).__init__(container, **kwargs)
		self.space = space
		self.bottom = bottom
		self.right = right
		self.top = top
		self.left = left
		
	def draw(self, device, offsets):
		pass
		
	def layout(self):
		document = self.getDocument()
		v = document.sizeToViewport(self.space)
		bottom = document.sizeToViewport(self.bottom)
		right = document.sizeToViewport(self.right)
		top = document.sizeToViewport(self.top)
		left = document.sizeToViewport(self.left)
		self.bounds = (v.x+left.x, v.y+bottom.y), (v.x+right.x, v.y+top.y)
		
class Title(Decorator):
	__fdoc__ = "Adds a title in the top/center location of the container"
	def __init__(self, container, text="", spacing="0mm", **kwargs):
		super(Title, self).__init__(container, **kwargs)
		self.text = text
		self.spacing = spacing
		
	def draw(self, device, offsets):
		document = self.getDocument()
		m = kaplot.Matrix.scalebox(*self.container.borderViewport).no_translation()
		(left, bottom), (right, top) = offsets
		top = (m * (0, top)).y
		space = document.sizeToViewport(self.spacing, self.container.borderViewport)
		
		device.pushContext(self.context)
		device.pushWorld(((0, 0), (1, 1)))
		device.drawText(self.text, 0.5, 1+top+space.y, halign="center", valign="bottom")
		device.popWorld()
		device.popContext()
		
	def layout(self):
		document = self.getDocument()
		space = document.sizeToViewport(self.spacing)

		fontname = self.getContextValue("fontname")
		fontsize = self.getContextValue("fontsize")
		font = kaplot.textmod.findFont(fontname, False, False)
		if self.text:
			textObject = kaplot.textmod.parseText(self.text, font, fontsize, fontname, document.dpi)
			valign, halign = "center", "center"
			points = textObject.getBBoxTransformed(0, 0, 0, valign, halign)
			width = (points[1] - points[0]).x
			height = (points[-1] - points[0]).y
			
			v = kaplot.Vector()
			x = document.sizeToViewport("%fpx" % width).x
			y = document.sizeToViewport("%fpx" % height).y
			y += space.y * 2
		else:
			y = 0
		self.bounds = (0, 0), (0, y)
		
class Labels(Decorator):
	__fdoc__ = "Adds 4 labels around the container"
	def __init__(self, container, bottom=None, left=None, right=None, top=None, 
					spacing="1mm", **kwargs):
		super(Labels, self).__init__(container, **kwargs)
		from kaplot.objects import Text, Page, Document
		dummy = Container(Page(Document()))
		self.bottom = Text(dummy, bottom, halign="center", valign="top")
		self.left = Text(dummy, left, halign="center", valign="bottom", textangle=pi/2)
		self.right = Text(dummy, right, halign="left", valign="top", textangle=pi/2)
		self.top = Text(dummy, top, halign="center", valign="bottom")
		self.spacing = spacing
		
	def draw(self, device, offsets):
		m = kaplot.Matrix.scalebox(*self.container.borderViewport).no_translation()
		(left, bottom), (right, top) = offsets
		(left, bottom) = m * (left, bottom)
		(right, top) = m * (right, top)
		
		device.pushContext(self.context)
		device.pushWorld(((0, 0), (1, 1)))
		if self.left.text:
			self.left.x = -left
			self.left.y = 0.5
			self.left.draw(device)
			#device.drawText(self.left, -left, 0.5, halign="right", valign="center", textangle=pi/2)
		if self.bottom.text:
			self.bottom.x = 0.5
			self.bottom.y = -bottom
			self.bottom.draw(device)
			#device.drawText(self.bottom, 0.5, -bottom, halign="center", valign="top")
		if self.right.text:
			self.right.x = 1+right
			self.right.y = 0.5
			self.right.draw(device)
			#device.drawText(self.right, 1+right, 0.5, halign="left", valign="center")
		if self.top.text:
			self.top.x = 0.5
			self.top.y = 1+top
			self.top.draw(device)
			#device.drawText(self.top, 0.5, 1+top, halign="center", valign="bottom")
		device.popWorld()
		device.popContext()
		
	def layout(self):
		document = self.getDocument()
		space = document.sizeToViewport(self.spacing)

		fontname = self.getContextValue("fontname")
		fontsize = self.getContextValue("fontsize")
		font = kaplot.textmod.findFont(fontname, False, False)
		x1 = 0
		y1 = 0
		x2 = 0
		y2 = 0
		if self.left.text:
			x, y = self._getTextBounds(self.left.text, self.left.textangle, font, fontname, fontsize, document)
			x1 = x + space.x
		if self.bottom.text:
			x, y = self._getTextBounds(self.bottom.text, self.bottom.textangle, font, fontname, fontsize, document)
			y1 = y + space.y
		if self.right.text:
			x, y = self._getTextBounds(self.right.text, self.right.textangle, font, fontname, fontsize, document)
			x2 = x + space.x
		if self.top.text:
			x, y = self._getTextBounds(self.top.text, self.top.textangle, font, fontname, fontsize, document)
			y2 = y + space.y
			
		self.bounds = (x1, y1), (x2, y2)
		
	def _getTextBounds(self, text, angle, font, fontname, fontsize, document):
		textObject = kaplot.textmod.parseText(text, font, fontsize, fontname, document.dpi)
		valign, halign = "center", "center"
		points = textObject.getBBoxTransformed(0, 0, angle, valign, halign)
		xs = [p.x for p in points]
		ys = [p.y for p in points]
		width = max(xs) - min(xs) #(points[1] - points[0]).x
		height = max(ys) - min(ys) #(points[-1] - points[0]).y
		
		x = document.sizeToViewport("%fpx" % width).x
		y = document.sizeToViewport("%fpx" % height).y
		#print kaplot.Matrix.rotate(angle) * kaplot.Vector(x, y)
		#print kaplot.Matrix.rotate(angle), kaplot.Vector(x, y)
		return kaplot.Vector(x, y)
		
		
class Border(Decorator):
	__fdoc__ = "Adds a solid border around the container"
	def __init__(self, container, **kwargs):
		super(Border, self).__init__(container, **kwargs)
		
	def draw(self, device, offsets):
		m = kaplot.Matrix.scalebox(*self.container.borderViewport).no_translation()
		(left, bottom), (right, top) = m * offsets[0], m * offsets[1]
		device.pushContext(self.context)
		document = self.getDocument()
		device.pushWorld(((0, 0), (1, 1)))
		#v = document.sizeToViewport(self.space, self.viewport)

		#device.drawPolyLine([0, 1, 1, 0, 0], [0, 0, 1, 1, 0], gridsnap=True)
		device.drawPolyLine([-left, 1+right, 1+right, -left], [-bottom, -bottom, 1+top, 1+top], close=True, gridsnap=True)
		#device.drawPolyLine([v.x, 1-v.x, 1-v.x, v.x, v.x], [v.y, v.y, 1-v.y, 1-v.y, v.y], gridsnap=True)
		
		device.popWorld()
		device.popContext()
		
		
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
	



class Axes(Decorator):
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
	def __init__(self, container=None, viewport=((0, 0), (1, 1)), 
			xinterval=None, xinteger=False, xstart=None, xsubticks=4, xlogarithmic=False,
			yinterval=None, yinteger=False, ystart=None, ysubticks=4, ylogarithmic=False,
			ticklength="3mm", labeloffset="1mm", linestyle="normal", linewidth="1px",
			**kwargs):
		super(Axes, self).__init__(container, viewport=viewport, linestyle=linestyle, linewidth=linewidth, **kwargs)
		self.xinterval = xinterval
		self.xinteger = xinteger
		self.xstart = xstart 
		self.xsubticks = xsubticks
		self.xlogarithmic = xlogarithmic
		
		self.yinterval = yinterval
		self.yinteger = yinteger
		self.ystart = ystart 
		self.ysubticks = ysubticks
		self.ylogarithmic = ylogarithmic
		self.ticklength = ticklength
		self.labeloffset = labeloffset
		
	def labelx(self, value):
		if self.xlogarithmic:
			return "10<sup>%s</sup>" % str(value)
		else:
			return str(value)

	def labely(self, value):
		if self.ylogarithmic:
			return "10<sup>%s</sup>" % str(value)
		else:
			return str(value)
		
	def _getTextBounds(self, text, font, fontname, fontsize, document):
		textObject = kaplot.textmod.parseText(text, font, fontsize, fontname, document.dpi)
		valign, halign = "center", "center"
		points = textObject.getBBoxTransformed(0, 0, 0, valign, halign)
		width = (points[1] - points[0]).x
		height = (points[-1] - points[0]).y
		
		x = document.sizeToViewport("%fpx" % width, self.viewport).x
		y = document.sizeToViewport("%fpx" % height, self.viewport).y
		return kaplot.Vector(x, y)
		
	def getBounds(self):
		fontname = self.getContextValue("fontname")
		fontsize = self.getContextValue("fontsize")
		font = kaplot.textmod.findFont(fontname, False, False)

		world = self.container.getWorld()
		worldMatrix = self.container.getWorldMatrix()
		document = self.getDocument()
		viewportMatrix = kaplot.Matrix.scalebox_inverse(*self.viewport)
		
		xticks, xtickvalues, xsubticks = self.getXticks(world)
		yticks, ytickvalues, ysubticks = self.getYticks(world)
		
		(wx1, wy1), (wx2, wy2) = world

		ticksizevp = document.sizeToViewport(self.ticklength, self.viewport).scale(-1, -1)
		labeloffsetvp = document.sizeToViewport(self.labeloffset, self.viewport)
		ticksizevp = viewportMatrix.no_translation() * ticksizevp
		labeloffsetvp = viewportMatrix.no_translation() * labeloffsetvp
		height = 0
		for x, value in zip(xticks, xtickvalues):
			label = self.labelx(value)
			newwidth, newheight = self._getTextBounds(label, font, fontname, fontsize, document)
			height = max(newheight, height)

		width = 0
		for y, value in zip(yticks, ytickvalues):
			label = self.labely(value)
			newwidth, newheight = self._getTextBounds(label, font, fontname, fontsize, document)
			width = max(newwidth, width)
		width += max(ticksizevp.x, 0)
		height += max(ticksizevp.y, 0)
		width += labeloffsetvp.x
		height += labeloffsetvp.y
		vp1, vp2 = self.viewport
		vp1, vp2 = kaplot.Vector(vp1), kaplot.Vector(vp2)
		#return (vp1.x+width, vp1.y+height), (vp2.x, vp2.y)
		self.offset = (width, height)
		#self.offset = (0, 0)
		return (width, height), (1, 1)
		#return (0, 0), (1, 1)

	def draw(self, device):
		device.pushContext(self.context)
		vp1 = kaplot.Matrix.scalebox_inverse(self.offset, (1, 1))
		vp2 = kaplot.Matrix.scalebox_inverse(*self.viewport)
		m = vp2 * vp1
		viewport = m * (0, 0), m * (1, 1)
		device.pushViewport(viewport)
		
		worldMatrix = device.getWorldMatrix()
		viewportMatrix = device.getViewportMatrix()
		document = self.getDocument()
		world = self.container.getWorld()
		(wx1, wy1), (wx2, wy2) = world
		
		xticks, xtickvalues, xsubticks = self.getXticks(world)
		yticks, ytickvalues, ysubticks = self.getYticks(world)

		ticksizevp = document.sizeToViewport(self.ticklength, device.getViewport()).scale(-1, -1)
		labeloffsetvp = document.sizeToViewport(self.labeloffset, device.getViewport())
		
		ticksize = worldMatrix.no_translation().inverse() * ticksizevp
		labeloffset = worldMatrix.no_translation().inverse() * labeloffsetvp
		
		clipping = device.getClipping()
		device.setClipping(False)

		device.pushWorld(((0, 0), (1, 1)))
		device.drawPolyLine([0, 1, 1, 0, 0], [0, 0, 1, 1, 0], gridsnap=True)
		device.popWorld()

		if True:
			for x, value in zip(xticks, xtickvalues):
				label = self.labelx(value)
				labelx = x
				labely = wy1 - max(0, ticksize.y) - labeloffset.y
				device.drawText(label, labelx, labely, "center", "top")
				device.drawLine(x, wy1, x, wy1-ticksize.y, gridsnap=True)
				device.drawLine(x, wy2, x, wy2+ticksize.y, gridsnap=True)
			for y, value in zip(yticks, ytickvalues):
				label = self.labely(value)
				labelx = wx1 - max(0, ticksize.x) - labeloffset.x
				labely = y
				device.drawText(label, labelx, labely, "right", "center")
				device.drawLine(wx1, y, wx1-ticksize.x, y, gridsnap=True)
				device.drawLine(wx2, y, wx2+ticksize.x, y, gridsnap=True)

		if False:
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

		ticksize = ticksize.scale(0.5, 0.5)

		for x in xsubticks:
			device.drawLine(x, wy1, x, wy1-ticksize.y, gridsnap=True)
			device.drawLine(x, wy2, x, wy2+ticksize.y, gridsnap=True)
		for y in ysubticks:
			device.drawLine(wx1, y, wx1-ticksize.x, y, gridsnap=True)
			device.drawLine(wx2, y, wx2+ticksize.x, y, gridsnap=True)
		device.setClipping(clipping)
		device.popViewport()
		device.popContext()
		
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
		t, sub = kaplot.utils.subdivide(v1, v2, subticks=self.xsubticks, interval=self.xinterval,
					start=self.xstart, integer=self.xinteger, logarithmic=self.xlogarithmic)		
		return t, t, sub

	def _getYticks(self, world):
		matrix = kaplot.Matrix.scalebox_inverse(*world) #.inverse()
		v1 = kaplot.Vector(matrix * (0,0)).y
		v2 = kaplot.Vector(matrix * (0,1)).y
		t, sub = kaplot.utils.subdivide(v1, v2, subticks=self.ysubticks, interval=self.yinterval,
					start=self.ystart, integer=self.yinteger, logarithmic=self.ylogarithmic)
		return t, t, sub
		
	def _getXticks(self, world):
		matrix = kaplot.Matrix.scalebox_inverse(*world)
		v1 = kaplot.Vector(matrix * (0,0)).x
		v2 = kaplot.Vector(matrix * (1,0)).x
		t, sub = self._getXticks2(v1, v2)
		return t, t, sub
		
	def _getXticks2(self, v1, v2):
		return kaplot.utils.subdivide(v1, v2, subticks=self.xsubticks, interval=self.xinterval,
					start=self.xstart, integer=self.xinteger, logarithmic=self.xlogarithmic)		

	def _getYticks(self, world):
		matrix = kaplot.Matrix.scalebox_inverse(*world) #.inverse()
		v1 = kaplot.Vector(matrix * (0,0)).y
		v2 = kaplot.Vector(matrix * (0,1)).y
		t, sub = self._getYticks2(v1, v2)
		return t, t, sub

	def _getYticks2(self, v1, v2):
		t, sub = kaplot.utils.subdivide(v1, v2, subticks=self.ysubticks, interval=self.yinterval,
					start=self.ystart, integer=self.yinteger, logarithmic=self.ylogarithmic)
		return t, sub

		