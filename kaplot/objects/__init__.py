# -*- coding: utf-8 -*-
import kaplot
import kaplot.utils
import math
import numpy
from time import time

class PlotBase(object):
	def draw(self, device):
		pass
		
		
	def getContextMenuFor(self, window, context, name, parentMenu=None):
		
		def delete(window, context, name):
			del context[name]
			window.refreshDocument()

		def set(window, context, name, value):
			context[name] = value
			window.refreshDocument()

		menu = window.createMenu(parentMenu)
		subMenu = window.createMenu(menu)
		for value in kaplot.context.sampleValues[name]:
			if name in context and context[name] == value:
				bold = True
			else:
				bold = False
			subMenu.addCommand(str(value), set, args=[context, name, value], bold=bold)

		if name in context:
			menu.addCommand("delete", delete, args=[context, name])
			menu.addSubMenu("change", subMenu)
		else:
			menu.addSubMenu("add", subMenu)
		return menu
	
	def getContextMenu(self, window, context=None, parentMenu=None):
		if context is None:
			context = self.context
		menu = window.createMenu(parentMenu)

		names = kaplot.context.sampleValues.keys()
		for name in names:
			if name in context:
				bold = True
			else:
				bold = False
			menu.addSubMenu(name, self.getContextMenuFor(window, context, name, parentMenu), bold=bold)
		return menu
			
	def getSelectionMenu(self):
		def select(window, object):
			window.select(object)
		def addPage(page):
			menu = []
			for container in page.containers:
				containerMenu = []
				containerMenu.append(("select", select, [container]))
				subMenu = []
				for plotObject in container.objects:
					plotSubMenu = []
					plotSubMenu.append(("select", select, [plotObject]))
					plotSubMenu.append(("context", self.getContextMenu(plotObject.context)))
					subMenu.append((str(plotObject), plotSubMenu))
				containerMenu.append(("children", subMenu))
				#menu.append(None)
				menu.append((str(container), containerMenu))
			if len(menu) > 1:
				menu.pop()
			return menu
			
		document = self.getDocument()
		menu = []
		if len(document.pages) == 1:
			menu = addPage(document.pages[0])
		else:
			for i, page in enumerate(document.pages):
				menu.append(("page %i" % i, addPage(page)))
		return menu
			
	def getZoomMenu(self, window, x, y, parentMenu=None):
		wx, wy = self.windowToWorld(x, y)
		menu = window.createMenu(parentMenu)
		def scale(window, x, y, s):
			(x1, y1), (x2, y2) = self.getWorld()
			width = x2 - x1
			height = y2 - y1
			self.world = (x-width*s/2, y-height*s/2), (x+width*s/2, y+height*s/2)
			window.refreshDocument()
		cx, cy = self.getWorldMatrix() * (0.5, 0.5)
		menu.addCommand("zoom in  x10  (10%)", scale, args=[wx, wy, 0.1])
		menu.addCommand("zoom in   x2  (50%)", scale, args=[wx, wy, 0.5])
		menu.addCommand("zoom out  x2 (200%)", scale, args=[wx, wy, 2.])
		menu.addCommand("zoom out x10 (1000%)", scale, args=[wx, wy, 10.])
		return menu
		
	def getGrowMenu(self, window, parentMenu=None):
		menu = window.createMenu(parentMenu)
		def grow(window, **kwargs):
			self.grow(**kwargs)
			window.refreshDocument()
		cx, cy = self.getWorldMatrix() * (0.5, 0.5)
		menu.addCommand("1.10x", grow, kwargs={"s":1.1})
		menu.addCommand("1.25x", grow, kwargs={"s":1.2})
		menu.addCommand("1.50x", grow, kwargs={"s":1.5})
		for side in ["x", "y", "left", "right", "bottom", "top"]:
			subMenu = window.createMenu(menu)
			subMenu.addCommand("1.10x", grow,  kwargs={side:1.1})
			subMenu.addCommand("1.25x", grow, kwargs={side:1.2})
			subMenu.addCommand("1.50x", grow, kwargs={side:1.5})
			menu.addSubMenu("grow %s" % side, subMenu)
		return menu
		
	def handleMouseEvent(self, x, y, options, window):
		window.setInfoText("pixel: x = %g; y = %g" % (x, y))
		
	def handleKeyboardEvent(self, x, y, keycode, character, options, window):
		window.setInfoExtraText("pressed key:\nkeycode = %r\ncharacter = %r" % (keycode, character))
		
		
		
	
class Document(PlotBase):
	def __init__(self, size=kaplot.size.default, dpi=kaplot.defaultDpi, offset="0cm, 0cm", extraborder="0mm, 0mm, 0, 0mm", **kwargs):
		self.size = size
		self.offset = offset
		self.extraborder = extraborder
		self.dpi = dpi
		self.pages = [] #[Page(self) for x in range(pages)]
		width, wunits, height, hunits = kaplot.utils.getSize(self.size)
		#if size == kaplot.size.default:
		#	raise "dsa"
		self.pixelWidth = int(kaplot.utils.convertToPixels(width, wunits, dpi=self.dpi))
		self.pixelHeight = int(kaplot.utils.convertToPixels(height, hunits, dpi=self.dpi))
		self.context = kaplot.defaultContext.clone()
		self.context.update(kwargs)
		
		#for units in kaplot.utils.supportedunits:
		#self.dimensions[units] = (
		#	kaplot.utils.convertPixelsTo(self.pixelWidth, units, self.dpi),
		#	kaplot.utils.convertPixelsTo(self.pixelHeight, units, self.dpi)
		#)
		
	def getPageCount(self):
		return len(self.pages)
		
	def getContextValue(self, name):
		if name in self.context:
			return self.context[name]
		else:
			raise AttributeError, "no context attribute value found with name %r'" % name

	def layout(self):		
		for page in self.pages:
			start = time()
			page.layout()
			kaplot.debug("time to layout page:", time() - start)
			

	def draw(self, device):
		device.preDraw(self)
		self.layout()
		#device.pushContext(self.context)
		for page in self.pages:
			device.preDrawPage(self, page)
			start = time()
			page.draw(device)
			kaplot.debug("time to draw page:", time() - start)
			device.postDrawPage(self, page)
		#device.popContext()
		device.postDraw(self)
			
	def sizeToViewport(self, size, viewport=((0, 0), (1, 1))):
		size, units = kaplot.utils.splitDimension(size)
		sizePixels = kaplot.utils.convertToPixels(float(size), units, dpi=self.dpi)
		(x1, y1), (x2, y2) = viewport
		width = float(x2 - x1)
		height = float(y2 - y1)
		sizeX = sizePixels / (self.pixelWidth-1) / width
		sizeY = sizePixels / (self.pixelHeight-1) / height
		return kaplot.Vector(sizeX, sizeY)
		
	def viewportToSize(self, x, y, units="mm", viewport=((0, 0), (1, 1))):
		#size, units = kaplot.utils.splitDimension(size)
		x, y = kaplot.Matrix.scalebox_inverse(*viewport) * (x, y)
		px = x * (self.pixelWidth-1)
		py = y * (self.pixelHeight-1)
		sx = kaplot.utils.convertPixelsTo(px, units, dpi=self.dpi)
		sy = kaplot.utils.convertPixelsTo(py, units, dpi=self.dpi)
		return kaplot.Vector(sx, sy)
		
	def windowToViewport(self, x, y, viewport=((0, 0), (1, 1))):
		v = kaplot.Vector(float(x) / (self.pixelWidth-1), float(y) / (self.pixelHeight-1))
		return kaplot.Matrix.scalebox_inverse(*viewport).inverse() * v
		
	def viewportToWindow(self, x, y, viewport=((0, 0), (1, 1))):
		x, y = kaplot.Matrix.scalebox_inverse(*viewport) * (x, y)
		v = kaplot.Vector(float(x) * (self.pixelWidth-1), float(y) * (self.pixelHeight-1))
		return v
		#return kaplot.Matrix.scalebox(*viewport).inverse() * v
		
class Page(PlotBase):
	def __init__(self, document, **kwargs):
		if not isinstance(document, Document):
			raise TypeError, "page parent should be a document"
		self.document = document
		self.document.pages.append(self)
		self.containers = []
		self.context = kaplot.Context(**kwargs)
		
	def getPageNr(self):
		return self.document.pages.index(self)
		
	def layout(self):
		for container in self.containers:
			container.layout()

	def draw(self, device):
		device.pushContext(self.context)
		for container in self.containers:
			container.draw(device)
		device.popContext()

	def getContextValue(self, name):
		if name in self.context:
			return self.context[name]
		else:
			return self.document.getContextValue(name)

	def getDocument(self):
		return self.document
		
	def findContainer(self, x, y, previous=None):
		#print "find", x, y
		containers = []
		for container in self.containers[::-1]:
			(x1, y1), (x2, y2) = container.viewport
			#print "vp", x1, y1, x2, y2
			if x >= x1 and x <= x2 and y >= y1 and y <= y2:
				containers.append(container)
		if previous in containers:
			index = containers.index(previous)
			index = (index + 1) % len(containers)
			#print "index =", index
			return containers[index]
		else:
			if len(containers) > 0:
				return containers[0]
			else:
				return None
		



from containers import Container, Box, Box2
from decorators import Decorator, Spacer, Border, Title, Labels, Axes
from axes import Axes2, Axis
from plotobjects import PlotObject, Text, Line, HLine, HFill, VLine, VFill, PolyLine, Polygon, Rectangle, \
	 FillRange, Symbols, IndexedImage, Contour, ContourFill, InnerColorbar,\
	 ErrorBars, ErrorRange, HistogramLine, BarChart, Legend, Grid, Pointer
