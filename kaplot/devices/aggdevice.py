# -*- coding: utf-8 -*-
import numpy
import PIL.Image
import math
import kaplot
from kaplot.devices.devicebase import DeviceBase
from kaplot.cext._agg import Agg
from kaplot.cext._image import Image

class AggDeviceBase(DeviceBase):
	def __init__(self, filename="kaplot.png"):
		super(AggDeviceBase, self).__init__()
		self.filename = filename
		
	def preDraw(self, document):
		self.width, self.height = document.pixelWidth, document.pixelHeight
		self.agg = Agg(self.width, self.height)
		#if self.paperColor == None:
		self.agg.clear(1,1,1,1)
		#else:
			#color = kaplot.utils.getColor(self.paperColor)
			#r, g, b = color.getRGB()
		#	r, g, b = 1, 0, 0
		#	self.agg.clear(r, g, b, 1)
		self.image = Image(self.width, self.height, self.agg.buffer)
		super(AggDeviceBase, self).preDraw(document)

	#def postDrawPage(self, document, page):
	#	super(AggDeviceBase, self).postDrawPage(document, page)
		#pagefilename = kaplot.utils.getPageFilename(self.filename, self.getCurrentPageNr(), self.getPageCount())
		#pagefilename = self.filename
		#data = self.image.get_argb_string()
		#image = PIL.Image.fromstring("RGBA", (document.pixelWidth, document.pixelHeight), data)
		
	def pushViewport(self, world):
		super(AggDeviceBase, self).pushViewport(world)
		self.setClipRegion()
		

	def _setColor(self):
		r, g, b = self._color.getRGB()
		self.agg.set_color(r, g, b)

	def _setAlpha(self):
		self.agg.set_alpha(self._alpha)

	def _setLinewidth(self):
		linewidth, units = kaplot.utils.splitDimension(self._linewidth)
		linewidthpx = kaplot.utils.convertToPixels(linewidth, units, dpi=self.dpi)
		self.agg.set_linewidth(linewidthpx)

	def _setLinestyle(self):
		linewidth, units = kaplot.utils.splitDimension(self._linewidth)
		linewidthpx = kaplot.utils.convertToPixels(linewidth, units, dpi=self.dpi)

		dasharray = self._linestyle
		dasharray = [k*linewidthpx for k in dasharray]
		self.agg.set_linedash(dasharray)

	def _setPatternSize(self):
		pass

	def _setSymbolSize(self):
		pass

	def _setFillstyle(self):
		self._setAggFillstyle()

	def _setFontname(self):
		pass

	def _setFontsize(self):
		pass

	def _setClipping(self, clipping):
		self._clipping = clipping
		self.setClipRegion()
	
	def setClipRegion(self):
		if self._clipping:
			matrix = self.getDeviceMatrix() * self.getViewportMatrix()
		else:
			matrix = self.getDeviceMatrix()
		p0 = matrix * (0, 0)
		p1 = matrix * (0, 1)# + (1, 0)
		p2 = matrix * (1, 1)# + (1, 1)
		p3 = matrix * (1, 0)# + (0, 1)
		self._setIdentityMatrix()
		#print p0, p3
		self.agg.clip(p0, p1, p2, p3)

	def _getMatrixParams(self, matrix=None):
		if matrix is None:
			matrix = kaplot.Matrix()
		m = self.getDeviceMatrix() * self.getViewportMatrix() * self.getWorldMatrix() * matrix
		return m.xx, m.yy, m.tx, m.ty
		m = m.matrix
		return m[0][0], m[1][1], m[0][2], m[1][2]
		
		(vx1, vy1), (vx2, vy2) = self.viewportList[-1]
		vwidth = vx2 - vx1
		vheight = vy2 - vy1
		(x1, y1), (x2, y2) = self.worldList[-1]
		width = x2 - x1
		height = y2 - y1
		sx = 1.0 / width * self.width * vwidth
		sy = 1.0 / height * self.height * vheight
		tx = (x1 / width + vx1)* self.width
		ty = (y1 / height + vy1) * self.height
		return sx, sy, tx, ty
		
	def _setMatrix(self):
		sx, sy, tx, ty = self._getMatrixParams()
		self.agg.set_matrix(sx, 0, 0, sy, tx, ty)
		
	def _setIdentityMatrix(self):
		sx, sy, tx, ty = 1, 1, 0, 0
		self.agg.set_matrix(sx, 0, 0, sy, tx, ty)
		
		
		
	def close(self):
		pass

	def drawText(self, text, x, y, halign="center", valign="center", textangle=0):
		if len(text) == 0:
			return
		# we don't wanna draw text with a pattern
		#self.agg.clear_pattern()
		worldmatrix = self.getWorldMatrix()
		viewportmatrix = self.getViewportMatrix()
		#devicematrix = Matrix.scaleXY(self.pixelWidth, self.pixelHeight)
		#devicematrix = kaplot.Matrix()
		devicematrix = self.getDeviceMatrix()
		matrix = devicematrix * (viewportmatrix * worldmatrix)
		position = matrix * (x, y)
		#self._setAggMatrix(kaplot.Matrix())
		self._setIdentityMatrix()
		self.drawText__(text, position, halign, valign, textangle)
		#self._setAggMatrix()
		# restore pattern
		#if self._currentPattern:
		#	self.agg.set_pattern(self._currentPattern)

	def outputGlyph(self, glyphName, textState, font, ftmatrix, drawCallable):
		dx, dy = drawCallable(font, *ftmatrix)
		self._setIdentityMatrix()
		color = self.getColor()
		self.setColor(textState.color)
		#print "outputGlyph", ftmatrix
		#self._setColor()
		#r, g, b = color.getRGB()
		#r, g, b = 0, 0, 1
		#self.agg.set_color(r, g, b)
		self.agg.fill();
		#self.restoreColor()
		self.setColor(color)
		return dx, dy, False

	def drawCachedGlyph(self, glyphName, textState, font, ftmatrix):
		# glyph caching not needed
		pass


	def getCInterface(self):
		sx, sy, tx, ty = self._getMatrixParams()
		self.agg.set_matrix(sx, 0, 0, sy, tx, ty)
		return self.agg.cinterface
		
	def _setAggFillstyle(self):
		fillstyle = self._fillstyle
		if fillstyle == "fill":
			self.agg.clear_pattern()
			return
		elif fillstyle not in kaplot.patterns:
			raise ValueError, "unknown fillstyle %r" % fillstyle

		pattern = kaplot.patterns[fillstyle]

		patternSize = self._patternsize
		patternSize, patternUnits = kaplot.utils.splitDimension(patternSize)
		patternSizePixels = kaplot.utils.convertToPixels(patternSize, patternUnits, dpi=self.dpi)
		width, height = int(patternSizePixels+0.5), int(patternSizePixels+0.5)
		patternsurface = Agg(width, height)
		patternsurface.clear(0,0,0,0)
		r, g, b = self._color.getRGB()
		patternsurface.set_color(r, g, b)
		for part in range(pattern.parts):
			xlistlist, ylistlist = pattern.getXY(part)
			for xlist, ylist in zip(xlistlist, ylistlist):
				patternsurface.move_to(xlist[0]*width, ylist[0]*height)
				for xvalue, yvalue in zip(xlist[1:], ylist[1:]):
					patternsurface.line_to(xvalue*width, yvalue*height)
				if pattern.solid:
					patternsurface.fill()
				else:
					patternsurface.stroke()

		#matrix = kaplot.Matrix.rotate(pattern.angle)
		matrix = kaplot.Matrix()
		#self._setAggSurfaceMatrix(patternsurface, matrix)
		#kaplot.Matrix.rotate(pattern.angle)
		#Matrix(numpy.array([[, ,0],[, ,0], [0,0,1]], numpy.Float))
		#sx, sy, tx, ty = matrix.xx, matrix.yy, matrix.tx, matrix.ty
		angle = pattern.angle
		
		patternsurface.set_matrix(math.cos(angle), -math.sin(angle), math.sin(angle), math.cos(angle), 0, 0)
		self._currentPattern = patternsurface
		self.agg.set_pattern(self._currentPattern)
		


	########### PLOTTING ################

	def _drawSymbol(self, x, y, symbolName, xscales, yscales, angles, colors=None, colormap=None):
		self.setClipRegion()
		#print "C", self._color
		self._setColor()
		#kaplot.debug("begin plotting symbol:", symbolName)
		#print self._symbolsize
		symbolSize = self._symbolsize
		symbolSize, symbolUnits = kaplot.utils.splitDimension(symbolSize)
		symbolSizePixels = kaplot.utils.convertToPixels(symbolSize, symbolUnits, dpi=self.dpi)
		#width, height = int(symbolSizePixels+0.5), int(symbolSizePixels+0.5)
		width, height = float(symbolSizePixels), float(symbolSizePixels)
		#symbolsurface = Agg(width, height)
		#symbolsurface.clear(0,0,0,0)
		#r, g, b = self._color.getRGB()
		#symbolsurface.set_color(r, g, b)
		#symbolsurface.set_alpha(self._alpha)
		#self.agg.set_dash([], 0)
		symbol = kaplot.markers.symbols[symbolName]

		#xlist, ylist = symbol.getXY()
		#symbolsurface.move_to(xlist[0]*width, ylist[0]*height)
		#for xvalue, yvalue in zip(xlist[1:], ylist[1:]):
		#	symbolsurface.line_to(xvalue*width, yvalue*height)
		#print width, height, "DDSADSA"
		for part in xrange(symbol.parts):
			xlist, ylist = symbol.getXY(part)
			#print xlist, ylist
			self.agg.move_to(xlist[0]*(width-1), ylist[0]*(height-1))
			for xvalue, yvalue in zip(xlist[1:], ylist[1:]):
				self.agg.line_to(xvalue*(width-1), yvalue*(height-1))

		#if symbol.solid:
		#	symbolsurface.fill()
		#else:
		#	symbolsurface.stroke()

		#self._setAggMatrix(kaplot.Matrix())
		self._setIdentityMatrix()
		#xlist, ylist = (self._getTotalMatrix()).mulXY(x, y)
		sx, sy, tx, ty = self._getMatrixParams()
		xlist = numpy.array(x) * sx + tx - width/2
		ylist = numpy.array(y) * sy + ty - height/2
		
		#xlist, ylist = (kaplot.Matrix.translate((-width/2,-height/2)) *self._getTotalMatrix()).mulXY(x, y)
		# normalize 
		#if colors is not None:
		#	colors = numpy.array(colors)
		#	delta = colors.max() - colors.min()
		#	if delta == 0:
		#		delta = 1
		#	colors = (colors - colors.min()) / delta
		if colormap:
			colormap = kaplot.utils.getColormap(colormap)
		#colormap(1)
			def colormapproxy(value):
				color = colormap(value)
				return color.r, color.g, color.b
				#pass
		else:
			colormapproxy = None

		if symbol.solid:
			self.agg.fill_repeat(xlist, ylist, xscales, yscales, angles, colors, colormapproxy)
		else:
			self.agg.stroke_repeat(xlist, ylist, xscales, yscales, angles)
		
		#for x, y in zip(xlist, ylist):
			#self._setAggMatrix(kaplot.Matrix.translate((x-width/2,y-height/2)))
		#	self.agg.set_matrix(1, 0, 0,1, x-width/2, y-height/2)
		#	self.agg.draw_agg(symbolsurface, True)
		#self._setAggMatrix()
		#kaplot.debug("end plotting symbol:", symbolName, len(xlist), "times")

	def drawLine(self, x1, y1, x2, y2, gridsnap=False):
		#r, g, b = 0, 0, 0
		#self._setMatrix()
		#self.agg.set_color(r, g, b)
		self._setIdentityMatrix()
		self.setClipRegion()
		if gridsnap or True:
			self._setIdentityMatrix()
			sx, sy, tx, ty = self._getMatrixParams()
			x1 = int(x1 * sx + tx + 0.5) + 0.5
			y1 = int(y1 * sy + ty + 0.5) + 0.5
			x2 = int(x2 * sx + tx + 0.5) + 0.5
			y2 = int(y2 * sy + ty + 0.5) + 0.5
			self.agg.polyline([x1, x2], [y1, y2])
		else:
			self._setMatrix()
			self.agg.polyline([x1, x2], [y1, y2])
		self.agg.stroke()
		
	def drawPolyLine(self, xlist, ylist, gridsnap=False, close=False):
		#r, g, b = 0, 0, 0
		#self.agg.set_color(r, g, b)
		self._setIdentityMatrix()
		self.setClipRegion()
		if gridsnap:
			self._setIdentityMatrix()
			sx, sy, tx, ty = self._getMatrixParams()
			xlist = numpy.array(xlist) * sx + tx + 0.5
			ylist = numpy.array(ylist) * sy + ty + 0.5
			self.agg.polyline(xlist.astype(numpy.int) + 0.5, ylist.astype(numpy.int) + 0.5)
		else:
			self._setMatrix()
			self.agg.polyline(xlist, ylist)
		if close:
			self.agg.close()
		self.agg.stroke()
		
	def drawPolygon(self, xlist, ylist, gridsnap=False):
		self._setIdentityMatrix()
		self.setClipRegion()
		if gridsnap:
			self._setIdentityMatrix()
			sx, sy, tx, ty = self._getMatrixParams()
			xlist = numpy.array(xlist) * sx + tx + 0.5
			ylist = numpy.array(ylist) * sy + ty + 0.5
			self.agg.polyline(xlist.astype(numpy.int) + 0.5, ylist.astype(numpy.int) + 0.5)
		else:
			self._setMatrix()
			self.agg.polyline(xlist, ylist)
		self.agg.fill()
		
	def _drawRbgData(self, datastring, width, height):
		self.agg.draw_rgba_image(datastring, width, height)

	def drawIndexedImage(self, data2d, colormap, function="linear", mask2d=None, matrix=None, datamin=None, datamax=None):
		if matrix is None:
			matrix = kaplot.Matrix()
		#self._setMatrix()
		#self.agg.set_matrix(2, 0, 0, 2, tx, ty)
		#self._setIdentityMatrix()
		colormap = kaplot.utils.getColormap(colormap)
		function = kaplot.utils.getFunction(function)
		data2d = numpy.array(data2d, numpy.float)
		if datamin == None:
			datamin = data2d.min()
		if datamax == None:
			datamax = data2d.max()
		scale = 255.0 / (datamax - datamin)
		data2d = ((data2d - datamin) * scale)
		data2d = numpy.clip(data2d, 0, 255)
		height, width = data2d.shape
		
		if matrix is None:
			matrix = kaplot.Matrix()
		#m = self.getDeviceMatrix() * self.getViewportMatrix() * self.getWorldMatrix() *\
		#		kaplot.Matrix.translate(0.5, 0.5) * \
		#		matrix * kaplot.Matrix.translate(-0.5, -0.5)
		m = self.getDeviceMatrix() * self.getViewportMatrix() * self.getWorldMatrix() *\
				matrix *\
				kaplot.Matrix.translate(-1.0, -1.0)
				#kaplot.Matrix.translate(-1.0, -1.0)
				#kaplot.Matrix.translate(0.5, 0.5) * \
				#matrix * kaplot.Matrix.translate(-0.5, -0.5)
		sx, sy, tx, ty  = m.xx, m.yy, m.tx, m.ty

		#sx, sy, tx, ty = self._getMatrixParams(matrix * )
		tx += 0.5
		ty += 0.5
		#print sx, sy, tx, ty
		# fixme, center small images
		dx = 0
		dy = 0
		self.agg.set_matrix(sx, 0, 0, sy, tx-dx, ty-dy)
		#print data2d.min(), data2d.max()
		#print data2d[0][0]

		palette = numpy.zeros((768,), numpy.int8)
		for i in range(0, 256):
			index = function(i/255.0)
			r, g, b = colormap(index).getRGB()
			palette[i*3+0] = r * 255
			palette[i*3+1] = g * 255
			palette[i*3+2] = b * 255


		pilIndexedImage = PIL.Image.fromstring("P", (width,height), data2d.astype(numpy.uint8).tostring())
		pilIndexedImage.putpalette(palette.tostring())
		#pilIndexedImage.show()
		if mask2d != None:
			alpha = self._alpha * 0xff
			mask2d = numpy.where(mask2d >= 1, alpha, 0).astype(numpy.int8)
			maskdata = mask2d.astype(numpy.int8).tostring()
			maskImage = PIL.Image.fromstring("L", (width, height), maskdata)
			pilRgbImage = pilIndexedImage.convert("RGBA")
			pilRgbImage.putalpha(maskImage)
		#elif self._alpha < 1:
		#	#alpha = self._alpha * 0xff
		#	#mask2d = numpy.where(mask2d >= 1, alpha, 0).astype(numpy.int8)
		#	alphadata = ((numpy.zeros((width,height)) + self._alpha)*255).astype(numpy.int8).tostring()
		#	alphaImage = PIL.Image.fromstring("L", (width, height), alphadata)
		#	pilRgbImage = pilIndexedImage.convert("RGBA")
		#	pilRgbImage.putalpha(alphaImage)
		else:
			pilRgbImage = pilIndexedImage.convert("RGBA")
		#pilRgbImage.show()
		datastring = pilRgbImage.tostring()
		self._drawRbgData(datastring, width, height)
		

class AggDeviceWindow(AggDeviceBase):
	def __init__(self, window):
		super(AggDeviceWindow, self).__init__()
		self.window = window
		
	def checkWindow(self):
		#if not self.window.isValid():
		#	self.window = self.window.clone()
		pass

	def preDraw(self, document):
		super(AggDeviceWindow, self).preDraw(document)
		#self.image = Image(self.width, self.height, self.agg.buffer)
		self.window.setImage(self.image)
		self.window.setDocument(document, self)

	def postDraw(self, document):
		super(AggDeviceWindow, self).postDraw(document)
		kaplot.debug("agg post draw")
		self.window.updateImage()

	#def draw(self, document):
	#	super(AggDeviceWindow, self).draw(document)
		
	def getWindow(self):
		return self.window
		
	def close(self):
		self.window.mainloop()

class AggDeviceImage(AggDeviceBase):
	def __init__(self, filename="kaplot.png"):
		super(AggDeviceImage, self).__init__()
		self.filename = filename
		
	def postDrawPage(self, document, page):
		super(AggDeviceImage, self).postDrawPage(document, page)
		pagefilename = kaplot.utils.getPageFilename(self.filename, page.getPageNr(), document.getPageCount())
		kaplot.info("writing page to filename", pagefilename)
		data = self.image.get_argb_string()
		image = PIL.Image.frombytes("RGBA", (document.pixelWidth, document.pixelHeight), data)
		image.save(pagefilename)
