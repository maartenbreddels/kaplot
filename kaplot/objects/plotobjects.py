# -*- coding: utf-8 -*-
import kaplot
import kaplot.context
from kaplot.objects import Container
from kaplot.objects import PlotBase
import numpy
import math

class PlotObject(PlotBase):
	def __init__(self, container, **kwargs):
		if not isinstance(container, Container):
			raise TypeError, "PlotObject parent should be a container, (not '%r')" % (container)
		self.parent = container
		self.container = container
		self.parent.objects.append(self)
		bbox = self.getBBox()
		if bbox is not None:
			self.container.fit(bbox)
		self.context = kaplot.Context(**kwargs)
		
	def getContextValue(self, name):
		if name in self.context:
			return self.context[name]
		else:
			return self.container.getContextValue(name)
		
	def getDocument(self):
		return self.container.getDocument()
		
	def getBBox(self):
		return None
		
	def clone(self, container):
		kaplot.info("clone not implemented for %r" % self.__class__)


class Text(PlotObject):
	__fdoc__ = """Draws a text string
	
	Arguments:
	 * halign -- horizontal placement of text relative to location
	 * valign -- vertical placement of text relative to location
	 
	Example:
	 * Text("Hello", 0.5, 0.5, "left", "center")
	 	This will draw the text "Hello" to the right of location (0.5, 0.5)
	
	"""
	
	def __init__(self, container, text, x=0.5, y=0.5, halign="center", valign="center", textangle=0, **kwargs):
		self.text = text
		self.x = x
		self.y = y
		self.halign = halign
		self.valign = valign
		self.textangle = textangle
		super(Text, self).__init__(container, **kwargs)
		
	def draw(self, device):
		device.pushContext(self.context)
		device.drawText(self.text, self.x, self.y, self.halign, self.valign, textangle=self.textangle)
		device.popContext()


class Line(PlotObject):
	__fdoc__ = """Draws a line from x1,y1 to x2,y2
	Example:
	 * line(0, 0, 10, 5)
	 * line(20, -5, 2, 50)
	"""
	def __init__(self, container, x1, y1, x2=1, y2=2, **kwargs):
		self.x1 = x1
		self.y1 = y1
		self.x2 = x2
		self.y2 = y2
		super(Line, self).__init__(container, **kwargs)
		
	def draw(self, device):
		#print "drawline"
		device.pushContext(self.context)
		device.drawLine(self.x1, self.y1, self.x2, self.y2)
		device.popContext()

	def getBBox(self):
		return (self.x1, self.y1), (self.x2, self.y2)

class HLine(PlotObject):
	def __init__(self, container, y=0, **kwargs):
		self.y = y
		super(HLine, self).__init__(container, **kwargs)
		
	def draw(self, device):
		device.pushContext(self.context)
		matrix = device.getWorldMatrix().inverse()
		x1, y1 = matrix * (0,0)
		x2, y2 = matrix * (1,0)
		device.drawLine(x1, self.y, x2, self.y)
		device.popContext()
	
	def getBBox(self):
		return None
				
class HFill(PlotObject):
	def __init__(self, container, y1, y2, gridsnap=True, **kwargs):
		self.y1 = y1
		self.y2 = y2
		self.gridsnap = gridsnap
		super(HFill, self).__init__(container, **kwargs)
		
	def draw(self, device):
		device.pushContext(self.context)
		matrix = device.getWorldMatrix().inverse()
		x1, y1 = matrix * (0,0)
		x2, y2 = matrix * (1,1)
		xlist = [x1, x2, x2, x1]
		ylist = [self.y1, self.y1, self.y2, self.y2]
		device.drawPolygon(xlist, ylist, gridsnap=self.gridsnap)
		device.popContext()
	
	def getBBox(self):
		return None
				
class VLine(PlotObject):
	def __init__(self, container, x=0, yscale1=0., yscale2=1.,**kwargs):
		self.x = x
		self.yscale1 = yscale1
		self.yscale2 = yscale2
		super(VLine, self).__init__(container, **kwargs)
		
	def draw(self, device):
		device.pushContext(self.context)
		matrix = device.getWorldMatrix().inverse()
		x1, y1 = matrix * (0,0)
		x2, y2 = matrix * (0,1)
		sy1 = y1 + self.yscale1 * (y2-y1)
		sy2 = y1 + self.yscale2 * (y2-y1) 
		device.drawLine(self.x, sy1, self.x, sy2)
		device.popContext()
	
	def getBBox(self):
		return None
	
class VFill(PlotObject):
	def __init__(self, container, x1, x2, gridsnap=True, **kwargs):
		self.x1 = x1
		self.x2 = x2
		self.gridsnap = gridsnap
		super(VFill, self).__init__(container, **kwargs)
		
	def draw(self, device):
		device.pushContext(self.context)
		matrix = device.getWorldMatrix().inverse()
		x1, y1 = matrix * (0,0)
		x2, y2 = matrix * (1,1)
		xlist = [self.x1, self.x2, self.x2, self.x1]
		ylist = [y1, y1, y2, y2]
		#print "vfill", xlist, ylist
		device.drawPolygon(xlist, ylist, gridsnap=self.gridsnap)
		device.popContext()
	
	def getBBox(self):
		return None
				
	
				
class Rectangle(PlotObject):
	__fdoc__ = """Draws a rectangle from x1,y1 to x2,y2
	
	Arguments:
	 * solid -- if True, the rectangle will be filled

	Example:
	 * rectangle(0, 0, 10, 5)
	 * rectangle(20, -5, 2, 50)

	"""
	def __init__(self, container, x1, y1, x2, y2, solid=False, gridsnap=True, **kwargs):
		self.x1 = x1
		self.y1 = y1
		self.x2 = x2
		self.y2 = y2
		self.solid = solid
		self.gridsnap = gridsnap
		super(Rectangle, self).__init__(container, **kwargs)
		
	def draw(self, device):
		device.pushContext(self.context)
		xlist = [self.x1, self.x2, self.x2, self.x1]
		ylist = [self.y1, self.y1, self.y2, self.y2]
		if self.solid:
			#device.drawPolygon(xlist, ylist, close=True, gridsnap=self.gridsnap)
			device.drawPolygon(xlist, ylist, gridsnap=self.gridsnap)
		else:
			#device.drawPolyLine(xlist, ylist, close=True, gridsnap=self.gridsnap)
			device.drawPolyLine(xlist, ylist, gridsnap=self.gridsnap, close=True)
		device.popContext()

	def getBBox(self):
		return (self.x1, self.y1), (self.x2, self.y2)
				
class PolyLine(PlotObject):
	__fdoc__ = """Draws a polyline from (x[0],y[0]) to (x[1],y[1]) ... to (x[n],y[n])
	
	Arguments:
	 * x -- an array or other sequence
	 * y -- idem
	 * close -- if True, the begin and endpoint will be connected
	 
	Example:
	 * polyline([0, 1, 2, 3], [0, 1, 4, 9], color='red')
	 * {{{#!python
    x = arange(0, 5, 0.1)
    y = sin(x*3) * x**2
    polyline(x, y, linestyle='dotdash')
    }}}
	"""
	def __init__(self, container, x, y, close=False, **kwargs):
		self.x = x
		self.y = y
		self.close = close
		super(PolyLine, self).__init__(container, **kwargs)
		
	def draw(self, device):
		#print "drawpolyline"
		device.pushContext(self.context)
		device.drawPolyLine(self.x, self.y, close=self.close)
		device.popContext()
		
	def getBBox(self):
		return (min(self.x), min(self.y)), (max(self.x), max(self.y))

	def clone(self, container):
		return PolyLine(container, x=self.x, y=self.y, close=self.close, **self.context)

class Polygon(PlotObject):
	__fdoc__ = """Same as polyline but now the interior will be filled.
	"""
	def __init__(self, container, x, y, close=True, **kwargs):
		self.x = x
		self.y = y
		self.close = close
		super(Polygon, self).__init__(container, **kwargs)
		
	def draw(self, device):
		device.pushContext(self.context)
		device.drawPolygon(self.x, self.y)
		device.popContext()
		
	def getBBox(self):
		return (min(self.x), min(self.y)), (max(self.x), max(self.y))

class FillRange(PlotObject):
	__fdoc__ = """Draws a polygon between the y1 values and y2 values"""
	def __init__(self, container, x, y1, y2, **kwargs):
		self.x = x
		self.y1 = y1
		self.y2 = y2
		assert len(x) == len(y1)
		assert len(x) == len(y2)
		super(FillRange, self).__init__(container, **kwargs)
		
	def draw(self, device):
		device.pushContext(self.context)
		#x = numpy.concatenate([[self.x[0]], self.x, [self.x[-1]]])
		#y = numpy.concatenate([[self.level], self.y, [self.level]])
		x = numpy.concatenate([self.x, self.x[::-1]])
		y = numpy.concatenate([self.y1, self.y2[::-1]])
		device.drawPolygon(x, y)
		device.popContext()
		
	def getBBox(self):
		ymin = min(min(self.y1), min(self.y2))
		ymax = max(max(self.y1), max(self.y2))
		return (min(self.x), ymin), (max(self.x), ymax)

class Symbols(PlotObject):
	__fdoc__ = """Draws symbols at locations (x[n], y[n])
	
	Example:
	{{{#!python
    x = arange(0.001, 10, 0.1)
    y = sin(x)/x
    symbols(x, y, symbolName='triangle')
    }}}
	"""
	def __init__(self, container, x, y, symbolName="x", xscales=None, yscales=None, angles=None, colors=None, colormap='rainbow', datamin=None, datamax=None, **kwargs):
		self.x, self.y = x, y
		self.xscales = xscales
		self.yscales = yscales
		self.angles = angles
		self.symbolName = symbolName
		self.colors = colors
		self.colormap = colormap
		self.datamin = datamin
		self.datamax = datamax
		PlotObject.__init__(self, container, **kwargs)

	def draw(self, device):
		colors = self.colors
		if colors is not None:
			colors = numpy.array(self.colors)
			#print colors.min(), colors.max()
			datamin = self.datamin
			datamax = self.datamax
			if datamin is None:
				datamin = colors.min()
			if datamax is None:
				datamax = colors.max()
			colors = (colors - datamin) / (datamax - datamin)
			colors = colors.clip(0,1)
		#if self.datamin != None and self.datamax != None: 
		#	colors = colors.clip(min=self.datamin, max=colors.max())
		#if self.datamax != None: 
		#	colors = colors.clip(min=colors.min(), max=self.datamax)
		#print colors.min(), colors.max()
		device.pushContext(self.context)
		device.drawSymbol(self.x, self.y, self.symbolName, xscales=self.xscales, yscales=self.yscales, angles=self.angles, colors=colors, colormap=self.colormap)
		device.popContext() 

	def getBBox(self):
		return (min(self.x), min(self.y)), (max(self.x), max(self.y))

	def clone(self, container):
		return Symbols(container, x=self.x, y=self.y, symbolName=self.symbolName,
			xscales=self.xscales, yscales=self.yscales, angles=self.angles, **self.context)

class IndexedImage(PlotObject):
	__fdoc__ = """Draws an intensity image using the colormap to map the intensity to a color
	
	Example:
	 * {{{#!python
    x, y = meshgrid()
    I = e**-(x**2+y**2)
    indexedimage(I, colormap='cool')}}}
	"""
	def __init__(self, container, data2d, matrix=None, mask2d=None, colormap="rainbow", datamin=None, datamax=None, function="linear", resize=None, context=None, **kwargs):
		self.data2d = numpy.array(data2d)
		if matrix is None:
			matrix = kaplot.Matrix()
		self.matrix = matrix
#		if resize:
#			height, width = self.data2d.shape
#			height, width = float(height), float(width)
#			(x1, y1), (x2, y2) = resize
#			self.matrix = \
#			kaplot.Matrix.translate(-0.5, -0.5) *\
#			kaplot.Matrix.translate(float(x1), float(y1)) *\
#			kaplot.Matrix.scale((x2-x1)/width, (y2-y1)/height)
		if resize is not None:
			height,width = data2d.shape
			(x1, y1), (x2, y2) = resize
			#print "~~~", resize, width, height
			#	kaplot.Matrix.translate(-0.5, -0.5) *\
			dx = (x2-x1)/float(width-1)
			dy = (y2-y1)/float(height-1)
			self.matrix = \
				kaplot.Matrix.translate(float(x1), float(y1)) *\
				kaplot.Matrix.scale(dx, dy)
		PlotObject.__init__(self, container, **kwargs)
		self.mask2d = mask2d
		self.colormap = colormap
		self.datamin = datamin
		self.datamax = datamax
		self.function = function
		if datamin == None:
			self.datamin = self.data2d.min()
		if datamax == None:
			self.datamax = self.data2d.max()
			
			
		#self.context.setWorldImage(self.data2d)

	def draw(self, device):
		device.pushContext(self.context)
		#transformedData2d = self.transformImage()
		#transformedData2d = self.data2d
		#device.drawIndexedImage(transformedData2d, self.colormap, 'linear', self.mask2d, matrix=self.matrix)
		device.drawIndexedImage(self.data2d, self.colormap, 'linear', self.mask2d, matrix=self.matrix, datamin=self.datamin, datamax=self.datamax)
		device.popContext()

	def ____transformImage(self):
		function = kaplot.utils.getFunction(self.function)
		data2d = function(self.data2d)
		datamin = function(self.datamin)
		datamax = function(self.datamax)
		data2d = numpy.clip(data2d, min(datamin, datamax), max(datamin, datamax))
		data2d = (data2d - datamin) / (datamax - datamin)
		#print datamin, datamax, min(datamin, datamax), max(datamin, datamax)
		#import pdb; pdb.set_trace()
		#print data2d.min(), data2d.max() 
		return data2d

	def getBBox(self):
		height, width = self.data2d.shape
		#p1, p2 = (0, 0), (width, height)
		#offset = kaplot.Vector(-0.5, -0.5)
		#p1, p2 = (0.5, 0.5), (width+0.5, height+0.5)
		p1, p2 = (-0.5, -0.5), (width-0.5, height-0.5)
		offset = kaplot.Vector(-0.0, -0.0)
		return self.matrix * p1 + offset, self.matrix * p2 + offset

import kaplot.cext._contour as _contour
from time import time
class Contour(PlotObject):
	__fdoc__ = """HIDE"""
	def __init__(self, container, data2d, levels, matrix=None, resize=None, datamin=None, datamax=None, fill=False, **kwargs):
		self.data2d = numpy.array(data2d)
		if datamax is None:
			datamax = self.data2d.max()
		if datamin is None:
			datamin = self.data2d.min()
		if hasattr(levels, "__getitem__"):
			self.levels = levels
		else:
			noLevels = levels
			#print noLevels
			levels = (numpy.arange(noLevels)+1.)/(noLevels+1)
			#print levels
			levels = levels*(datamax-datamin)+datamin
			#print levels, self.data2d.min(), self.data2d.max()
			self.levels = levels
		self.matrix = matrix
		if self.matrix is None:
			self.matrix = kaplot.Matrix()
		self.fill = fill
		self.resize = resize
		if resize is not None:
			height,width = data2d.shape
			(x1, y1), (x2, y2) = resize
			#print "~~~", resize, width, height
				#kaplot.Matrix.translate(-0.5, -0.5) *\
			self.matrix = \
				kaplot.Matrix.translate(x1, y1) *\
				kaplot.Matrix.scale((x2-x1)/float(width-1), (y2-y1)/float(height-1)) *\
				kaplot.Matrix.translate(-1.0, -1.0)
				#kaplot.Matrix.scale((x2-x1)/float(width-1), (y2-y1)/float(height-1))
		PlotObject.__init__(self, container, **kwargs)
		
	def draw(self, device):
		device.pushContext(self.context)
		cinterface = device.getCInterface()
		begin = time()
		for level in self.levels:
			if False:
				polylines, labels = _contour.contour(self.data2d.astype(numpy.float32), level, cinterface)
			else:
				#print self.data2d.shape
				polylines, labels = _contour.contour(self.data2d.astype(numpy.float32), level)
				xs = []
				ys = []
				for x, y in polylines:
					m = self.matrix
					x, y = m.xx * x + m.xy * y + m.tx, m.yx * x + m.yy * y + m.ty,
					#print self.data2d.min(), self.data2d.max(), level
					#print list(x), list(y)
					if self.fill:
						xs.extend(x)
						ys.extend(y)
					else:
						device.drawPolyLine(x, y, close=False)
					#x = [0, 1, 2, 3]
					#y = [-1,2,0,1]
				if self.fill:
					x = numpy.array(xs)
					y = numpy.array(ys)
					if 1:
						#print "=" * 70
						#for p in zip(x, y):
						#	print p
						center_x = numpy.mean(x)
						center_y = numpy.mean(y)
						angles = numpy.arctan2(y-center_y, x-center_x)
						indices = numpy.argsort(angles)
						x_sorted = x[indices]
						y_sorted = y[indices]
						#print "-" * 70
						#for p in zip(x_sorted, y_sorted):
						#	print p
						#print "**" * 70
						device.drawPolygon(x_sorted, y_sorted)
					else: 
						device.drawPolygon(x, y)
					
					
					#device.drawPolyLine(x, y, close=False)
			#kaplot.debug("time for contour:", time()-begin)
		#kaplot.debug("time for all contour:", time()-begin)
		device.popContext()

	def _getBBox(self):
		height, width = self.data2d.shape
		m = self.matrix
		x = numpy.array([0.5, width-0.5])
		y = numpy.array([0.5, height-0.5])
		x, y = m.xx * x + m.xy * y + m.tx, m.yx * x + m.yy * y + m.ty,
		return (min(x), min(y)), (max(x), max(y))
		#height, width = self.data2d.shape
		#return (0.5, 0.5), (width+0.5, height+0.5)
	
	def __getBBox(self):
		height, width = self.data2d.shape
		p1, p2 = (0, 0), (width, height)
		#offset = kaplot.Vector(0.5, 0.5)
		offset = kaplot.Vector(0, 0)
		#matrix = \
		#	kaplot.Matrix.translate(-0.5, -0.5) *\
		#	self.matrix *\
		#	kaplot.Matrix.translate(0.5, 0.5)
		height,width = self.data2d.shape
		(x1, y1), (x2, y2) = self.resize
		#print "~~~", resize, width, height
			#kaplot.Matrix.translate(-0.5, -0.5) *\
		matrix = \
			kaplot.Matrix.translate(x1, y1) *\
			kaplot.Matrix.scale((x2-x1)/float(width+1), (y2-y1)/float(height+1)) *\
			kaplot.Matrix.translate(0.5, 0.5)
		return matrix * p1 + offset, matrix * p2 + offset

	def getBBox(self):
		height, width = self.data2d.shape
		#p1, p2 = (0, 0), (width, height)
		#offset = kaplot.Vector(-0.5, -0.5)
		#p1, p2 = (0.5, 0.5), (width+0.5, height+0.5)
		p1, p2 = (0.5, 0.5), (width+0.5, height+0.5)
		offset = kaplot.Vector(-0.0, -0.0)
		return self.matrix * p1 + offset, self.matrix * p2 + offset

class ContourFill(PlotObject):
	__fdoc__ = """HIDE"""
	def __init__(self, container, data2d, level1, level2, **kwargs):
		self.data2d = numpy.array(data2d)
		self.level1 = level1
		self.level2 = level2
		PlotObject.__init__(self, container, **kwargs)
		
	def draw(self, device):
		device.pushContext(self.context)
		cinterface = device.getCInterface()
		mask2d = numpy.logical_and(self.data2d >= self.level1, self.data2d <= self.level2)
		device.drawIndexedImage(self.data2d, mask2d=mask2d, colormap="rainbow")
		device.popContext()

	def getBBox(self):
		height, width = self.data2d.shape
		return (0.5, 0.5), (width+0.5, height+0.5)

class Grid(PlotObject):
	__fdoc__ = """HIDE"""
	def __init__(self, container, x, y, **kwargs):
		self.x = x
		self.y = y
		super(PolyLine, self).__init__(container, **kwargs)
		
	def draw(self, device):
		device.pushContext(self.context)
		device.drawPolyLine(self.x, self.y)
		device.popContext()
		
	def getBBox(self):
		return None
		
class ErrorBars(PlotObject):
	__fdoc__ = """Draws errorbar at (x[n],y[n]) locations
	
	Arguments:
	 * xerr -- error in x direction, both positive and negative
	 * xpos -- positive error in x, overriding xerr
	 * xneg, ypos, yerr -- ...
	
	"""
	def __init__(self, container, x, y, size="1.5mm", xerr=None, yerr=None, xpos=None, xneg=None, ypos=None, yneg=None, **kwargs):
		PlotObject.__init__(self, container, **kwargs)
		self.x = x
		self.y = y
		self.xerr = xerr
		self.yerr = yerr
		self.xpos = xpos
		self.xneg = xneg
		self.ypos = ypos
		self.yneg = yneg
		self.size = size

	def draw(self, device):
		device.pushContext(self.context)
		document = self.getDocument()
		width, height = document.sizeToViewport(self.size, device.getViewport())
		width, height = device.getWorldMatrix().no_translation().inverse() * kaplot.Vector(width, height)
		hwidth = width #/ 200
		hheight = height #/ 200

		xneg, xpos = None, None
		if self.xerr is not None:
			xneg = self.xerr
			xpos = self.xerr
		if self.xpos is not None:
			xpos = self.xpos
		if self.xneg is not None:
			xneg = self.xneg

		if xneg is not None and xpos is not None:
			for x, y, xneg, xpos in zip(self.x, self.y, xneg, xpos):
				device.drawLine(x-xneg, y, x+xpos, y)
				device.drawLine(x-xneg, y-hheight, x-xneg, y+hheight)
				device.drawLine(x+xpos, y-hheight, x+xpos, y+hheight)
		elif xneg is not None:
			for x, y, xneg in zip(self.x, self.y, xneg):
				device.drawLine(x-xneg, y, x, y)
				device.drawLine(x-xneg, y-hheight, x-xneg, y+hheight)
		elif xpos is not None:
			for x, y, xpos in zip(self.x, self.y, xpos):
				device.drawLine(x, y, x+xpos, y)
				device.drawLine(x+xpos, y-hheight, x+xpos, y+hheight)

		yneg, ypos = None, None
		if self.yerr is not None:
			yneg = self.yerr
			ypos = self.yerr
		if self.ypos is not None:
			ypos = self.ypos
		if self.yneg is not None:
			yneg = self.yneg

		if yneg is not None and ypos is not None:
			for x, y, y1, y2 in zip(self.x, self.y, yneg, ypos):
				device.drawLine(x, y-y1, x, y+y2)
				device.drawLine(x-hwidth, y-y1, x+hwidth, y-y1)
				device.drawLine(x-hwidth, y+y2, x+hwidth, y+y2)
		elif yneg is not None:
			for x, y, y1 in zip(self.x, self.y, yneg):
				device.drawLine(x, y-y1, x, y)
				device.drawLine(x-hwidth, y-y1, x+hwidth, y-y1)
		elif ypos is not None:
			for x, y, y2 in zip(self.x, self.y, ypos):
				device.drawLine(x, y, x, y+y2)
				device.drawLine(x-hwidth, y+y2, x+hwidth, y+y2)

		device.popContext() 		

class ErrorRange(PlotObject):
	__fdoc__ = """Fills between the errors instead of drawing error bars (see errorbars)
	
	Arguments:
	 * x, y -- arrays or sequences containing the locations
	 * err -- the error in y, both positive and negative
	 * pos, neg -- the positive and negative error in y, overriding err
	 * fill -- if False, doesn't fill, but draws a line at the edges
	 * caps -- if fill is False, and caps is False, the 'caps' at the left and right end are not drawn
	"""
	def __init__(self, container, x, y, err, pos=None, neg=None, fill=True, caps=False, **kwargs):
		PlotObject.__init__(self, container, **kwargs)
		self.x = x
		self.y = y
		self.err = err
		self.pos = pos
		self.neg = neg
		self.fill = fill
		self.caps = caps

	def draw(self, device):
		device.pushContext(self.context)
		
		neg, pos = None, None
		
		if self.pos is not None:
			pos = self.pos
		else:
			if self.err is not None:
				pos = self.err
			else:
				pos = numpy.zeros(len(self.x))
		if self.neg is not None:
			neg = self.neg
		else:
			if self.err is not None:
				neg = self.err
			else:
				neg = numpy.zeros(len(self.x))
		
			
		indices = numpy.argsort(self.x)
		xsorted = numpy.take(self.x, indices)
		ysorted = numpy.take(self.y, indices)
		possorted = numpy.array(pos)[indices]
		negsorted = numpy.array(neg)[indices]
		x1 = numpy.array(xsorted)
		x2 = numpy.array(list(xsorted)[::-1])
#<<<<<<< plotobjects.py
#		y1 = numpy.array(ysorted) + possorted
#		y2 = numpy.array(list(numpy.array(ysorted) - negsorted)[::-1])
#=======
		y1 = numpy.array(ysorted) + numpy.array(pos)
		y2 = numpy.array(list(numpy.array(ysorted) - numpy.array(neg))[::-1])
#>>>>>>> 1.23
		x = numpy.concatenate([x1, x2])
		y = numpy.concatenate([y1, y2])

		if self.fill:
			device.drawPolygon(x, y)
		else:
			if self.caps:
				device.drawPolyLine(x, y)
			else:
				device.drawPolyLine(x1, y1)
				device.drawPolyLine(x2, y2)

		device.popContext() 		


def bindata(bindata, bincount=10, datamin=None, datamax=None):
	length = len(bindata)
	#bindata = array(bindata)
	#scaled = (((bindata - datamin) / (float(datamax) - datamin)) * float(bins))#.astype(Int)
	#indices = searchsorted(sort(scaled), arange(bins))
	#end = len(scaled)
	#a = concatenate([indices, [end]])
	#return a[1:] - a[:-1]
	if datamin == None:
		datamin = min(bindata)
	if datamax == None:
		datamax = max(bindata)

	binData = numpy.zeros(bincount)
	for i in xrange(0, length):
		binNo = int(math.floor( ((bindata[i] - datamin) / (float(datamax) - datamin)) * float(bincount)))
		if binNo >= 0 and binNo < bincount:
			binData[binNo] += 1
		elif binNo == bins:
			binData[binNo-1] += 1
	step = float(datamax-datamin)/bincount
	return numpy.arange(datamin, datamax+step/2, step), binData

def _bindata(bindata, binwidth=1.0, datamin=None, datamax=None, weights=None):
	length = len(bindata)
	if weights is None:
		weights = numpy.ones(len(bindata), numpy.float64)
	#weights = weights / sum(weights) * len(weights)
	#bindata = array(bindata)
	#scaled = (((bindata - datamin) / (float(datamax) - datamin)) * float(bins))#.astype(Int)
	#indices = searchsorted(sort(scaled), arange(bins))
	#end = len(scaled)
	#a = concatenate([indices, [end]])
	#return a[1:] - a[:-1]
	if datamin == None:
		datamin = min(bindata)
	if datamax == None:
		datamax = max(bindata)
	startbin = math.floor(datamin/binwidth)
	endbin = math.floor(datamax/binwidth)
	bincount = endbin - startbin # +1
	print "bins:", startbin, endbin, "bincount", bincount
	binData = numpy.zeros(bincount)
	for i in xrange(0, length):
		#binNo = int(math.floor( ((bindata[i] - datamin) / (float(datamax) - datamin)) * float(bincount)))
		#binNo = int(math.floor( ((bindata[i] - datamin) / (float(datamax) - datamin)) * float(bincount)))
		binNo = math.floor(bindata[i]/binwidth) - startbin
		if binNo >= 0 and binNo < bincount:
			binData[binNo] += weights[i]
		#elif binNo == bins:
		#	binData[binNo-1] += 1
	#step = float(datamax-datamin)/bincount
	return numpy.arange(startbin*binwidth, (endbin+1.5)*binwidth, binwidth), binData

bindata2 = _bindata

class HistogramLine(PlotObject):
	__fdoc__ = """Draws a histogram line
	
	Arguments:
	 * bins -- values of the bins, the first bin will be drawn between bins[0] and bins[1]
	 * data -- the binned or unbinned data. If unbinned, the height of the bin, otherwise the raw data
	 * binned -- if False, data will be binned according to bincount
	 * fill -- boolean, fill or just draw the outline
	 * drawverticals -- if fill is False, this determines if the vertical lines between bins are also drawn
	 * drawsides -- if fill is False, this determines if the outer left and right line are drawn
	"""
	def __init__(self, container, bins, data, binned=True, bincount=10, fill=True, drawverticals=False, drawsides=True, **kwargs):
		self.data = data
		self.binneddata = None
		self.bins = bins
		self.data = data
		self.binned = binned
		self.bincount = bincount
		self.fill = fill
		self.drawverticals = drawverticals
		self.drawsides = drawsides

		if self.binned:
			self.binneddata = self.data
		else:
			self.binneddata = bindata(self.data, self.bincount)
		PlotObject.__init__(self, container, **kwargs)

	def draw(self, device):
		device.pushContext(self.context)

		length = len(self.binneddata)
		#print self.fill, self.drawverticals
		if not self.fill and self.drawverticals:
		#if not self.fill and not self.drawverticals:
			#import pdb
			#pdb.set_trace()
			x = numpy.repeat(self.bins, 3)[1:-1]
			y = numpy.transpose([numpy.zeros(len(self.binneddata), dtype=numpy.float), 
						self.binneddata, self.binneddata]).flat
			y = numpy.concatenate([list(y), [0]])
			#print len(self.bins), len(self.binneddata)
			#print len(x), len(y), type(x), type(y)
			if not self.fill and not self.drawsides:
				device.drawPolyLine(x[1:-1], y[1:-1], gridsnap=True)
				#print self.binneddata
				#print x[1:-1], y[1:-1]
				pass
			else:
				device.drawPolyLine(x, y, gridsnap=True)
				#print x
				#print "y=",y
		else:
			x = numpy.repeat(self.bins, 2)
			y = numpy.transpose([self.binneddata, self.binneddata]).flat
			y = numpy.concatenate([[0], list(y), [0]])
			if self.fill:
				device.drawPolygon(x, y, gridsnap=True)
				pass
			else:
				if self.drawsides:
					device.drawPolyLine(x, y, gridsnap=True)
				else:
					device.drawPolyLine(x[1:-1], y[1:-1], gridsnap=True)

		device.popContext()
 
 	def getBBox(self):
 		#print self.binneddata
 		bbox = (min(self.bins), min(self.binneddata)), (max(self.bins), max(self.binneddata))
 		#print "bbox=", bbox
		return bbox

class BarChart(PlotObject):
	def __init__(self, container, datalist, autoscale=True, contexts=None, barwidth=0.8, groupspacing=0.1, sortbars=False, bordercontext=None, **kwargs):
		self.datalist = datalist
		self.autoscale = autoscale
		self.contexts = contexts
		self.barwidth = barwidth
		self.groupspacing = groupspacing
		self.sortbars = sortbars
		if bordercontext:
			self.bordercontext = bordercontext
		else:
			self.bordercontext = kaplot.context.Context(color="lightgrey")
		PlotObject.__init__(self, container, **kwargs)
		

	def draw(self, device):
		device.pushContext(self.context)
		ymin = min([min(data) for data in self.datalist])
		ymax = max([max(data) for data in self.datalist])
		barcount = min([len(data) for data in self.datalist])
		groupcount = len(self.datalist)
		#if self.autoscale:
		#	self.context.setWorld(p1=(0.5, 0-(ymax-ymin)*self.bottommargin), p2=(barcount+0.5, ymax+(ymax-ymin)*self.topmargin))
			#self.context.setWorld(p1=(0.0, ymin-(ymax-ymin)*self.bottommargin), p2=(barcount+1.0, ymax+(ymax-ymin)*self.topmargin))

		contexts = [self.context.clone() for k in range(groupcount)]
		if self.contexts != None:
			for i, context in enumerate(self.contexts):
				if context:
					contexts[i] = kaplot.context.Context(context)

		#device.pushContext(self.context)
		#self.box.plot(device)

		#print len(self.datalist), len(self.datalist[0]), groupcount, barcount
		#print barcount
		for barNr in xrange(barcount):
			items = [(self.datalist[groupNr][barNr], contexts[groupNr]) for groupNr in xrange(groupcount)]
			if self.sortbars:
				items.sort(lambda x,y: cmp(y[0], x[0]))
			for groupNr, (value, context) in enumerate(items):
				if context != None:
					device.pushContext(context)
				#x1 = barNr - 0.5 - self.barwidth/2 + self.groupspacing*groupNr + 0.5
				#x2 = barNr - 0.5 + self.barwidth/2 - self.groupspacing*(groupcount-groupNr-1) + 0.5
				x1 = barNr -self.barwidth/41*groupcount- self.barwidth/2 + self.groupspacing*(groupNr-(groupcount-1)/2)
				x2 = barNr -self.barwidth/41*groupcount+ self.barwidth/2 + self.groupspacing*(groupNr-(groupcount-1)/2)
				x = [x1, x1, x2, x2]
				y = [0, value, value, 0]
				#print x, y
				device.drawPolygon(x, y)
				device.pushContext(self.bordercontext)
				#device.pushContext({"color":)
				x = [x1, x1, x2, x2, x1]
				y = [0, value, value, 0, 0]
				device.drawPolyLine(x, y)
				device.popContext()
				if context != None:
					device.popContext()

		device.popContext()
 
 	def getBBox(self):
		ymin = min([min(data) for data in self.datalist])
		ymax = max([max(data) for data in self.datalist])
		barcount = min([len(data) for data in self.datalist])
		groupcount = len(self.datalist)
 		#print self.binneddata
 		#bbox = (min(self.bins), 0), (max(self.bins), max(self.binneddata))
 		#print "bbox=", bbox
		ymin = min(0, ymin)
		bbox = ((-0.5,ymin), (barcount-0.5, ymax))
		return bbox

class Legend(PlotObject):
	__fdoc__ = """Draws a legend, as information for graphs for instance
	
	Arguments:
	 * types -- a list of string, specifing the marker that should be drawn
	 * labels -- a list of string
	 * location -- specifies where the legend is drawn.
	 		Format is "<hloc>, <vloc>", where <hloc> is 'left', 'center' or 'top'
	 		and <vloc> is  'bottom', 'center' or 'top'
	 * spacing -- the horizontal seperation between the symbols and the labels
	 * edgespacing -- the displacement from the edge, specified by 'location'
	 * borderspacing -- the seperation of the text and symbols, and the border drawn
	 		around it
	 * linelength -- if type contains a line, it's length will be specified by this
	 		arguments. (dotted or dashed lines sometimes need to be longer to be
	 		clearly visible)
	 	
	 	
	"""
	def __init__(self, container, types, labels, objects, location="right, top",
			spacing="2mm", edgespacing="10mm", borderspacing="2mm", linelength="1cm", drawborder=False, **kwargs):
		PlotObject.__init__(self, container, **kwargs)
		self.types = types
		self.labels = labels
		self.objects = objects
		self.location = location
		#self._position = self._getPosition()
		self.spacing = spacing
		self.edgespacing = edgespacing
		self.borderspacing = borderspacing
		self.linelength = linelength
		self.drawborder = drawborder
		
	def draw(self, device):
		fontname = self.getContextValue("fontname")
		fontsize = self.getContextValue("fontsize")
		font = kaplot.textmod.findFont(fontname, False, False)
		document = self.getDocument()
		
		device.pushContext(self.context)
		device.pushWorld(((0, 0), (1,1)))
		linelength = document.sizeToViewport(self.linelength, self.container.borderViewport).x
		spacing = document.sizeToViewport(self.spacing, self.container.borderViewport).x
		edgespacing = document.sizeToViewport(self.edgespacing, self.container.borderViewport)
		borderspacing = document.sizeToViewport(self.borderspacing, self.container.borderViewport)
		mm = document.sizeToViewport("1mm", self.container.borderViewport)
		textwidth = 0
		totalheight = 0
		totalwidth = 0
		for text, object in zip(self.labels, self.objects):
			if text:
				textObject = kaplot.textmod.parseText(text, font, fontsize, fontname, document.dpi)
				valign, halign = "center", "center"
				points = textObject.getBBoxTransformed(0, 0, 0, valign, halign)
				width = (points[1] - points[0]).x
				height = (points[-1] - points[0]).y
				width = document.sizeToViewport("%fpx" % width, self.container.borderViewport).x
				height = document.sizeToViewport("%fpx" % height, self.container.borderViewport).y
				textwidth = max(textwidth, width)
			else:
				height = 0.001 # fix, what to do with empty strings
			totalheight += height + mm.y*2
		totalheight -= mm.y*2
		totalwidth = textwidth + linelength + spacing# + borderspacing.x*2
		hloc, vloc = self.location.split(",")
		hloc, vloc = hloc.strip(), vloc.strip()
		if hloc == "right":
			x = 1-totalwidth-edgespacing.x #- borderspacing.x
		elif hloc == "left":
			x = edgespacing.x
		elif hloc == "center":
			x = 0.5 - totalwidth / 2 
		else:
			raise Exception, "horizontal location should be 'right', 'left' or 'center', not %r" % hloc
			
		if vloc == "top":
			y = 1-edgespacing.y
		elif vloc == "center":
			y = 0.5+totalheight/2
		elif vloc == "bottom":
			y = totalheight + edgespacing.y
		else:
			raise Exception, "vertical location should be 'top', 'bottom' or 'center', not %r" % hloc
		
		for type, text, object in zip(self.types, self.labels, self.objects):
			if text:
				textObject = kaplot.textmod.parseText(text, font, fontsize, fontname, document.dpi)
				valign, halign = "center", "center"
				points = textObject.getBBoxTransformed(0, 0, 0, valign, halign)
				height = (points[-1] - points[0]).y
				height = document.sizeToViewport("%fpx" % height, self.container.borderViewport).y
			else:
				height = 0.001 # fix, what to do with empty strings
			
			color = object.getContextValue("color")
			linestyle = object.getContextValue("linestyle")
			linewidth = object.getContextValue("linewidth")
			symbolsize = object.getContextValue("symbolsize")
			alpha = object.getContextValue("alpha")
			device.setColor(color)
			device.setLinestyle(linestyle)
			device.setLinewidth(linewidth)
			device.setSymbolSize(symbolsize)
			device.setAlpha(alpha)
			#device.drawText(text, 1-maxwidth-0.1, y, "left", "top")
			#device.drawLine(1-maxwidth-0.1-size-spacing, y-height/2, 1-maxwidth-0.1-spacing, y-height/2)
			# special case for lines, 
			if type == "line":
				device.drawLine(x, y-height/2, x+linelength, y-height/2, gridsnap=True)
			else:
				device.drawSymbol([x+linelength/2], [y-height/2], type)
			device.drawText(text, x+linelength+spacing, y, "left", "top")
			y = y - height - mm.y*2
		y += mm.y*2
		#y -= totalheight
		s = borderspacing
		#s = kaplot.Vector(0, 0)
		xlist = [x-s.x, x+totalwidth+s.x, x+totalwidth+s.x, x-s.x]
		ylist = [y-s.y, y-s.y, y+totalheight+s.y, y+totalheight+s.y]
		device.restoreColor()
		device.restoreLinestyle()
		device.restoreLinewidth()
		device.restoreSymbolSize()
		device.restoreAlpha()
		if self.drawborder:
			device.drawPolyLine(xlist, ylist, close=True, gridsnap=True)
		
		device.popWorld()
		device.popContext()

		
		
class InnerColorbar(PlotObject):
	__fdoc__ = """HIDE"""
	def __init__(self, container, label=None, image=None, levels=[], direction="up", location="right, top", markers=[], markercolor="white",
			labelposition=None, size=None, colormap='rainbow', datamin=None, datamax=None, edgespacing="10mm", **kwargs):
		self.image = image
		self.label = label
		self.levels = levels
		self.direction = direction
		self.location = location
		self.edgespacing = edgespacing
		self.colormap = colormap
		self.datamin = datamin
		self.datamax = datamax
		if image is not None:
			self.colormap = image.colormap
			self.datamin = image.datamin
			self.datamax = image.datamax
		self.markers = markers
		self.markercolor = markercolor
		hloc, vloc = self.location.split(",")
		hloc, vloc = hloc.strip(), vloc.strip()
		
		if labelposition is None:
			if direction in ["up", "down"]:
				if hloc == "left":
					self.labelposition = "right"
				else:
					self.labelposition = "left"
			else:
				if vloc == "bottom":
					self.labelposition = "top"
				else:
					self.labelposition = "bottom"
		else:
			self.labelposition = labelposition
		if size is None:
			if direction in ["right", "left"]:
				self.size = "4cm, 1cm"
			else:
				self.size = "1cm, 4cm"
		else:
			self.size = size
		super(InnerColorbar, self).__init__(container, **kwargs)
	
	def draw(self, device):
		device.pushContext(self.context)
		
		hsize, vsize = self.size.split(",")
		hsize, vsize = hsize.strip(), vsize.strip()
		hsizex = self.getDocument().sizeToViewport(hsize, self.container.borderViewport).x
		vsizey = self.getDocument().sizeToViewport(vsize, self.container.borderViewport).y
		size = kaplot.Vector(hsizex, vsizey)
		
		edgespacing = self.getDocument().sizeToViewport(self.edgespacing, self.container.borderViewport)
		
		hloc, vloc = self.location.split(",")
		hloc, vloc = hloc.strip(), vloc.strip()
		hlocs = {"left":0+edgespacing.x, "center":0.5-size.x/2., "right":1-size.x-edgespacing.x}
		vlocs = {"bottom":0+size.y+edgespacing.y, "center":0.5+size.y/2., "top":1-edgespacing.y}
		if hloc not in hlocs:
			raise Exception, "horizontal location should be 'right', 'left' or 'center', not %r" % hloc
		if vloc not in vlocs:
			raise Exception, "vertical location should be 'top', 'bottom' or 'center', not %r" % hloc
		
		origin = kaplot.Vector(hlocs[hloc], vlocs[vloc])
		
		
		device.pushWorld(((0, 0), (1,1)))
		#print origin
		#print size
		#print edgespacing
		colorbarimage = kaplot.utils.createColorbar(self.direction, 256)
		height, width = colorbarimage.shape
		#viewport = (origin.x, origin.y-size.y), (origin.x+size.y, origin.y)
		#m = kaplot.Matrix.scalebox_inverse(*viewport) * device.getViewportMatrix() 
		#m = device.getViewportMatrix().inverse() * kaplot.Matrix.scalebox_inverse(*viewport)
		#vp = m * (0, 0), m * (1, 1)
		#m = kaplot.Matrix.translate(origin.x, origin.y) * \
		m = kaplot.Matrix.translate(origin.x, origin.y-size.y) *\
			kaplot.Matrix.scale(size.x/width, size.y/height) *\
			kaplot.Matrix.translate(0.5, 0.5)
			# * \
			#kaplot.Matrix.translate(0.5, 0.5)
			#kaplot.Matrix.translate(-0.5, -0.5) *\
		
			
		#print origin.x, origin.y-size.y
		
		
		#print height, width
		#device.pushWorld(((0.5, 0.5), (width+0.5, height+0.5)))
		#device.pushViewport(vp)
		device.drawIndexedImage(colorbarimage, self.colormap, matrix=m)
		
		if self.direction in ["right", "left"]:
			device.pushContext({"color":self.markercolor})
			for marker in self.markers:
				x = (marker - self.datamin) / (self.datamax - self.datamin)
				device.drawLine(origin.x + x*size.x, origin.y, origin.x+x*size.x, origin.y-size.y)
				print "MARKER", marker, self.datamin, self.datamax, x
			device.popContext()
		
		xlist = [origin.x, origin.x + size.x, origin.x + size.x, origin.x]
		ylist = [origin.y, origin.y, origin.y - size.y, origin.y - size.y]
		device.drawPolyLine(xlist, ylist, close=True, gridsnap=True)
		
		#device.popViewport()
		#device.popWorld()
		
		ticksize = "3mm"
		labeloffset = "1mm"
		ticksizevp = self.getDocument().sizeToViewport(ticksize, self.container.borderViewport)
		labeloffsetvp = self.getDocument().sizeToViewport(labeloffset, self.container.borderViewport)
		#dmin = self.image.data2d.min()
		#dmax = self.image.data2d.max()
		#self.levels = [dmin, dmin + (dmax-dmin)/2., dmax]
		levels = numpy.array(self.levels, dtype=float)
		if self.direction in ["right", "left"]:
			if self.labelposition == "top":
				for level in list(levels):
					x = (level - self.datamin) / (self.datamax - self.datamin)
					if x >= 0 and x <= 1:
						nx = origin.x+x*size.x
						if self.direction == "left":
							nx = 1 - nx
						
						device.drawLine(nx, origin.y, nx, origin.y-ticksizevp.y)
						device.drawText("%g" % level, nx, origin.y-max(0, -ticksizevp.y)+labeloffsetvp.y, "center", "bottom")
					if self.label:
						device.drawText(self.label, origin.x + size.x / 2, origin.y-size.y-labeloffsetvp.y, halign="center", valign="top")
			if self.labelposition == "bottom":
				for level in list(levels):
					x = (level - self.datamin) / (self.datamax - self.datamin)
					if x >= 0 and x <= 1:
						nx = origin.x+x*size.x
						if self.direction == "left":
							nx = 1 - nx
						device.drawLine(nx, origin.y-size.y, nx, origin.y+ticksizevp.y-size.y)
						device.drawText("%g" % level, nx, origin.y-size.y+max(0, -ticksizevp.y)-labeloffsetvp.y, "center", "top")
					if self.label:
						device.drawText(self.label, origin.x + size.x / 2, origin.y+labeloffsetvp.y, halign="center", valign="bottom")
		if self.direction in ["up", "down"]:
			if self.labelposition == "left":
				for level in list(levels):
					y = (level - self.datamin) / (self.datamax - self.datamin)
					if y >= 0 and y <= 1:
						ny = origin.y-size.y*(1-y)
						if self.direction == "down":
							ny = 1 - ny
						device.drawLine(origin.x, ny , origin.x+ticksizevp.x, ny)
						device.drawText("%g" % level, origin.x-max(0, -ticksizevp.x)-labeloffsetvp.x, ny, "right", "center")
					if self.label:
						device.drawText(self.label, origin.x + size.x + labeloffsetvp.x, origin.y - size.y / 2, halign="center", valign="bottom", textangle=-numpy.pi/2)
			if self.labelposition == "right":
				for level in list(levels):
					y = (level - self.datamin) / (self.datamax - self.datamin)
					if y >= 0 and y <= 1:
						ny = origin.y-size.y*(1-y)
						if self.direction == "down":
							ny = 1 - ny
						device.drawLine(origin.x+size.x, ny, origin.x+size.x-ticksizevp.x, ny)
						device.drawText("%g" % level, origin.x+size.x+max(0, -ticksizevp.x)+labeloffsetvp.x, ny, "left", "center")
					if self.label:
                                                device.drawText(self.label, origin.x - labeloffsetvp.x, origin.y - size.y / 2, halign="center", valign="bottom", textangle=numpy.pi/2)
		
		device.popWorld()
		
		if False:
			colorbarimage = kaplot.utils.createColorbar(self.direction, 256)
			height, width = colorbarimage.shape
			m = kaplot.Matrix.scalebox_inverse(*viewport) * device.getViewportMatrix() 
			m = device.getViewportMatrix() * kaplot.Matrix.scalebox_inverse(*viewport)
			vp = m * (0, 0), m * (1, 1)
			#device.pushViewport(vp)
	
			
			device.pushWorld(((0.5, 0.5), (width+0.5, height+0.5)))
			device.drawIndexedImage(colorbarimage, self.colormap)
			device.popWorld()
	
			clipping = device.getClipping()
			
			device.setClipping(False)
			device.pushWorld(((0, 0), (1, 1)))
			device.drawPolyLine([0, 1, 1, 0], [0, 0, 1, 1], close=True, gridsnap=True)
	
			ticksize = "3mm"
			ticksizevp = self.getPlot().sizeToViewport(ticksize, viewport)
			labeloffset = "1mm"
			
			labeloffsetvp = self.getPlot().sizeToViewport(labeloffset, viewport)
			ticksizevp = self.getPlot().sizeToViewport(ticksize, viewport)
			
			if self.direction in ["right", "left"]:
				if self.labelposition == "top":
					for level in list(self.levels) + [self.datamin, self.datamax]:
						x = (level - self.datamin) / (self.datamax - self.datamin)
						if x >= 0 and x <= 1:
							device.drawLine(x, 0, x, 1+ticksizevp.y)
							device.drawText("%g" % level, x, 1+ticksizevp.y+labeloffsetvp.y, "center", "bottom")
			elif self.direction in ["down", "up"]:
				if self.labelposition == "left":
					for level in list(self.levels) + [self.datamin, self.datamax]:
						y = (level - self.datamin) / (self.datamax - self.datamin)
						if y >= 0 and y <= 1:
							device.drawLine(-ticksizevp.x, y, 1, y)
							device.drawText("%g" % level, -ticksizevp.x-labeloffsetvp.x, y, "center", "bottom")
	
			
			device.setClipping(clipping)
			
			device.popWorld()
	
			device.popViewport()
		device.popContext()

class Grid(PlotObject):
	__fdoc__ = """Draws a grid on the whole of the container

	Arguments:
	 * subgrid == if True, only draw the gridlines of the minor ticks
	 * xinterval -- if specified, the major tick seperation for the x axis
	 * xinteger -- if True, x will always be an integer, so no floating point strings in your plot
	 * xstart -- if specified, the start value for the major ticks
	 * xsubticks -- the number of subticks (minor ticks) between mayor ticks
	 * xlogarithmic -- if True, the minor subticks will be seperated as on logarithmic paper.
	 		Note that you have to take the logarithm of your data yourself. Also, labels will
	 		be draws as the base (currently only 10 is supported) with the x-value as superscript
	 * yinterval and the rest -- same, but now for y
	 		
	 TODO: example and explain how to do custom labeling and tick locations
	"""
	def __init__(self, container, subgrid=False,
			xinterval=None, xinteger=False, xstart=None, xsubticks=4, xlogarithmic=False,
			yinterval=None, yinteger=False, ystart=None, ysubticks=4, ylogarithmic=False,
			**kwargs):
		super(Grid, self).__init__(container, **kwargs)
		self.subgrid = subgrid
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
		
	def draw(self, device):
		device.pushContext(self.context)
		
		world = self.container.getWorld()
		matrix = kaplot.Matrix.scalebox_inverse(*world)
		p1 = kaplot.Vector(matrix * (0,0))
		p2 = kaplot.Vector(matrix * (1,0))
		p3 = kaplot.Vector(matrix * (0,1))
		p4 = kaplot.Vector(matrix * (1,1))
		plist = [p1, p2, p3, p4]
		x1 = min([p.x for p in plist])
		x2 = max([p.x for p in plist])
		y1 = min([p.y for p in plist])
		y2 = max([p.y for p in plist])
		x, xsub = kaplot.utils.subdivide(x1, x2, subticks=self.xsubticks, interval=self.xinterval,
					start=self.xstart, integer=self.xinteger, logarithmic=self.xlogarithmic)
		y, ysub = kaplot.utils.subdivide(y1, y2, subticks=self.ysubticks, interval=self.yinterval,
					start=self.ystart, integer=self.yinteger, logarithmic=self.ylogarithmic)
		if self.subgrid:
			xlist = xsub
			ylist = ysub
		else:
			xlist = x
			ylist = y
		for x in xlist:
			device.drawLine(x, y1, x, y2, gridsnap=True)
		for y in ylist:
			device.drawLine(x1, y, x2, y, gridsnap=True)
		
		device.popContext()
		

class Pointer(PlotObject):
	def __init__(self, container, x1, y1, x2, y2, text, offset="3mm", halign=None, valign=None, **kwargs):
		self.x1 = x1
		self.y1 = y1
		self.x2 = x2
		self.y2 = y2
		self.text = text
		self.offset = offset
		self.halign = halign
		self.valign = valign
		super(Pointer, self).__init__(container, **kwargs)
		
	def draw(self, device):
		device.pushContext(self.context)
		size, units = kaplot.utils.splitDimension(self.offset)
		dy = self.y2 - self.y1
		dx = self.x2 - self.x1
		dxu, dyu = self.container.worldToSize(dx, dy, units)
		angle = math.atan2(dyu, dxu)
		#print "angle =", math.degrees(angle), dxu, dyu

		if self.halign is None:
			halign = kaplot.utils.getHalign(angle, 0)
		else:
			halign = self.halign
		if self.valign is None:
			valign = kaplot.utils.getValign(angle, 0)
		else:
			valign = self.valign

		#print halign, valign
		device.drawLine(self.x1, self.y1, self.x2, self.y2)
		d = kaplot.Vector(dxu, dyu)
		d = d.scale(size/d.length, size/d.length)
		#s = 1./d.length * size
		#print d, d.length, size
		#offset = kaplot.Matrix.scalebox_inverse(*self.container.getWorld()).no_translation() * d.scale(size, size)
		offsetx = self.container.sizeToWorld("%f%s" % (d.x, units)).x
		offsety = self.container.sizeToWorld("%f%s" % (d.y, units)).y
		#print "--", self.x2, self.y2
		#print "offset", offsetx, offsety
		device.drawText(self.text, self.x2 + offsetx, self.y2 + offsety, halign, valign)
		device.popContext()
