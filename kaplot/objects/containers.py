# -*- coding: utf-8 -*-
import kaplot
import kaplot.text
from kaplot.objects import Page
from kaplot.objects import PlotBase

class Container(PlotBase):
	__fdoc__ = """Container holds objects which can be drawn on the page.
	
	It can also have decorators (they 'decorate' the container). Which will
	normally be drawn on the borders of the container, like 'labels' and 'axis' do.
	They shrink the viewport, resulting in an shrunk inner viewport so that your labels
	are always visible. 

	Arguments:
	 * viewport -- the viewport for this container, in normalized page coordinates
	 * world -- the world tuple, specifying range and domain
	"""
	def __init__(self, page, viewport=((0, 0), (1, 1)), world=None, **kwargs):
		if not isinstance(page, Page):
			raise TypeError, "container parent should be a page"
		self.parent = page
		self.page = page
		self.parent.containers.append(self)
		self.objects = []
		self.decorators = []
		self.context = kaplot.Context(**kwargs)
		self.viewport = viewport
		#self.innerViewport = tuple(viewport)
		self.borderViewport = tuple(viewport)
		self.world = world
		self.fitmode = "xy"
		self.drawOutside = False
		self.drawOutsideLeft = False
		self.drawOutsideRight = False
		self.drawOutsideTop = False
		self.drawOutsideBottom = False
		self.onmouse = None
		#Border(self)
		
	def copyObjectsFrom(self, container):
		for object in container.objects:
			object.clone(self)
		
	def worldToSize(self, x, y, units="mm"):
		normalized = kaplot.Matrix.scalebox(*self.getWorld()).no_translation() * (x, y)
		return self.getDocument().viewportToSize(normalized.x, normalized.y, units=units, viewport=self.borderViewport)

	def sizeToWorld(self, size):
		#size, units = kaplot.utils.splitDimension(size)
		#normalized = kaplot.Matrix.scalebox(*self.getWorld()).no_translation() * (x, y)
		#print "!!!",normalized
		#return self.getDocument().viewportToSize(normalized.x, normalized.y, units=units, viewport=self.innerViewport)
		vp = self.getDocument().sizeToViewport(size, self.borderViewport)
		return kaplot.Matrix.scalebox_inverse(*self.getWorld()).no_translation() * vp
		

	def windowToWorld(self, x, y):
		vx, vy = self.getDocument().windowToViewport(x, y, self.borderViewport)
		#w = self.getWorldMatrix().inverse() * (vx, vy)
		w = kaplot.Matrix.scalebox_inverse(*self.getWorld()) * (vx, vy)
		#print x, y, vx, vy, w.x, w.y
		return w

	def getMouseMoveText(self, x, y):
		#print self.borderViewport, self.viewport
		vx, vy = self.getDocument().windowToViewport(x, y, self.borderViewport)
		px = kaplot.utils.convertPixelsTo(x, "cm")
		py = kaplot.utils.convertPixelsTo(y, "cm")
		wx, wy = self.windowToWorld(x, y)
		text = """pixel:\tx = %g; y = %g
world:\tx = %g; y = %g
viewport:\tx = %g; y = %g
page:\tx = %gcm; y = %gcm
size:\t%s/%ipx,%ipx""" % (x, y, wx, wy, vx, vy, px, py, self.getDocument().size, self.getDocument().pixelWidth, self.getDocument().pixelHeight)
		if vx < 0 or vx > 1 or vy < 0 or vy > 1:
			text += "\noutside viewport"
		return text
		
	def getMouseDragText(self, x_begin, y_begin, x, y):
		vx1, vy1 = self.getDocument().windowToViewport(x_begin, y_begin, self.borderViewport)
		vx2, vy2 = self.getDocument().windowToViewport(x, y, self.borderViewport)
		wx1, wy1 = self.getWorldMatrix().inverse() * (vx1, vy1)
		wx2, wy2 = self.getWorldMatrix().inverse() * (vx2, vy2)
		px1 = kaplot.utils.convertPixelsTo(x_begin, "cm")
		py1 = kaplot.utils.convertPixelsTo(y_begin, "cm")
		px2 = kaplot.utils.convertPixelsTo(x, "cm")
		py2 = kaplot.utils.convertPixelsTo(y, "cm")
		text = """pixel/world/viewport/page:
\"%gpx, %gpx\", \"%gpx, %gpx\"
(%g, %g), (%g, %g)
(%g, %g), (%g, %g)
\"%gcm, %gcm\", \"%gcm, %gcm\"
""" % (x_begin, y_begin, x, y, wx1, wy1, wx2, wy2, vx1, vy1, vx2, vy2, px1, py1, px2, py2)		
		return text
		
	def testClipboard(self, window, *args, **kwargs):
		#print "testClipboard", args, kwargs
		window.setClipboardText("hoeba")

	def test1(self, window, *args, **kwargs):
		print "test1", args, kwargs
		
	def test2(self, window, *args, **kwargs):
		print "test2", args, kwargs
		
	def flashViewport(self, window, viewport=None):
		if viewport is None:
			viewport = self.viewport
		(vx1, vy1), (vx2, vy2) = viewport
		x1, y1 = self.getDocument().viewportToWindow(vx1, vy1)
		x2, y2 = self.getDocument().viewportToWindow(vx2, vy2)
		x1 += 5
		x2 -= 0
		y1 += 0
		y2 -= 5
		xlist = [x1, x2, x2, x1]
		ylist = [y1, y1, y2, y2]
		window.setFlashRegion(xlist, ylist, close=True)
		
	def handleKeyboardEvent(self, x, y, keycode, character, options, window):
		super(Container, self).handleKeyboardEvent(x, y, keycode, character, options, window)
		if character == "V":
			self.fitmode = "x"
			window.setXMouseCursor()
		if character == "H":
			self.fitmode = "y"
			window.setYMouseCursor()
		if character == "B":
			self.fitmode = "xy"
			window.setDefaultMouseCursor()
			
	def getFlipMenu(self, window, parentMenu=None):
		menu = window.createMenu(parentMenu)
		def flipx(*args):
			self.flipx()
			window.refreshDocument()
		def flipy(*args):
			self.flipy()
			window.refreshDocument()
		def flipxy(*args):
			self.flipx()
			self.flipy()
			window.refreshDocument()
		menu.addCommand("flip x", flipx)
		menu.addCommand("flip y", flipy)
		menu.addCommand("flip x+y", flipxy)
		return menu
		
	def handleMouseEvent(self, x, y, options, window):
		if self.onmouse and self.onmouse(x, y, options, window):
			return
		text = self.getMouseMoveText(x, y)
		window.setInfoText(text)
		if options["leftdouble"]:
			#print "double click, select container"
			vx, vy = self.getDocument().windowToViewport(x, y, viewport=((0, 0), (1,1)))
			container = self.page.findContainer(vx, vy, previous=self)
			kaplot.debug("found container", container)
			if container:
				container.flashViewport(window)
				window.select(container)
				
			
		
		if options["rightup"]:
			self.flashViewport(window)
			menu = window.createMenu()
			clipboardMenu = window.createMenu()

			clipboardMenu.addCommand("viewport", self.testClipboard)
			
			menu.addSubMenu("zoom", self.getZoomMenu(window, x, y, menu))
			menu.addSubMenu("grow", self.getGrowMenu(window, menu))
			menu.addSubMenu("flip", self.getFlipMenu(window, menu))
			menu.addSeparator()
			wx, wy = self.windowToWorld(x, y)
			def center(window, x, y):
				self.center(x, y)
				window.refreshDocument()
			def centerx(window, x):
				self.centerx(x)
				window.refreshDocument()
			def centery(window, y):
				self.centery(y)
				window.refreshDocument()
			menu.addCommand("center", center, args=[wx, wy])
			menu.addCommand("center x", centerx, args=[wx])
			menu.addCommand("center y", centery, args=[wy])
        
			def fitChildren(window):
				self.fitChildren()
				window.refreshDocument()
			menu.addCommand("fit", fitChildren)
        
			menu.addSeparator()
        
			#menuOptions.append(("select", self.getSelectionMenu()))
			menu.addSubMenu("context", self.getContextMenu(window, self.context, menu))
			#childMenu = window.createMenu(menu)
			#for i, child in enumerate(self.objects):
			#	name = "object [%d] = %s" % (i, str(child.__class__))
			#	childMenu.addSubMenu(name, self.getContextMenu(window, child.context, childMenu))
			#menu.addSubMenu("children", childMenu)
			#print "showing popup menu"
			window.showPopupMenu(menu)
			#print "showed it"

		if options["dragging"] and options["leftisdown"]:
			x1, y1 = options["dragposition"]
			x2, y2 = x, y
			xlist = [x1, x2, x2, x1]
			ylist = [y1, y1, y2, y2]
			#winx1, winy1 = self.getDocument().viewportToWindow(0, 0, self.innerViewport)
			#winx2, winy2 = self.getDocument().viewportToWindow(1, 1, self.innerViewport)
			#print winx1, winy1
			extraText = self.getMouseDragText(x1, y1, x2, y2)
			#if self.fitmode == "xy":
			#	xlist = [x1, x2, x2, x1]
			#	ylist = [y1, y1, y2, y2]
			#elif self.fitmode == "x":
			#	xlist = [x1, x2, x2, x1]
			#	ylist = [winy1, winy1, winy2, winy2]
			#elif self.fitmode == "y":
			#	xlist = [winx1, winx2, winx2, winx1]
			#	ylist = [y1, y1, y2, y2]
			window.setRubberBand(xlist, ylist, close=True)
			window.setInfoExtraText(extraText)
			window.refreshWindow()
		elif options["wasdragging"] and options["leftup"]:
			x1, y1 = options["dragposition"]
			x2, y2 = x, y
			w1 = self.windowToWorld(x1, y1)
			w2 = self.windowToWorld(x2, y2)
			v1 = self.getDocument().windowToViewport(x1, y1)
			v2 = self.getDocument().windowToViewport(x2, y2)
			#if self.fitmode == "x":
			#	
			def zoomtobox(window, p1, p2):
				self.world = p1, p2
				window.refreshDocument()
			def changeviewport(window, v1, v2):
				self.viewport = v1, v2
				window.refreshDocument()
			menu = window.createMenu()
			menu.addCommand("zoom", zoomtobox, args=[w1, w2])
			menu.addCommand("change viewport", changeviewport, args=[v1, v2])
			window.showPopupMenu(menu)
			window.removeRubberBand()
			window.refreshWindow()
		
		if options["dragging"] and options["middleisdown"]:
			x1, y1 = options["dragposition"]
			x2, y2 = x, y
			extraText = self.getMouseDragText(x1, y1, x2, y2)
			xlist = [x1, x2]
			ylist = [y1, y2]
			window.setRubberBand(xlist, ylist, close=False)
			window.setInfoExtraText(extraText)
			window.refreshWindow()
		elif options["wasdragging"] and options["middleup"]:
			x1, y1 = options["dragposition"]
			x2, y2 = x, y
			(wx1, wy1) = self.windowToWorld(x1, y1)
			(wx2, wy2) = self.windowToWorld(x2, y2)
			dx = wx2 - wx1
			dy = wy2 - wy1
			def pan(window, dx, dy):
				(x1, y1), (x2, y2) = self.getWorld()
				self.world = (x1+dx, y1+dy), (x2+dx, y2+dy)
				window.refreshDocument()
			menu = window.createMenu()
			menu.addCommand("pan", pan, args=[dx, dy])
			menu.addCommand("pan (x only)", pan, args=[dx, 0])
			menu.addCommand("pan (y only)", pan, args=[0, dy])
			window.showPopupMenu(menu)
			window.removeRubberBand()
			window.refreshWindow()
		
	def getContextValue(self, name):
		if name in self.context:
			return self.context[name]
		else:
			return self.page.getContextValue(name)
			
	def grow(self, s=1., x=1., y=1., top=1., bottom=1., left=1., right=1.):
		if self.world is None:
			self.world = (0, 0), (1, 1)
		(x1, y1), (x2, y2) = self.world
		width = float(x2 - x1)
		height = float(y2 - y1)
		xc = x1 + width/2.
		yc = y1 + height/2.
		p1 = xc - width*s*x*left/2., yc - height*s*y*bottom/2.,
		p2 = xc + width*s*x*right/2., yc + height*s*y*top/2.,
		self.world = p1, p2
		
	def setDomain(self, x1, x2):
		if self.world is None:
			self.world = (0, 0), (1, 1)
		(dontcare, y1), (dontcare, y2) = self.world
		self.world = (x1, y1), (x2, y2)

	def setRange(self, y1, y2):
		if self.world is None:
			self.world = (0, 0), (1, 1)
		(x1, prevy1), (x2, prevy2) = self.world
		self.world = (x1, y1 if y1 is not None else prevy1), (x2, y2 if y2 is not None else prevy2)

	def center(self, x, y):
		world = self.getWorld()
		(x1, y1), (x2, y2) = world
		width = float(x2 - x1)
		height = float(y2 - y1)
		self.world = (x-width/2., y-height/2.), (x+width/2., y+height/2.)

	def centerx(self, x):
		world = self.getWorld()
		(x1, y1), (x2, y2) = world
		width = float(x2 - x1)
		self.world = (x-width/2., y1), (x+width/2., y2)

	def centery(self, y):
		world = self.getWorld()
		(x1, y1), (x2, y2) = world
		height = float(y2 - y1)
		self.world = (x1, y-height/2.), (x2, y+height/2.)

	def fitChildren(self):
		self.world = None
		for object in self.objects:
			bbox = object.getBBox()
			if bbox:
				self.fit(bbox)
				
	def fit(self, bbox):
		if self.world is None:
			self.world = tuple(bbox)
		else:
			(x1a, y1a), (x2a, y2a) = bbox
			(x1b, y1b), (x2b, y2b) = self.world
			flippedx = x1b > x2b
			flippedy = y1b > y2b
			x = [x1a, x2a, x1b, x2b]
			y = [y1a, y2a, y1b, y2b]
			xmin = min(x)
			ymin = min(y)
			xmax = max(x)
			ymax = max(y)
			if xmin == xmax:
				xmax += 1
			if ymin == ymax:
				ymax += 1 
			self.world = (xmin, ymin), (xmax, ymax)
			if flippedx:
				self.flipx()
			if flippedy:
				self.flipy()
			
	def flipx(self):
		(x1, y1), (x2, y2) = self.world
		self.world = (x2, y1), (x1, y2)
		
	def flipy(self):
		(x1, y1), (x2, y2) = self.world
		self.world = (x1, y2), (x2, y1)
		
	def getDocument(self):
		return self.page.getDocument()
		
	def getWorld(self):
		if self.world is None:
			world = ((0, 0), (1, 1))
		else:
			world = self.world
		return world

	def getWorldMatrix(self):
		return kaplot.Matrix.scalebox(*self.getWorld())

	def layout(self):
		#matrix = kaplot.Matrix.scalebox_inverse(*self.viewport)
		#matrix = kaplot.Matrix.scalebox(*self.viewport).inv
		for decorator in self.decorators:
			decorator.layout()

		left = sum([k.bounds[0][0] for k in self.decorators])
		right = sum([k.bounds[1][0] for k in self.decorators])
		bottom = sum([k.bounds[0][1] for k in self.decorators])
		top = sum([k.bounds[1][1] for k in self.decorators])
		
		(x1, y1), (x2, y2) = self.viewport
		#print "in layout"
		if not (self.drawOutside or self.drawOutsideLeft):
			#print "x1"
			x1 += left
		if not (self.drawOutside or self.drawOutsideBottom):
			#print "y1"
			y1 += bottom
		if not (self.drawOutside or self.drawOutsideRight):
			#print "x2"
			x2 -= right
		if not (self.drawOutside or self.drawOutsideTop):
			#print "y2"
			y2 -= top
			
		self.borderViewport = (x1, y1), (x2, y2)
		


	def preDraw(self, device):
		#device.pushViewport(self.innerViewport)
		device.pushViewport(self.borderViewport)
		device.pushWorld(self.getWorld())
		device.pushContext(self.context)

	def drawDecorators(self, device):
		left = right = bottom = top = 0
		clipping = device.getClipping()
		device.setClipping(False)
		for decorator in self.decorators:
			if 0:
				print decorator, ((left, bottom), (right, top)),
				if hasattr(decorator, "location"):
					print decorator.location
				else:
					print 
			decorator.draw(device, ((left, bottom), (right, top)))
			left += decorator.bounds[0][0]
			right += decorator.bounds[1][0]
			bottom += decorator.bounds[0][1]
			top += decorator.bounds[1][1]
			#print "\t", ((left, bottom), (right, top))
		device.setClipping(clipping)

	def drawObjects(self, device):
		for object in self.objects:
			object.draw(device)

	def postDraw(self, device):
		device.popContext()
		device.popWorld()
		device.popViewport()
	
	def draw(self, device):
		self.preDraw(device)
		self.drawObjects(device)
		self.drawDecorators(device)
		self.postDraw(device)
		
	def clear(self):
		self.objects = []
	


def nextpow10(n):
	"""Return the next power of 10"""
	if n == 0:
		return 0
	else:
		return math.ceil(math.log10(abs(n)))

def fround(value, mod):
	if mod == 0:
		return value
	else:
		return int(value/mod) *mod

def magicnr(value, error):
	"""Return a number that looks 'nice', with a maximum error"""
	magics = [	(10 ** (nextpow10(error))),
				(10 ** (nextpow10(error))) / 2.0,
				(10 ** (nextpow10(error))) / 4.0,
				(10 ** (nextpow10(error))) / 10.0,
				(10 ** (nextpow10(error))) / 20.0,
				(10 ** (nextpow10(error))) / 40.0,
				(10 ** (nextpow10(error))) / 100.0,
				]
	magics.sort()
	magics.reverse()
	magic = magics[-1]
	for n in magics:
		if n < abs(value):
			magic = n
			break
	return fround(value, magic)

from kaplot.objects.decorators import *


class Box(Container):
	__fdoc__ = """Creates a box, which is a container, with axes around it
	
	Arguments:
	 * viewport -- the viewport for this container, in normalized page coordinates
	 * world -- the world tuple, specifying range and domain
	 * title -- title (a string) with will be displayed at the top of the container
	 * xxx-label -- a string/label that will be placed as indicated by 'xxx'
	
	For the rest of the arguments, see 'axes'
	
	"""
	def __init__(self, page, viewport=((0, 0), (1, 1)), world=None,
		title="", bottomlabel=None, leftlabel=None, rightlabel=None, toplabel=None, 
		xinterval=None, xinteger=False, xstart=None, xsubticks=4, xlogarithmic=False,
		yinterval=None, yinteger=False, ystart=None, ysubticks=4, ylogarithmic=False,
		ticklength="3mm", labeloffset="1mm",
		**kwargs):
		super(Box, self).__init__(page, viewport=viewport, world=world, **kwargs)
		
		self.leftaxes = []
		self.rightaxes = []
		self.topaxes = []
		self.bottomaxes = []

		self.border = Border(self)

		self.xaxis = self.addAxis("bottom", interval=xinterval, integer=xinteger, start=xstart, subticks=xsubticks,
			logarithmic=xlogarithmic, ticklength=ticklength, labeloffset=labeloffset)
		
		self.xaxis2 = self.addAxis("top", interval=xinterval, integer=xinteger, start=xstart, subticks=xsubticks,
			logarithmic=xlogarithmic, ticklength=ticklength, labeloffset=labeloffset)
		self.xaxis2.drawLabels = False
		
		self.yaxis = self.addAxis("left", interval=yinterval, integer=yinteger, start=ystart, subticks=ysubticks,
			logarithmic=ylogarithmic, ticklength=ticklength, labeloffset=labeloffset)

		self.yaxis2 = self.addAxis("right", interval=yinterval, integer=yinteger, start=ystart, subticks=ysubticks,
			logarithmic=ylogarithmic, ticklength=ticklength, labeloffset=labeloffset)
		self.yaxis2.drawLabels = False
		
		#self.spacerInside = Spacer(self)
		#self.testBorder = Border(self, color="red")
		self.labelsspacer = Spacer(self, "0mm")
		self.labels = Labels(self, bottom=bottomlabel, left=leftlabel, right=rightlabel, top=toplabel)
		#self.spacerExtra = Spacer(self)
		#self.testBorder = Border(self, color="green")
		self.title = Title(self, text=title)
		self.spacer = Spacer(self, "0mm")

		#self.spacerOutside = Spacer(self)
		#self.axes = Axes(self,
		#	xinterval=xinterval, xinteger=xinteger, xstart=xstart, xsubticks=xsubticks, xlogarithmic=xlogarithmic,
		#	yinterval=yinterval, yinteger=yinteger, ystart=ystart, ysubticks=ysubticks, ylogarithmic=ylogarithmic,
		#	ticklength=ticklength, labeloffset=labeloffset
		#	)

	def draw(self, device):
		self.preDraw(device)
		self.drawObjects(device)
		self.drawDecorators(device)
		self.postDraw(device)

	def addAxis(self, location, *args, **kwargs):
		axis = kaplot.objects.Axis(self, location=location, *args, **kwargs)
		if location == "left":
			self.leftaxes.append(axis)
		elif location == "bottom":
			self.bottomaxes.append(axis)
		elif location == "right":
			self.rightaxes.append(axis)
		elif location == "top":
			self.topaxes.append(axis)
		else:
			raise ValueError, "location should be 'left', 'right', 'top' or 'bottom'"
		return axis
		
class Box2(Container):
	__fdoc__ = """Creates a box, which is a container, with axes around it
	
	Arguments:
	 * viewport -- the viewport for this container, in normalized page coordinates
	 * world -- the world tuple, specifying range and domain
	 * title -- title (a string) with will be displayed at the top of the container
	 * xxx-label -- a string/label that will be placed as indicated by 'xxx'
	
	For the rest of the arguments, see 'axes'
	
	"""
	def __init__(self, page, viewport=((0, 0), (1, 1)), world=None,
		title="", bottomlabel=None, leftlabel=None, rightlabel=None, toplabel=None, 
		xinterval=None, xinteger=False, xstart=None, xsubticks=4, xlogarithmic=False,
		yinterval=None, yinteger=False, ystart=None, ysubticks=4, ylogarithmic=False,
		ticklength="3mm", labeloffset="1mm",
		**kwargs):
		super(Box2, self).__init__(page, viewport=viewport, world=world, **kwargs)
		
		#self.axes = kaplot.objects.Axes2(self)
			
		self.leftaxes = []
		self.rightaxes = []
		self.topaxes = []
		self.bottomaxes = []
		
		#self.border

		self.xaxis = self.addAxis("bottom", interval=xinterval, integer=xinteger, start=xstart, subticks=xsubticks,
			logarithmic=xlogarithmic, ticklength=ticklength, labeloffset=labeloffset)
		
		self.yaxis = self.addAxis("left", interval=yinterval, integer=yinteger, start=ystart, subticks=ysubticks,
			logarithmic=ylogarithmic, ticklength=ticklength, labeloffset=labeloffset)

		self.rightaxis = self.addAxis("right", interval=yinterval, integer=yinteger, start=ystart, subticks=ysubticks,
			logarithmic=ylogarithmic, ticklength=ticklength, labeloffset=labeloffset)

		self.topaxis = self.addAxis("top", interval=xinterval, integer=xinteger, start=xstart, subticks=xsubticks,
			logarithmic=xlogarithmic, ticklength=ticklength, labeloffset=labeloffset)

		if True:
			self.xaxis = self.addAxis("bottom", interval=xinterval, integer=xinteger, start=xstart, subticks=xsubticks,
				logarithmic=xlogarithmic, ticklength="-3mm", labeloffset=labeloffset)
			
			self.yaxis = self.addAxis("left", interval=yinterval, integer=yinteger, start=ystart, subticks=ysubticks,
				logarithmic=ylogarithmic, ticklength="-3mm", labeloffset=labeloffset)
	
			self.rightaxis = self.addAxis("right", interval=yinterval, integer=yinteger, start=ystart, subticks=ysubticks,
				logarithmic=ylogarithmic, ticklength="-3mm", labeloffset=labeloffset)
	
			self.topaxis = self.addAxis("top", interval=xinterval, integer=xinteger, start=xstart, subticks=xsubticks,
				logarithmic=xlogarithmic, ticklength="-3mm", labeloffset=labeloffset)
		
	def addAxis(self, location, *args, **kwargs):
		axis = kaplot.objects.Axis(self, location=location, *args, **kwargs)
		if location == "left":
			self.leftaxes.append(axis)
		elif location == "bottom":
			self.bottomaxes.append(axis)
		elif location == "right":
			self.rightaxes.append(axis)
		elif location == "top":
			self.topaxes.append(axis)
		else:
			raise ValueError, "location should be 'left', 'right', 'top' or 'bottom'"
		return axis
		
