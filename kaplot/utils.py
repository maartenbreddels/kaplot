# -*- coding: utf-8 -*-
#import kaplot.color
#import kaplot.colormap
import kaplot
from math import pi
import math
#import numpy.nd_image
import scipy.ndimage as nd_image
import numpy
import os
from numpy import *

def getColor(color):
	if isinstance(color, basestring):
		if color in kaplot.colors.keys():
			return kaplot.colors[color]
		else:
			raise ValueError, "unkown color: %r" % color
	elif isinstance(color, kaplot.Color):
		return color
	else:
		raise ValueError, "color should be a Color instance, or a string"

# TODO: this is the old name, refactor it out
decodeColor = getColor

def getLinestyle(linestyle):
	if isinstance(linestyle, list) or isinstance(linestyle, tuple):
		return linestyle
	elif linestyle in kaplot.linestyles:
		return kaplot.linestyles[linestyle]
	else:
		linestyles = kaplot.linestyles.keys()
		linestyles.sort()
		raise ValueError, "unkown linestyle: %r, possible values: %r" % (linestyle, linestyles)

def getColormap(colorMap):
	if isinstance(colorMap, kaplot.ColorMap):
		return colorMap
	elif isinstance(colorMap, basestring):
		if colorMap in kaplot.colormaps:
			return kaplot.colormaps[colorMap]
		else:
			cmapNames = kaplot.colormaps.keys()
			cmapNames.sort()
			raise ValueError, "unknown colormap: %r, possible values: %r" % (colorMap, cmapNames)
	elif callable(colorMap):
		return colorMap
	else:
		raise ValueError, "colormap should be a ColorMap instance, or a string"

def getFunction(function):
	if not callable(function):
		if function in kaplot.functions:
			return kaplot.functions[function]
		else:
			ValueError, "unknown function: %r, possible values: %r" % kaplot.functions.keys()
	else:
		return function

def todegrees(radians):
	"""Convert radians to degrees"""
	return radians * 180/pi

def toradians(degrees):
	"""Convert degrees to radians"""
	return degrees * pi/180

def splitDimension(dim):
	dim = dim.strip()
	done = False
	stringpos = 0
	while not done:
		if len(dim)-1 == stringpos:
			done = True
		elif dim[stringpos] not in "-+0123456789.":
			done = True
		else:
			stringpos += 1
	size, units = dim[:stringpos], dim[stringpos:]
	try:
		size = eval(size)
	except:
		raise ValueError, "invalid number '%s' (dim was %r)" % (size, dim)
	return size, units.strip()

def splitSize(size):
	parts = size.split(",")
	if len(parts) != 2:
		raise ValueError, "size didn't contain 1 ','"
	width, height = parts
	width, wunits = splitDimension(width)
	height, hunits = splitDimension(height)
	return width, wunits, height, hunits

def box_to_points(box, dpi):
	parts = box.split(",")
	if len(parts) != 4:
		raise ValueError, "size didn't contain 3 ','"
	points = []
	for part in parts:
		value, units = splitDimension(part)
		pixels = kaplot.utils.convertToPixels(value, units, dpi)
		points.append(int(kaplot.utils.convertPixelsTo(pixels, "pt")))
	return points
	
def getSize(size):
	if size in kaplot.papersize:
		return splitSize(kaplot.papersize[size])
	else:
		return splitSize(size)
	

supportedunits = ["mm", "cm", "pt", "in", "px"]

def convertToPixels(n, units, dpi=72):
	if units == "mm":
		return (n * dpi) / 25.4
	if units == "cm":
		return (n * dpi) / 2.54
	if units in ["pt"]:
		return (n * dpi) / 72
	if units in ["in"]:
		return n * dpi
	if units in ["px"]:
		return n
	else:
		raise ValueError, "unkown units: '%s'" % units

def convertPixelsTo(pixels, units, dpi=72):
	if units == "mm":
		return (pixels * 25.4) / dpi
	if units == "cm":
		return (pixels * 2.54) / dpi
	if units in ["pt"]:
		return (pixels  * 72)/ dpi
	if units in ["in"]:
		return pixels / dpi
	if units in ["px"]:
		return pixels
	else:
		raise ValueError, "unkown units: '%s'" % units

def __dimToViewport(dim, device):
	unitMatrix = device.getUnitMatrix("px")
	viewportMatrix = device.getViewportMatrix()
	matrix = viewportMatrix.nolocation().inverse() * unitMatrix
	width, units = kaplot.utils.splitDimension(dim)
	pixelWidth = kaplot.utils.convertToPixels(width, units, dpi=device.dpi)
	width, height = matrix * (pixelWidth, pixelWidth)
	return width, height

def __dimToWorld(dim, device):
	worldMatrix = device.getWorldMatrix()
	vpwidth, vpheight = dimToViewport(dim, device)
	width, height = worldMatrix.nolocation().inverse() * (vpwidth, vpheight)
	return width, height

def _parseSize(size, outputUnits, dpi=72):
	parts = size.split(",")
	if len(parts) != 2:
		raise ValueError, "size didn't contain a ','"
	width, height = parts
	width, units = splitDimension(width)
	height, units = splitDimension(height)
	height = convertUnits(height, units, outputUnits, dpi)

def imageresize(image, newwidth, newheight):
	height, width = image.shape
	zoomx = float(newwidth)/width
	zoomy = float(newheight)/height
	return nd_image.zoom(image, (zoomx, zoomy), order=2)

def imageboxcarfilter(image, size, mode='nearest'):
	return nd_image.boxcar_filter(image, size=size, mode=mode)

def imagegaussianfilter(image, sigma, order=0, mode='nearest'):
	return nd_image.gaussian_filter(image, sigma=sigma, order=order, mode=mode)


def getHalign(tickangle, textangle):
	"""
	Return the horizontal alignment based on the (-22.5 degrees rotated)'octant'
	the tickangle is in respect to the baseline of the text.

	The first octant starts at -22.5 and ends at 22.5 degrees.

	octant:
		1,2,8:		"left"
		3,7:		"center"
		4,5,6:		"right"

	"""
	tickangle = (math.degrees(tickangle) + 360) % 360
	textangle = (math.degrees(textangle) + 360) % 360
	angle = (tickangle-textangle + 360.0) % 360
	octant = int(((angle+22.5) % 360) / 45) + 1
	print "octant", octant
	if octant in [1,2,8]:
		return "left"
	elif octant in [3,7]:
		return "center"
	elif octant in [4,5,6]:
		return "right"
	return "center"


def getValign(tickangle, textangle):
	"""
	Return the vertical alignment based on the (-22.5 degrees rotated)'octant'
	the tickangle is in respect to the baseline of the text.

	The first octant starts at -22.5 and ends at 22.5 degrees.

	octant:
		2,3,4:		"bottom"
		1,5:		"center"
		6,7,8:		"top"

	"""
	tickangle = (math.degrees(tickangle) + 360) % 360
	textangle = (math.degrees(textangle) + 360) % 360
	angle = (tickangle-textangle + 360.0) % 360
	octant = int(((angle+22.5) % 360) / 45) + 1
	print "octant", octant
	if octant in [2,3,4]:
		return "bottom"
	elif octant in [1,5]:
		return "center"
	elif octant in [6,7,8]:
		return "top"
	return "center"

def getPageFilename(filename, pageNr, pageCount):
	if pageCount == 1:
		return filename
	elif pageCount > 1:
		basename, ext = os.path.splitext(filename)
		zerofill = int(math.log(pageCount)/math.log(10)) + 1
		format = basename +("-page-%%0%ii" % zerofill) + ext
		return format % pageNr


def createColorbar(direction, colors):
	step = 1.0 / (colors - 1) 
	
	if direction == "up":
		data = numpy.array([numpy.arange(0, 1 + step/2, step)]*1)
		data = numpy.transpose(data)
		corrmatrix = kaplot.matrix.Matrix.translate((-0.5, 0.0))
	elif direction == "left":
		data = numpy.array([numpy.arange(1, 0 - step/2, -step)]*1)
		corrmatrix = kaplot.matrix.Matrix.translate((0.0, -0.5))
	elif direction == "down":
		data = numpy.array([numpy.arange(1, 0 - step/2, -step)]*1)
		data = numpy.transpose(data)
		corrmatrix = kaplot.matrix.Matrix.translate((-0.5, 0.0))
	elif direction == "right":
		data = numpy.array([numpy.arange(0, 1 + step/2, step)]*1)
		corrmatrix = kaplot.matrix.Matrix.translate((0.0, -0.5))
	else:
		raise Exception, "invalid direction" +str(direction) 
	return data
	
def gaussian(x, mean, sigma):
	return 1/(sqrt(2*pi)*sigma)*e**(-(x-mean)**2/(2*sigma**2))

def gaussian2d(x, y, meanx, meany, sigma):
	return 1/(sqrt(2*pi)*sigma)*e**(-(((x-meanx)**2.+(y-meany)**2.))/(2*sigma**2))

def subdivide(v1, v2, ticks=3, subticks=None, interval=None, start=None, integer=False, logarithmic=False):
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
	
	realinterval = interval
	if realinterval == None:
		diff = v2 - v1
		#ticks = 3
		tick = diff / ticks
		error = diff / 10.0
		realinterval = magicnr(tick, error)

	interval = realinterval

	if integer:
		interval = int(interval+0.5)
		if interval == 0 and realinterval > 0:
			interval = 1
		if interval == 0 and realinterval < 0:
			interval = -1

	if start == None:
		start = fround(v1, interval) -interval

	if integer:
		ticks = numpy.arange(start, int(v2+1) + interval*1, interval)
	else:
		ticks = numpy.arange(start, v2 + interval*1.5, interval)
	subticklist = []
	#import pdb;pdb.set_trace()

	if subticks is not None and subticks > 0:
		if logarithmic:
			sigma = 1.0e-9
			# ok, this looks weird, but take base 10, with 8 subticks as an example
			# and it will make sense :), or base 3, with 1 subtick
			offsets = log(numpy.arange(2, subticks+1+sigma))/log(subticks+2)
			length = len(ticks)
			for i in range(length-1):
				offset = ticks[i]
				width = ticks[i+1] - ticks[i]
				subticklist.extend(list(offset+offsets*width))
		else:
			#print float(interval), subticks
			subinterval = float(interval) / (1+subticks)
			length = len(ticks)
			for i in range(length-1):
				v1 = ticks[i]+subinterval
				v2 = ticks[i+1]
				subticklist.extend(numpy.arange(v1, v2-subinterval/2, subinterval))
	if subticks is not None:
		return ticks, numpy.array(subticklist)
	else:
		return ticks
	