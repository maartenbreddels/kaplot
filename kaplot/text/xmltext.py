import xml.sax
import xml.dom.pulldom
from cStringIO import StringIO
import htmlentitydefs
import re
import kaplot.matrix
import math
from kaplot.cext._pyfont import *
from kaplot.text.fonts import findFont, findMatchingFontFamilies
#import cairo subsupscale = 0.5

def _fromMatrix(matrix):
	a = int(matrix[0][0] * (1<<16))
	b = int(matrix[0][1] * (1<<16))
	c = int(matrix[1][0] * (1<<16))
	d = int(matrix[1][1] * (1<<16))
	tx = int(matrix[0][2] * (1<<6))
	ty = int(matrix[1][2] * (1<<6))
	return a, b, c, d, tx, ty

def _fromMatrix(matrix):
	a = int(matrix.xx * (1<<16))
	b = int(matrix.xy * (1<<16))
	c = int(matrix.yx * (1<<16))
	d = int(matrix.yy * (1<<16))
	tx = int(matrix.tx * (1<<6))
	ty = int(matrix.ty * (1<<6))
	return a, b, c, d, tx, ty


class TextPartBase(object):
	def _getTextParts(self):
		raise Exception, "abstract"

	def getBBox(self, relx=0, rely=0):
		parts = self._getTextParts()
		if parts:
			bboxes = [line.getBBox(relx, rely) for line in parts]
			x1 = min([bbox[0][0] for bbox in bboxes])
			y1 = min([bbox[0][1] for bbox in bboxes])
			x2 = max([bbox[2][0] for bbox in bboxes])
			y2 = max([bbox[2][1] for bbox in bboxes])
			newbbox = ((x1, y1), (x2, y2))
			return (x1, y1), (x2, y1), (x2, y2), (x1, y2)
		else:
			return (relx, rely), (relx, rely), (relx, rely), (relx, rely)

	def getBBoxTransformed(self, x, y, angle, valign, halign):
		parts = self._getTextParts()
		if len(parts) > 0:
			p1, p2, p3, p4 = self.getBBox()
			x0 = p1[0]
			y0 = p1[1]
			width = p2[0] - p1[0]
			height = p4[1] - p1[1]

			if halign == "left":
				xa = - x0
			elif halign in ["middle", "center"]:
				xa = - x0 - width/2
			elif halign == "right":
				xa = - x0 - width
			else:
				raise Exception, "unknown halign: %r" % halign

			if valign == "bottom":
				ya = -y0
			elif valign in ["middle", "center"]:
				ya = -y0 - height/2
			elif valign == "top":
				ya = -y0 - height
			else:
				raise Exception, "unknown valign: %r" % valign

			matrix =	kaplot.Matrix.translate((x, y)) *\
						kaplot.Matrix.rotate(angle) * \
						kaplot.Matrix.translate((xa, ya))
			matrix = matrix
			points = self.getBBox()
			points = [matrix*k for k in points]
			return points

	def getLineMetrics(self, relx=0, rely=0):
		metrics = [k.getLineMetrics(relx, rely) for k in self.parts]
		height = max([k[0] for k in metrics])
		ascender = max([k[1] for k in metrics])
		descender = min([k[2] for k in metrics])
		line_gap = max([k[3] for k in metrics])
		return height, ascender, descender, line_gap

	def getMetrics(self):
		metrics = [k.getMetrics() for k in self.parts]
		height = max([k[0] for k in metrics])
		ascender = max([k[1] for k in metrics])
		descender = min([k[2] for k in metrics])
		line_gap = max([k[3] for k in metrics])
		return height, ascender, descender, line_gap

	def setLinePos(self, x, y):
		self.linex = x
		self.liney = y
		for part in self.parts:
			part.setLinePos(x, y)

	def translate(self, x, y):
		self.x += x
		self.y += y
		for part in self.parts:
			part.translate(x, y)

	def scale(self, x, y):
		for part in self.parts:
			part.scale(x, y)


class Text(TextPartBase):
	def __init__(self):
		self.lines = []
		self.justify = "left"

	def getLine(self):
		return self.lines[-1]

	def addLine(self, textState):
		self.lines.append(Line(textState))

	def draw(self, cinterface, x, y, angle, valign, halign, defaultcolor, device):
		if len(self.lines) > 0:
			p1, p2, p3, p4 = self.getBBox()
			x0 = p1[0]
			y0 = p1[1]
			width = p2[0] - p1[0]
			height = p4[1] - p1[1]

			if halign == "left":
				xanchor = - x0
			elif halign in ["middle", "center"]:
				xanchor = - x0 - width/2
			elif halign == "right":
				xanchor = - x0 - width
			else:
				raise Exception, "unknown halign: %r" % halign

			if valign == "bottom":
				yanchor = -y0
			elif valign in ["middle", "center"]:
				yanchor = -y0 - height/2
			elif valign == "top":
				yanchor = -y0 - height
			else:
				raise Exception, "unknown valign: %r" % valign

			justify = self.justify

			for line in self.lines:
				line.draw(cinterface, x, y, xanchor, yanchor, justify, width, angle, valign, halign, defaultcolor, device)


	def _getTextParts(self):
		return [line for line in self.lines if not line.isEmpty()]

	def positionLines(self):
		liney = 0
		if len(self.lines) > 0:
			prevline = self.lines[0]
			for line in self.lines[1:]:
				lineheight = 0
				height, ascender, descender, line_gap = prevline.getLineMetrics()
				liney -= -descender
				height, ascender, descender, line_gap = line.getLineMetrics()
				liney -= line_gap
				liney -= ascender
				line.setLinePos(0, liney)
				prevline = line



class Line(TextPartBase):
	def __init__(self, textState):
		self.parts = []
		self.textState = textState

	def getLineMetrics(self, relx=0.0, rely=0.0):
		if self.isEmpty():
			font = self.textState.getFont()
			return font.height, font.ascender, font.descender, font.line_gap
		else:
			metrics = [k.getLineMetrics(relx, rely) for k in self.parts]
			height = max([k[0] for k in metrics])
			ascender = max([k[1] for k in metrics])
			descender = min([k[2] for k in metrics])
			line_gap = max([k[3] for k in metrics])
			return height, ascender, descender, line_gap

	def getMetrics(self):
		if self.isEmpty():
			font = self.textState.getFont()
			return font.height, font.ascender, font.descender, font.line_gap
		else:
			metrics = [k.getMetrics() for k in self.parts]
			height = max([k[0] for k in metrics])
			ascender = max([k[1] for k in metrics])
			descender = min([k[2] for k in metrics])
			line_gap = max([k[3] for k in metrics])
			return height, ascender, descender, line_gap

	def isEmpty(self):
		return self._getTextParts() == []

	def setLinePos(self, x, y):
		for part in self.parts:
			part.setLinePos(x, y)

	def add(self, *parts):
		self.parts.extend(parts)

	def draw(self, cinterface, x, y, xanchor, yanchor, justify, blockwidth, angle, valign, halign, defaultcolor, device):
			for part in self.parts:
				p1, p2, p3, p4 = self.getBBox()
				textwidth = p2[0] - p1[0]
				if justify == "center":
					xjustify = blockwidth/2-textwidth/2
				elif justify == "right":
					xjustify = blockwidth-textwidth
				elif justify == "left":
					xjustify = 0
				else:
					raise Exception, "unknown justify: %r" % justify

				part.draw(cinterface, x, y, xanchor, yanchor, xjustify, angle, defaultcolor, device)

	def _getTextParts(self):
		return self.parts

	def translate(self, x, y):
		for part in self.parts:
			part.translate(x, y)

class TextPart(TextPartBase):
	def __init__(self, text, x, y, textState, dpi):
		self.text = text
		self.x = x
		self.y = y
		self.textState = textState
		self.linex = 0
		self.liney = 0
		self.scalex = 1.0
		self.scaley = 1.0
		self.dpi = dpi
		self.font = textState.getFont()

		self.usedFonts = [self.font]
		self.fontList = None
		self.setFontSize()
		self.metrics = []
		self.calcMetrics()

	def scale(self, x, y):
		self.scalex *= x
		self.scaley *= y
		self.calcMetrics()

	def translate(self, x, y):
		self.x += x
		self.y += y
		self.calcMetrics()

	def getLineMetrics(self, relx=0, rely=0):
		lineGap = max(self.font.line_gap, self.relLineGap)
		lineHeight = max(self.font.height, self.relLineHeight + self.y - rely)
		lineAscender = max(self.font.ascender, self.relLineAscender + self.y  -rely)
		lineDescender = min(self.font.descender, self.relLineDescender + self.y - rely)
		return lineHeight, lineAscender, lineDescender, lineGap

	def getMetrics(self):
		return self.relLineHeight, self.relLineAscender, self.relLineDescender, self.relLineGap

	def setFontSize(self, font=None):
		if font is None:
			font = self.font
		size = self.textState.fontScale * self.textState.fontSizeFt2
		font.set_char_size(int(size*self.scalex), int(size*self.scaley))


	def setLinePos(self, x, y):
		self.linex = x
		self.liney = y

	def setLinePos(self, x, y):
		self.linex = x
		self.liney = y

	def calcMetrics(self):
		self.relLineGap			= self.font.line_gap
		self.relLineHeight		= self.font.height
		self.relLineDescender	= self.font.descender
		self.relLineAscender	= self.font.ascender

		for char in unicode(self.text):
			charfound = False
			charfont = self.font

			if self.font.has_char(char):
				charfound = True
			else:
				fontList = self.getFontList()
				glyphsubstitution = True
				if glyphsubstitution:
					for fontFamily in fontList:
						font = fontFamily.get(bold=self.font.is_bold, italic=self.font.is_italic)
						if font != self.font and font.has_char(char):
							charfont = font
							charfound = True
							break
			if not charfound:
				char = u"?"
			#print "char->", `char`," ",
			self.setFontSize(charfont)
			result = charfont.get_text_metrics(char, FT_LOAD_NO_HINTING, False)
			self.metrics.append(result)
			self.relLineGap = max(self.relLineGap, charfont.line_gap)
			self.relLineHeight = max(self.relLineHeight, charfont.height)
			self.relLineDescender = max(self.relLineDescender, charfont.descender)
			self.relLineAscender = min(self.relLineAscender, charfont.ascender)

		#self.font.set_char_size(0, int(self.textState.fontSizeFt2))
		self.setFontSize()
		self.lineGap = max(self.font.line_gap, self.relLineGap)
		self.lineHeight = max(self.font.height, self.relLineHeight + self.y)
		self.lineAscender = max(self.font.ascender, self.relLineAscender + self.y)
		self.lineDescender = min(self.font.descender, self.relLineDescender + self.y)

		self.relLineGap = max(self.font.line_gap, self.relLineGap)
		self.relLineHeight = max(self.font.height, self.relLineHeight)
		self.relLineAscender = max(self.font.ascender, self.relLineAscender)
		self.relLineDescender = min(self.font.descender, self.relLineDescender)

		self.width = 0
		self.height = 0
		self.advance = 0
		self.bearingx = 0
		self.bearingy = 0
		for width, height, advance, bearingx, bearingy in self.metrics:
			self.height = max(self.height, height)
			self.advance += advance
			self.bearingy = max(self.bearingy, bearingy)
		if len(self.metrics):
			self.bearingx = self.metrics[0][3]
			leftoverx = self.metrics[-1][2] - self.metrics[-1][3] - self.metrics[-1][0]
			self.width = self.advance - self.bearingx - leftoverx
		scale = 1/float(1<<6)
		self.width = self.width * scale
		self.height = self.height * scale
		self.advance = self.advance * scale
		self.bearingx = self.bearingx * scale
		self.bearingy = self.bearingy * scale


	def draw(self, cinterface, x, y, xanchor, yanchor, xjustify, angle, defaultcolor, device):
		color = self.textState.color
		if self.textState.color is None:
			self.textState.color = defaultcolor
		self.setFontSize()
		matrix =	kaplot.Matrix.translate((x, y)) *\
					kaplot.Matrix.rotate(angle) * \
					kaplot.Matrix.translate((self.x + self.linex + xanchor + xjustify,
													self.y + self.liney + yanchor))
		a, b, c, d, tx, ty = _fromMatrix(matrix)
		#a, b, c, d, tx, ty = 0, -65536, 65536, 0, 22860, 13031
		#print a, b, c, d, tx, ty
		#b, c = -1000, 1000
		#import pdb;
		#pdb.set_trace()
		tx0, ty0 = tx, ty
		for char in unicode(self.text):
			#print "char", char
			def drawFt2Glyph(_font, a,b,c,d,tx,ty):
				#print a, b, c, d, tx, ty, char
				return _font.draw_path(char, cinterface, a,b,c,d,tx,ty, FT_LOAD_NO_HINTING)

			if self.font.has_char(char):
				dx, dy = device.drawGlyph(char, self.textState,
							self.font, (a,b,c,d,tx,ty), drawFt2Glyph)
			else:
				fontList = self.getFontList()
				charfound = False
				glyphsubstitution = True
				if glyphsubstitution:
					for fontFamily in fontList:
						font = fontFamily.get(bold=self.font.is_bold, italic=self.font.is_italic)
						if font != self.font and font.has_char(char):
							self.setFontSize(font)
							dx, dy = device.drawGlyph(char, self.textState,
										font, (a,b,c,d,tx,ty), drawFt2Glyph)
							charfound = True
							break
				if not charfound:
					dx, dy = device.drawGlyph(u"#", self.textState, self.font, (a,b,c,d,tx,ty), drawFt2Glyph)
			tx += dx
			ty += dy

		if self.textState.underline:
			linewidth = "%fpt" % self.font.underline_thickness
			context = {"color":self.textState.color, "linewidth":linewidth}
			device.pushContext(context)
			p1 = (float(tx0)/(1<<6), float(ty0)/(1<<6)+self.font.underline_position)
			p2 = (float(tx)/(1<<6),  float(ty)/(1<<6)+self.font.underline_position)
			#device.plotLine(p1, p2)
			device.drawLine(p1[0], p1[1], p2[0], p2[1])
			device.popContext()
		if self.textState.overline:
			linewidth = "%fpt" % self.font.underline_thickness
			context = {"color":self.textState.color, "linewidth":linewidth}
			device.pushContext(context)
			p1 = (float(tx0)/(1<<6), float(ty0)/(1<<6)+self.font.ascender)
			p2 = (float(tx)/(1<<6),  float(ty)/(1<<6)+self.font.ascender)
			device.drawLine(p1[0], p1[1], p2[0], p2[1])
			device.popContext()

		self.textState.color = color


	def getFontList(self):
		if self.fontList is None:
			self.fontList = findMatchingFontFamilies(self.font.family_name)
		return self.fontList


	def getBBox(self, relx=0, rely=0):
		x = self.x + self.linex - relx
		y = self.y + self.liney - rely
		xmin = self.bearingx
		ymin = -(self.height - self.bearingy)
		xmax = self.bearingx + self.width
		ymax = self.bearingy
		p1 = (xmin + x, ymin + y)
		p2 = (xmax + x, ymin + y)
		p3 = (xmax + x, ymax + y)
		p4 = (xmin + x, ymax + y)
		return p1, p2, p3, p4

class TextFraction(TextPartBase):
	def __init__(self, x, y, textState, upperLine, bottomLine, upperWidth, bottomWidth):
		self.upperLine = upperLine
		self.bottomLine = bottomLine
		upperParts = upperLine.parts
		bottomParts = bottomLine.parts
		self.textState = textState
		self.upperParts  = upperParts
		self.bottomParts = bottomParts
		self.parts = self.upperParts + self.bottomParts
		self.x = x
		self.y = y
		self.linex = 0
		self.liney = 0

		#self.midliney = midliney
		#self.midlineWidth = midlineWidth
		if upperWidth > bottomWidth: # upper part is wider, translate bottom part
			translateParts = bottomParts
			tx = upperWidth/2.0 - bottomWidth/2.0
		else:
			translateParts = upperParts
			tx = bottomWidth/2.0 - upperWidth/2.0
		for part in translateParts:
			part.translate(tx, 0)

		font = textState.getFont()
		self.midliney = font.ascender*0.5
		_, _, descender, _ = upperLine.getLineMetrics(self.x, self.y)
		_, ascender, _, lineGap = bottomLine.getLineMetrics(self.x, self.y)
		#descender = font.descender
		#ascender = font.ascender
		#lineGap = font.line_gap
		fractionGap = textState.fontSizePt * textState.fontScale / 10.0
		for part in upperParts:
			part.translate(0, self.midliney-descender+fractionGap/2)
		for part in bottomParts:
			part.translate(0, self.midliney-lineGap-ascender-fractionGap/2)
		self.midlineWidth = max(upperWidth, bottomWidth)

	def _getTextParts(self):
		return self.parts

	def draw(self, cinterface, x, y, xanchor, yanchor, xjustify, angle, defaultcolor, device):
		for part in self.parts:
			part.draw(cinterface, x, y, xanchor, yanchor, xjustify, angle, defaultcolor, device)
		# the fraction line will be the same width as the underline

		matrix =	kaplot.Matrix.translate((x, y)) *\
					kaplot.Matrix.rotate(angle) * \
					kaplot.Matrix.translate((self.x + self.linex + xanchor + xjustify,
													self.y + self.liney + yanchor))

		font = self.textState.getFont()
		linewidth = "%fpt" % font.underline_thickness
		context = {"linewidth":linewidth}
		if self.textState.color:
			context["color"] = self.textState.color
		else:
			context["color"] = defaultcolor
		device.pushContext(context)
		p1 = matrix * (0, +self.midliney)
		p2 = matrix * (self.midlineWidth, +self.midliney)
		device.drawLine(p1.x, p1.y, p2.x, p2.y)
		device.popContext()

class TextOverline(TextPartBase):
	def __init__(self, x, y, textState, overlineLine, width):
		self.textState = textState
		self.overlineLine = overlineLine
		self.parts = self.overlineLine._getTextParts()
		self.width = width
		self.x = x
		self.y = y
		self.linex = 0
		self.liney = 0


	def _getTextParts(self):
		return self.parts

	def draw(self, cinterface, x, y, xanchor, yanchor, xjustify, angle, defaultcolor, device):
		for part in self.parts:
			part.draw(cinterface, x, y, xanchor, yanchor, xjustify, angle, defaultcolor, device)

		matrix =	kaplot.Matrix.translate((x, y)) *\
					kaplot.Matrix.rotate(angle) * \
					kaplot.Matrix.translate((self.x + self.linex + xanchor + xjustify,
													self.y + self.liney + yanchor))

		_, ascender, _, _ = self.getLineMetrics(relx=self.x, rely=self.y)
		font = self.textState.getFont()
		linewidth = "%fpt" % font.underline_thickness
		context = {"linewidth":linewidth}
		if self.textState.color:
			context["color"] = self.textState.color
		else:
			context["color"] = defaultcolor
		device.pushContext(context)
		p1 = matrix * (0, ascender)
		p2 = matrix * (self.width, ascender)
		device.plotLine(p1, p2)
		device.popContext()




class TextRow(TextPartBase):
	def __init__(self, x, y, textState, lines):
		self.x = x
		self.y = y
		self.textState = textState
		self.lines = lines
		self.parts = []
		for line in lines:
			self.parts.extend(line._getTextParts())

		_, maxascender, _, _ = self.getLineMetrics(self.x, self.y)
		for line in lines:
			_, ascender, _, _ = line.getLineMetrics(self.x, self.y)
			yscale = maxascender/ascender
			line.scale(1,yscale)


	def _getTextParts(self):
		return self.parts

	def draw(self, cinterface, x, y, xanchor, yanchor, xjustify, angle, defaultcolor, device):
		for part in self.parts:
			part.draw(cinterface, x, y, xanchor, yanchor, xjustify, angle, defaultcolor, device)

