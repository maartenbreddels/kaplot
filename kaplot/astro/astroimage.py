import kaplot
import kaplot.astro
import kaplot.context
from kaplot.objects import Box, Labels, Border, Spacer
from kaplot.objects.plotobject import PlotObject
from kaplot.objects.container import Container
from kaplot.astro import ContourLine
from kaplot.astro import WcsBox
import numarray
import kaplot.colormap
import kaplot.astro.utils

class AstroImage(Container):
	def __init__(self, data2d, mask2d=None, contourlevels=[], boxtype="grid", wcsvalues={},
				colormap="rainbow", datamin=None, datamax=None,
				function="linear", level=None, p1=(0.0, 0.0), p2=(1., 1.),
				#colorwedgesize=0.15, colorwedgeside="bottom", colorwedgescale=0.9,
				#plotcolorwedge=True,
				contourcontexts=[],
				preserveaspectratio=True, aspectratio=None,
				leftlabel="", bottomlabel="", rightlabel="", toplabel="", title="",
				lock=True, context=None, **kwargs):
		Container.__init__(self, lock=False, context=kaplot.context.mergeDicts(context, kwargs))
		self.data2d = numarray.array(data2d)
		self.mask2d = mask2d
		self.colormap = colormap
		self.datamin = datamin
		self.datamax = datamax
		self.function = function
		self.preserveaspectratio = preserveaspectratio
		self.aspectratio = aspectratio
		if datamin == None:
			self.datamin = self.data2d.min()
		if datamax == None:
			self.datamax = self.data2d.max()

		if boxtype == "world":
			self.box = Box(title=title)
		elif boxtype == "grid":
			self.box = Box(title=title)
		elif "wcs":
			self.box = WcsBox(wcsvalues)

		#if colorwedgeside in ["bottom", "top"]:
		#	self.colorwedge = kaplot.objects.ColorWedge(self, "right")
		#else:
		#	self.colorwedge = kaplot.objects.ColorWedge(self, "up")
		#self.colorwedgesize = colorwedgesize
		#self.colorwedgeside = colorwedgeside
		#self.colorwedgescale = colorwedgescale
		#self.plotcolorwedge = plotcolorwedge

		self.labels = Labels(title=title, leftlabel=leftlabel, bottomlabel=bottomlabel, rightlabel=rightlabel, toplabel=toplabel)

		self.border = Border("3D")
		self.addDecorator(self.border)
		self.addDecorator(Spacer("4pt"))
		self.addDecorator(self.labels)
		self.addDecorator(Spacer("6pt"))
		self.addDecorator(self.box)

		self.contourlines = []
		#import pdb; pdb.set_trace()
		try:
			contourlevelcount = int(contourlevels)
		except:
			pass
		else:
			contourlevels = []
			datamin = self.data2d.min()
			datamax = self.data2d.max()
			for i in range(contourlevelcount):
				level = datamin + ((datamax - datamin) / (contourlevelcount + 1)) * (i+1)
				contourlevels.append(level)

		for i in range(len(contourlevels)):
			#level = datamin + ((datamax - datamin) / (contourlevels + 1)) * (i+1)
			level = contourlevels[i]
			if len(contourcontexts) > i:
				context = contourcontexts[i]
			else:
				context = None
			self.add(ContourLine(data2d, level, context=context))

		self.context.setWorldImage(self.data2d)

		if lock:
			self._lock()

	def ___layout(self, device):
		device.pushContext(self.context, graphics=False)

		self.splitContext.viewport = self.border.layout(device)
		device.pushContext(self.splitContext, graphics=False)


		if self.colorwedgeside == "right":
			self.imageContext.viewport = (0, 0), (1-self.colorwedgesize, 1)
			self.colorWedgeContext.viewport = (1-self.colorwedgesize, 0), (1, 1)
		elif self.colorwedgeside == "top":
			self.imageContext.viewport = (0, 0), (1, 1-self.colorwedgesize)
			self.colorWedgeContext.viewport = (0, 1-self.colorwedgesize), (1, 1)
		elif self.colorwedgeside == "left":
			self.imageContext.viewport = (self.colorwedgesize, 0), (1, 1)
			self.colorWedgeContext.viewport = (0, 0), (self.colorwedgesize, 1)
		elif self.colorwedgeside == "bottom":
			self.imageContext.viewport = (0, self.colorwedgesize), (1, 1)
			self.colorWedgeContext.viewport = (0, 0), (1, self.colorwedgesize)
		else:
			raise Exception, "unknown colorwedge side %r" % self.colorwedgeside

		device.pushContext(self.colorWedgeContext, graphics=False)
		self.colorwedge.layout(device)
		device.popContext(graphics=False)

		device.pushContext(self.imageContext, graphics=False)

		height, width = self.data2d.shape
		aspectratio = width/float(height)

		#if self.preserveaspectratio:
		#	self.childContext.viewport = self.box.layout(device, aspectratio)
		#else:
		self.innerContext.viewport = self.box.layout(device)

		device.popContext(graphics=False) # self.imageContext
		device.popContext(graphics=False) # self.splitContext
		device.popContext(graphics=False) # self.context
		return self.getChildViewport()

	def layout(self, device):
		device.pushContext(self.context)
		self.layoutDecorators(device)
		device.popContext()

	def plot(self, device):
		transformedData2d = self.transformImage()

		device.pushContext(self.context)
		device.pushContext(self.innerContext)
		device.plotIndexedImage(transformedData2d, self.colormap, self.function, self.mask2d)
		for contourline in self.contourlines:
			contourline.plot(device)
		self.plotChildren(device)
		device.popContext()
		self.plotDecorators(device)
		device.popContext()

	def transformImage(self):
		datamin = self.datamin
		datamax = self.datamax
		data2d = numarray.clip(self.data2d, min(datamin, datamax), max(datamin, datamax))
		return data2d

	def configure(self, window):
		#import kaplot.tktools.imageconf
		#result = kaplot.tktools.imageconf.imageconf(self.data2d, self.datamin, self.datamax, self.colormap, self.function)
		#import kaplot.windows.wximageconf
		#result = kaplot.windows.wximageconf.imageconf(self.data2d, self.datamin, self.datamax, self.colormap, self.function)
		result = window.configureImage(self.data2d, self.colormap, self.function, self.datamin, self.datamax)

		if result != None:
			self.data2d, self.colormap, self.function, self.datamin, self.datamax = result
			return True
		else:
			return False

	def onMouseMove(self, x, y, device, window):
		viewportMatrix = device.getViewportMatrix()
		worldMatrix = device.getWorldMatrix()
		vx, vy = viewportMatrix.inverse() * (x, y)
		matrix = (viewportMatrix * worldMatrix).inverse()
		wx, wy = matrix * (x, y)
		if isinstance(self.box, WcsBox):
			physicalx, physicaly = self.box.projection.reverse(wx, wy)
			physicalxstr = kaplot.astro.utils.formatX(physicalx)
			physicalystr = kaplot.astro.utils.formatY(physicaly)
			#image = self.transformImage()
			image = self.data2d
			height, width = image.shape
			pixelx, pixely = int(wx+0.5), int(wy+0.5)
			if pixelx >= 0 and pixelx < width and pixely >= 0 and pixely < height:
				pixelstr = str(image[pixely, pixelx])
			else:
				pixelstr = "out of bounds"

			window.printInfo("normalised: %f %f\nworld: %f %f\nphysical x: %s\n"\
					"physical y: %s\npixel value: %s(not exact)" % (vx, vy, wx, wy, physicalxstr, physicalystr, pixelstr))
		else:
			super(AstroImage, self).onMouseMove(x, y, device, window)

	def ___getContextList(self):
		return [self.context, self.splitContext, self.imageContext, self.innerContext]
