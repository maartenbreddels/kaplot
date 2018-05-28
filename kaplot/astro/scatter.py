import kaplot
import kaplot.astro
import kaplot.context
import kaplot.vector
import kaplot.matrix
from kaplot.objects.plotobject import PlotObject
import numarray

class Scatter(PlotObject):
	def __init__(self, width, height, mask=True, **kwargs):
		apply(PlotObject.__init__, (self,), kwargs)
		self.width = width
		self.height = height
		self.mask = mask

		self.data2d = numarray.zeros((self.height, self.width), numarray.Float)

		self.context = kaplot.context.buildContext(kwargs, linestyle="normal")
		self.callback = self.notifyChange
		self.context.addWeakListener(self.callback)
		self.context.setWorldImage(self.data2d)
		
	def put(self, x, y, value=1.0, clip=False):
		#x, y = (kaplot.matrix.Matrix.scaleXY(self.width, self.height) * self.context.worldmatrix) * kaplot.vector.Vector(x, y)
		if clip and ((x >= self.width) or (y >= self.height) or (x < 0) or (y < 0)):
			return False
		else:
			self.data2d[int(y)][int(x)] = value
			return True
		
	def add(self, x, y, value=1.0, clip=False):
		#x, y = (self.context.worldmatrix) * kaplot.vector.Vector(x, y)
		#print x, y
		if clip and ((x >= self.width) or (y >= self.height) or (x < 0) or (y < 0)):
			return False
		else:
			self.data2d[int(y)][int(x)] += value
			return True
		
		
	def plot(self, device):
		device.pushContext(self.context)
		if self.mask:
			mask2d = self.createMask(self.data2d)
			#mask2d.shape = self.data2d.shape
			print 1 in list(mask2d.flat)
			print max(mask2d.flat), max(self.data2d.flat)
		else:
			mask2d = None
		device.plotIndexedImage(data2d=self.data2d, mask2d=mask2d)
		device.popContext()
		
	def createMask(self, data2d):
		return self.data2d > 1e-8

		
		