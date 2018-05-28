# -*- coding: utf-8 -*-
"""
Document sources
 * PostScript Language Reference, Third Edition (PDF: 7.5M)
   * http://partners.adobe.com/public/developer/en/ps/PLRM.pdf
 * PostScript Language Document Structuring Conventions (DSC)
 		Specification Version 3.0 #5001 (PDF: 521k)
   * http://partners.adobe.com/public/developer/en/ps/5001.DSC_Spec.pdf
  * Encapsulated PostScript (EPS) File Format Specification
  		Version 3.0 #5002 (PDF: 182k)
    * http://partners.adobe.com/public/developer/en/ps/5002.EPSF_Spec.pdf


PS guidelines:
 * keep lines <= 255 (TODO)
  * also comments, '%%+' on next line (TODO)
 * binary code is ok
 * showpage after save/restore
 * do not use these, or with care (TODO)
	 banddevice framedevice quit setpagedevice
	 clear grestoreall renderbands setscreen
	 cleardictstack initclip setglobal setshared
	 copypage initgraphics setgstate settransfer
	 erasepage initmatrix sethalftone startjob
	 exitserver nulldevice setmatrix undefinefont
  (only setmatrix is used, but using the CTM, which is ok
  according to PS Language Reference Manual Appendix I)

"""
import time
import math
import textwrap
from cStringIO import StringIO

from kaplot.matrix import Matrix
import kaplot.devices.devicebase
import kaplot.utils
import kaplot.vector
import kaplot.cext._kaplot
import numpy
from kaplot.cext._pyfont import FT_LOAD_NO_HINTING

onefloat = "%.2f"
twofloats = onefloat + " " + onefloat
threefloats = onefloat + " " + twofloats
fourfloats = twofloats + " " + twofloats
sixfloats = fourfloats + " " + twofloats
eightfloats = fourfloats + " " + fourfloats

class CInterfaceWrapper(object):
	def __init__(self, device):
		self.device = device
		self.buffer = StringIO()

	def clearBuffer(self):
		self.buffer = StringIO()

	def getBufferValue(self):
		return self.buffer.getvalue()

	def move_to(self, x, y):
		self.buffer.write((twofloats + " m\n") % (x, y))
		#self.device.writeln("%f %f m" % (x, y))

	def line_to(self, x, y):
		self.buffer.write((twofloats + " l\n") % (x, y))
		#self.device.writeln("%f %f l" % (x, y))

	def curve_to(self, x1, y1, x2, y2, x3, y3):
		self.buffer.write((sixfloats + " c\n") % (x1, y1, x2, y2, x3, y3))
		#self.device.writeln("%f %f %f %f %f %f c" % (x1, y1, x2, y2, x3, y3))

	def fill(self):
		self.device.writeln("gs")
		self.device.saveCTM()
		self.device.outputCTM()
		self.device.writeln(self.getBufferValue())
		self.device.restoreCTM()
		self.device.writeln("f")
		self.device.writeln("gr")
		self.clearBuffer()

	def stroke(self):
		self.device.writeln("gs")
		self.device.saveCTM()
		self.device.outputCTM()
		self.device.writeln(self.getBufferValue())
		self.device.restoreCTM()
		self.device.writeln("s")
		self.device.writeln("gr")
		self.clearBuffer()

	def setcolor(self, r, g, b):
		self.device.writeln("%f %f %f setrgbcolor" % (r, g, b))

class PSInfo(object):
	#orientation = "Portrait"
	title = "no title"
	pagelabel = "no label"

class PsDeviceBase(kaplot.devices.devicebase.DeviceBase):
	def __init__(self ):
		kaplot.devices.devicebase.DeviceBase.__init__(self)
		self._colorCode = None
		self.lastcp0 = None
		self.lastcp1 = None
		self.lastcp2 = None
		self.lastcp3 = None
		self.arrayCache = {}
		self.arrayNr = 0
		self.shortarrayNr = 0
		self.shortarrayCache = {}
		self.lastCTM = None
		self.psinfo = PSInfo()
		
	def close(self):
		pass

	def preDraw(self, document):
		#self.file = open(self.filename, "w")
		#w, wu, h, hu= kaplot.utils.splitSize(document.size)
		w, wu, h, hu= kaplot.utils.getSize(document.size)
		widthpx = kaplot.utils.convertToPixels(w, wu, document.dpi)
		heightpx = kaplot.utils.convertToPixels(h, hu, document.dpi)
		width = int(kaplot.utils.convertPixelsTo(widthpx, "pt"))
		height = int(kaplot.utils.convertPixelsTo(heightpx, "pt"))
		self.resx = width
		self.resy = height
		w, wu, h, hu= kaplot.utils.getSize(document.offset)
		offsetxpx = kaplot.utils.convertToPixels(w, wu, document.dpi)
		offsetypx = kaplot.utils.convertToPixels(h, hu, document.dpi)
		self.offsetxpt = int(kaplot.utils.convertPixelsTo(offsetxpx, "pt"))
		self.offsetypt = int(kaplot.utils.convertPixelsTo(offsetypx, "pt"))
		self.offsetx = int(kaplot.utils.convertPixelsTo(offsetxpx, "pt"))
		self.offsety = int(kaplot.utils.convertPixelsTo(offsetypx, "pt"))
		print document.extraborder
		self.extraborder = kaplot.utils.box_to_points(document.extraborder, document.dpi)
		print "EXTRA BORDER", self.extraborder
		#print document.offset
		#print "offset", offsetx, offsety

		kaplot.debug("drawting... (psdevice)")
		self.writeDSCHeader(document)
		super(PsDeviceBase, self).preDraw(document)
		kaplot.debug("pre draw")

	def preDrawPage(self, document, page):

		self.writeDSCPageHeader(page)
		#self.writeln("save") # gives problems with resources
		self.saveCTM()
		self.writeln("%f %f translate" % (self.offsetx, self.offsety))
		self.writeln("/initialpagestate gstate currentgstate def")
		self.writeln("gsave")
		#self.pushContext(self.defaultContext)
		super(PsDeviceBase, self).preDrawPage(document, page)
		kaplot.debug("pre draw page")

	def postDrawPage(self, document, page):
		super(PsDeviceBase, self).postDrawPage(document, page)
		self.popContext()
		self.writeln("%f %f translate" % (-self.offsetx, -self.offsety))
		self.writeln("grestore")
		#self.writeln("restore")
		self.showpage()
		self.writeDSCPageFooter()
		kaplot.debug("post draw page")

	def postDraw(self, document):
		super(PsDeviceBase, self).postDraw(document)
		#self.restoreCTM()
		self.writeDSCFooter()
		kaplot.debug("ended drawting (psdevice)")

	def _setPatternSize(self):
		pass

	def _setSymbolSize(self):
		pass

	def _setFontname(self):
		pass

	def _setFontsize(self):
		pass

	def saveCTM(self):
		self.writeln("matrix currentmatrix")

	def outputCTM(self, ctm=None):
		if ctm is None:
			ctm = self.getCurrentCTMCode()
		else:
			ctm = self.getCurrentCTMCode(ctm)
		code = ctm + " concat"
		self.writeln(code)

	def restoreCTM(self):
		ctm = self.getCurrentCTMCode()
		self.writeln("setmatrix")

	def writelnDSC(self, text):
		self.writeln("%%" + text)

	def writeFileHeader(self):
		self.writeln("%!PS-Adobe-3.0")

	def writeDSCHeader(self, document):
		self.writeFileHeader()
		self.writelnDSC("BoundingBox: %i %i %i %i" % (self.offsetx + self.extraborder[0], self.offsety + self.extraborder[1], 
				self.resx + self.offsetx + self.extraborder[2], self.resy + self.offsety + self.extraborder[3]))
		self.writelnDSC("Creator: kaplot %s" % kaplot.__version__)
		self.writelnDSC("CreationDate: %s" % time.asctime())
		self.writelnDSC("DocumentData: Binary")
		self.writelnDSC("Orientation: %s" % kaplot.quick.default.psorientation)
		self.writelnDSC("LanguageLevel: 2")
		self.writelnDSC("Pages: %i" % document.getPageCount())
		self.writelnDSC("Title: %s" % self.psinfo.title)
		# gs doesn't recognise this, maybe sth is wrong with this
		# self.writelnDSC("Version: %f %i" % (self.psinfo.version, self.psinfo.revision))
		self.writelnDSC("EndComments")


		self.writelnDSC("BeginProlog")
		self.writelnDSC("EndProlog")

		self.writelnDSC("BeginSetup")
		# code
		self.writeln("/l {lineto} def")
		self.writeln("/m {moveto} def")
		self.writeln("/c {curveto} def")
		self.writeln("/s {stroke} def")
		self.writeln("/f {fill} def")
		self.writeln("/tr {translate} def")
		
		self.writeln("/cc {concat} def")
		self.writeln("/gs {gsave} def")
		self.writeln("/gr {grestore} def")
		self.writeln("/xget {exch get} def")
		
		# set clippath
		#507.702412 37.925687 178.118469 663.637355 
		# 507.702412 37.925687 507.702412 178.118469 663.637355 178.118469 663.637355 37.925687 scp
		self.writeln("/scp {")
		self.writeln("newpath initclip gsave initialpagestate setgstate clippath false upath grestore")
		self.writeln("uappend clip newpath")
		self.writeln("m l l l ")
		self.writeln("closepath")
		self.writeln("clip")
		self.writeln("newpath")
		self.writeln("} def")
		
		# clear clippath
		self.writeln("/ccp {")
		self.writeln("newpath initclip gsave initialpagestate setgstate clippath false upath grestore")
		self.writeln("uappend clip newpath")
		self.writeln("} def")
		
		# execute zipped, takes 1 argument, data length
		self.writeln("/ez {currentfile exch () /SubFileDecode filter /FlateDecode filter cvx exec} def")
		
		# init file filter
		self.writeln("/iff {currentfile /ASCIIHexDecode filter /FlateDecode filter"\
						" /ReusableStreamDecode filter} def")
		
		
		self.writelnDSC("EndSetup")
		if kaplot.quick.default.psorientation == "Portait":
			pass # it's ok
		#elif

	def writeDSCPageHeader(self, page):
		# repeat n times
		#width = int(kaplot.utils.convertPixelsTo(self.resx, "pt"))
		#height = int(kaplot.utils.convertPixelsTo(self.resy, "pt"))
		width = self.resx
		height = self.resy
		label = self.psinfo.pagelabel.replace("(", "\(").replace(")", "\)")
		page = page.getPageNr() + 1
		self.writelnDSC("Page: (%s) %i" % (label, page))
		self.writelnDSC("PageBoundingBox: %i %i %i %i" % (self.offsetx + self.extraborder[0], self.offsety + self.extraborder[1], 
				self.resx + self.offsetx + self.extraborder[2], self.resy + self.offsety + self.extraborder[3]))
		self.writelnDSC("BeginPageSetup")
		self.writelnDSC("EndPageSetup")
		kaplot.debug("writeDSCPageHeader")
		# code and comments

	def writeDSCPageFooter(self):
		self.writelnDSC("PageTrailer")
		# page script

	def writeDSCFooter(self):
		self.writelnDSC("Trailer")
		self.writelnDSC("EOF")

	def getCInterface(self):
		#self.outputMatrix()
		ciw = CInterfaceWrapper(self)
		self.ciw = ciw
		self.ci = kaplot.cext._kaplot.cinterface_wrap(ciw.move_to, ciw.line_to, ciw.curve_to, ciw.fill, ciw.stroke, ciw.setcolor)
		return self.ci

	def _setColor(self):
		#color = kaplot.utils.decodeColor(color)
		r, g, b = self._color.getRGB()
		colorCode = "%f %f %f setrgbcolor\n" % (r, g, b)
		if colorCode != self._colorCode:
			self.write(colorCode)
		self._colorCode = colorCode

	def getCurrentCTM(self):
		worldmatrix = self.getWorldMatrix()
		viewportmatrix = self.getViewportMatrix()
		devicematrix = self.getDeviceMatrix()
		matrix = devicematrix * (viewportmatrix * worldmatrix)
		return matrix
		
	def getCurrentCTMCode(self, m=None):
		if m is None:
			m = self.getCurrentCTM()
		#code = "[%f %f %f %f %f %f]" % (m[0][0], m[1][0], m[0][1], m[1][1], m[0][2], m[1][2])
		code = "[%f %f %f %f %f %f]" % (m.xx, m.xy, m.yx, m.yy, m.tx, m.ty)
		return code

	def drawLine(self, x1, y1, x2, y2, gridsnap=False):
		#ctm = self.getCurrentCTMCode()
		
		#self.writeln("% line")
		m = self.getCurrentCTM()
		x1, y1 = m * (x1, y1)
		x2, y2 = m * (x2, y2)
		code = (twofloats + " m " + twofloats + " l") % (x1, y1, x2, y2)

		#if 0 or (self.lastCTM is None) or (ctm != self.lastCTM):
		#	self.writeln("gs")
		#	self.saveCTM()
		#	self.outputCTM()
		#	self.writeln(code)
		#	self.restoreCTM()
		#	self.writeln("s")
		#	self.writeln("gr")
		#else:
		self.write(code)
		self.writeln(" s")
		#self.lastCTM = ctm
		
	def drawLines(self, x1, y1, x2, y2, gridsnap=False):
		x1name = self._ensurefloatarray(numpy.array(x1))
		y1name = self._ensurefloatarray(numpy.array(y1))
		x2name = self._ensurefloatarray(numpy.array(x2))
		y2name = self._ensurefloatarray(numpy.array(y2))
		self.writeln("gs")
		#self.writeln("%f %f translate" % (m.tx-width/2, m.ty-height/2))
		#self.writeln("%f %f scale" % (m.tx-width/2, m.ty-height/2))
		#self.writeln("matrix currentmatrix")
		m = self._getTotalMatrix()
		length = min(len(x1), len(y1), len(x2), len(y2))
		kaplot.debug("length line array", length) 
		self.writeln("/getx {exch get %f mul %f add} def" % (m.xx, m.tx) )
		self.writeln("/gety {exch get %f mul %f add} def" % (m.yy, m.ty) )
		self.writeln("0 1 %d {dup dup dup %s getx exch %s gety moveto %s getx exch %s gety lineto stroke} for" % (length-1, x1name, y1name, x2name, y2name))
		self.writeln("gr")
	
	def _transformed(self, x, y):
		m = self.getCurrentCTM()
		x_out = m.xx * numpy.array(x) + m.xy * numpy.array(y) + m.tx;
		y_out = m.yx * numpy.array(x) + m.yy * numpy.array(y) + m.ty;
		return x_out, y_out


	def drawPolyLine(self, x, y, close=False, gridsnap=False):
		#self.writeln("% polyline")
		length = min(len(x), len(y))
		if 0:
			x, y = self._transformed(x, y)
			#x, y = m.mulXY(x, y)
			if length > 1:
				code = StringIO()
				code.write((twofloats + " m ") % (x[0], y[0]))
				for i in range(1, length):
					code.write((twofloats + " l ") % (x[i], y[i]))
				if close:
					code.write((twofloats + " l\n") % (x[0], y[0]))
				else:
					code.write("\n")
	
				#self.writeln("gs")
				#self.saveCTM()
				#self.outputCTM()
				#self.writeln(code.getvalue())
				self.writeln2(code.getvalue() + " s")
				#self.restoreCTM()
				#self.writeln("s")
				#self.writeln("gr")
		else:
			m = self._getTotalMatrix()
			xname = self._ensurefloatarray(numpy.array(x))
			yname = self._ensurefloatarray(numpy.array(y))
			#self.writeln("gs")
			#self.writeln("%f %f translate" % (m.tx-width/2, m.ty-height/2))
			#self.writeln("%f %f scale" % (m.tx-width/2, m.ty-height/2))
			#self.writeln("matrix currentmatrix")
			length = min(len(x), len(y))
			#self.writeln("0 0 %s exch get %f mul %f add exch %s exch get %f mul %f add moveto " % (xname, m.xx, m.tx, yname, m.yy, m.ty))
			self.writeln("0 1 %d {dup %s xget %f mul %f add exch dup %s xget %f mul %f add exch 0 eq {moveto} {lineto} ifelse } for " % (length-1, xname, m.xx, m.tx, yname, m.yy, m.ty))
			if close:
				self.writeln(" closepath")
			self.writeln(" stroke")
			#self.writeln("gr")
			

	def drawPolygon(self, x, y, gridsnap=False):
		self.writeln("% polygon")
		x, y = self._transformed(x, y)
		length = min(len(x), len(y))
		if length > 1:
			code = ""
			code += "%f %f m\n" % (x[0], y[0])
			for i in range(1, length):
				code += "%f %f l\n" % (x[i], y[i])

			self.writeln("gs")
			#self.saveCTM()
			#self.outputCTM()
			self.writeln(code)
			#self.restoreCTM()
			self.outputPattern()
			self.writeln("f")
			self.writeln("gr")

	def drawRgbImage(self, image, mask2d=None):
		self.writeln("% rgbimage")
		return
		self.writeln("gsave")
		self.setClippath()
		self.outputMatrix()
		self.writeln("0.5 0.5 translate")
		import pdb
		#pdb.set_trace()
		import Image
		width, height = image.size
		if not isinstance(image, Image.Image):
			raise Exception, "image should be a PIL Image instance"




		self.writeln("[/DeviceRGB 255] setcolorspace")

		# /Interpolated true
		datadict = "<< /ImageType 1 /Width %i /Height %i /BitsPerComponent 8 /Decode [0 1 0 1 0 1] /ImageMatrix [1 0 0 1 0 0] /DataSource currentfile /ASCIIHexDecode filter /FlateDecode filter >>" % (width, height)
		maskdict = "<< /ImageType 1 /Width %i /Height %i /BitsPerComponent 1 /Decode [1 0] /ImageMatrix [1 0 0 1 0 0] /DataSource currentfile /ASCIIHexDecode filter /FlateDecode filter >>"  % (width, height)

		# TODO, make sure the lines are < 255 chars
		if mask2d != None:
			self.write("""<< /ImageType 3 /MaskDict %s  /DataDict %s /InterleaveType 3 >> image """ % (maskdict, datadict))
			maskdata = self._createMaskBitmap(mask2d)
			maskdatastring = maskdata.encode("zlib").encode("hex")
			self.write(maskdatastring)
		else:
			self.write("%s image\n" % datadict)

		hexstring = image.transpose(Image.FLIP_TOP_BOTTOM).tostring()
		datastring = hexstring.encode("zlib").encode("hex")
		self.writeln(datastring)
		self.flush()
		self.writeln("grestore")


	#def drawIndexedImage(self, data2d, colormap, function="linear", mask2d=None, matrix=None):#, colormap, datamin, datamax, function):
	def drawIndexedImage(self, data2d, colormap, function="linear", mask2d=None, matrix=None, datamin=None, datamax=None):
		#if matrix:
		#	kaplot.info("matrix argument not implemented for ps device")
		self.writeln("% indexed image")
		colormap = kaplot.utils.getColormap(colormap)
		function = kaplot.utils.getFunction(function)
		
		if matrix is None:
			matrix = kaplot.Matrix()
		#m = self.getDeviceMatrix() * self.getViewportMatrix() * self.getWorldMatrix() *\
		#		kaplot.Matrix.translate(0.5, 0.5) * \
		#		matrix * kaplot.Matrix.translate(-0.5, -0.5)
		m = self.getDeviceMatrix() * self.getViewportMatrix() * self.getWorldMatrix() *\
				matrix *\
				kaplot.Matrix.translate(-1.0, -1.0)
		self.writeln("gs")
		self.saveCTM()
		self.outputCTM(m)
		matrix = kaplot.Matrix()

		data2d = numpy.array(data2d)
		if datamin == None:
			datamin = data2d.min()
		if datamax == None:
			datamax = data2d.max()
		scale = 255.0 / (datamax - datamin)
		data2d = ((data2d - datamin) * scale)
		data2d = numpy.clip(data2d, 0, 255)
		lutstr = "<"
		offset = 0
		for i in range(0, 256):
			#index = i/256.0
			index = function(i/255.0)
			#index = Numeric.clip(index, 0.0, 1.0)
			color = colormap(index)
			r = color.r * 255
			g = color.g * 255
			b = color.b * 255
			#r = 0
			#g = i
			#b = 0
			lutstr += "%0.2x%0.2x%0.2x " % (r, g, b)
			# we dont want lines > 255 chars
			if len(lutstr) - offset > 200:
				offset += 200
				lutstr += "\n"
		lutstr = lutstr[:-1]
		lutstr += ">"
		height, width = data2d.shape
		self.writeln("0.5 0.5 translate")

		self.writeln("[/Indexed /DeviceRGB 255 %s] setcolorspace" % lutstr)

		# /Interpolated true
		#datadict = "<< /ImageType 1 /Width %i /Height %i /BitsPerComponent 8 /Decode [0 255] /ImageMatrix [1 0 0 1 0 0] /DataSource currentfile /ASCIIHexDecode filter /FlateDecode filter >>" % (width, height)
		#maskdict = "<< /ImageType 1 /Width %i /Height %i /BitsPerComponent 1 /Decode [1 0] /ImageMatrix [1 0 0 1 0 0] /DataSource currentfile /ASCIIHexDecode filter /FlateDecode filter >>"  % (width, height)
		#datadict = "<< /ImageType 1 /Width %i /Height %i /BitsPerComponent 1 /Decode [0 255] /ImageMatrix [1 0 0 1 0 0] /DataSource currentfile /ASCIIHexDecode filter >>" % (width, height)
		#maskdict = "<< /ImageType 1 /Width %i /Height %i /BitsPerComponent 8 /Decode [0 1] /ImageMatrix [1 0 0 1 0 0] /DataSource currentfile /ASCIIHexDecode filter >>"  % (width, height)

		#maskdict = "<< /ImageType 1 /MultipleDataSource true /Width %i /Height %i /BitsPerComponent 1 /Decode [1 0] /ImageMatrix [1 0 0 1 0 0] /DataSource currentfile /ASCIIHexDecode filter /FlateDecode filter >>"  % (width, height)
		matrix = matrix.inverse()
		datadict = "<< /ImageType 1 /Interpolated true /Width %i /Height %i" \
					" /BitsPerComponent 8 /Decode [0 255] /ImageMatrix [%f 0 0 %f %f %f]" \
					" /DataSource currentfile /ASCIIHexDecode filter /FlateDecode filter >>" % (width, height, matrix.xx, matrix.yy, matrix.tx, matrix.ty)
		maskdict = "<< /ImageType 1 /Interpolated true /Width %i /Height %i"\
					" /BitsPerComponent 8 /Decode [1 0] /ImageMatrix [1 0 0 1 0 0]" \
					" /ASCIIHexDecode filter /FlateDecode filter >>"  % (width, height)

		data = None

		if mask2d != None:
			#import pdb
			#pdb.set_trace()
			maskdata = numpy.where(mask2d >= 1, 0xff, 0).astype(numpy.byte)
			#maskdata = self._createMaskBitmap(data2d)
			#a = numpy.array((maskdata.flat, data2d.flat), numpy.byte)
			a = numpy.hstack([maskdata.flat, data2d.flat])
			a = a.astype(numpy.byte)
			#a = numpy.array((data2d, maskdata), numpy.Byte)
			a.transpose()
			data = a.tostring()
			self.write("<< /ImageType 3 /MaskDict %s /DataDict %s /InterleaveType 1 >> image " % (maskdict, datadict))
			# TODO: why is this commented out??, and make sure the lines are < 255 chars
			#maskdatastring = maskdata.encode("hex")
			#self.writeln(maskdatastring)
			#self.writeln(">")
		else:
			data = numpy.array(data2d.flat).astype(numpy.int8).tostring()
			self.write("%s image\n" % datadict)


		# we dont want lines > 255 chars
		datastring = data.encode("zlib").encode("hex")
		self.writeHexData(datastring)
		self.writeln(">")
		self.flush()

		self.restoreCTM()
		self.writeln("gr")

	def writeHexData(self, datastring):
		lines = (len(datastring)+252)/253
		for lineNr in range(lines):
			self.writeln(datastring[lineNr*253:(lineNr+1)*253])

	def drawText(self, text, x, y, halign, valign, textangle=0):
		#self.writeln("%%text: %s" % text)
		self.setClipRegion()

		worldmatrix = self.getWorldMatrix()
		viewportmatrix = self.getViewportMatrix()
		devicematrix = Matrix.scale(self.resx, self.resy)
		matrix = devicematrix * (viewportmatrix * worldmatrix)
		position = matrix * (x, y)

		m = self._getTotalMatrix()
		self.pushWorld((m * (0, 0), m * (1, 1)))
		if text == "3.0":
			if y > 1e4:
				import pdb; pdb.set_trace()
			print text, position
			print x, y
			print worldmatrix
			print viewportmatrix
			print devicematrix
			
			print matrix
		self.drawText__(text, position, halign, valign, textangle)
		self.popWorld()

	def writeln2(self, codestring):
		# TODO, this isn't beging used, but it could make postscript files alot smaller
		cstring = codestring.encode("zlib") #.encode("hex")
		if len(cstring) > len(codestring):
			kaplot.info("encoded string of length %i to length %i" % (len(codestring), len(cstring)))
		self.writeln("%d ez" % len(cstring))
		#self.writeln("currentfile /ASCIIHexDecode filter /FlateDecode filter cvx exec")
		self.writeln(cstring)
		#self.writeHexData(cstring)
		#self.writeln(">")
		#print len(codestring), len(cstring)

	def _ensureshortarray(self, ar):
		raise "dont use"
		arstr = (ar).astype(numpy.uint16).tostring()
		if arstr in self.shortarrayCache:
			arname = self.shortarrayCache[arstr]
			kaplot.debug("using cache(short int)", len(arstr))
		else:
			arname = "sharr" + str(self.shortarrayNr)
			self.shortarrayNr += 1 
			self.shortarrayCache[arstr] = arname
			self.writeln("\n%%BeginBinary: " +str(len(arname) + 2+2+2+len(arstr)))
			self.write("/%s " % arname)
			self.write(numpy.array([149,128+32]).astype(numpy.uint8).tostring())
			self.write(numpy.array([len(x)]).astype(numpy.uint16).tostring())
			#self.write(numpy.array([149,49+128]).astype(numpy.uint8).tostring())
			#self.write(numpy.array([len(x)]).astype(numpy.uint16).tostring())
			self.write(arstr)
			self.write("\n%%EndBinary\n")
			self.write(" def ")
		return arname
		
	def _ensurefloatarray(self, ar):
		#raise "bla"
		arstr = (ar).astype(numpy.float32).tostring()
		if arstr in self.arrayCache:
			arname = self.arrayCache[arstr]
			kaplot.debug("using cache(float)", len(arstr))
		else:
			arname = "flarr" + str(self.arrayNr)
			self.arrayNr += 1 
			self.arrayCache[arstr] = arname
			if 0:
				self.writeln("\n%%BeginData: " +str(len(arname) + 2+2+2+len(arstr)+1) + " Binary Bytes" )
				self.write("/%s " % arname)
				#self.write(numpy.array([149,128+32]).astype(numpy.uint8).tostring())
				#self.write(numpy.array([len(x)]).astype(numpy.uint16).tostring())
				self.write(numpy.array([149,48+128]).astype(numpy.uint8).tostring())
				self.write(numpy.array([len(ar)]).astype(numpy.uint16).tostring())
				self.write(arstr)
				self.write("\n%%EndData\n")
				self.write(" def ")
			else:
				#print ar, `ar`, len([1,2]), ar[0]
				self.write("/%s [" % arname)
				#ar2 = list(ar)
				#l = len(ar)
				for i in range(len(ar)):
					self.write("%f " % ar[i])
				self.write("] def\n")
				
		return arname
		
	def _drawSymbol(self, x, y, symbolName, xscales, yscales, angles, colors=None, colormap=None):
		symbolSize = self._symbolsize
		symbolSize, symbolUnits = kaplot.utils.splitDimension(symbolSize)
		symbolSizePixels = kaplot.utils.convertToPixels(symbolSize, symbolUnits, dpi=self.dpi)
		symbolSizePt = kaplot.utils.convertPixelsTo(symbolSizePixels, "pt", dpi=self.dpi)
		#symbolSizePixels
		width, height = float(symbolSizePt), float(symbolSizePt)

		self.writeln("gsave")
		if 0:
			symbol = kaplot.markers.symbols[symbolName]
			codestring = ""
			for part in range(symbol.parts):
				xlist, ylist = symbol.getXY(part)
				codestring += (twofloats +" m ") % (xlist[0]*width, ylist[0]*height)
				for xvalue, yvalue in zip(xlist[1:], ylist[1:]):
					codestring += (" " + twofloats +" l ") % (xvalue*width, yvalue*height)
				if symbol.solid:
					codestring += " f "
				else:
					codestring += " s "
				codestring += "\n"
	
			cstring = codestring.encode("zlib") #.encode("hex")
			# create a reusable file stream
			self.writeln("/%sfile currentfile %d () /SubFileDecode filter /FlateDecode filter"\
							" /ReusableStreamDecode filter" % (symbolName, len(cstring)))
			#self.writeHexData(cstring)
			self.writeln(cstring)
			self.writeln("def")
			# create a reusable data stream
			self.writeln("/%(name)sdata { %(name)sfile dup 0 setfileposition } def" % {"name":symbolName})
			# create a reusable exec block
			self.writeln("/%(name)s { %(name)sdata cvx exec } def" % {"name":symbolName})
		else:
			symbol = kaplot.markers.symbols[symbolName]
			codestring = "/sympath { "
			xmin, ymin, xmax, ymax = 0, 0, 0, 0
			for part in range(symbol.parts):
				xlist, ylist = symbol.getXY(part)
				xlist, ylist = numpy.array(xlist), numpy.array(ylist)
				xmin = min(min(xlist*width), xmin)
				ymin = min(min(ylist*height), ymin)
				xmax = max(max(xlist*width), xmax)
				ymax = max(max(ylist*height), ymax)
			#codestring += "%f %f %f %f setbbox " % (xmin, ymin, xmax, ymax) 
			for part in range(symbol.parts):
				xlist, ylist = symbol.getXY(part)
				codestring += (twofloats +" moveto ") % (xlist[0]*width, ylist[0]*height)
				for xvalue, yvalue in zip(xlist[1:], ylist[1:]):
					codestring += (" " + twofloats +" lineto ") % (xvalue*width, yvalue*height)
			codestring += " }  def"
			codestring += "\n"
			if symbol.solid:
				codestring += "/sym {sympath fill} def\n"
				drawop = "fill"
			else:
				codestring += "/sym {sympath stroke} def\n"
				drawop = "stroke"
			self.writeln(codestring)
	

		m = self._getTotalMatrix()
		#xlist, ylist = (self._getTotalMatrix()).mulXY(x, y)
		x = numpy.array(x)
		y = numpy.array(y)
		xlist = x
		ylist = y
		length = min(len(x), len(y))
		# we can't push it all on stack, since that can generate a stack overflow
		count = 0
		buffer = StringIO()
		maxlength = 150
		self.writeln("matrix currentmatrix\n")
		
		
		if xscales is None and yscales is None and angles is None:
			if colors is not None:
				if 0:
					self.writeln(("/y {translate " + twofloats +" translate setrgbcolor %s dup setmatrix} def") % (-width/2.0, -height/2.0, symbolName))
					#template = "%i {matrix currentmatrix 6 1 roll translate %f %f translate setrgbcolor %s  setmatrix} repeat\n"
					colors = numpy.array(colors)
					#delta = colors.max() - colors.min()
					#if delta == 0:
					#	delta = 1
					#colors = (colors - colors.min()) / delta
					colormap = kaplot.utils.getColormap(colormap)
					for i, (x, y, color) in enumerate(zip(xlist, ylist, colors)):
						color = colormap(color)
						r, g, b = color.getRGB()
						buffer.write((fourfloats + "y ") % (r, g, b, x+m.tx, y+m.ty))
						#if (i > 0) and (i % maxlength == 0):
						#	count += maxlength
						#	buffer.write(template % (maxlength, -width/2.0, -height/2.0, symbolName))
					#if (length - count) > 0:
					#	buffer.write(template % (length-count, -width/2.0, -height/2.0, symbolName))
				else:
					rs, gs, bs = [], [], []
					colormap = kaplot.utils.getColormap(colormap)
					for color in colors:
						color = colormap(color)
						r, g, b = color.getRGB()
						rs.append(r)
						gs.append(g)
						bs.append(b)
					#rname = 
					xname = self._ensurefloatarray(numpy.array(x))
					yname = self._ensurefloatarray(numpy.array(y))
					colorscale = 32000.
					rname = self._ensurefloatarray(numpy.array(rs)*colorscale)
					gname = self._ensurefloatarray(numpy.array(gs)*colorscale)
					bname = self._ensurefloatarray(numpy.array(bs)*colorscale)
					self.writeln("gs")
					self.writeln("matrix currentmatrix")
					#self.writeln("%f %f translate" % (m.tx-width/2, m.ty-height/2))
					#self.writeln("%f %f scale" % (m.tx-width/2, m.ty-height/2))
					#self.writeln("matrix currentmatrix")
					self.writeln("/setcolor {dup %s xget %d div exch dup %s xget %d div exch %s xget %d div setrgbcolor} def" % (rname, colorscale, gname, colorscale, bname, colorscale))
					self.writeln("0 1 %d {dup dup setcolor %s exch get %f mul %f add exch %s exch get %f  mul %f add translate sympath dup setmatrix %s} for" % (length-1, xname, m.xx, m.tx-width/2, yname, m.yy, m.ty-height/2, drawop))
					self.writeln("pop")
					self.writeln("gr")
					
			else:
				if 0:
					self.writeln(("/y {translate " +twofloats +" translate sym dup setmatrix} def") % (-width/2.0, -height/2.0))
					for i, (x, y) in enumerate(zip(xlist, ylist)):
						buffer.write((twofloats +" y ") % (x+m.tx, y+m.ty))
				else:
					assert len(x) == len(x)
					#xstr = ((xlist)*8).astype(numpy.uint16).tostring()
					if 0:
						xstr = (xlist).astype(numpy.float32).tostring()
						if xstr in self.arrayCache:
							xname = self.arrayCache[xstr]
							kaplot.debug("using cache(x)", len(xstr))
						else:
							xname = "arr" + str(self.arrayNr)
							self.arrayNr += 1 
							self.arrayCache[xstr] = xname
							self.write(" /%s " % xname)
							#self.write(numpy.array([149,128+32+3]).astype(numpy.uint8).tostring())
							#self.write(numpy.array([len(x)]).astype(numpy.uint16).tostring())
							self.write(numpy.array([149,49+128]).astype(numpy.uint8).tostring())
							self.write(numpy.array([len(x)]).astype(numpy.uint16).tostring())
							self.write(xstr)
							
							self.write(" def ")
						
						if 0:
							self.write(" /xarr ")
							self.write(numpy.array([149,49+128]).astype(numpy.uint8).tostring())
							self.write(numpy.array([len(x)]).astype(numpy.uint16).tostring())
							self.write((xlist+m.tx).astype(numpy.float32).tostring())
							self.write(" def ")
						
						#ystr = ((ylist)*8).astype(numpy.uint16).tostring()
						ystr = (ylist).astype(numpy.float32).tostring()
						if ystr in self.arrayCache:
							yname = self.arrayCache[ystr]
							kaplot.debug("using cache(y), ", len(ystr))
						else:
							yname = "arr" + str(self.arrayNr)
							self.arrayNr += 1 
							self.write(" /%s " % yname)
							#self.write(numpy.array([149,128+32+3]).astype(numpy.uint8).tostring())
							#self.write(numpy.array([len(y)]).astype(numpy.uint16).tostring())
							self.write(numpy.array([149,49+128]).astype(numpy.uint8).tostring())
							self.write(numpy.array([len(y)]).astype(numpy.uint16).tostring())
							self.write(ystr)
							self.write(" def ")
							self.arrayCache[ystr] = yname
						
						if 0:
							self.write(" /yarr ")
							self.write(numpy.array([149,49+128]).astype(numpy.uint8).tostring())
							self.write(numpy.array([len(y)]).astype(numpy.uint16).tostring())
							#self.write((ylist+m.ty).astype(numpy.float32).tostring())
							self.write(" def ")
							
					xname = self._ensurefloatarray(x)
					yname = self._ensurefloatarray(y)
					self.writeln("gs")
					self.writeln("matrix currentmatrix")
					#self.writeln("%f %f translate" % (m.tx-width/2, m.ty-height/2))
					#self.writeln("%f %f scale" % (m.tx-width/2, m.ty-height/2))
					#self.writeln("matrix currentmatrix")
					self.writeln("0 1 %d {dup %s exch get %f mul %f add exch %s exch get %f  mul %f add translate sympath dup setmatrix %s} for" % (length-1, xname, m.xx, m.tx-width/2, yname, m.yy, m.ty-height/2, drawop))
					#print ">>>", symbolName, m.xx, m.tx, width/2
					#print " ", symbol.getXY(0)
					self.writeln("pop")
					self.writeln("gr")
					#self.writeln("")
					#self.writeln("1 gs xarr 1 get yarr 1 get translate sym gr")
					#for i in range(len(x)-1):
					#	self.writeln("gs xarr %i get yarr %i get translate sym gr" % (i+1,i+1))
				#self.writeln("grestore")
				
				
				
					#if (i > 0) and (i % maxlength == 0):
					#	count += maxlength
					#	buffer.write("%i {gsave translate %f %f translate %s grestore} repeat\n" % (maxlength, -width/2.0, -height/2.0, symbolName))
				#if (length - count) > 0:
				#	buffer.write("%i {gsave translate %f %f translate %s grestore} repeat\n" % (length-count, -width/2.0, -height/2.0, symbolName))
		else:
			if xscales == None:
				xscales = ones(len(xlist))
			if yscales == None:
				yscales = ones(len(xlist))
			if angles == None:
				angles = zeros(len(xlist))
			for i, (x, y, xscale, yscale, angle) in enumerate(zip(xlist, ylist, xscales, yscales, angles)):
				buffer.write((fourfloats + "\n") % (xscale, yscale, angle*180/math.pi, x+m.tx, y+m.ty))
				if (i > 0) and (i % 10000 == 0):
					count += 10000
					buffer.write("%i {gsave translate %f %f translate %s grestore} repeat\n" % (10000, -width/2.0, -height/2.0, symbolName))
			if (length - count) > 0:
				buffer.write("%i {gsave translate %f %f translate rotate scale %s grestore} repeat\n" % (length-count, -width/2.0, -height/2.0, symbolName))
		
		#self.saveCTM()
		#self.outputCTM()
		#self.write(buffer.getvalue())
		self.writeln(buffer.getvalue())
		self.writeln("pop") # pop currentmatrix
		#self.restoreCTM()

		#print len(buffer.getvalue())
		#print len(buffer.getvalue().encode("zlib").encode("hex"))
		self.writeln("grestore")

	def _drawCharacterSymbol(self, x, y, symbol):
		symbol = unicode(symbol)
		xlist, ylist = (self._getTotalMatrix()).mulXY(x, y)
		length = min(len(x), len(y))
		if len(symbol) != 1:
			raise ValueError, "symbol should be a character(string of length 1)"
		fontname = self._fontname
		font = kaplot.text.findFont(fontname, False, False)
		if not font.has_char(symbol):
			fontList = findMatchingFontFamilies(self.font.family_name)
			for fontFamily in fontList:
				font = fontFamily.get(bold=False, italic=False)
				if font.has_char(char):
					break
			font = None
		if font != None:
			fontsizepixels = self._convertUnits(self.fontsize, "px")
			fontsize = int(fontsizepixels * 96)
			font.set_char_size(0, int(fontsize))

			result = font.get_text_metrics(symbol, FT_LOAD_NO_HINTING, True)
			width, height, advance, bearingx, bearingy = result

			cinterface = self.getCInterface()
			descend = -(height-bearingy)
			font.draw_path(symbol, cinterface, 1<<16, 0, 0, 1<<16, int(-bearingx*(1<<6)), int(-descend*(1<<6)))
			codestring = self.ciw.getBufferValue()
			self.ciw.clearBuffer()
			codestring += " fill\n"

			symbolName = "symbol1"

			cstring = codestring.encode("zlib").encode("hex")
			if 1:
				# create a reusable file stream
				#self.writeln("/%sfile currentfile /ASCIIHexDecode filter /FlateDecode filter"\
				#				" /ReusableStreamDecode filter" % symbolName)
				self.writeln("/%sfile iff" % symbolName)
				self.writeHexData(cstring)
				self.writeln("> def")
				# create a reusable data stream
				self.writeln("/%(name)sdata { %(name)sfile dup 0 setfileposition } def" % {"name":symbolName})
				# create a reusable exec block
				self.writeln("/%(name)s { %(name)sdata cvx exec } def" % {"name":symbolName})
	
				for x, y in zip(xlist, ylist):
					self.writeln("%f %f " % (x, y))
	
				self.writeln("%i {gsave translate %s grestore} repeat" % (length, symbolName))
			else:
				#self.writeln("/%(name)s { ez %(data)sdata cvx exec } def" % {"name":symbolName})
				self.writeln("/" + symbolName + " {")
				self.writeln("ez")
				self.writeHexData(cstring)
				self.writeln(">")
				self.writeln("} def")

	def outputGlyph(self, glyphName, textState, font, ftmatrix, drawCallable):
		dx, dy = drawCallable(font, 1<<16, 0, 0, 1<<16, 0, 0)
		#return dx, dy, True
		codestring = self.ciw.getBufferValue()
		self.ciw.clearBuffer()
		codestring += " fill\n"

		if 1:
			cstring = codestring.encode("zlib").encode("hex")
			# create a reusable file stream
			self.writeln("/%sfile currentfile /ASCIIHexDecode filter /FlateDecode filter"\
							" /ReusableStreamDecode filter" % glyphName)
			#self.writeln("/%sfile iff" % glyphName)
			self.writeHexData(cstring)
			self.writeln("> def")
			# create a reusable data stream
			self.writeln("/%(name)sdata { %(name)sfile dup 0 setfileposition } def" % {"name":glyphName})
			# create a reusable exec block
			self.writeln("/%(name)s { %(name)sdata cvx exec } def" % {"name":glyphName})
		else:
			cstring = codestring.encode("zlib") #.encode("hex")
			# create a reusable file stream
			self.writeln("/%sfile currentfile %d () /SubFileDecode filter /FlateDecode filter"\
							" /ReusableStreamDecode filter" % (glyphName, len(cstring)))
			#self.writeHexData(cstring)
			self.writeln(cstring)
			self.writeln("def")
			# create a reusable data stream
			self.writeln("/%(name)sdata { %(name)sfile dup 0 setfileposition } def" % {"name":glyphName})
			# create a reusable exec block
			self.writeln("/%(name)s { %(name)sdata cvx exec } def" % {"name":glyphName})
			
			#self.writeln("/" + glyphName + " {")
			#self.writeln("ez")
			#self.writeHexData(cstring)
			#self.writeln(">")
			#self.writeln("} def")
		return dx, dy, True

	def drawCachedGlyph(self, glyphName, textState, font, ftmatrix):
		scale16 = 1.0/(1<<16)
		scale6 = 1.0/(1<<6)

		a, b, c, d, tx, ty = ftmatrix

		# draw this glyph
		color = kaplot.utils.decodeColor(textState.color)
		red, green, blue = color.getRGB()
		#print "drawCachedGlyph", ftmatrix

		if a*scale16 == 1 and c*scale16==0 and b*scale16 == 0 and d*scale16 == 1:
			self.write("gs ")
			#self.writeln("%f %f %f setrgbcolor"  % (red, green, blue))
			#self.write((twofloats + " tr ") % (tx*scale6, ty*scale6))
			self.write("%f %f tr " % (float(tx)*scale6, float(ty)*scale6))
			self.write(glyphName)
			#self.write(" gr %% %s\n" % self.currentChar)
			self.write(" gr\n")
		else:
					
			matrixcode = "[%f %f %f %f %f %f] cc " % \
				(float(a)*scale16, float(c)*scale16, float(b)*scale16, float(d)*scale16, float(tx)*scale6, float(ty)*scale6)
	
			self.write("gs ")
			#self.writeln("%f %f %f setrgbcolor"  % (red, green, blue))
			self.write(matrixcode)
			self.write(" ")
			self.write(glyphName)
			self.write(" gr\n")

	def _getTotalMatrix(self):
		worldmatrix = self.getWorldMatrix()
		viewportmatrix = self.getViewportMatrix()
		devicematrix = self.getDeviceMatrix()
		matrix = devicematrix * (viewportmatrix * worldmatrix)
		return matrix

	def _moveto(self, x, y):
		self.writeln("%f %f m " % (x, y))
		self.lx = x
		self.ly = y

	def _lineto(self, x, y):
		self.writeln("%f %f l " % (x, y))
		self.lx = x
		self.ly = y

	def _conicto(self, cx,cy, x3, y3):
		self.writeln(" %f %f %f %f %f %f c " % (	self.lx + 2.0/3.0*(cx-self.lx),
							self.ly + 2.0/3.0*(cy-self.ly),
							x3 + 2.0/3.0*(cx-x3),
							y3 + 2.0/3.0*(cy-y3),
							x3,
							y3))
		self.lx = x3
		self.ly = y3

	def _cubicto(self, x1,y1,x2,y2,x3,y3):
		self.writeln("%f %f %f %f %f %f c " % (x1, y1, x2, y2, x3, y3))
		self.lx = x3
		self.ly = y3

	def _setLinestyle(self):
		#self._linestyle = linestyle
		dasharray = kaplot.utils.getLinestyle(self._linestyle)
		dasharray = [k*self._linewidthPt for k in dasharray]
		dasharraystr = repr(dasharray).replace(", ", " ")
		self.writeln("%s 0 setdash" % dasharraystr)

	def _setLinewidth(self):
		linewidth, units = kaplot.utils.splitDimension(self._linewidth)
		linewidthpx = kaplot.utils.convertToPixels(linewidth, units, dpi=self.dpi)
		linewidth = kaplot.utils.convertPixelsTo(linewidthpx, "pt", dpi=self.dpi)
		#linewidth = self._getBla(linewidth, "pt")
		self.writeln("%f setlinewidth" % linewidth)
		self._linewidthPt = linewidth

	def _setClipping(self, clipping):
		#clipping = False
		self._initClippath(clipping)
		self.clipping = clipping

	def _getBla(self, value, outputUnits="pt"):
		value, units = kaplot.utils.splitDimension(value)
		v = kaplot.vector.Vector(value, value)
		nv = self.getUnitMatrix(units) * v
		v = self.getUnitMatrix(outputUnits).inverse() * nv
		value = min(v.x, v.y)
		return value

	def _convertUnits(self, value, outputUnits="pt"):
		value, units = kaplot.utils.splitDimension(value)
		v = kaplot.vector.Vector(value, value)
		nv = self.getUnitMatrix(units) * v
		v = self.getUnitMatrix(outputUnits).inverse() * nv
		value = min(v.x, v.y)
		return value

	def _initClippath(self, clipping):
		#return
		#clipping = False
		if 0:
			self.writeln("newpath initclip gsave initialpagestate setgstate clippath false upath grestore")
			self.writeln("uappend clip newpath")
			devicematrix = self.getDeviceMatrix()
			if clipping:
				viewportmatrix = self.getViewportMatrix()
				matrix = devicematrix * viewportmatrix
			else:
				matrix = self.getDeviceMatrix()
				#return
			offset = kaplot.Vector(self.offsetx, self.offsety)
			offset = kaplot.Vector(0, 0)
			#offset = kaplot.Vector(-self.offsetx*2, -self.offsety*2) #.scale(0.1,0.1)
			p0 = matrix * (0, 0) - offset
			p1 = matrix * (0, 1) - offset
			p2 = matrix * (1, 1) - offset
			p3 = matrix * (1, 0) - offset
			#print "OFFSET for clipping", offset, p0
			
			self.writeln("%f %f m " % (p0[0], p0[1]))
			self.writeln("%f %f l " % (p1[0], p1[1]))
			self.writeln("%f %f l " % (p2[0], p2[1]))
			self.writeln("%f %f l " % (p3[0], p3[1]))
			self.writeln("closepath")
			self.writeln("clip")
			self.writeln("newpath")
		devicematrix = self.getDeviceMatrix()
		if clipping:
			viewportmatrix = self.getViewportMatrix()
			matrix = devicematrix * viewportmatrix
		else:
			matrix = self.getDeviceMatrix()
			#return
		offset = kaplot.Vector(self.offsetx, self.offsety)
		offset = kaplot.Vector(0, 0)
		#offset = kaplot.Vector(-self.offsetx*2, -self.offsety*2) #.scale(0.1,0.1)
		p0 = matrix * (0, 0) - offset
		p1 = matrix * (0, 1) - offset
		p2 = matrix * (1, 1) - offset
		p3 = matrix * (1, 0) - offset
		
		#if self.lastcp0 == tuple(p0) and self.lastcp1 == tuple(p1) and self.lastcp2 == tuple(p2) and self.lastcp3 == tuple(p3):
		#	pass
		#else:		
		if clipping:
			#self.writeln((sixfloats + " scp") % (p0[0], p0[1], p1[0], p1[1], p2[0], p2[1], p3[0], p3[1]))
			self.writeln((eightfloats + " scp") % (p0[0], p0[1], p1[0], p1[1], p2[0], p2[1], p3[0], p3[1]))
			self.lastcp0 = tuple(p0)
			self.lastcp1 = tuple(p1)
			self.lastcp2 = tuple(p2)
			self.lastcp3 = tuple(p3)
		else:
			self.writeln("ccp ")
		#507.702412 37.925687 507.702412 178.118469 663.637355 178.118469 663.637355 37.925687 scp
		#self.writeln((fourfloats + " scp") % (p0[0], p0[1], p2[0], p2[1]))
		self.lastCTM = None

	def getCaps(self):
		return []

	def pushContext(self, context=None, **kwargs):
		# while intclip shouldn't be used in EPS, this does respect the originial clippath
		
		self.writeln("ccp")
		super(PsDeviceBase, self).pushContext(context, **kwargs)
		self._initClippath(self._clipping)
		self.lastCTM = None

	def popContext(self, **kwargs):
		super(PsDeviceBase, self).popContext(**kwargs)
		#self.writeln("grestore")
		#self._initClippath(self.clipping)

	def pushViewportMatrix(self, matrix):
		super(PsDeviceBase, self).pushViewportMatrix(matrix)
		self._initClippath(self.clipping)

	def popViewportMatrix(self):
		super(PsDeviceBase, self).popViewportMatrix()
		self._initClippath(self.clipping)

	def _setFillstyle(self):
		#self._fillstyle = fillstyle
		pass

	def outputPattern(self):
		patternTemplate = """/Pattern setcolorspace
<<
	/PatternType 1 /PaintType 1 /TilingType 1
	/BBox [0 0 %(width)s %(width)s]
	/XStep %(width)s /YStep %(width)s
	/PaintProc {
	begin
		%(initcode)s
		%(code)s
	end
	} bind
>>
%(matrix)s
makepattern
setcolor
"""
		fillstyle = self._fillstyle
		#halfwidth = width/2
		patterncode = ""
		#initcode = "%s %f setlinewidth" % (self._colorCode, self._linewidth)
		#values = {"width":width, "halfwidth":halfwidth, "initcode":initcode, "matrix":matrix}
		#if fillstyle == "fill":
		#	pass
		#elif fillstyle == "crosshatch":
		#	code = "0 %(halfwidth)s moveto %(width)s %(halfwidth)s lineto strokepath fill %(halfwidth)s 0 moveto %(halfwidth)s %(width)s lineto strokepath fill"
		#	code = code % values
		#	values["code"] = code
		#	patterncode = patternTemplate % values
		#elif fillstyle == "hatch":
		#	code = "0 %(halfwidth)s moveto %(width)s %(halfwidth)s lineto strokepath fill"
		#	code = code % values
		#	values["code"] = code
		#	patterncode = patternTemplate % values
		#else:
		#	kaplot.info("fillstyle %r not supported, assuming 'fill'" % fillstyle)
		if fillstyle in kaplot.patterns:
			patternSize = self._patternsize
			patternSize, patternUnits = kaplot.utils.splitDimension(patternSize)
			patternSizePixels = kaplot.utils.convertToPixels(patternSize, patternUnits, dpi=self.dpi)
			patternSizePt = kaplot.utils.convertPixelsTo(patternSizePixels, "pt", dpi=self.dpi)
			pattern = kaplot.patterns[fillstyle]
			width = patternSizePt
			height = width
			pattern = kaplot.patterns[fillstyle]
			matrixcode = "matrix %f rotate" % math.degrees(pattern.angle)

			codestring = ""
			for part in xrange(pattern.parts):
				xlistlist, ylistlist = pattern.getXY(part)
				for xlist, ylist in zip(xlistlist, ylistlist):
					codestring += "%f %f m" % (xlist[0]*width, ylist[0]*height)
					for xvalue, yvalue in zip(xlist[1:], ylist[1:]):
						codestring += " %f %f l" % (xvalue*width, yvalue*height)
					if pattern.solid:
						codestring += " f"
					else:
						codestring += " s"
					codestring += "\n"

			initcode = "%s %f setlinewidth" % (self._colorCode, 1) # self._linewidth
			values = {"width":width, "initcode":initcode, "matrix":matrixcode}
			values["code"] = codestring
			patterncode = patternTemplate % values


		self._fillstylecode = patterncode
		self.writeln(self._fillstylecode)


	def _createMaskBitmap(self, mask2d):
		booleanmask = (numpy.array(mask2d) > 0)

		bytelist = []

		for row in booleanmask:
			byterowlist = []
			bytecount = len(row) / 8
			restbits = len(row) - bytecount*8
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
			bytelist.extend(byterowlist)
		row = booleanmask[0]
		bytecount = len(row) / 8
		restbits = len(row) - bytecount*8
		bytesperrow = bytecount
		if restbits:
			bytesperrow += 1
		#bytelist = "\xAA" * bytesperrow * len(booleanmask)
		#bytelist = [0xaa] * bytesperrow * len(booleanmask)
		maskdata = numpy.array(bytelist, numpy.Byte).tostring()
		#maskdata = numpy.array(bytelist, numpy.Byte).tostring()
		return maskdata
		
	def _setClipping(self, clipping):
		self._clipping = clipping
		self.setClipRegion()

	def setClipRegion(self):
		self._initClippath(self._clipping)
