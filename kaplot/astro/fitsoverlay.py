import kaplot
import kaplot.objects
import kaplot.context
import kaplot.colormap
import kaplot.cext._contour as _contour
from kaplot.objects.container import Container
import kaplot.astro.projection
import kaplot.cext._gipsy

class FitsOverlay(Container):
	def __init__(self, image1, image2, contourlevels=[], context=None,
				colormap="rainbow", datamin=None, datamax=None, function="linear",
				**kwargs):
		Container.__init__(self, context=kaplot.context.mergeDicts(context, kwargs))
		self.image1 = image1
		self.image2 = image2
		self.datamin = datamin
		self.datamax = datamax
		self.function = function
		self.colormap = colormap

		try:
			self.contourlevels = [int(contourlevels)]
		except:
			pass
		else:
			self.contourlevels = []
			datamin = self.image2.data.min()
			datamax = self.image2.data.max()
			for i in range(contourlevels):
				#print "minmax", datamin, datamax, contourlevels
				level = datamin + ((datamax - datamin) / (contourlevels + 1)) * (i+1)
				self.contourlevels.append(level)
				#print level
				#self.add(ContourLine(data2d, level))

		self.context.setWorldImage(self.image1.data)

	def plot(self, device):
		device.pushContext(self.context)
		device.plotIndexedImage(self.image1.data, self.colormap, self.function)
		#self.image2.headers["CRVAL1"] = self.image2.headers["CRVAL1"] * 1.0001
		projection1 = kaplot.astro.projection.fromDict(self.image1.headers)
		projection2 = kaplot.astro.projection.fromDict(self.image2.headers)
		if "EQUINOX" in self.image1.headers:
			epoch1 = self.image1.headers["EQUINOX"]
		else:
			epoch1 = self.image1.headers["EPOCH"]
		if "EQUINOX" in self.image2.headers:
			epoch2 = self.image2.headers["EQUINOX"]
		else:
			epoch2 = self.image2.headers["EPOCH"]
		print "epoch: %r -> %r" % (epoch1, epoch2)
		#epoch1 = 1999
		for level in self.contourlevels:
			polylines, labels = _contour.contour(self.image2.data, level)
			for x, y in polylines:
				x, y = projection2.reversearray(x, y)
				if x and y:
					if True:
						nx = []
						ny = []
						#print "<", x, y, ">"
						for xp, yp in zip(x, y):
							nxp, nyp = kaplot.cext._gipsy.epoco(xp, yp, epoch2, epoch1)
							#print xp, yp, "-", nxp, nyp, "|"
							nx.append(nxp)
							ny.append(nyp)
						x, y = projection1.forwardarray(nx, ny)
					else:
						x, y = projection1.forwardarray(x, y)
				device.plotPolyline(x, y)

		device.popContext()
