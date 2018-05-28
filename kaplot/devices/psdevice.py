# -*- coding: utf-8 -*-
"""
 * EPS
  * Illigal EPS commands:
     banddevice exitserver initmatrix setshared
     clear framedevice quit startjob
     cleardictstack grestoreall renderbands
     copypage initclip setglobal
     erasepage initgraphics setpagedevice
  * These must be used properly according to PLRM Appendix I
     nulldevice sethalftone setscreen undefinefont
     setgstate setmatrix settransfer
  * Leave stack intact, no leftover or extra pops
  * Preferrably no binary data (but 7bit)


"""
from kaplot.devices.psdevicebase import PsDeviceBase
import kaplot
import kaplot.utils
from kaplot import Matrix
from cStringIO import StringIO
import struct
import PIL.Image
import os

class PSDevice(PsDeviceBase):
	def __init__(self, filename="kaplot.ps", ):
		self.filename = filename
		PsDeviceBase.__init__(self)
		#self.resx = self.pixelWidth
		#self.resy = self.pixelHeight
		#self.filename = filename
		#self.file = None
		self.psinfo.title = os.path.splitext(os.path.basename(filename))[0]

	def __open(self):
		self.pushContext(self.defaultContext)
		#GsDevice.open(self)

	def __close(self):
		#self.writeln("showpage")
		#if not self.interactive:
		#	kaplot.debug("device is not interactive, so generating output automaticly")
		#self.output()
		pass

	def preDraw(self, document):
		self.file = open(self.filename, "wb")
		kaplot.info("writing plot to filename", self.filename)
		super(PSDevice, self).preDraw(document)

	def postDraw(self, document):
		super(PSDevice, self).postDraw(document)
		self.file.close()

	def getOffsetMatrix(self):
		return Matrix.translate(self.offsetx, self.offsety)
	
	def getDeviceMatrix(self):
		width, height = self.resx, self.resy
		return Matrix.scale(width, height)

	def showpage(self):
		self.writeln("showpage")

	def write(self, code):
		try:
			self.file.write(code)
		except:
			kaplot.debug("code trying to execute", `code`, "length =",len(code))
			raise

	def writeln(self, code):
		try:
			self.file.write(code)
			self.file.write("\n")
		except:
			kaplot.debug("code trying to execute", `code`, "length =",len(code))
			raise

	def flush(self):
		pass

class EPSDevice(PSDevice):
	def __init__(self, filename="kaplot.eps"):
		PSDevice.__init__(self, filename=filename)
		self.tiffPreviewFilename = None

	def writeFileHeader(self):
		self.writeln("%!PS-Adobe-3.0 EPSF-3.0")

	def showpage(self):
		pass # EPS doesn't contain a showpage

	def preDraw(self, document):
		kaplot.info("writing plot to filename", self.filename)
		self.psbuffer = StringIO()
		#self.pushContext(self.defaultContext)
		super(EPSDevice, self).preDraw(document)
		#GsDevice.open(self)

	def __close(self):
		#if not self.interactive:
		#	kaplot.debug("device is not interactive, so generating output automaticly")
		#	self.output()

		#self.tiffPreviewFilename = "preview.tiff"
		if self.tiffPreviewFilename:
			#raise Exception, "this code isn't working somehow"
			import PIL.Image
			from cStringIO import StringIO
			#previewImage = PIL.Image.open("kaplot.png")
			#previewImage = PIL.Image.open("naamloos.tif")
			#tiffbuffer = StringIO()
			#previewImage.save(tiffbuffer)
			#previewImage.save("preview.tiff", "TIFF")

			#tiffcode = tiffbuffer.getvalue()
			tiffcode = file(self.tiffPreviewFilename, "rb").read()
			pscode = self.psbuffer.getvalue()

			headerformat = "BBBBIIIIIIH"
			offset = struct.calcsize(headerformat)
			psoffset = offset
			pslength = len(pscode)
			tiffoffset = psoffset+pslength
			tifflength = len(tiffcode)
			header = struct.pack(headerformat, 0xC5, 0xD0, 0xD3, 0xC6, psoffset, pslength,
					0, 0, tiffoffset, tifflength, 0xffff)
			self.file.write(header)
			self.file.write(pscode)
			self.file.write(tiffcode)
			self.file.close()
		else:
			pscode = self.psbuffer.getvalue()
			self.file.write(pscode)
			self.file.close()


	def _clear(self):
		self.file.seek(0)
		self.file.truncate(0)
		self.psbuffer = StringIO()

	def _write(self, code):
		self.psbuffer.write(code)

	def _writeln(self, code):
		self.psbuffer.write(code)
		self.psbuffer.write("\n")
