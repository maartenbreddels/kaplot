import kaplot.objects
from kaplot.objects import Container

class WcsPlotObject(PlotObject):
	pass

class WcsContainer(Container):
	def __init__(self, projection, border=False, lock=True, context=None, **kwargs):
		Container.__init__(self, border=border, lock=False, context=kaplot.context.buildContext(kwargs, context))
		self.projection = projection
