from kaplot.matrix import Matrix
import kaplot.devices.devicebase
import kaplot.utils
import kaplot.vector
import kaplot.cext._kaplot
import numpy
import math
import time
from cStringIO import StringIO

def mulXY(m, xlist, ylist):
	xlist = numpy.array(xlist)
	ylist = numpy.array(ylist)
	return \
		m.xx * xlist + m.xy * ylist + m.tx, \
		m.yx * xlist + m.yy * ylist + m.ty
		
class PDF:
	CLOSE_PATH = "h"	

class CInterfaceWrapper(object):
	def __init__(self, device):
		self.device = device
		self.buffer = StringIO()
		#worldmatrix = self.getWorldMatrix()
		viewportmatrix = self.device.getViewportMatrix()
		devicematrix = self.device.getDeviceMatrix()
		

		self.matrix = (viewportmatrix)

	def clearBuffer(self):
		self.buffer = StringIO()

	def getBufferValue(self):
		return self.buffer.getvalue()

	def move_to(self, x, y):
		x, y = self.matrix * (x, y)
		self.buffer.write("%f %f m\n" % (x, y))

	def line_to(self, x, y):
		x, y = self.matrix * (x, y)
		#self.string += "%f %f lineto\n" % (x, y)
		self.buffer.write("%f %f l\n" % (x, y))

	def curve_to(self, x1, y1, x2, y2, x3, y3):
		x1, y1 = self.matrix * (x1, y1)
		x2, y2 = self.matrix * (x2, y2)
		x3, y3 = self.matrix * (x3, y3)
		#self.string += "%f %f %f %f %f %f curveto\n" % (x1, y1, x2, y2, x3, y3)
		self.buffer.write("%f %f %f %f %f %f c\n" % (x1, y1, x2, y2, x3, y3))

	def fill(self):
		#return
		self.device.gsave()
		self.device.setClippath()
		#self.device.writeln("initclip")
		#self.device.outputMatrix()
		self.device.initmatrix()
		self.device.writeln(self.getBufferValue())
		self.device.gsave()
		self.device.initmatrix()
		self.device.fill()
		self.device.grestore()
		self.device.newpath()
		self.device.grestore()
		self.clearBuffer()

	def stroke(self):
		self.device.gsave()
		self.device.setClippath()
		#self.device.writeln("initclip")
		#self.device.outputMatrix()
		self.device.initmatrix()
		self.device.writeln(self.getBufferValue())
		self.device.gsave()
		self.device.initmatrix()
		self.device.stroke()
		self.device.grestore()
		self.device.newpath()
		self.device.grestore()
		self.clearBuffer()

	def setcolor(self, r, g, b):
		#color = kaplot.utils.decodeColor(color)
		#r, g, b = color.getRGB()
		code = "%f %f %f RG %f %f %f rg\n" % (r, g, b, r, g, b)
		self.device.write(code)
		#self.device._setColor(


class PdfIObject(object):
	def __init__(self, id, content=None, stream=None, **kwargs):
		if content and kwargs:
			raise ValueError, "content and kwargs are mutualy exclusive"
		self.content = content
		self.dict = PdfDict(**kwargs)
		self.stream = stream
		self.id = id

	def __str__(self):
		if self.stream is not None:
			streamstring = "\nstream\n%s\nendstream\n" % self.stream
		else:
			streamstring = ""

		if self.content:
			string = "%i 0 obj\n%s %sendobj" % (self.id, self.content, streamstring)
		else:
			string = "%i 0 obj %s %sendobj" % (self.id, self.dict, streamstring)
		return string

	def ref(self):
		return "%i 0 R" % self.id

class PdfDict(object):
	def __init__(self, **kwargs):
		self.values = kwargs

	def __str__(self):
		return self.tostring()

	def tostring(self, indent=0):
		indentString = "    " * indent
		string = "<<"
		for key, value in self.values.items():
			if isinstance(value, PdfDict):
				valuestr = value.tostring(indent+1)
			else:
				valuestr = str(value)
			string += " /%s %s " % (key, valuestr)
		string += ">>"
		return string


class PdfPage(PdfIObject):
	def __init__(self, document, width, height):
		self.document = document
		#font = PdfDict()
		#self.page = self.document.createObject(Type="/Page", Parent="3 0 R", MediaBox="[0 0 612 792]", Contents="8 0 R", Resources=self.resource)
		#self.procSet = self.document.createObject("[/PDF /Text /ImageC /ImageI /ImageB]")
		#self.font = self.document.createObject(Type="/Font", Subtype="/Type1", Name="/F1", BaseFont="/Helvetica", Encoding="/MacRomanEncoding")
		#self.resource.values["ProcSet"] = "%i 0 R" % self.procSet.id
		#self.xobjects.values["F1"] = "%i 0 R" % (self.font.id)
		#font.values["F1"] = "%i 0 R" % self.font.id

		self.gstates = PdfDict()
		self.patterns = PdfDict()
		self.xobjects = PdfDict()
		self.resource = PdfDict(ExtGState=self.gstates, Pattern=self.patterns, XObject=self.xobjects)

		#self.resource = resource
		#self.gstates = self.resource.values["ExtGState"]
		#self.patterns = self.resource.values["Pattern"]
		#self.xobjects = self.resource.values["XObject"]

		self.contentObject = self.document.createObject() #Length=size, stream=stream)

		mediaBox = "[0 0 %f %f]" % (width, height)

		PdfIObject.__init__(self, document.getId(), Type="/Page", MediaBox=mediaBox, Resources=self.resource)
		self.dict.values["Contents"] = self.contentObject.ref()
		self.document.objects.append(self)
		self.resource.values["ProcSet"] = "[/PDF /ImageC /ImageI /ImageB]"
		self.contentObject.stream = ""
		self.contentObject.dict.values["Length"] = 0


class PdfDocument(object):
	def __init__(self, width, height, pageCount, pdfInfo):
		self.objects = []
		self.pdfInfo = pdfInfo
		self._lastId = 0
		self.stateobjectsbuffer = ""

		self.catalogObject = self.createObject(Type="/Catalog")

		self.pages = [PdfPage(self, width, height) for k in range(pageCount)]
		kids = "[%s]" % " ".join([page.ref() for page in self.pages])
		self.pagesObject = self.createObject(Type="/Pages", Kids=kids, Count=len(self.pages))
		self.catalogObject.dict.values["Pages"] = self.pagesObject.ref()
		for page in self.pages:
			page.dict.values["Parent"] = self.pagesObject.ref()


		if False:
			# this date form isn't very readable
			datestr = time.strftime("(D:%Y:%m:%d:%H:%M:%S")

			timezone = time.timezone
			if timezone <= 0:
				datestr += "-"
			else:
				datestr += "+"

			#timezone = abs(timezone)
			hours = (abs(timezone)/3600)
			minutes = (abs(timezone)-hours*3600) / 60

			datestr += ("%02i'" % hours)
			datestr += ("%02i'" % minutes)
			datestr += ")"
			#print `datestr`
		else:
			datestr = time.asctime()

		self.info = self.createObject()
		self.info.dict.values["Title"] = "(" +self.pdfInfo.title +")"
		self.info.dict.values["Author"] = "(" +self.pdfInfo.author +")"
		self.info.dict.values["Subject"] = "(" +self.pdfInfo.subject +")"
		self.info.dict.values["Keywords"] = "(" +self.pdfInfo.keywords +")"
		self.info.dict.values["Creator"] = "(kaplot)"
		self.info.dict.values["Producer"] = "(kaplot)"
		self.info.dict.values["CreationDate"] = "(" +datestr +")"
		#self.info.values["Author"] = "kaplot, no author"
		#self.info.values["Author"] = "kaplot, no author"


		self.currentPageNr = 0

	def getCurrentPage(self):
		return self.pages[self.currentPageNr]

	def setPageNr(self, pageNr):
		self.currentPageNr = pageNr

	def getId(self):
		id = self._lastId + 1
		self._lastId += 1
		return id

	def createObject(self, content=None, stream=None, **kwargs):
		object = PdfIObject(content=content, stream=stream, id=self.getId(), **kwargs)
		self.objects.append(object)
		return object

	def write(self, file):
		header = "%PDF-1.4\n"
		file.write(header)

		offset = len(header)
		offsets = []

		for object in self.objects:
			offsets.append(offset)
			objectString = str(object) + "\n"
			file.write(objectString)
			offset += len(objectString)
			assert file.tell() == offset
		startxref = offset
		xrefsstring = "%010i 65535 f \n" % 0
		for xref in offsets:
			xrefsstring += "%010i 00000 n \n" % xref
		file.write("xref\n0 %i\n%s" % (len(offsets)+1, xrefsstring))
		pdfTrailer = PdfDict(Size=len(offsets)+1, Root=self.catalogObject.ref(), Info=self.info.ref())
		file.write("trailer\n%s\n" % (pdfTrailer))
		file.write("startxref\n%i\n" % startxref)
		file.write("%%EOF")



class PdfInfo(object):
	author = "no author"
	title = "no title"
	keywords = "no keywords"
	subject = "no subject"

class PdfDeviceBase(kaplot.devices.devicebase.DeviceBase):
	def __init__(self):
		kaplot.devices.devicebase.DeviceBase.__init__(self)
		#self.pointWidth = int(kaplot.utils.convertPixelsTo(self.pixelWidth, "pt", dpi=self.dpi))
		#self.pointHeight = int(kaplot.utils.convertPixelsTo(self.pixelHeight, "pt", dpi=self.dpi))
		self.pdfDoc = None
		self._glyphCache2 = {}
		self.pdfInfo = PdfInfo()
		self._lastId = 1
		
	def _getId(self):
		id = self._lastId
		self._lastId += 1
		return id

	def getCInterface(self):
		self.ciw = CInterfaceWrapper(self)
		return kaplot.cext._kaplot.cinterface_wrap(self.ciw.move_to, self.ciw.line_to,
			self.ciw.curve_to, self.ciw.fill, self.ciw.stroke, self.ciw.setcolor)

	def getDeviceMatrix(self):
		width, height = self.resx, self.resy
		return Matrix.scale(width, height)

	#def getDeviceMatrix(self):
	#	width, height = self.pointWidth, self.pointHeight
	#	return Matrix.scaleXY(width, height)

	def preDraw(self, document):
		w, wu, h, hu= kaplot.utils.splitSize(document.size)
		widthpx = kaplot.utils.convertToPixels(w, wu, document.dpi)
		heightpx = kaplot.utils.convertToPixels(h, hu, document.dpi)
		width = int(kaplot.utils.convertPixelsTo(widthpx, "pt"))
		height = int(kaplot.utils.convertPixelsTo(heightpx, "pt"))
		self.resx = width
		self.resy = height

		self.buffer = StringIO()
		self.imagebuffer = ""
		self.xobjectsbuffer = ""
		self.objects = []
		self.stateobjectsbuffer = ""
		self.alphaMap = {}
		#width = kaplot.utils.convertPixelsTo(self.pixelWidth, "pt", self.dpi)
		#height = kaplot.utils.convertPixelsTo(self.pixelHeight, "pt", self.dpi)
		self.pdfDoc = PdfDocument(width, height, document.getPageCount(), self.pdfInfo)
		super(PdfDeviceBase, self).preDraw(document)

	def preDrawPage(self, document, page):
		#self.pdfDoc.setPageNr(self.getCurrentPageNr())
		super(PdfDeviceBase, self).preDrawPage(document, page)

	def postDrawPage(self, document, page):
		super(PdfDeviceBase, self).postDrawPage(document, page)
		stream = self.buffer.getvalue().encode("zlib")
		#size = self.buffer.tell()
		size = len(stream)
		self.pdfDoc.getCurrentPage().contentObject.dict.values["Length"] = size
		self.pdfDoc.getCurrentPage().contentObject.dict.values["Filter"] = "/FlateDecode"
		self.pdfDoc.getCurrentPage().contentObject.stream = stream
		print "postplot"
		self.buffer = StringIO()

	def postDraw(self, document):
		super(PdfDeviceBase, self).postDraw(document)
		self.pdfDoc.write(self.file)

	def write(self, string):
		self.buffer.write(string)

	def writeln(self, string):
		self.buffer.write(string)
		self.buffer.write("\n")

	def gsave(self):
		self.writeln("q")

	def grestore(self):
		self.writeln("Q")

	def initmatrix(self):
		self.writeln("1 0 0 1 0 0 cm")

	def stroke(self):
		self.writeln("S")

	def newpath(self):
		self.writeln("n")

	def fill(self):
		self.writeln("f")

	def _setColor(self):
		_color = kaplot.utils.decodeColor(self._color)
		r, g, b = _color.getRGB()
		code = "%f %f %f RG %f %f %f rg\n" % (r, g, b, r, g, b)
		self.write(code)

	def getCurrentMatrix(self):
		worldmatrix = self.getWorldMatrix()
		viewportmatrix = self.getViewportMatrix()
		devicematrix = self.getDeviceMatrix()
		return devicematrix * (viewportmatrix * worldmatrix)

	def drawLine(self, x1, y1, x2, y2, gridsnap=False):
		self.gsave()
		self.setClippath()
		matrix = self.getCurrentMatrix()
		p1 = matrix * (x1, y1)
		p2 = matrix * (x2, y2)
		code = ""
		code += "%f %f m\n" % (p1.x, p1.y)
		code += "%f %f l\n" % (p2.x, p2.y)
		self.writeln(code)
		self.gsave()
		self.stroke()
		self.grestore()
		self.grestore()

	def drawPolyLine(self, x, y, close=False, gridsnap=False):
		self.gsave()
		self.setClippath()
		matrix = self.getCurrentMatrix()
		x, y = mulXY(matrix, x, y)
		length = min(len(x), len(y))
		print x, y

		if length > 1:
			#if colors != None:
			#	r, g, b = colors
			#	for i in range(0, length-1):
			#		code = ""
			#		code += "%f %f m\n" % (x[i], y[i])
			#		code += "%f %f l\n" % (x[i+1], y[i+1])
			#		code += "%f %f %f RG\n" % (r[i], g[i], b[i])
			#		#self.outputMatrix()
			#		self.writeln(code)
			#		self.gsave()
			#		self.initmatrix()
			#		self.stroke()
			#		self.grestore()
			#		self.newpath()
			#else:
				code = StringIO()
				code.write("%f %f m\n" % (x[0], y[0]))
				for i in range(1, length):
					code.write("%f %f l\n" % (x[i], y[i]))
				if close:
					code.write(PDF.CLOSE_PATH)
				self.writeln(code.getvalue())
				self.gsave()
				self.initmatrix()
				self.stroke()
				self.grestore()
		self.grestore()

	def drawPolygon(self, x, y, gridsnap=False):
		self.gsave()
		self.setClippath()
		self.outputFillstyle()
		matrix = self.getCurrentMatrix()
		x, y = mulXY(matrix, x, y)
		code = StringIO()
		code.write("%f %f m\n" % (x[0], y[0]))
		length = min(len(x), len(y))
		print length
		for i in range(1, length):
			code.write("%f %f l\n" % (x[i], y[i]))
		self.writeln(code.getvalue())
		self.gsave()
		self.initmatrix()
		self.fill()
		self.grestore()
		self.newpath()
		self.grestore()


	def _createMaskBitmap(self, mask2d):
		booleanmask = (numpy.array(mask2d) > 0)

		bytelist = []

		for row in booleanmask:
			byterowlist = []
			bytecount = len(row) / 8
			restbits = len(row) - bytecount*8
			#print "restbits", restbits, "bytecount", bytecount
			for byte in range(bytecount):
				b = 0
				for i in range(8):
					b |= (row[byte*8+i]) << (7-i)
				byterowlist.append(b)
			if len(booleanmask) % 8:
				b = 0
				for i in range(restbits):
					b |= (row[bytecount*8+i]) << (7-i)
				byterowlist.append(b)
			#print "row", byterowlist
			#print len(byterowlist)
			bytelist.extend(byterowlist)
		row = booleanmask[0]
		bytecount = len(row) / 8
		restbits = len(row) - bytecount*8
		bytesperrow = bytecount
		if restbits:
			bytesperrow += 1
		maskdata = numpy.array(bytelist, numpy.Byte).tostring()
		return maskdata

	def plotRgbImage(self, image, mask2d=None):
		kaplot.info("plotRgbImage not implemented yet")

	def drawIndexedImage(self, data2d, colormap, function="linear", matrix=None, mask2d=None):
		colormap = kaplot.utils.getColormap(colormap)
		function = kaplot.utils.getFunction(function)

		self.gsave()
		self.setClippath()
		#self.outputMatrix()
		data2d = numpy.array(data2d)
		datamin = data2d.min()
		datamax = data2d.max()
		scale = 255.0 / (datamax - datamin)
		data2d = ((data2d - datamin) * scale)
		lutstr = "<"
		for i in range(0, 256):
			index = function(i/256.0)
			#index = Numeric.clip(index, 0.0, 1.0)
			color = colormap(index)
			r = color.r * 255
			g = color.g * 255
			b = color.b * 255
			lutstr += "%0.2x%0.2x%0.2x " % (r, g, b)
		lutstr = lutstr[:-1]
		lutstr += ">"
		height, width = data2d.shape

		data = None
		data = numpy.array(data2d.flat).astype(numpy.int8).tostring()
		datastring = data.encode("hex")

		worldmatrix = self.getWorldMatrix()
		viewportmatrix = self.getViewportMatrix()
		devicematrix = self.getDeviceMatrix()
		#print matrix
		matrix = (devicematrix * viewportmatrix  * worldmatrix * \
					Matrix.translate((0.5, 0.5)) * matrix * Matrix.translate((0,height)) *\
					Matrix.scale(width, -height))
		m = matrix
		self.write("%f %f %f %f %f %f cm\n" % (m.xx, m.xy, m.yx, m.yy, m.tx, m.ty))

		indexedlutstring = "[/Indexed /DeviceRGB 255 %s]" % lutstr
		if mask2d != None:
			maskObject = self.pdfDoc.createObject(Type="/XObject",
							Subtype="/Image", Width=width, Height=height,
							ColorSpace=indexedlutstring, BitsPerComponent=1,
							Length=len(datastring)+1, Filter="/ASCIIHexDecode",
							stream=datastring+">")
			dataMaskedObject = self.pdfDoc.createObject(Type="/XObject",
							Subtype="/Image", Width=width, Height=height,
							ColorSpace=indexedlutstring, BitsPerComponent=8,
							Length=len(datastring)+1, Filter="/ASCIIHexDecode",
							Mask=maskObject.ref(),
							stream=datastring+">")
			maskdata = numpy.where(mask2d >= 1, 0, 0x1).astype(numpy.Byte)
			maskstring = self._createMaskBitmap(maskdata).encode("hex")
			maskId = self._getId()
			self.objects.append(datamaskdict % (imageId, width, height, indexedlutstring, len(datastring)+1, maskId, datastring))
			self.objects.append(maskdict % (maskId, width, height, len(maskstring)+1, maskstring))
			maskName = "kaplotmask%i" % maskObject.id
			dataMaskedName = "kaplotmaskedimage%i" % dataMaskedObject.id
			self.pdfDoc.getCurrentPage().xobjects.values[maskName] = maskObject.ref()
			self.pdfDoc.getCurrentPage().xobjects.values[dataMaskedName] = dataMaskedObject.ref()
			self.write("/%s Do\n" % dataMaskedName)
		else:
			dataObject = self.pdfDoc.createObject(Type="/XObject",
							Subtype="/Image", Width=width, Height=height,
							ColorSpace=indexedlutstring, BitsPerComponent=8,
							Length=len(datastring)+1, Filter="/ASCIIHexDecode",
							stream=datastring+">")
			dataName = "kaplotimage%i" % dataObject.id
			self.pdfDoc.getCurrentPage().xobjects.values[dataName] = dataObject.ref()
			self.write("/%s Do\n" % dataName)

		self.grestore()

	def _setAlpha(self):
		if self.pdfDoc:
			if self._alpha in self.alphaMap:
				name, alphaObject = self.alphaMap[self._alpha]
			else:
				alphaObject = self.pdfDoc.createObject(Type="/ExtGState",
								CA=self._alpha, ca=self._alpha, AIS="false", SA="true")
				name = "gstate%i" % alphaObject.id
				self.alphaMap[self._alpha] = (name, alphaObject)

			self.pdfDoc.getCurrentPage().gstates.values[name] = alphaObject.ref()
			self.write("/%s gs\n" % name)

	def _setFillstyle(self):
		#self._fillstyle = fillstyle
		pass

	def _setLinestyle(self):
		dasharray = kaplot.utils.getLinestyle(self._linestyle)
		# scale the dasharray with respect to the current linewidth
		linewidth, units = kaplot.utils.splitDimension(self._linewidth)
		linewidthpx = kaplot.utils.convertToPixels(linewidth, units, dpi=self.dpi)
		linewidthpt = kaplot.utils.convertPixelsTo(linewidthpx, "pt", dpi=self.dpi)
		dasharray = [k*linewidthpt for k in dasharray]
		dasharraystr = repr(dasharray).replace(", ", " ")
		code = "%s 0 d" % dasharraystr
		#print code
		self.writeln(code)

	def outputFillstyle(self):
		if self.pdfDoc:
			if self._fillstyle == "fill":
				pass
			elif self._fillstyle in kaplot.patterns:
				pattern = kaplot.patterns[self._fillstyle]
				patternSize = self._patternsize
				patternSize, patternUnits = kaplot.utils.splitDimension(patternSize)
				patternSizePixels = kaplot.utils.convertToPixels(patternSize, patternUnits, dpi=self.dpi)
				patternSizePt = kaplot.utils.convertPixelsTo(patternSizePixels, "pt", dpi=self.dpi)
				r, g, b = self._color.getRGB()
				colorcode = "%f %f %f RG %f %f %f rg\n" % (r, g, b, r, g, b)
				width = patternSizePt
				height = width
				bbox = "[0 0 %i %i]" % (width, width)
				matrix = kaplot.matrix.Matrix.rotate(pattern.angle)
				#m = matrix.matrix
				#matrix = "[%f %f %f %f %f %f]" % (m[0][0], m[1][0], m[0][1], m[1][1], m[0][2], m[1][2])
				m = matrix
				matrix = "[%f %f %f %f %f %f]" % (m.xx, m.xy, m.yx, m.yy, m.tx, m.ty)
				codestring = colorcode + " "
				# TODO: parts
				xlistlist, ylistlist = pattern.getXY(0)
				for xlist, ylist in zip(xlistlist, ylistlist):
					codestring += "%f %f m" % (xlist[0]*width, ylist[0]*height)
					for xvalue, yvalue in zip(xlist[1:], ylist[1:]):
						codestring += " %f %f l" % (xvalue*width, yvalue*height)
					if pattern.solid:
						codestring += " f"
					else:
						codestring += " S"
					codestring += "\n"

				pdfResource = PdfDict(ProcSet="[/PDF]")
				fillObject = self.pdfDoc.createObject(Type="/Pattern",
							PatternType=1, PaintType=1, TilingType=1,
							BBox=bbox, XStep=width, YStep=width,
							Resources=pdfResource, Matrix=matrix,
							stream=codestring, Length=len(codestring)+1)
				name = "kaplotpattern%i" % fillObject.id
				self.pdfDoc.getCurrentPage().patterns.values[name] = fillObject.ref()
				self.write("/Pattern cs\n")
				self.write("/%s scn\n" % name)
			else:
				kaplot.info("unknown fillstyle %r, assuming 'fill'" % self._fillstyle)


	def drawText(self, text, x, y, halign, valign, textangle=0):
		self.gsave()
		self.initmatrix()

		matrix = self.getCurrentMatrix()
		position = matrix * (x, y)

		m = matrix.inverse()
		self.pushWorld((m * (0, 0), m * (1, 1)))

		self.drawText__(text, position, halign, valign, textangle)
		self.popWorld()

		self.grestore()

	def outputGlyph(self, glyphName, textState, font, ftmatrix, drawCallable):
		dx, dy = drawCallable(font, 1<<16, 0, 0, 1<<16, 0, 0)
		# TODO: this bbox is too large in general, and too small for
		# large fonts
		bbox = "[-1000 -1000 1000 1000]"
		glyphcode = self.ciw.getBufferValue()
		glyphcode += " f\n"
		#glyphcode = glyphcode.encode("zlib").encode("hex")
		self.ciw.clearBuffer()
		pdfResource = PdfDict(ProcSet="[/PDF]")
		glyphXObject = self.pdfDoc.createObject(Type="/XObject",
					Subtype="/Form", BBox=bbox, FormType=1,
					#Filter="[/ASCIIHexDecode /FlateDecode]",
					Resources=pdfResource, Name="/"+glyphName,
					stream=glyphcode, Length=len(glyphcode)+1)
		self._glyphCache2[glyphName] = glyphXObject
		return dx, dy, True

	def drawCachedGlyph(self, glyphName, textState, font, ftmatrix):
		scale16 = 1.0/(1<<16)
		scale6 = 1.0/(1<<6)

		a, b, c, d, tx, ty = ftmatrix

		color = kaplot.utils.decodeColor(textState.color)
		red, green, blue = color.getRGB()

		matrixcode = "%f %f %f %f %f %f cm" % \
			(a*scale16, c*scale16, b*scale16, d*scale16, tx*scale6, ty*scale6)

		self.gsave()
		self.writeln("%f %f %f RG %f %f %f rg\n" % (red, green, blue, red, green, blue))
		self.writeln(matrixcode)
		self.write("/%s Do\n" % glyphName)
		print glyphName
		self.grestore()

		glyphXObject = self._glyphCache2[glyphName]
		self.pdfDoc.getCurrentPage().xobjects.values[glyphName] = glyphXObject.ref()

	def _drawSymbol(self, x, y, symbolName, xscales, yscales, angles, colors=None, colormap=None):
		symbolSizeStr = self._symbolsize
		symbolSize, symbolUnits = kaplot.utils.splitDimension(symbolSizeStr)
		symbolSizePixels = kaplot.utils.convertToPixels(symbolSize, symbolUnits, dpi=self.dpi)
		symbolSizePt = kaplot.utils.convertPixelsTo(symbolSizePixels, "pt", dpi=self.dpi)
		width, height = symbolSizePt, symbolSizePt

		symbol = kaplot.markers.symbols[symbolName]
		# TODO: parts
		xlist, ylist = symbol.getXY(0)

		pathData = "%f %f m " % (xlist[0]*width, ylist[0]*height)
		for xvalue, yvalue in zip(xlist[1:], ylist[1:]):
			pathData += "%f %f l " % (xvalue*width, yvalue*height)
		if symbol.solid:
			pathData += "f "
		else:
			pathData += "S "

		symbolId = symbolName+symbolSizeStr
		bbox = "[-10 -10 %f %f]" % (width*2, height*2)
		symbolcode = pathData.encode("zlib").encode("hex")

		pdfResource = PdfDict(ProcSet="[/PDF]")
		#symbolcode += ">"
		symbolXObject = self.pdfDoc.createObject(Type="/XObject",
					Subtype="/Form", BBox=bbox, FormType=1,
					Filter="[/ASCIIHexDecode /FlateDecode]",
					Resources=pdfResource, Name="/"+symbolId,
					stream=symbolcode, Length=len(symbolcode)+1)
		self.pdfDoc.getCurrentPage().xobjects.values[symbolId] = symbolXObject.ref()

		# TODO: getCurrentMatrix inconsistent naming(_getTotalMatrix etc)
		xlist, ylist = mulXY(self.getCurrentMatrix(), x, y)
		self.gsave()
		r, g, b = self._color.getRGB()
		self.writeln("%f %f %f RG %f %f %f rg\n" % (r, g, b, r, g, b))
		codebuffer = StringIO()
		if colors is not None:
			colors = numpy.array(colors)
			delta = colors.max() - colors.min()
			if delta == 0:
				delta = 1
			colors = (colors - colors.min()) / delta
			colormap = kaplot.utils.getColormap(colormap)
			for x, y, color in zip(xlist, ylist, colors):
				color = colormap(color)
				r, g, b = color.getRGB()
				colorcode = "%f %f %f RG %f %f %f rg\n" % (r, g, b, r, g, b)
				matrixcode = "1 0 0 1 %f %f cm" % (x-width/2, y-height/2)
				codebuffer.write("q %s %s /%s Do Q " % (matrixcode, colorcode, symbolId))
		else:
			for x, y in zip(xlist, ylist):
				matrixcode = "1 0 0 1 %f %f cm" % (x-width/2, y-height/2)
				codebuffer.write("q %s /%s Do Q " % (matrixcode, symbolId))

		code = codebuffer.getvalue()
		compressedcode = code.encode("zlib")

		overhead = 20 # this is an estimate
		# the compressed code doesn't always seem to work..
		# examples\quick\graphwitherrors.py
		if False: #len(compressedcode) - overhead < code:
			compressedcode = compressedcode.decode("zlib")
			symbolPlotCode = compressedcode
			bbox = "[0 0 %f %f]" % (self.pointWidth, self.pointHeight)
			symbolPlotId = symbolId+str(self._getId())
			pdfResource = PdfDict(ProcSet="[/PDF]")
			symbolPlotXObject = self.pdfDoc.createObject(Type="/XObject",
						Subtype="/Form", BBox=bbox, FormType=1,
						#Filter="/FlateDecode",
						Resources=pdfResource, Name="/"+symbolPlotId,
						stream=symbolPlotCode, Length=len(symbolPlotCode))
			self.pdfDoc.getCurrentPage().xobjects.values[symbolPlotId] = symbolPlotXObject.ref()
			self.writeln("/%s Do" % symbolPlotId)
		else:
			self.writeln(code)
		self.grestore()


	def _setLinewidth(self):
		linewidth, units = kaplot.utils.splitDimension(self._linewidth)
		linewidthpx = kaplot.utils.convertToPixels(linewidth, units, dpi=self.dpi)
		linewidthpt = kaplot.utils.convertPixelsTo(linewidthpx, "pt", dpi=self.dpi)
		self.writeln("%f w" % (float(linewidthpt)))

	def _convertUnits(self, value, outputUnits="pt"):
		value, units = kaplot.utils.splitDimension(value)
		v = kaplot.vector.Vector(value, value)
		nv = self.getUnitMatrix(units) * v
		v = self.getUnitMatrix(outputUnits).inverse() * nv
		value = min(v.x, v.y)
		return value

	def _setClipping(self, clipping):
		self._clipping = clipping
		print "clipping =", self._clipping

	def setClippath(self):
		#return
		#self.writeln("initclip")
		if self._clipping:
			viewportmatrix = self.getViewportMatrix()
			devicematrix = self.getDeviceMatrix()
			matrix = devicematrix * viewportmatrix
		else:
			matrix = self.getDeviceMatrix()
		p0 = matrix * (0, 0)
		p1 = matrix * (0, 1)
		p2 = matrix * (1, 1)
		p3 = matrix * (1, 0)
		#self.initmatrix()
		self.writeln("%f %f m" % (p0[0], p0[1]))
		self.writeln("%f %f l" % (p1[0], p1[1]))
		self.writeln("%f %f l" % (p2[0], p2[1]))
		self.writeln("%f %f l" % (p3[0], p3[1]))
		self.writeln("h") # closepath
		self.writeln("W") # clip
		self.newpath()

	def setClipRegion(self):
		#self.setClippath()
		pass

	def hardcopy(*args):
		kaplot.info("FIXME", "pdfdevice.hardcopy not implemented")



class PdfDevice(PdfDeviceBase):
	def __init__(self, filename="kaplot.pdf"):
		PdfDeviceBase.__init__(self)

		self.filename = filename

	def preDraw(self, document):
		self.file = open(self.filename, "wb")
		super(PdfDevice, self).preDraw(document)


