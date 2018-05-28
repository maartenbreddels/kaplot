# -*- coding: utf-8 -*-
import kaplot
#import kaplot.context
import kaplot.objects
import sys
#from kaplot.cext._wcslib import Wcs
#import kaplot.astro
#from numpy.random_array import *
#import numpy.fft
from kaplot.objects.plotobjects import _bindata
import os
#from numpy import *
import numpy
from optparse import OptionParser
import inspect
import math

#x = arange(-10, 15, 0.5)
#y = x ** 2 + sin(x) * 20
#xerr = random(len(x)) * 1 + 0.5
#yerr = random(len(x)) * 5 + 2
#perlin2d = kaplot.data.perlin2dnoise(8)
#perlin1d = kaplot.data.perlin1dnoise(8)
#
#population1950		= kaplot.data.population1950
#population2000		= kaplot.data.population2000
#population2003		= kaplot.data.population2003
#populationgroups 	= kaplot.data.populationgroups
#populationcontexts	= kaplot.data.populationcontexts
#populationlabels	= kaplot.data.populationlabels

goodcolors = ["black", "red", "green", "blue", "orange", "purple", "grey", "pink"] 

class current(object):
	device = None
	document = None
	page = None
	container = None
	container_array = []
	container_indices = []
	object = None
	wcs = None
	
	legend_objects = []
	legend_types = []
	interactive = False
	
class default(object):
	guiDeviceName = None
	deviceName = "ps"
	size = kaplot.size.default
	dpi = kaplot.defaultDpi
	filename = None
	parsedArguments = False
	#psoffset = "3.17cm, 2.54cm"
	psoffset = "1cm, 1cm"
	extraborder = "0mm, 0mm, 0mm, 0mm"
	psorientation = "Portrait" # "Landscape"
	psrotation = "0"
	hardcopy = None
	
	
	
devicemap= {}
devicemap["ps"] = "kaplot.devices.psdevice.PSDevice"
devicemap["eps"] = "kaplot.devices.psdevice.EPSDevice"
devicemap["pdf"] = "kaplot.devices.pdfdevice.PdfDevice"
#devicemap["svg"] = "kaplot.devices.svgdevice.SvgDevice"
#devicemap["svgz"] = "kaplot.devices.svgdevice.SvgzDevice"

try:
	import kaplot.cext._agg
	devicemap["agg"] = "kaplot.devices.aggdevice.AggDeviceWindow"
	devicemap["agg-image"] = "kaplot.devices.aggdevice.AggDeviceImage"
	default.hcDeviceName = "agg-image"
	default.guiDeviceName = "agg"
	default.deviceName = "agg"
except ImportError:
	pass

extensiondevicemap = {} # maps an extension to a device name
extensiondevicemap["ps"] = "ps"
extensiondevicemap["pdf"] = "pdf"
extensiondevicemap["eps"] = "eps"
extensiondevicemap["png"] = "agg-image"
extensiondevicemap["gif"] = "agg-image"
extensiondevicemap["jpeg"] = "agg-image"


defaultextrausage="[script specific arguments]\nthe script specific arguments can be filenames for instance"

def defaultparser(extrausage=defaultextrausage):
	"""HIDE"""
	usage = "usage: %prog [options] " + extrausage
	#guilist = guimap.keys()
	devicelist = devicemap.keys()
	devicelist.sort()
	#guilist.sort()
	deviceliststring = ", ".join([repr(k) for k in devicelist])
	#guiliststring = ", ".join([repr(k) for k in guilist])
	#parser = OptionParser(usage, version="%%prog %s" % __version__)
	parser = OptionParser(usage, version="kaplot %s" % kaplot.__version__)
	parser.add_option("-f", "--filename", dest="filename", help="the filename used for output\n(if output to a file is generated)")
	parser.add_option("--hardcopy", dest="hardcopy", help="the plot will be saved to the filename given")
	parser.add_option("-d", "--device", default=default.deviceName, help="the devicename used for output, default=%s, possible values: %s" % (default.deviceName, deviceliststring))
	#parser.add_option("-g", "--gui", default=defaultGuiName, help="the gui backend used for devices which need a gui window, default=%s, possible values: %s" % (defaultGuiName, guiliststring))
	parser.add_option("-s", "--size", type="string", default=default.size, help="a tuple which defines the size of the output(use quotes('') to prevent misparsing), default=%r" % default.size)
	#parser.add_option("-t", "--threaded", type="int", default=threaded, help="if 1, run the gui in a seperate thread default=%r" % threaded)
	parser.add_option("--dpi", type="int", default=default.dpi, help="dpi(dots(or pixels) per inch), determines the relation between physical units and pixels/dots, default=%s" % (default.dpi))
	parser.add_option("--ps-offset", type="string", default=default.psoffset, help="offset (relative to the lower left corder) from where the plot will start, default=%s" % (default.psoffset))
	parser.add_option("--ps-extraborder", type="string", default=default.extraborder, help="extra border for BoundingBox, to allow drawing outside the original BoundingBox")
	parser.add_option("--ps-orientation", type="string", default=default.psorientation, help="Orientation of the page(doesn't rotate your plot), default=%s" % (default.psorientation))
	parser.add_option("--ps-rotation", type="string", default=default.psrotation, help="Like orientation, but rotates the plot, default=%s" % (default.psrotation))
	parser.add_option("--debug", type="int", default=int(kaplot.printDebug), help="if 1, prints debug information to stdout, if 0 it will not, default=%r" % int(kaplot.printDebug))
	parser.add_option("--printinfo", type="int", default=int(kaplot.printInfo), help="if 1, prints information about things that went wrong etc, if 0 it won't, default=%r" % int(kaplot.printInfo))
	return parser

def parseargs(argv=None, parser=None):
	"""HIDE"""
	global defaultGuiName, printDebug, printInfo, threaded
	if argv is None:
		argv = sys.argv[1:]
	if parser is None:
		parser = defaultparser()
	opts, arguments = parser.parse_args(argv)
	default.deviceName = opts.device
	default.size = opts.size
	default.dpi = opts.dpi
	default.filename = opts.filename
	default.hardcopy = opts.hardcopy
	default.psoffset = opts.ps_offset
	default.extraborder = opts.ps_extraborder
	kaplot.printDebug = opts.debug
	kaplot.printInfo = opts.printinfo
	default.parsedArguments = True
	return opts, arguments
	
def _checkArgs():
	"""HIDE"""
	if not default.parsedArguments:
		parseargs()

def _checkDevice():
	"""HIDE"""
	_checkArgs()
	if current.device is None:
		current.device = device()
	else:
		if current.device.isGuiDevice():
			current.device.checkWindow()

def _checkDocument():
	"""HIDE"""
	_checkArgs()
	#_checkDevice()
	if current.document is None:
		current.document = document()#kaplot.objects.Plot()

def _checkPage():
	"""HIDE"""
	_checkDocument()
	if current.page is None:
		page(current.document)

def _checkContainer():
	"""HIDE"""
	_checkPage();
	if not current.container:
		current.container = kaplot.objects.Container(current.page)

def _checkBox():
	"""HIDE"""
	_checkPage();
	if not current.container:
		current.container = box()
		
def _checkWcs():
	"""HIDE"""
	if not current.wcs:
		ref = (0, 0)
		current.wcs = Wcs(ref, ["RA---AIT", "DEC--AIT"], [1,0,0,1], (1,1), (0, 0), (0,0), [1,0,0,1], 1|2|4, [(1,0,1), (2,1,1)] )


def _checkRedraw():
	"""HIDE"""
	if current.interactive:
		draw()

def clear():
	"""Removes the document, and page, to start with a new plot"""
	current.document = None
	current.page = None
	current.container = None
	current.container_array = []
	current.container_indices = []
	current.object = None
	current.wcs = None
	
	current.legend_objects = []
	current.legend_types = []
	current.interactive = False
	

def clearcontainer(container=None):
	"""Removes the document, and page, to start with a new plot"""
	if container is None:
		container = current.container
	container.objects = []

def device(name=None, **kwargs):
	"""Creates the default device
	
	If name argument is not given, a default device is created.
	
	TODO: explaind about default device, and argument parsing
	"""
	#return AggDeviceBase()
	return guidevice(name, **kwargs)
	
def guidevice(name=None, window=None, **kwargs):
	"""Creates a device capable of displaying it's output to a window

	The name argument is the same as in the `device` function.		
	If the window arguments is not given, a default window will be created
	"""
	if name == None:
		name = default.deviceName
	if name not in devicemap:
		raise Exception, "there is no device with the name %r" % name
	parts = devicemap[name].split(".")
	moduleName = ".".join(parts[:-1])
	className = parts[-1]
	exec "import " +moduleName
	exec "module = " +moduleName
	kwargs_ = {}
	classObject = getattr(module, className)
	acceptedarguments = inspect.getargs(classObject.__init__.im_func.func_code)[0]
	for key, value in kwargs.items():
		if key in acceptedarguments:
			kwargs_[key] = value
		else:
			kaplot.info("argument %r ignored in function kaplot.createDevice for class contructor of device" % key)
	kwargs_.update(kwargs)
	#return classObject(**kwargs_)
	kaplot.debug("creating device: %r" % classObject)
	if "window" in acceptedarguments:
		if window is None:
			window = kaplot.window(current.interactive)
		return classObject(window, **kwargs_)
	else:
		if "filename" in acceptedarguments and default.filename and "filename" not in kwargs_:
			return classObject(filename=default.filename, **kwargs_)
		else:
			return classObject(**kwargs_)

def draw(device=None):
	"""Draws and the current document
	
		If the device argument isn't given, a default device will be created
		using the `device` function.
	"""
	if default.hardcopy:
		hardcopy(default.hardcopy)
	else:
		_checkDevice()
		if current.device and current.device.isGuiDevice():
			if current.device.getWindow().getSelected() is None:
				current.device.getWindow().select(current.container)
		current.document.draw(current.device)
		if not current.interactive:
			current.device.close()

def export(deviceName):
	"""Draws the plot on a device specified be the deviceName argument
	
	Returns the created device
	"""
	#_checkDevice()
	device = device(deviceName)
	_checkDocument()
	current.document.draw(device)
	return device
	
def hardcopy(filename, deviceName=None, document=None):
	if document is None:
		_checkDocument()
	if deviceName is None:
		__, extension = os.path.splitext(filename)
		if not extension:
			raise Exception, "no extension given in filename, use one of the extensions: %r, or specify the"\
					"device name" % (extensiondevicemap.keys())
		else:
			if extension[1:] in extensiondevicemap:
				deviceName = extensiondevicemap[extension[1:]]
			else:
				raise Exception, "didn't recognise extension %r, use one of the extensions: %r, or specify the"\
						" device name" % (extension[1:], extensiondevicemap.keys())
	dev = device(deviceName, filename=filename)
	current.document.draw(dev)
				
	
def setdevice(device):
	"""Changes the current device"""
	current.device = device

def guiselect(object):
	"""HIDE"""
	_checkDevice()
	if current.device.isGuiDevice():
		current.device.getWindow().select(object)
	else:
		kaplot.info("current device is not a gui device")
	
def grow(s=1., x=1., y=1., top=1., bottom=1., left=1., right=1., container=None):
	"""Grows the world coordinates of the current container
	
	All arguments are relative, where 1 means 100%, 0.2 means 20% etc
	Arguments:
		* s -- for all directions
		* x, y -- in x or y diction
		* top, bottom, left, right -- as your except
	"""
	if container is None:
		_checkContainer()
		container = current.container
	container.grow(s=s, x=x, y=y, top=top, bottom=bottom, left=left, right=right)
	
def setdomain(x1, x2, container=None):
	"""Changes the domain of the current container"""
	if container is None:
		_checkContainer()
		container = current.container
	container.setDomain(x1, x2)
	
def setrange(y1, y2, container=None):
	"""Changes the range of the current container"""
	if container is None:
		_checkContainer()
		container = current.container
	container.setRange(y1, y2)
	
def flipx(container=None):
	"""Changes the range of the current container"""
	if container is None:
		_checkContainer()
		container = current.container
	container.flipx()
	
def flipy(container=None):
	"""Changes the range of the current container"""
	if container is None:
		_checkContainer()
		container = current.container
	container.flipy()
	
def document(size=None, dpi=None, offset=None, extraborder=None, **kwargs):
	"""Creates a document, the root of your whole plot
	
	Arguments:
	 * size -- a string which specifies the size for all pages in
	 		the document. Examples: '10cm, 15cm'
	 		If not set, the default size (if not changes by command
	 		lines arguments) will be used.
	 * dpi -- dots per inch(or read pixels per inch), it specifies the 
	 		relation between physical units of measure and pixels
	 		If not set, the default dpi of 72 (if not changes by command
	 		lines arguments) will be used.
	 * kwargs -- graphics context arguments
	 		If set, for instance color, everything on every page
	 		will be draw in the color, if not specified.
	 
	 Example:
	 	document('10cm, 400px', 72, color='green')
	 	
	"""

	if dpi is None:
		dpi = default.dpi

	if size is None:
		size = default.size
	if offset is None:
		offset = default.psoffset
	if extraborder is None:
		extraborder = default.extraborder

	current.document = kaplot.objects.Document(size=size, dpi=dpi, offset=offset, extraborder=extraborder, **kwargs)
	return current.document
	
def page(document=None, **kwargs):
	"""Adds a page on document and make it the current page
	
	If document not specified, the current document will be used, and a new one
	will be creates if it doesn't exist yet.
	
	As in 'document', keyword arguments like 'color' makes all objects on this page
	be drawn in that color (if not specified for that object)
	"""
	if document is None:
		_checkDocument()
		document = current.document
	current.page = kaplot.objects.Page(document, **kwargs)
	return current.page
	
def function(function, range=(0, 1., 0.01), container=None, **kwargs):
	"""Will draw a function on the current container
	
	Arguments:
	 * function -- if it is a function (meaning, callable in Python) it will be 
	 		called with an array(sepecified by range) of values (the x values). The result should
	 		be also an array (y values).
	 		If it's not callable, it will be assumed to be a Python expression(a string), and will be 
	 		evaluated
	 * range -- a tuple (x1, x2, step) which determines the x values for the function. Not that x2 is not
	 	in this range! If you need x2 to be in your range, add a small value (ie step/2)
	 	to x2, like: range=(1, 4.01, 0.1). If step is omitted, step is assumed 1.
	 	
	 Examples:
	  * function('x**2')
	  * function('x**2', range(0, 10, 0.1), color='orange')
	  * function(abs, range=(-10, 20), linestyle='dashed')
	 	
	 	
	 		
	"""
	if container is None:
		_checkBox()
		container = current.container
	x1, x2 = range[:2]
	if len(range) > 2:
		step = range[2]
	else:
		step = 1
	x = numpy.arange(x1, x2, step)
	if callable(function):
		y = function(x)
	else:
		y = eval(function)
	if isinstance(container, kaplot.objects.Box):
		if isinstance(function, basestring):
			if not container.title.text:
				container.title.text = function
			if not container.labels.left:
				container.labels.left = "y"
			if not container.labels.bottom:
				container.labels.bottom = "x"
	p = kaplot.objects.PolyLine(current.container, x, y, **kwargs)
	current.legend_objects.append(p)
	current.legend_types.append("line")
	return p, x, y
	
def parametric(z_or_x_function, yfunction=None, args=(), symbolName=None, symbolSize='5mm', range=(0, 1, 0.01), container=None, **kwargs):
	"""Draws a parametric equation specicfied by 2 functions or one complex function
	
	Arguments:
	 * z_or_x_function -- if yfunction is not specified, this is assumed to be a complex function.
	 		Otherwise, it's treated as the argument in the 'function' function, but now with 't' as
	 		variable.
	 * yfunction -- ...
	 * symbolName -- if specified will draw symbols on each (x, y) or (z) point specified by the
	 		function(s), with size symbolSize
	 * symbolSize -- see symbolName
	 * range -- see function
	"""
	if container is None:
		_checkBox()
		container = current.container
	t1, t2 = range[:2]
	if len(range) > 2:
		step = range[2]
	else:
		step = 1
	t = numpy.arange(t1, t2, step)
	if yfunction is None:
		z = eval(z_or_x_function)
		x = z.real
		y = z.imag
	else:
		if callable(z_or_x_function):
			x = z_or_x_function(t, *args)
		else:
			x = eval(z_or_x_function)
		if callable(yfunction):
			y = yfunction(t, *args)
		else:
			y = eval(yfunction)
			
	p = kaplot.objects.PolyLine(current.container, x, y, **kwargs)
	if symbolName:
		symbols(x, y, symbolName=symbolName, symbolSize=symbolSize, **kwargs)
	if isinstance(container, kaplot.objects.Box):
		if isinstance(z_or_x_function, basestring) and (isinstance(yfunction, basestring) or yfunction is None):
			if not container.title.text:
				if yfunction is None:
					container.title.text = "z = %s\n" % (z_or_x_function)
				else:
					container.title.text = "x = %s\ny = %s" % (z_or_x_function, yfunction)
			if not container.labels.left:
				container.labels.left = "y"
			if not container.labels.bottom:
				container.labels.bottom = "x"
	#current.object = pline
	current.legend_objects.append(p)
	current.legend_types.append("line")
	return p
	
def meshgrid(xrange, yrange):
	"""HIDE"""
	xar = numpy.arange(*xrange)
	yar = numpy.arange(*yrange)
	shape = (len(yar), len(xar))

	nx = len(xar)
	ny = len(yar)
	
	x = numpy.transpose(numpy.reshape(numpy.repeat(xar, len(yar)), (len(xar), len(yar))))
	y = numpy.reshape(numpy.repeat(yar, len(xar)), shape)
	x = x * 1.
	y = y * 1.
	#r = sqrt(x**2+y**2)
	return x, y

def function2d(function, args=(), xrange=(-1, 1, 0.01), yrange=(-1, 1, 0.01), container=None, array=True, **kwargs):
	"""Draws a 2d image where the sample value is specified by function
	
	Arguments:
	 * function -- same as in 'function', but it is a function of 2 arguments (x, y) and should
	 		return a 2 dimensional array if the 'array' argument is True, otherwise it should return
	 		the sample value. Note that using arrays if alot faster!
	 		Note that if function is a string (thus will be evaluated), the variable 'r' is
	 		also available, r=sqrt(x**2+y**2), which is the distance to the origin.
	 * args -- extra arguments which will be added to function, if it is a callable.
	 * xrange -- specifies the range in the x direction, same as in 'function'
	 * yrange -- same, now for y
	 
	 Example:
	  * function2d('e**-r**2')
	 
	 Example:
	 {{{#!python
	 def gaussian(x, y, mean_x, mean_y):
	   return e**(-(x-mean_x)**2 -(y-mean_y)**2)
	 function2d(gaussian, (0.2, 0.1))}}}
	 
	 
	
	"""
	if container is None:
		_checkBox()
		container = current.container
	#x1, x2 = range[:2]
	#if len(range) > 2:
	#	step = range[2]
	#else:
	#	step = 1
	#x = arange(x1, x2, step)
	if array:
		x, y = meshgrid(xrange, yrange)
		r = numpy.sqrt(x**2+y**2)
		if callable(function):
			data2d = function(x, y, *args)
		else:
			data2d = eval(function)
	else:
		xar = numpy.arange(*xrange)
		yar = numpy.arange(*yrange)
		shape = (len(yar), len(xar))
		data2d = numpy.zeros(shape=shape, type=Float)
		for xi, x in enumerate(xar):
			for yi, y in enumerate(yar):
				#print x, y, function(x, y, *args)
				if callable(function):
					data2d[yi][xi] = function(x, y, *args)
				else:
					data2d[yi][xi] = eval(function)
	#current.object = kaplot.objects.Indexed(current.container, x, y, **kwargs)
	#print data2d.min(), data2d.max()
	#print data2d
	return indexedimage(data2d, **kwargs)

def vectorfield(xfunction, yfunction, args=(), setlabels=True, scale=1., xscale=1., yscale=1, xrange=(-1, 1, 0.1), yrange=(-1, 1, 0.1), array=True, angle=0, symbolName="vector", container=None, **kwargs):
	"""Draws a vectorfield determined by the 2 functions xfunction and yfunction
	
	(TODO: as in parametric, it should also take a complex function)
	
	Arguments:
	 * xfunction -- see parametric
	 * yfunction -- see parametric
	 * args -- extra arguments to both the x and the yfunction
	 * setlabels -- boolean, if True, and the current container is a box, 
	 	the title, bottomlabel and leftlabel will be set (if not already set)
	 * scale -- see below
	 * xscale -- the vectors lengths will be scaled to scale*xscale in the x direction
	 * yscale -- the vectors lengths will be scaled to scale*yscale in the y direction
	 * xrange -- see function2d
	 * yrange -- see function2d
	 * array -- see function2d
	
	Examples:
	 * vectorfield('-y', 'x')
	 * vectorfield('x/sqrt(x**2+y**2)', 'y/sqrt(x**2+y**2)')
	 
	"""
	if container is None:
		_checkBox()
		container = current.container
	if isinstance(container, kaplot.objects.Box) and setlabels:
		if isinstance(xfunction, basestring) and isinstance(yfunction, basestring):
			if not container.title.text:
				container.title.text = "x' = %s; y' = %s\n" % (xfunction, yfunction)
			if not container.labels.left:
				container.labels.left = "y'"
			if not container.labels.bottom:
				container.labels.bottom = "x'"
	
	x, y = meshgrid(xrange, yrange)
	
	if callable(xfunction):
		xg = xfunction(x, y, *args)
	else:
		xg = eval(xfunction)
	
	if callable(yfunction):
		yg = yfunction(x, y, *args)
	else:
		yg = eval(yfunction)
	
	angles = numpy.arctan2(yg,xg)
	lengths = numpy.sqrt(xg**2+yg**2)
	lengths = lengths / lengths.max() * 3
	return symbols(numpy.array(x.flat), numpy.array(y.flat), symbolName=symbolName, angles=numpy.array(angles.flat)+angle,
		xscales=numpy.array(lengths.flat)*xscale*scale, yscales=numpy.array(lengths.flat)*yscale*scale)


def _get_selected():
	"""HIDE"""
	indices = list(current.container_indices)
	if not indices:
		return None, current.container_array
	else:
		current_array = current.container_array
		for index in indices[:-1]:
			current_array = current_array[index][1]
		return current_array[indices[-1]]
	
def vsplit(type=None, splits=2, weights=None, container=None):
	"""Creates containers, of type 'type', equally is size, relative the the current container's viewport
	
	vsplit stands for vertical split, thus all containers are of the same height
	
	Argument:
	 * type -- callable (can be a function) that creates a container(ie box or container)
	 		if not specified, containers will be creates
	 * splits -- the number of splits vertical splits
	 
	Example:
	 * vsplit(box, 3) # creates 3 containers
	 
	 	Will look something like this:
	 	
		Ascii art:
		{{{
		|-----|-----|-----|
		|  0  |  1  |  3  |
		|-----|-----|-----|
		}}}
		
		use the select function to make the containers current.
		{{{
		select(0)
		# add objects on container #0
		select(2)
		# add objects on container #2
		}}}
		
	TODO: explain splitting multiple times
	
	"""
	if container is None:
		_checkContainer()
		container = current.container
	if type is None:
		types = [kaplot.quickgen.container for k in range(splits)]
	elif callable(type):
		types = [type for k in range(splits)]
	else:
		types = type
	if weights is None:
		weights = [1. for k in range(splits)]
	(x1, y1), (x2, y2) = container.viewport
	dx = float(x2 - x1)
	selectedContainer, selectedSubList = _get_selected()
	
	totalweight = sum(weights)
	prevoffset = 0.
	offset = 0.
	for i in range(splits):
		offset += float(weights[i]) / totalweight
		type = types[i]
		sx1 = x1 + dx * prevoffset
		sx2 = x1 + dx * offset
		viewport = (sx1, y1), (sx2, y2)
		selectedSubList.append((type(viewport=viewport), []))
		prevoffset = offset
	current.container_indices.append(0)
	select(*current.container_indices)

def hsplit(type=None, splits=2, weights=None, container=None):
	"""Same as vsplit, but now horizontally"""
	if container is None:
		_checkContainer()
		container = current.container
	if type is None:
		types = [kaplot.quickgen.container for k in range(splits)]
	elif callable(type):
		types = [type for k in range(splits)]
	else:
		types = type
	if weights is None:
		weights = [1. for k in range(splits)]
	(x1, y1), (x2, y2) = container.viewport
	dy = float(y2 - y1)
	selectedContainer, selectedSubList = _get_selected()

	totalweight = sum(weights)
	prevoffset = 0.
	offset = 0.
	for i in range(splits):
		offset += float(weights[i]) / totalweight
		type = types[i]
		sy1 = y1 + dy * prevoffset
		sy2 = y1 + dy * offset
		viewport = (x1, sy1), (x2, sy2)
		selectedSubList.append((type(viewport=viewport), []))
		prevoffset = offset
	current.container_indices.append(0)
	select(*current.container_indices)
	
def copyobjects(fromcontainer, container=None):
	if container is None:
		_checkContainer()
		container = current.container
	container.copyObjectsFrom(fromcontainer)
	
def zoomcontainer(fromcontainer, world, drawrectangle=True, container=None, **kwargs):
	if container is None:
		_checkContainer()
		container = current.container
	copyobjects(fromcontainer, container=container)
	container.world = world
	(x1, y1), (x2, y2) = world
	if drawrectangle:
		return rectangle(x1, y1, x2, y2, container=fromcontainer, **kwargs)
	
	
	
	

def mozaic(x=2, y=2, type=None, container=None):
	"""Splits the current viewport into x by y new containers of type 'type'
	
	Similar to vsplit and hsplit, but now in both directions.
	
	Example:
	 {{{
	mozaic(2,3)
	select(0,0) # selecting the container in the lower left corner
	select(1,0) # lower right corner
	select(1,2) # top right corner}}}
	 
	
	"""
	if container is None:
		_checkContainer()
		container = current.container
	indices = list(current.container_indices)
	vsplit(type=kaplot.quickgen.container, splits=x, container=container)
	for i in range(x):
		indices.append(i)
		select(*indices)
		hsplit(type=type, splits=y)
		indices.pop()
	indices.append(0)
	indices.append(0)
	select(*indices)
	
def select(*indices):
	"""Selects the viewport indicated by indices as current
	
	List arguments:
	 * indices -- a list of integer values, specifing the container
		See vsplit, and mozaic for it's use.
	"""
	if current.container_array is None:
		raise Exception, "no container array if created (with vplit for instance)"
	current.container_indices = list(indices)
	selectedContainer, selectedSubList = _get_selected()
	current.container = selectedContainer
	return current.container
	
def graph(x_or_y, y=None, addlegend=True, container=None, **kwargs):
	"""Draws a graph(polyline) on the current container
	
	Arguments:
	 * x_or_y -- if y is not specified, it will be the y values, and the x values are
	 		generated, running from 0 to len(y)-1.
	 		Otherwise it should container the x values, an array, or other sequence
	 * y -- y values, a sequence or array
	 * addlegend -- if True, an entry will be created for the `autolegend`
	 
	 the autolegend function can create automated legends for polylines drawn with the
	 graph function.
	 
	"""
	if container is None:
		_checkBox()
		container = current.container
	if y is None:
		y = x_or_y
		x = numpy.arange(len(y))
	else:
		x = x_or_y
	p = kaplot.objects.PolyLine(container, x, y, **kwargs)
	if addlegend:
		current.legend_objects.append(p)
		current.legend_types.append("line")
	_checkRedraw()
	return p
	
def symbol(x, y, symbolName="dot", addlegend=True, symbolsize="5mm", xscale=None, yscale=None, angle=None, container=None, **kwargs):
	if container is None:
		_checkContainer()
		container = current.container
	if xscale is not None:
		xscale = [xscale]
	if yscale is not None:
		yscale = [yscale]
	if angle is not None:
		angle = [angle]
	s = symbols([x], [y], symbolName=symbolName, symbolsize=symbolsize, xscales=xscale, yscales=yscale, angles=angle, **kwargs)
	if addlegend:
		current.legend_objects.append(s)
		current.legend_types.append(symbolName)
	return s
	
def clearautolegend():
	"""Clear all information obtained for automaticly generating legends using autolegend"""
	current.legend_objects = []
	current.legend_types = []
	
def autolegend(*labels, **kwargs):
	"""Creates a legend with labels gives by labels.
	
	List arguments:
	 * labels -- strings, which will be displayed on the legend
	
	All other information (the type and the object) are internally stored.
	Function which support the autolegend are:
	 * graph
	 * function
	 * parametric
	 
	After use, the number of autolegend entrys equal to the 
	number of labels is removed. This makes it possible to
	spread legends across multiple containers.
	
	Example:
	autolegend('first try', 'second try', 'theory')
	
	"""

	l = legend(current.legend_types, labels, current.legend_objects, **kwargs)
	removelength = min(len(current.legend_objects), len(labels))
	current.legend_objects = current.legend_objects[removelength:]
	current.legend_types = current.legend_types[removelength:]
	return l
	
def xlabel(text, otheraxis=False, container=None, **kwargs):
	if container is None:
		_checkBox()
		container = current.container
	if hasattr(container, "labels"):
		labels = container.labels
		if otheraxis:
			label = labels.top
		else:
			label = labels.bottom
		label.text = text
		for name, value in kwargs.items():
			label.context[name] = value
		return label
	
def ylabel(text, otheraxis=False, container=None, **kwargs):
	if container is None:
		_checkBox()
		container = current.container
	if hasattr(container, "labels"):
		labels = container.labels
		if otheraxis:
			label = labels.right
		else:
			label = labels.left
		label.text = text
		#labels.context = kaplot.Context(labels.context, **kwargs)
		for name, value in kwargs.items():
			label.context[name] = value
		return label

def labels(xtext, ytext, container=None, **kwargs):
	x = xlabel(xtext, container=container, **kwargs)
	y = ylabel(ytext, container=container, **kwargs)
	return x,y

def __label(xtext, ytext, otheraxes=False, container=None, **kwargs):
	if container is None:
		_checkBox()
		container = current.container
	if hasattr(container, "labels"):
		labels = container.labels
		xlabel(xtext, otheraxes, container, **kwargs)
		ylabel(ytext, otheraxes, container, **kwargs)
		return labels

def ftspectrum(data, T=1, shifted=True, normalized=False, **kwargs):
	"""Creates a Fourier transform spectrum(using FFT).
	
	Arguments:
	 * data -- the data for which the the spectrum should be displayed
	 * T -- the sample time interval
	 * normalized -- if True, the maximum value will be 1
	"""
	_checkBox()
	import time
	start = time.time()
	#print "calculating fft of", len(I), "data points"
	#F = abs(fft.fft(I))
	F = fft.fft(data).real
	#print "done calculating fft, took", time.time() - start, "seconds"
	if shifted:
		length = len(F)
		center = int(ceil(length / 2.))
		y = concatenate([F[center:length], F[0:center]])
		x = (arange(0, len(y), type=Float) - length + center) / (length) / T
	else:
		length = float(len(F))
		y = F[0:]
		x = arange(0, len(y)) / length / T
		center = int(ceil(length / 2.))
		x = x[0:center+1]
		y = y[1:center]
	if normalized:
		y = y / max(y)
	#if logarithmic:
	#	y = log(y+0.01)
	#print "creating polyline"
	kaplot.objects.PolyLine(current.container, x, y, **kwargs)
	#kaplot.objects.Symbols(current.container, x, y, 'dot', color="red", **kwargs)

from kaplot.quickgen import *
#try:
#	from kaplot.quickgen import *
#except ImportError, e:
#	print kaplot.info("error importing module 'kaplot.quickgen'", e)

xlim = setdomain
ylim = setrange
def squarelim(xmin, xmax):
	xlim(xmin, xmax)
	ylim(xmin, xmax)
scatter = symbols

def title(text, container=None, **kwargs):
	if container is None:
		_checkBox()
		container = current.container
	if hasattr(container, "title"):
		container.title.text = text
	for name, value in kwargs.items():
		container.title.context[name] = value
	return container.title
		
def circle(x0, y0, r, parts=200, **kwargs):
	_checkContainer()
	step = 2*numpy.pi/parts
	theta = numpy.arange(0, 2*numpy.pi, step)
	x = x0 + r * numpy.sin(theta)
	y = y0 + r * numpy.cos(theta)
	return kaplot.objects.PolyLine(current.container, x, y, close=True, **kwargs)
	
def arcfill(r1, r2, theta1, theta2, x0=0, y0=0, parts1=100, parts2=200, **kwargs):
	_checkContainer()
	step1 = (theta2-theta1)/parts1
	step2 = (theta2-theta1)/parts2
	thetas1 = numpy.arange(theta1, theta2+step1/2, step1)
	thetas2 = numpy.arange(theta1, theta2+step2/2, step2)
	x1 = x0 + r1 * numpy.cos(thetas1)
	y1 = y0 + r1 * numpy.sin(thetas1)
	x2 = x0 + r2 * numpy.cos(thetas2)
	y2 = y0 + r2 * numpy.sin(thetas2)
	x = numpy.concatenate((x1, x2[::-1]))
	y = numpy.concatenate((y1, y2[::-1]))
	return kaplot.objects.Polygon(current.container, x, y, close=True, **kwargs)
	
def histogram(data, addlegend=True, binwidth=None, weights=None, bincount=10, datamin=None, datamax=None, normalize=False, drawverticals=False, fill=False, container=None, function=None, percentage=False, differential=True, **kwargs):
	if container is None:
		_checkContainer()
		container = current.container
	if datamin is None:
		datamin = min(data)
	if datamax is None:
		datamax = max(data)
	if binwidth is None:
		binwidth = (datamax - datamin)/bincount
	
	if "drawverticals" not in kwargs:
		kwargs["drawverticals"] = drawverticals
	if "fill" not in kwargs:
		kwargs["fill"] = fill
	bins_, bindata = _bindata(data, binwidth=binwidth, datamin=datamin, datamax=datamax, weights=weights)
	bindata = numpy.array(bindata)
	if normalize:
		bindata = bindata / sum(bindata)
		if differential:
			bindata /= binwidth
		if percentage:
			bindata *= 100
	if function:
		bindata = function(bindata)
	h = histogramline(bins_, bindata, **kwargs)

	if addlegend:
		current.legend_objects.append(h)
		current.legend_types.append("line")
	return h
	
def cumhistogram(data, addlegend=True, weights=None, bincount=None, binwidth=None, datamin=None, datamax=None, normalize=False, percentage=False, drawverticals=False, drawsides=False, fill=False, container=None, function=None, **kwargs):
	if container is None:
		_checkContainer()
		container = current.container
	if "drawverticals" not in kwargs:
		kwargs["drawverticals"] = drawverticals
	if "drawsides" not in kwargs:
		kwargs["drawsides"] = drawsides
	if "fill" not in kwargs:
		kwargs["fill"] = fill
	if datamin is None:
		datamin = min(data)
	if datamax is None:
		datamax = max(data)
	if binwidth is None and bincount is not None:
		binwidth = (datamax - datamin)/bincount
	
	#if weights is None:
	#	weights = 1.
	if binwidth is not None:
	#print max(values), std(values), mean(values)
		#bins, bindata = _bindata(values, binwidth=binwidth, datamin=minValue, datamax=maxValue)
		bins_, bindata = _bindata(data, binwidth=binwidth, datamin=datamin, datamax=datamax, weights=weights)
		bindata = numpy.array(bindata)
		#print bindata
		#print datamin, datamax
		if normalize:
			bindata = bindata / sum(bindata)
			if percentage:
				bindata *= 100
		bindata = numpy.cumsum(bindata)
		if function:
			bindata = function(bindata)
		#bins, bindata = _bindata(v, binwidth=1)
		#bindata = array(bindata)
		#bindata = bindata / sum(bindata) * 100
		sorteddata = bins_
	else:
		indices = numpy.argsort(data)
		sorteddata = (data)[indices]
		bindata = numpy.cumsum(numpy.ones(len(data)-1))
		if weights is not None:
			bindata = bindata * weights[indices][0:-1]
		if normalize:
			#bindata = bindata / sum(bindata) * 100
			bindata = bindata / bindata.max()
			if percentage:
				bindata *= 100
		if function:
			bindata = function(bindata)
			
	h = histogramline(sorteddata, bindata, **kwargs)

	if addlegend:
		current.legend_objects.append(h)
		current.legend_types.append("line")
	return h
	
	
def _todensityarray():
	pass

def density2d(x, y, binwidth=None, binwidthx=None, binwidthy=None, bincount=100, bincountx=None, bincounty=None, container=None, xmin=None, xmax=None, ymin=None, ymax=None, scale=1., rescale=None, drawimage=True, drawcontour=False, contourlevels=None, smooth=True, normalize=False, normalizecolumns=False, f=None, datamin=None, datamax=None, **kwargs):
	if container is None:
		_checkContainer()
		container = current.container
	if bincountx is None:
		bincountx = bincount
	if bincounty is None:
		bincounty = bincount
	if xmin is None:
		xmin = min(x)
	if xmax is None:
		xmax = max(x)
	if ymin is None:
		ymin = min(y)
	if ymax is None:
		ymax = max(y)
	width = xmax - xmin
	height = ymax - ymin
	xmin -= width * (scale-1)/2
	xmax += width * (scale-1)/2
	ymin -= height * (scale-1)/2
	ymax += height * (scale-1)/2
	
	if binwidthx is None:
		if binwidth is None:
			binwidthx = (xmax-xmin)/bincountx
		else:
			binwidthx = binwidth
	if binwidthy is None:
		if binwidth is None:
			binwidthy = (ymax-ymin)/bincounty
		else:
			binwidthy = binwidth

	xres = int((xmax-xmin) / binwidthx)
	yres = int((ymax-ymin) / binwidthy)
	if 0:
		print "#"*70
		print xmin, xmax
		print ymin, ymax
		print xres, yres
	xindex = ((x-xmin)/(xmax-xmin) * xres-0.5).astype(numpy.int)
	yindex = ((y-ymin)/(ymax-ymin) * yres-0.5).astype(numpy.int)
	indices = numpy.where((xindex < xres) & (yindex < yres) & (xindex >= 0) & (yindex >= 0))
	xindex = xindex[indices]
	yindex = yindex[indices]
	data = numpy.zeros((yres, xres), numpy.int)
	#data[yindex,xindex] += 1.
	for i in range(len(yindex)):
		data[yindex[i], xindex[i]] += 1
	#data = numpy.sqrt(data**4)
	#matrix = kaplot.Matrix.translate(-bincountx/2,-bincounty/2) * kaplot.Matrix.scale(2,2)
	#matrix = kaplot.Matrix.scale((ymax-ymin)/yres,(xmax-xmin)/xres) #*
	#matrix = None
	#matrix = kaplot.Matrix.scale((xmax-xmin)/xres,(ymax-ymin)/yres) * kaplot.Matrix.translate(xmax,ymax)
	#matrix = kaplot.Matrix.translate((xmax+xmin)/2.,(ymax+ymin)/2.) * kaplot.Matrix.scale((xmax-xmin)/xres,(ymax-ymin)/yres)
	#matrix = (kaplot.Matrix.scale((xmax-xmin)/xres,(ymax-ymin)/yres) * kaplot.Matrix.translate(-xres/2.,-yres/2.)).inverse()
	#matrix = kaplot.Matrix.scale((ymax-ymin)/yres,(xmax-xmin)/xres) * kaplot.Matrix.translate(-yres/2.,-xres/2.)
	#matrix = kaplot.Matrix.translate(-xres/2.,-yres/2.) * kaplot.Matrix.scale((xmax-xmin)/xres,(ymax-ymin)/yres)
	#data = numpy.log(data+1)
	resize = (xmin, ymin), (xmax, ymax)
	if resize not in kwargs:
		kwargs["resize"] = resize
	import kaplot.utils
	result = []
	data = data.astype(numpy.float32)
	if datamin and datamax:
		data = numpy.clip(data, datamin, datamax)
	data = (data-data.min())/(data.max()-data.min())
	if smooth:
		data = kaplot.utils.imagegaussianfilter(data, 1.1, 0, 'reflect')
	#print "###", data.min(), data.max()
	#print data.shape
	if normalizecolumns:
		for c in range(data.shape[1]):
			if data[:,c].max() > 0:
				data[:,c] /= data[:,c].max()
	if normalize:
		data = data / data.max()
	if f:
		data = f(data)
	if rescale:
		dmin, dmax = rescale
		data = data.astype(numpy.float32)
		normdata = (data-data.min())/(data.max()-data.min())
		data = normdata * (dmax-dmin) + dmin
	#print "###", data.min(), data.max()
	if drawimage:
		image = indexedimage(data, **kwargs)
		result.append(image)
	if drawcontour:
		if contourlevels is None:
			contourlevels = [(data.max() - data.min())/2. + data.min()]
		#for level in contourlevels:
		c = contour(data.astype(numpy.float32), contourlevels, **kwargs)
		result.append(c)
	if len(result) == 1:
		return result[0]
	else:
		return result
			
	#print data.max()
	#if "drawverticals" not in kwargs:
	#	kwargs["drawverticals"] = drawverticals
	#if "fill" not in kwargs:
	#	kwargs["fill"] = fill
	#bins_, bindata = _bindata(data, binwidth=binwidth, datamin=datamin, datamax=datamax)
	#bindata = numpy.array(bindata)
	#if normalize:
	#	bindata = bindata / sum(bindata) * 100
	#h = histogramline(bins_, bindata, **kwargs)

	#$if addlegend:
	#	current.legend_objects.append(h)
	#	current.legend_types.append("line")
	#return h
	#return image

def gaussian(x, mu, sigma):
	y = 1/(numpy.sqrt(math.pi*2)*sigma)*numpy.exp(-0.5*((x-mu)/sigma)**2)
	return y

def loggaussian(x, mu, sigma):
	y = numpy.log(1/(numpy.sqrt(math.pi*2)*sigma))  + -0.5*((x-mu)/sigma)**2
	return y
	
	
def mergerow(index=None,top=False,bottom=False,left=True,right=True):
	if index is None:
		for col in range(len(current.container_array)-1):
			select(col)
			current.container.drawOutsideLeft = True
			current.container.drawOutsideRight = True
			current.container.rightaxes[0].drawLabels = False
			select(col+1)
			current.container.drawOutsideLeft = True
			current.container.drawOutsideRight = True
			current.container.leftaxes[0].drawLabels = False
	else:
		for col in range(len(current.container_array)-1):
			select(col, index)
			if col > 0 or left:
				current.container.drawOutsideLeft = True
			current.container.drawOutsideRight = True
			current.container.rightaxes[0].drawLabels = False
			if top:
				current.container.drawOutsideTop = True
				current.container.topaxes[0].drawLabels = False
			if bottom:
				current.container.drawOutsideBottom = True
				current.container.bottomaxes[0].drawLabels = False
			select(col+1, index)
			current.container.drawOutsideLeft = True
			if col + 1 < len(current.container_array)-1 or right:
				current.container.drawOutsideRight = True
			current.container.leftaxes[0].drawLabels = False
			if top:
				current.container.drawOutsideTop = True
				current.container.topaxes[0].drawLabels = False
			if bottom:
				current.container.drawOutsideBottom = True
				current.container.bottomaxes[0].drawLabels = False

def mergecol(index=None,left=False,right=False):
	if index is None:
		for col in range(len(current.container_array)-1):
			select(col)
			current.container.drawOutsideTop = True
			current.container.drawOutsideBottom = True
			current.container.topaxes[0].drawLabels = False
			if left:
				current.container.drawOutsideLeft = True
			if right:
				current.container.drawOutsideRight = True
			select(col+1)
			current.container.drawOutsideTop = True
			current.container.drawOutsideBottom = True
			current.container.bottomaxes[0].drawLabels = False
			if left:
				current.container.drawOutsideLeft = True
			if right:
				current.container.drawOutsideRight = True
	for row in range(len(current.container_array[0][1])-1):
		select(index, row)
		current.container.drawOutsideTop = True
		current.container.topaxes[0].drawLabels = False
		select(index, row+1)
		current.container.drawOutsideBottom = True
		current.container.bottomaxes[0].drawLabels = False
		
def xlabels(show):
	current.container.bottomaxes[0].drawLabels = show

def ylabels(show):
	current.container.leftaxes[0].drawLabels = show
	
def configure_xaxis(**kwargs): #:, bottom=True, index=0):
	axes = current.container.bottomaxes + current.container.topaxes
	_configure_axis(axes, **kwargs)

def configure_yaxis(**kwargs):
	axes = current.container.leftaxes + current.container.rightaxes
	_configure_axis(axes, **kwargs)
	
def _configure_axis(axes, interval=None, subticks=None): #:, bottom=True, index=0):
	for axis in axes:
		if interval is not None:
			axis.interval = interval
		if subticks is not None:
			axis.subticks = subticks



def multisum(a, axes):
	correction = 0
	for axis in axes:
		a = numpy.sum(a, axis=axis-correction)
		correction += 1
	return a

def _minmax(x, y):
	return ( (min(x), min(y)), (max(x), max(y))) 


def _findlevels(image, *fractions):
	from scipy.optimize import fsolve
	def helper(level, fraction, image):
		return sum(image[image>level]) - fraction
	levels = []
	for fraction in fractions:
		level = fsolve(helper, image.mean() * 0.1, (fraction, image), xtol=0.01)
		levels.append(level)
	return levels

def probgraph(probgrid, axis, x=None, dx=None, resize=None, name=None, scaletounity=False, labelscaleyoffset=1., f=None, fit=False, **kwargs):
	#axes = allaxes[:axis] + allaxes[axis+1:]
	axes = range(len(probgrid.shape))
	axes.remove(axis)
	p = multisum(probgrid, axes=axes)
	if x is not None:
		dx = x[1] - x[0]
		x1 = x.min()
		x2 = x.max()
	elif resize is not None:
		x1, x2 = resize
		xs = (numpy.arange(len(p)) + 0.5) / (len(p))  * (x2-x1) + x1
		dx = abs(xs[1] - xs[0])
		#dx = (x2-x1)/float(len(p))
	dx = abs(dx)
	p /= p.sum() * dx
	#print p
	#if name is not None:
	if 1:
		if x is None:
			assert resize is not None
			x1, x2 = resize
			print (numpy.arange(len(p)) + 0.5)/ (len(p))
		else:
			xs = x
		#print xs
		#assert dx == abs(xs[1] - xs[0]), "%.20e %.20e" % (dx,  abs(xs[1] - xs[0]))
		#dx = abs(xs[1] - xs[0]) 
		mean = sum(xs*p*dx)
		sigma = sum((xs-mean)**2*p*dx)**0.5
		print ">>>", name, mean, sigma
		
		#text("%s = %.2f +/- %.2f" % (name, mean, sigma), x2-(x2-x1)*0.5, p.max() * labelscaleyoffset * 1.08, "center", "top", **kwargs)
		text("mean = %.2f +/- %.2f" % (mean, sigma), x2-(x2-x1)*0.5, p.max() * labelscaleyoffset * 1.01, "center", "bottom", **kwargs)
	
	if x is None:
		x1, x2 = resize
		x = xs
	else:
		assert len(p) == len(x)
	if scaletounity:
		p /= p.max()
	if f:
		y = f(p)
	else:
		y = p
	g = graph(x, y, **kwargs)
	if fit:
		ylim(0, y.max())
	#xlim(x1, x2)
	#print "xlim", x1, x2
	return g
	#grow(top=1.25)
	#labels(label, "p")
	#current.container.context.color = "green"

def _normalize(image):
	image = image * 1.
	image -= min(image.flat) #.min()
	return image/sum(image.flat)

def probimage2d(probgrid, axisx, axisy, x=None, y=None, resize=None, fill=True, colormap="whiterainbow", color=None, drawcontourlines=False, premultiply=False, addlegend=True, sigmas=3,**kwargs):
	#select(i, j)
	
	axes = range(len(probgrid.shape))
	axes.remove(axisx)
	axes.remove(axisy)
	p = multisum(probgrid, axes=axes)
	if axisx < axisy:
		p = numpy.transpose(p) 
	p = _normalize(p)
	sigmas = [0.682689492137 , 0.954499736104, 0.997300203937][:sigmas]
	contourlevels = _findlevels(p, *sigmas)
	#print contourlevels
	colormap = colormap
	if x is not None and y is not None:
		resize = _minmax(x, y)
	p = p.astype(numpy.float32)
	if colormap is not None:
		indexedimage(p, resize=resize, colormap=colormap, **kwargs)
	originalalpha = 1
	if "alpha" in kwargs:
		originalalpha = kwargs["alpha"]
	obj = None
	if fill is True and color is not None:
		color = kaplot.utils.getColor(color)
		for i, level in enumerate(contourlevels[::-1]):
			alpha = (i+1) * 1/3. * originalalpha
			levelcolor = color.blend(kaplot.Color.white, alpha)
			if premultiply:
				obj = contour(p, levels=[level], resize=resize, fill=True, color=levelcolor, addlegend=False)
			else:
				obj = contour(p, levels=[level], resize=resize, fill=True, color=color, alpha=alpha, addlegend=False)
			#contourfill(p, level, p.max() * 10, color=levelcolor) 
			#fillcontour(p.astype(numpy.float32), contourlevels, resize=resize, color="black", linewidth="2pt")
			#polygon(
	#print contourlevels
	if drawcontourlines:
		if color is not None:
			kwargs["color"] = color
		obj = c = contour(p, contourlevels, fill=False, resize=resize, addlegend=False, **kwargs)
		if addlegend:
			current.legend_objects.append(c)
			current.legend_types.append("line")
			
	
	#assert len(p) == len(y)
	#graph(y, p)
	#labels(labelx, labely)
	return obj
			
			
_scatter = scatter			
def scatter(*args, **kwargs):
	o = _scatter(*args, **kwargs)
	if "addlegend" not in kwargs or kwargs["addlegend"]:
		current.legend_objects.append(o)
		if "symbolName" in kwargs:
			current.legend_types.append(kwargs["symbolName"])
		else:
			current.legend_types.append("dot")
	return o
	
	
_histogramline = histogramline
def histogramline(*args, **kwargs):
	o = _histogramline(*args, **kwargs)
	if "addlegend" not in kwargs or kwargs["addlegend"]:
		current.legend_objects.append(o)
		current.legend_types.append("line")
	return o
	
_hline = hline
def hline(*args, **kwargs):
	o = _hline(*args, **kwargs)
	if "addlegend" not in kwargs or kwargs["addlegend"]:
		current.legend_objects.append(o)
		current.legend_types.append("line")
	return o
	
_vline = vline
def vline(*args, **kwargs):
	o = _vline(*args, **kwargs)
	if "addlegend" not in kwargs or kwargs["addlegend"]:
		current.legend_objects.append(o)
		current.legend_types.append("line")
	return o
	
_contour = contour
def contour(*args, **kwargs):
	o = _contour(*args, **kwargs)
	if "addlegend" not in kwargs or kwargs["addlegend"]:
		current.legend_objects.append(o)
		current.legend_types.append("line")
	return o	
