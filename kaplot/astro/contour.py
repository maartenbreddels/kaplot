import kaplot
import kaplot.astro
import kaplot.cext._contour as _contour
import kaplot.context
from kaplot.objects.plotobject import PlotObject
from time import time

class ContourLine(PlotObject):
	def __init__(self, data2d, level=None, lock=True, context=None, **kwargs):
		PlotObject.__init__(self, lock=False, context=kaplot.context.buildContext(kwargs, context))
		self.data2d = data2d
		if level == None:
			minvalue = min([min(k) for k in data2d])
			maxvalue = max([max(k) for k in data2d])
			self.level = minvalue + (maxvalue - minvalue) / 2
		else:
			self.level = level

		if lock:
			self._lock()

	def plot(self, device):
		device.pushContext(self.context)
		begin = time()
		cinterface = device.getCInterface()
		if cinterface:
			polylines, labels = _contour.contour(self.data2d, self.level, cinterface)
		else:
			polylines, labels = _contour.contour(self.data2d, self.level)
			for x, y in polylines:
				device.plotPolyline(x, y)
		kaplot.debug("time for contour:", time()-begin)
		device.popContext()

	def onMouseEvent(self, device, x, y, options, window):
		viewportMatrix = device.getViewportMatrix()
		worldMatrix = device.getWorldMatrix()
		#vx, vy = viewportMatrix.inverse() * (x, y)
		matrix = (viewportMatrix * worldMatrix).inverse()
		wx, wy = matrix * (x, y)
		image = self.data2d
		height, width = image.shape
		pixelx, pixely = int(wx+0.5), int(wy+0.5)
		if pixelx >= 0 and pixelx < width and pixely >= 0 and pixely < height:
			#pixelstr = str(image[pixely, pixelx])
			if options["leftdown"]:
				self.level = image[pixely, pixelx]
				return True

		#else:
		#	pixelstr = "out of bounds"
		#super(AstroImage, self).onMouseMove(x, y, device, window)
