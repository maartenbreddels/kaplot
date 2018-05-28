# -*- coding: utf-8 -*-
import kaplot
import kaplot.objects
import kaplot.utils
import kaplot.text

class DeviceBase(object):
	def __init__(self):
		self.contextList = [kaplot.defaultContext.clone()]
		self.worldList = [((0, 0), (0.100, 0.100))]
		#self.worldList = [((0, 0), (3, 3))]
		#self.worldList = [((10, 10), (0, 0))]
		self.viewportList = [((0.2, 0.1), (0.7, 0.9))]
		#self.viewportList = [((0.0, 0.0), (1.0, 1.0))]

		self._glyphCache = {}
		self._glyphNr = 1
		self._clipping = True
		self._color = kaplot.utils.getColor("red")
		#self._fontsize = "10mm"
		self._fontname = "Verdana"
		#self._symbolsize = "5mm"
		
		#self.dpi = 72
		self._alpha = 1
		
	def preDraw(self, document):
		pass

	def postDraw(self, document):
		pass

	def preDrawPage(self, document, page):
		self.setClipRegion()
		self.dpi = document.dpi
		self.pushContext(self.contextList[0])
	
	def postDrawPage(self, document, page):
		#print len(self.contextList)
		#print len(self.worldList)
		#print len(self.viewportList)
		pass

	###########  CONTEXT  #######################		
	def setColor(self, color):
		self._color = kaplot.utils.decodeColor(kaplot.utils.getColor(color))
		self._setColor()
		
	def getColor(self):
		return self._color
		
	def _setColor(self):
		kaplot.info("color not implementen on device", printonce=True)
		
	def setAlpha(self, alpha):
		self._alpha = alpha
		self._setAlpha()
		
	def getAlpha(self):
		return self._alpha
		
	def _setAlpha(self):
		kaplot.info("alpha not implementen on device", printonce=True)
		
	def setLinewidth(self, linewidth):
		self._linewidth = linewidth
		self._setLinewidth()

	def getLinewidth(self):
		return self._linewidth
		
	def _setLinewidth(self):
		kaplot.info("linewidth not implementen on device", printonce=True)
		
	def setLinestyle(self, linestyle):
		self._linestyle = kaplot.utils.getLinestyle(linestyle)
		self._setLinestyle()

	def getLinestyle(self):
		return self._linestyle
		
	def _setLinestyle(self):
		kaplot.info("linestyle not implementen on device", printonce=True)
		
	def setPatternSize(self, patternsize):
		self._patternsize = patternsize
		self._setPatternSize()

	def getPatternSize(self):
		return self._fillstyle
		
	def _setPatternSize(self):
		kaplot.info("patternsize not implementen on device", printonce=True)
		
	def setSymbolSize(self, symbolsize):
		self._symbolsize = symbolsize
		self._setSymbolSize()

	def getSymbolSize(self):
		return self._symbolsize
		
	def _setSymbolSize(self):
		kaplot.info("symbolsize not implementen on device", printonce=True)
		
	def setFillstyle(self, fillstyle):
		self._fillstyle = fillstyle
		self._setFillstyle()

	def getFillstyle(self):
		return self._fillstyle
		
	def _setFillstyle(self):
		kaplot.info("fillstyle not implementen on device", printonce=True)
		
	def setFontname(self, fontname):
		self._fontname = fontname
		self._setFontname()

	def getFontname(self):
		return self._fontname
		
	def _setFontname(self):
		kaplot.info("fontname not implementen on device", printonce=True)
		
	def setFontsize(self, fontsize):
		self._fontsize = fontsize
		self._setFontsize()

	def getFontsize(self):
		return self._fontsize
		
	def _setFontsize(self):
		kaplot.info("fontsize not implementen on device", printonce=True)
		
	def setClipping(self, clipping):
		self._clipping = clipping
		self._setClipping(clipping)
		
	def getClipping(self):
		return self._clipping
		
	def _setClipping(self, clipping):
		kaplot.info("clipping not implementen on device", printonce=True)
		
	def restoreColor(self):
		self.setColor(self._findInContextStack("color"))
		
	def restoreAlpha(self):
		self.setAlpha(self._findInContextStack("alpha"))
		
	def restoreLinewidth(self):
		self.setLinewidth(self._findInContextStack("linewidth"))
		
	def restoreLinestyle(self):
		self.setLinestyle(self._findInContextStack("linestyle"))

	def restorePatternSize(self):
		self.setPatternSize(self._findInContextStack("patternsize"))
		
	def restoreSymbolSize(self):
		self.setSymbolSize(self._findInContextStack("symbolsize"))
		
	def restoreFillstyle(self):
		self.setFillstyle(self._findInContextStack("fillstyle"))
		
	def restoreFontname(self):
		self.setFontname(self._findInContextStack("fontname"))
		
	def restoreFontsize(self):
		self.setFontsize(self._findInContextStack("fontsize"))
		
	def _findInContextStack(self, name):
		for context in self.contextList[::-1]:
			if hasattr(context, name):
				return getattr(context, name)
		raise Exception, "attribute '%s' not found in context stack" % name

	def pushContext(self, context):
		context = kaplot.Context(context)
		self.contextList.append(context)
		if "color" in context:
			self.setColor(context.color)
		if "alpha" in context:
			self.setAlpha(context.alpha)
		if "linewidth" in context:
			self.setLinewidth(context.linewidth)
		if "linestyle" in context:
			self.setLinestyle(context.linestyle)
		if "patternsize" in context:
			self.setPatternSize(context.patternsize)
		if "symbolsize" in context:
			self.setSymbolSize(context.symbolsize)
		if "fillstyle" in context:
			self.setFillstyle(context.fillstyle)
		if "fontname" in context:
			self.setFontname(context.fontname)
		if "fontsize" in context:
			self.setFontsize(context.fontsize)
		
	def popContext(self):
		context = self.contextList.pop()
		if "color" in context:
			self.restoreColor()
		if "alpha" in context:
			self.restoreAlpha()
		if "linewidth" in context:
			self.restoreLinewidth()
		if "linestyle" in context:
			self.restoreLinestyle()
		if "patternsize" in context:
			self.restorePatternSize()
		if "symbolsize" in context:
			self.restoreSymbolSize()
		if "fillstyle" in context:
			self.restoreFillstyle()
		if "fontname" in context:
			self.restoreFontname()
		if "fontsize" in context:
			self.restoreFontsize()
		#if hasattr(context, "viewport"):
		#	self.popViewport()
			
	############## COORDINATES ########################
	def pushWorld(self, world):
		self.worldList.append(world)
		
	def popWorld(self):
		self.worldList.pop()
		
	def getWorld(self):
		#(x1, y1), (x2, y2) = self.worldList[-1]
		#return (float(x1), float(y1)), (float(x2), float(y2))
		return self.worldList[-1]
		
	def getWorldMatrix(self):
		p1, p2 = self.worldList[-1]
		#return kaplot.Matrix.scalebox(p1, p2) 
		(x1, y1), (x2, y2) = self.worldList[-1]
		width = x2 - x1
		height = y2 - y1
		sx = 1.0 / width
		sy = 1.0 / height
		tx = -x1 / float(width)
		ty = -y1 / float(height)
		mat = kaplot.Matrix(sx, sy, tx, ty)
		return mat
		
	def pushViewport(self, viewport):
		if viewport is None:
			raise Exception, "viewport can't be None"
		self.viewportList.append(viewport)
		
	def popViewport(self):
		self.viewportList.pop()
		
	def getViewport(self):
		return self.viewportList[-1]

	def getViewportMatrix(self):
		p1, p2 = self.viewportList[-1]
		return kaplot.Matrix.scalebox_inverse(p1, p2)
		(x1, y1), (x2, y2) = self.viewportList[-1]
		width = x2 - x1
		height = y2 - y1
		sx = width
		sy = height
		tx = x1
		ty = y1
		return kaplot.Matrix(sx, sy, tx, ty)
		
	def getDeviceMatrix(self):
		return kaplot.Matrix.scale(self.width-1, self.height-1)

	###### TEXT #######

	def drawText__(self, text, position, halign, valign, textangle):
		fontname = self._fontname
		#fontname = "verdana"
		font = kaplot.textmod.findFont(fontname, False, False)
		#fontsizepixels = self._convertUnits(self.fontsize, "px")
		#fontsize = int(fontsizepixels * 96)
		#x, y = self._getTotalMatrix() * position
		#font.set_char_size(0, int(fontsize))
		x, y = position
		#matrix = (	self.getDeviceMatrix() * \
		#			self.getViewportMatrix()\
		#		)
		#x, y = matrix * position
		fontsize = self._fontsize
		#print self._fontsize, self.dpi
		dpi = self.dpi
		#print fontsize, textangle
		try:
			textObject = kaplot.textmod.parseText(text, font, fontsize, fontname, dpi)
		except:
			kaplot.info("failed to parse text: %r" % text)
			raise
		#color = self._findInContextStack("color")
		#color = "red"
		#print "textangle =",textangle
		color = self._color
		textObject.draw(self.getCInterface(), x, y, textangle, valign, halign, color, self)
		points = textObject.getBBoxTransformed(x, y, textangle, valign, halign)
		#matrix = (	self.getDeviceMatrix() * \
		#			self.getViewportMatrix()\
		#		).inverse()
		#points = [matrix * k for k in points]
		#self.plotBbox(color="black", *points)


	def drawGlyph(self, char, textState, font, ftmatrix, drawCallable):
		key = (char, textState.fontSizePt, font)
		a, b, c, d, tx, ty = ftmatrix
		
		#print "drawGlyph", ftmatrix

		# it's assumed that cached glyphs have unrotated dx, dy's
		rotated = True

		if not key in self._glyphCache:
			# we first create a unrotated, untranslated glyph, so it's
			# easier to reuse
			glyphName = "gl%i" % self._glyphNr
			self._glyphNr += 1

			dx, dy, cached, = self.outputGlyph(glyphName, textState, font, ftmatrix, drawCallable)
			if cached:
				self._glyphCache[key] = (glyphName, dx, dy)
				rotated = False
		else:
			glyphName, dx, dy = self._glyphCache[key]
			rotated = False

		scale16 = 1.0/(1<<16)
		scale6 = 1.0/(1<<6)

		# draw this glyph
		self.currentChar = char
		self.drawCachedGlyph(glyphName, textState, font, ftmatrix)

		# these cached values were unrotated, so rotate it
		if not rotated:
			#print "matrix"
			matrix = kaplot.matrix.Matrix(a*scale16, d*scale16)
			matrix.xx = a*scale16
			matrix.xy = b*scale16
			matrix.yx = c*scale16
			matrix.yy = d*scale16
			#matrix.tx = tx*scale6
			#matrix.ty = tx*scale6
			#print a*scale16,b*scale16,c*scale16,d*scale16,tx*scale6,ty*scale6
			#print matrix
			#print dx, dy
			dx, dy = matrix * (dx, dy)
			#print dx, dy
		return int(dx), int(dy)

	def getTextBbox(self, text, x, y, halign, valign, textangle=0):
		fontname = self._fontname
		font = kaplot.textmod.findFont(fontname, False, False)
		#fontsizepixels = self._convertUnits(self.fontsize, "px")
		#fontsize = int(fontsizepixels * 96)
		#font.set_char_size(0, int(fontsize))
		#worldmatrix = self.getWorldMatrix()
		#print worldmatrix
		worldmatrix = self.getWorldMatrix()
		matrix = (	self.getDeviceMatrix() * \
					self.getViewportMatrix() *\
					worldmatrix
				)
		x, y = matrix * (x, y)
		#x, y = position
		try:
			textObject = kaplot.textmod.parseText(text, font, self._fontsize, fontname, self.dpi)
		except:
			kaplot.info("failed to parse text: %r" % text)
			raise
		#x, y = 0, 0
		points = textObject.getBBoxTransformed(x, y, textangle, valign, halign)
		matrix = (	self.getDeviceMatrix() * \
					self.getViewportMatrix() *\
					worldmatrix
				).inverse()
		vppoints = [matrix * k for k in points]
		#if self.debug:
		#self.plotBbox(*vppoints)
		#print points
		#import pdb
		#pdb.set_trace()
		return vppoints

	def drawLines(self, x1, y1, x2, y2, gridsnap=False):
		for x1_, y1_, x2_, y2_ in zip(x1, y1, x2, y2):
			self.drawLine(x1_, y1_, x2_, y2_, gridsnap=gridsnap)

	########### SYMBOL ################
	
	def drawSymbol(self, x, y, symbolName, xscales=None, yscales=None, angles=None, colors=None, colormap=None):
		if ":" in symbolName:
			_group, name = symbolName.split(":", 1)
			# TODO, entity -> unicode
			character = unicode(name)
			if len(character) != 1:
				raise ValueError, "a character symbol can only be of length 1"
			self._drawCharacterSymbol(x, y, character)
		else:
			if symbolName in kaplot.markers.symbols:
				self._drawSymbol(x, y, symbolName, xscales, yscales, angles, colors, colormap)
			else:
				raise ValueError, "unknown symbol: %r, choose between %r" % (symbolName, kaplot.markers.symbols.keys())

	def _drawSymbol(self, x, y, symbolName, xscales, yscales, angles):
		kaplot.info("plotting symbols not implemented")

	def getWindow(self):
		return None
		
	def isGuiDevice(self):
		return self.getWindow() is not None
		
	def checkWindow(self):
		pass