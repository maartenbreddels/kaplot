import kaplot
import kaplot.objects
import kaplot.context
import kaplot.colormap
import kaplot.cext._contour as _contour
import kaplot.cext._wcslib as wcslib
from kaplot.objects.container import Container
import kaplot.astro.projection
import kaplot.cext._gipsy

class FitsReprojection(Container):
	def __init__(self, image1, image2, context=None,
				colormap="rainbow", datamin=None, datamax=None, function="linear",
				**kwargs):
		Container.__init__(self, context=kaplot.context.mergeDicts(context, kwargs))
		self.image1 = image1
		self.image2 = image2
		self.datamin = datamin
		self.datamax = datamax
		self.function = function
		self.colormap = colormap

		self.context.setWorldImage(self.image1.data)

	def plot(self, device):
		device.pushContext(self.context)
		device.plotIndexedImage(self.image1.data, self.colormap, self.function)
		projection1 = kaplot.astro.projection.fromDict(self.image1.headers)
		projection2 = kaplot.astro.projection.fromDict(self.image2.headers, True)
		projection1.wcs.print_()
		print "&"*80
		projection2.wcs.print_()
		data = self.image2.data
		datadiff = data.max() - data.min()
		BLANK = data.min()-datadiff/2
		newimage, tx, ty, blank = wcslib.reproj(data, projection2.wcs, projection1.wcs, BLANK)
		matrix = kaplot.matrix.Matrix.translate((tx, ty))
		#matrix = kaplot.matrix.Matrix.translate((5, 5))

		device.pushContext({"alpha":0.95, "worldmatrix":matrix})
		#device.plotIndexedImage(self.image2.data[0], kaplot.colormap.ColorMap.cool, self.function)
		#datamin, datamax = self.image2.data[0].min(), self.image2.data[0].max()
		mask = newimage != BLANK
		device.plotIndexedImage(newimage, kaplot.colormap.ColorMap.blackwhite, self.function, mask2d=mask)
		device.popContext()

		print self.image1.data.shape
		print newimage.shape, tx, ty, blank
		device.popContext()
