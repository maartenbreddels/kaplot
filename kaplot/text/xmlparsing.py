import xml.sax
import xml.dom.pulldom
from cStringIO import StringIO
import htmlentitydefs
import re
import kaplot.matrix
import math
from kaplot.cext._pyfont import *
from kaplot.text.xmltext import *
from kaplot.text.xmltext import _fromMatrix
from kaplot.text.fonts import findFont
import copy

subsupscale = 1
fractionscale = 1
subsupscale = 0.6
fractionscale = 0.6

kaplot_entities = {"solar": 0x2299}

def entity2unicode(string):
	newstring = u""
	string = unicode(string)
	if "&" not in string:
		return string
	else:
		index = 0
		ampindex = string.find("&", index)
		while ampindex != -1:
			delindex = string.find(";", ampindex)
			if delindex == -1:
				raise Exception, "undelimited entity at index %i in string %r" % (ampindex, string)
			else:
				newstring += string[index:ampindex]
				entityname = string[ampindex+1:delindex]
				# these are handled by the xml parser, and should be left alone
				if entityname not in ["lt", "gt", "amp", "apos", "quot"]:
					if entityname[0] == "#" and entityname[1] == 'x':
						newstring += unichr(int(entityname[2:], 16))
					elif entityname[0] == "#":
						newstring += unichr(int(entityname[1:], 10))
					elif entityname in htmlentitydefs.name2codepoint:
						codepoint = htmlentitydefs.name2codepoint[entityname]
						newstring += unichr(codepoint)
					elif entityname in kaplot_entities:
						codepoint = kaplot_entities[entityname]
						newstring += unichr(codepoint)
					else:
						#pdb.set_trace()
						raise Exception, "unknown entity reference: %r at offset %i" % (entityname, ampindex)
				else:
					newstring += "&%s;" % entityname
			index = delindex+1
			ampindex = string.find("&", index)
			#print "TODO", string[index:]
			#print
			#print `newstring`
			#print
		newstring += string[index:]
		#print "$"*80
		#print `newstring`
		#print "$"*80
		return newstring


def getNodeAttribute(node, attributeName, defaultValue):
	value = defaultValue
	if node.attributes is not None:
		attributeNode = dict(node.attributes).get(attributeName)
		if attributeNode is not None:
			value = attributeNode.nodeValue
	return value

#def getNodeColor(node, defaultColor):
#	color = defaultColor
#	return defaultColor

#import mathml
#import mathml.xml.minidom_parser
#import mathml.xml.libxml2_parser
#import mathml.plotter

#class PlotterProxy(mathml.plotter.Plotter):
class _PlotterProxy(object):
	def __init__(self):
		self.proxy = None

	def __gattr__(self, name):
		if self.__dict__["proxy"] != None:
			return getattr(__dict__["proxy"], name)
		else:
			return self.__dict__[name]

	def labelmetrics(self, text):
		return self.proxy.labelmetrics(text)

from copy import deepcopy
#class OnlyFontPlotter(mathml.plotter.Plotter):
class _OnlyFontPlotter(object):
	noclipping = True

	class State(object):
		tx = 0
		ty = 0
		x = 0
		y = 0
		font_name = 'Arial'
		font_size = 16


	def __init__(self, fontname):
		self.state = self.State()
		self.state.font_name = fontname
		self.font = fontFamilies[self.state.font_name].getRegular()
		self.font.set_char_size(0, self.state.font_size*(1<<6))
		self.states = []
		self.cinterface = None
		self.device = None
		self.noclipping = True
		#self.cinterface = kaplot.cext._cairo.create_cinterface(ctx, cairo.Matrix(1,0,0,1,0,0))

	def setfont(self, family, style, size):
		"""Changes to the font described by @family, @style, and @size."""
		#return
		self.state.font_name = family
		self.state.font_size = size
		self.font = fontFamilies[self.state.font_name].getRegular()
		self.font.set_char_size(0, self.state.font_size*(1<<6))

	def labelmetrics(self, text):
		'''     axis is the axis position of the text, relative to the bottom
		        of the text.  '''
		self.font.set_char_size(0, self.state.font_size*(1<<6))
		result = self.font.get_text_metrics(unicode(text), FT_LOAD_NO_HINTING)
		width, height, advance, bearingx, bearingy = result
		#axis = height - bearingy
		#axis = 0
		#axis = (height - bearingy)
		axis = 0
		return None, advance, height*0.99, axis

	def moveto(self, x, y):
		self.state.x = x
		self.state.y = y

	def label(self, text, layout=None, stretchy=1):
		result = self.font.get_text_metrics(unicode(text), FT_LOAD_NO_HINTING)
		width, height, advance, bearingx, bearingy = result
		descender = -(height - bearingy)
		fx = self.state.x+self.state.tx
		fy = self.state.y+self.state.ty
		#if stretchy != 1:
		#	stretchy = (stretchy+0.05)*1.1
		matrix = kaplot.matrix.Matrix.translate((fx, fy)) * \
				kaplot.matrix.Matrix.scaleXY(1,stretchy) *\
				kaplot.matrix.Matrix.translate((0, -descender))
		#matrix = kaplot.matrix.Matrix.scaleXY(1,stretchy) * kaplot.matrix.Matrix.translate((fx, fy))
		a, b, c, d, tx, ty = _fromMatrix(matrix)
		self.font.draw_path(unicode(text), self.cinterface, a,b,c,d,tx,ty, FT_LOAD_NO_HINTING)
		self.device._fill()
		#self.device.context.fill().		#height = bearingy
		#dontcare, newadvance, newheight, axis = self.labelmetrics(text)
		#assert advance == newadvance
		#assert height == newheight

		self.state.x += advance

	def savestate(self):
		self.states.append(deepcopy(self.state))
		#self.device.context.save()

	def restorestate(self):
		self.state = self.states.pop()
		self.font = fontFamilies[self.state.font_name].getRegular()
		self.font.set_char_size(0, self.state.font_size*(1<<6))
		#self.device.context.restore()

	def translate(self, x, y):
		self.state.tx += x
		self.state.ty += y

	def lineto(self, x, y):
		x1 = self.state.x + self.state.tx
		y1 = self.state.y + self.state.ty
		x2 = self.state.tx + x
		y2 = self.state.ty + y
		self.device.plotLine((x1, y1), (x2, y2))
		self.state.x = x
		self.state.y = y

	def linewidth(self, width):
		self.device._setLinewidth("%spx" % width)

	def resolve_length(self, value, unit):
		if unit == "pt":
		        return value
		else:
		        raise Exception, "unknown unit: %r" % unit


def _parseMathMLNode(textNode, x, y, font, fontsize, bold, italic, textObject, fontname, color):
	plotterProxy = PlotterProxy()
	plotter = OnlyFontPlotter(fontname)
	xmlcode = textNode.toxml()
	root = mathml.xml.libxml2_parser.parseString(xmlcode.encode("utf8"), plotter)
	#root = mathml.xml.minidom_parser.parseTree(node, plotterProxy)
	#plotter = OnlyFontPlotter(fontname)
	plotterProxy.proxy = plotter
	#root = mathMLParseTree(node, PlotterProxy())
	root.x0 = 0
	root.y0 = 0
	root.setAttribute("fontsize", "20pt")
	root.update()
	textPart = TextPartMathML(root, font, fontsize, x, y, color)
	textObject.getLine().add(textPart)
	return root.width

class TextState(object):
	fontFamilyName = None
	fontSize = None
	fontSizePx = None
	fontSizePt = None
	fontSizeFt2 = None
	underline = False
	overline = False
	bold = False
	italic = False
	color = None
	fontScale = 1.0

	def setFontSize(self, fontSize, dpi):
		self.fontSize = fontSize
		fontSizeNr, fontSizeUnits = kaplot.utils.splitDimension(self.fontSize)
		self.fontSizePx = kaplot.utils.convertToPixels(float(fontSizeNr), fontSizeUnits, dpi=dpi)
		self.fontSizePt = kaplot.utils.convertPixelsTo(self.fontSizePx, fontSizeUnits, dpi=dpi)
		self.fontSizeFt2 = int(self.fontSizePt*(1<<6))

	def scaleFontSize(self, scale, dpi):
		fontSizeNr, fontSizeUnits = kaplot.utils.splitDimension(self.fontSize)
		fontSizeNr *= scale
		self.fontSize = "%s%s"% (fontSizeNr, fontSizeUnits)
		self.fontSizePx = kaplot.utils.convertToPixels(float(fontSizeNr), fontSizeUnits, dpi=dpi)
		self.fontSizePt = kaplot.utils.convertPixelsTo(self.fontSizePx, fontSizeUnits, dpi=dpi)
		self.fontSizeFt2 = int(self.fontSizePt*(1<<6))

	def getFont(self):
		font = findFont(self.fontFamilyName, self.bold, self.italic)
		font.set_char_size(0, int(self.fontScale * self.fontSizeFt2))
		return font


xmlelements = lambda node: [k for k in node.childNodes if k.nodeType != xml.dom.Node.TEXT_NODE]
xmltextnodes = lambda node: [k for k in node.childNodes if k.nodeType == xml.dom.Node.TEXT_NODE]

def parseNode(textNode, x, y, textObject, textState, dpi):
	x0 = x
	orgTextState = copy.deepcopy(textState)

	for node in textNode.childNodes:
		textState = copy.deepcopy(orgTextState)
		textState.color = getNodeAttribute(textNode, "color", orgTextState.color)
		textState.fontFamilyName = getNodeAttribute(textNode, "font", orgTextState.fontFamilyName)
		textState.setFontSize(getNodeAttribute(textNode, "fontsize", orgTextState.fontSize), dpi)
		if node.nodeType == xml.dom.Node.TEXT_NODE:
			text = unicode(node.nodeValue)
			textparts = text.split("\n")
			for i, textpart in enumerate(textparts):
				if i > 0:
					textObject.addLine(textState)
					x = 0#x0
				if textpart:
					textPart = TextPart(textpart, x, y, textState, dpi)
					textObject.getLine().add(textPart)
					x += textPart.advance
		else:
			if node.nodeName == "sup":
				dy = textState.fontSizePt/3.0 * textState.fontScale
				textState.scaleFontSize(subsupscale, dpi)
				x += parseNode(node, x, y+dy, textObject, textState, dpi)
			elif node.nodeName == "sub":
				dy = -textState.fontSizePt/3.0 * textState.fontScale
				textState.scaleFontSize(subsupscale, dpi)
				x += parseNode(node, x, y+dy, textObject, textState, dpi)
			elif node.nodeName == "subsup":
				childElements = xmlelements(node)
				textNodes = xmlelements(node)
				text = "".join([k.nodeValue for k in textNodes if k.nodeValue != None])
				if text.strip():
					kaplot.info("ignoring text in subsup tag:", `text`)
				subnode = childElements[0]
				supnode = childElements[1]

				subTextState = copy.deepcopy(textState)
				suby = y - subTextState.fontSizePt/2.0 * subTextState.fontScale
				subTextState.scaleFontSize(subsupscale, dpi)
				dx1 = parseNode(subnode, x, suby, textObject, subTextState, dpi)

				supTextState = copy.deepcopy(textState)
				supy = y + supTextState.fontSizePt/2.0 * supTextState.fontScale
				supTextState.scaleFontSize(subsupscale, dpi)
				dx2 = parseNode(supnode, x, supy, textObject, supTextState, dpi)
				x += max(dx1, dx2)
			elif node.nodeName == "supmidsub":
				childElements = xmlelements(node)
				textNodes = xmlelements(node)
				text = "".join([k.nodeValue for k in textNodes if k.nodeValue != None])
				if text.strip():
					kaplot.info("ignoring text in row tag:", `text`)

				if len(childElements) != 3:
					raise Exception, "supmidsub nodes should have 3 child nodes(nothing more or less)"
				upperNode = childElements[0]
				midNode = childElements[1]
				bottomNode = childElements[2]

				upperTextObject = Text()
				upperTextState = copy.deepcopy(textState)
				upperTextState.scaleFontSize(subsupscale, dpi)
				upperTextObject.addLine(upperTextState)

				midTextObject = Text()
				midTextState = copy.deepcopy(textState)
				midTextObject.addLine(midTextState)

				bottomTextObject = Text()
				bottomTextState = copy.deepcopy(textState)
				bottomTextState.scaleFontSize(subsupscale, dpi)
				bottomTextObject.addLine(bottomTextState)

				dx1 = parseNode(upperNode, x, y, upperTextObject, upperTextState, dpi)
				dx2 = parseNode(midNode, x, y, midTextObject, midTextState, dpi)
				dx3 = parseNode(bottomNode, x, y, bottomTextObject, bottomTextState, dpi)

				upperLine = upperTextObject.getLine()
				midLine = midTextObject.getLine()
				bottomLine = bottomTextObject.getLine()

				upperParts = upperLine.parts
				midParts = midLine.parts
				bottomParts = bottomLine.parts

				if len(upperTextObject.lines) > 1 or len(bottomTextObject.lines) > 1 \
						or len(midTextObject.lines) > 1:
					raise Exception, "there can be no newline in a supmidsub"
				textObject.getLine().add(*upperParts)
				textObject.getLine().add(*midParts)
				textObject.getLine().add(*bottomParts)

				p1, p2, p3, p4 = upperLine.getBBox(x, y)
				upperminy = p1[1]
				p1, p2, p3, p4 = midLine.getBBox(x, y)
				midmaxy = p3[1]
				midminy = p1[1]
				p1, p2, p3, p4 = bottomLine.getBBox(x, y)
				bottommaxy = p3[1]

				upperLine.translate(0, midmaxy-upperminy)
				bottomLine.translate(0,midminy-bottommaxy)

				maxwidth = max(dx1, dx2, dx3)
				minwidth = min(dx1, dx2, dx3)
				#if dx2 < dx1 or dx2 < dx2:
				if True:
					upperLine.translate(-dx1/2.0+maxwidth/2, 0)
					midLine.translate(-dx2/2.0+maxwidth/2, 0)
					bottomLine.translate(-dx3/2.0+maxwidth/2, 0)
				else:
					left = -max(dx1-dx2, 0, 0)
					upperLine.translate(-dx1+dx2-left, 0)
					midLine.translate(0-left, 0)
					bottomLine.translate(0-left, 0)
				#upperLine.translate(-dx1/2.0+maxwidth/2)
				#bottomLine.translate(-dx3/2.0+maxwidth/2)


				width = max(dx1, dx2, dx3)
				x += width

			elif node.nodeName == "i":
				textState.italic = True
				x += parseNode(node, x, y, textObject, textState, dpi)
			elif node.nodeName == "b":
				textState.bold = True
				x += parseNode(node, x, y, textObject, textState, dpi)
			elif node.nodeName == "u":
				textState.underline = True
				x += parseNode(node, x, y, textObject, textState, dpi)
			elif node.nodeName == "o":
				textState.overline = True
				x += parseNode(node, x, y, textObject, textState, dpi)
			elif node.nodeName == "ol":
				overlineTextObject = Text()
				overlineTextState = copy.deepcopy(textState)
				overlineTextObject.addLine(overlineTextState)
				dx = parseNode(node, x, y, overlineTextObject, overlineTextState, dpi)
				if len(overlineTextObject.lines) > 1:
					raise Exception, "there can be no newline in a ol tag"
				overline = TextOverline(x, y, overlineTextState, overlineTextObject.getLine(), dx)
				textObject.getLine().add(overline)
				x += dx
			elif node.nodeName == "row":
				childElements = xmlelements(node)
				textNodes = xmlelements(node)
				text = "".join([k.nodeValue for k in textNodes if k.nodeValue != None])
				if text.strip():
					kaplot.info("ignoring text in row tag:", `text`)
				dxlist = []
				lines = []
				xstart = x
				for childElement in childElements:
					rowElementTextObject = Text()
					rowElementTextState = copy.deepcopy(textState)
					rowElementTextObject.addLine(rowElementTextState)
					dx = parseNode(childElement, x, y, rowElementTextObject, rowElementTextState, dpi)
					#overline = TextOverline(x, y, overlineTextState, overlineTextObject.getLine(), dx)
					if len(rowElementTextObject.lines) > 1:
						raise Exception, "there can be no newline in a row tag"
					dxlist.append(dx)
					lines.append(rowElementTextObject.getLine())
					x += dx
				row = TextRow(xstart, y, copy.deepcopy(textState), lines)
				textObject.getLine().add(row)
				#x += sum(dxlist)
			elif node.nodeName == "fraction":
				childElements = xmlelements(node)
				textNodes = xmlelements(node)
				text = "".join([k.nodeValue for k in textNodes if k.nodeValue != None])
				if text.strip():
					kaplot.info("ignoring text in fraction tag:", `text`)

				textState.scaleFontSize(fractionscale, dpi)
				upperNode = childElements[0]
				bottomNode = childElements[1]

				upperTextObject = Text()
				upperTextObject.addLine(textState)
				upperTextState = copy.deepcopy(textState)

				bottomTextObject = Text()
				bottomTextObject.addLine(textState)
				bottomTextState = copy.deepcopy(textState)

				dx1 = parseNode(upperNode, x, y, upperTextObject, upperTextState, dpi)
				dx2 = parseNode(bottomNode, x, y, bottomTextObject, bottomTextState, dpi)
				upperLine = upperTextObject.getLine()
				bottomLine = bottomTextObject.getLine()
				upperParts = upperLine.parts
				bottomParts = bottomLine.parts
				if len(upperTextObject.lines) > 1 or len(bottomTextObject.lines) > 1:
					raise Exception, "there can be no newline in a fraction"
				fraction = TextFraction(x, y, textState, upperLine, bottomLine, dx1, dx2)
				textObject.getLine().add(fraction)
				width = max(dx1, dx2)
				x += width
			#elif node.nodeName == "math":
			#	x += parseMathMLNode(node, x, y, font, fontsize, bold, italic, textObject, fontname, color)
			else:
				if node.nodeName != "text":
					kaplot.debug("unkown node <%s>, will render it as plain text" % node.nodeName)
				x += parseNode(node, x, y, textObject, textState, dpi)
	return x - x0


def buildText(textNode, font, fontSize, fontFamilyName, dpi):
	color = getNodeAttribute(textNode, "color", None)
	justify = getNodeAttribute(textNode, "justify", "center")
	fontFamilyName = getNodeAttribute(textNode, "font", fontFamilyName)
	x = 0
	y = 0
	textState = TextState()
	textState.fontFamilyName = fontFamilyName
	textState.setFontSize(fontSize, dpi)
	textState.color = color

	textObject = Text()
	textObject.addLine(textState)
	textObject.justify = justify
	parseNode(textNode, x, y, textObject, textState, dpi)

	textObject.positionLines()

	return textObject

_cache = {}
def parseText(text, font, fontsize, fontname, dpi):
	try:
		cachekey = (fontname, text, fontsize)
		if cachekey in _cache:
			#kaplot.debug("cache hit for text")
			return _cache[cachekey]
		else:
			if text.strip().startswith("<text") and text.strip().endswith("</text>"):
				xmlstring = text
			else:
				xmlstring = "<text>%s</text>" % text
			xmlstring = entity2unicode(xmlstring)
			encoding = "utf-8"
			encodingheader = "<?xml version='1.0' encoding='%s'?>" % encoding
			properxmlstring =  encodingheader + xmlstring
			parser = xml.sax.make_parser()
			buf = StringIO(xmlstring.encode(encoding))
			bufsize = len(xmlstring)
			#pdb.set_trace()
			events = xml.dom.pulldom.DOMEventStream(buf, parser, bufsize)
			toktype, rootNode = events.getEvent()
			events.expandNode(rootNode)
			events.clear()
			document = rootNode
			document.normalize()
			textNode = document.childNodes[0]
			textObject = buildText(textNode, font, fontsize, fontname, dpi)
			_cache[cachekey] = textObject
			return textObject
	except:
		kaplot.info("error while parsing text: %r" % text)
		raise

if __name__ == "__main__":
	import kaplot.cext._cairo
	string2 = u"""<text color="#ff00ff">&epsilon;</text> &lambda; lim<sub>n&rarr;&infin;</sub>&sum;<subsup color='red'><span>i=1</span><span>i=n</span></subsup>1/i&sup2; = 2"""
	fontname = "Arial"
	font = findtFont(fontname, False, False)
	fontsize = 25 * 1 << 6
	font.set_char_size(0, int(fontsize))
	text = parseText(string2, font, fontsize, fontname)

	width, height = 600, 600
	ctx = cairo.Context()
	surface = cairo.win32_surface_create("Cairo demo (win32 surface)", width, height)
	ctx.set_target_surface(surface)
	ctx.set_matrix(cairo.Matrix(1, 0, 0, -1, 0, height))
	ctx.set_rgb_color(1,1,1)
	ctx.set_line_width(0.8)
	points = [(150, 150, "left", "top"), (450, 450, "right", "bottom"), (450, 150, "middle", "middle")]
	cinterface = kaplot.cext._cairo.create_cinterface(ctx, cairo.Matrix(1,0,0,1,0,0))
	for x, y, halign, valign in points:
		ctx.move_to(x - 10, y)
		ctx.line_to(x + 10, y)
		ctx.move_to(x, y-10)
		ctx.line_to(x, y+10)
		ctx.stroke()
		angle = math.radians(20)
		text.draw(cinterface, x, y, angle, valign, halign, lambda x: x, lambda x: x, "red")
		ctx.fill()
		points = text.getBBoxTransformed(x, y, angle, valign, halign)
		ctx.move_to(points[0].x, points[0].y)
		for i in range(1):
			ctx.line_to(points[(i+1)%4].x, points[(i+1)%4].y)
		ctx.close_path()
		ctx.stroke()
	ctx.show_page()
