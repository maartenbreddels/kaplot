# -*- coding: utf-8 -*-
"""An image uses a colormap to map it's value to a color.

Colormaps should be callable objects, like a function, lambda, or an object
with the __call__ method.

If you want to make you own colormap in Kplot you can just create a function.
	def totalwhite(value):
		return Color.white

or a lambda object:
	lambda value: return Color(value, 0, 0)

or a class with the __call__ method:
	class SharpEdgeColorMap:
		def __init__(self, colorlist):
			self.colorlist = colorlist
		def __call__(self,  value):
			length = len(self.colorlist)
			index = int((value * (length-1)))
			return self.colorlist[index]

the colormap will be called with values between 0 and 1. Where 0 should map
to the color of the lowest value, and 1 should map to the color with the highest
value.

Use the ColorMap class to make colormaps that linear interpolates between colors

"""

from kaplot.color import Color
from kaplot.utils import getColor
import math

class ColorMap(object):
	"""A colormap that linearly interpolates between colors in a list

	example:
		colormap = ColorMap([Color.red, Color.white, Color.green])
	With this colormap, the minimum intensity maps to red, the maximum to
	green. The mean maps to white, and other values are linear interpolated.

	There are some predefined ColorMaps
		ColorMap.rainbow:
			purple-blue-cyan-green-yellow-red
		ColorMap.heat:
			black-red-orange-white
		ColorMap.cool:
			black-blue-white
		ColorMap.blackwhite:
			black-white
		ColorMap.whiteblack:
			white-black
	"""
	def __init__(self, colors, interpolate=True):
		"""Constructor

		Arguments:
		colors -- A sequence of Kplot.Color objects
		"""
		self.colors = [getColor(k) for k in colors]
		self.interpolate = interpolate

	def __call__(self, position):
		length = float(len(self.colors))
		if not self.interpolate:
			colindex = int(math.floor(0.5+(float(position) * (length-1))))
			return self.colors[colindex]
		else:
			
			colindex1 = int(math.floor((float(position) * (length-1))))
			colindex2 = int(math.ceil((float(position) * (length-1))))
			color1 = self.colors[colindex1]
			color2 = self.colors[colindex2]
			rdiff = color2.r - color1.r
			gdiff = color2.g - color1.g
			bdiff = color2.b - color1.b
			relposition = self.getRelpos(position, colindex1, length)
			color = Color(color1.r + rdiff*relposition, color1.g + gdiff*relposition, color1.b + bdiff*relposition)
		return color

	def getRelpos(self, position, colorindex, colorCount):
		return (position - colorindex / (colorCount-1)) * (colorCount-1)

import numpy

class LevelColorMap(ColorMap):
	def __init__(self, colors, levels):
		ColorMap.__init__(self, colors)
		if len(colors) != len(levels)-1:
			raise ValueError, "length of colors should be 1 less than length of levels"
		self.levels = numpy.array(levels, numpy.Float)
		self.levelsn = (self.levels - min(self.levels)) / (max(self.levels) - min(self.levels))

	def __call__(self, index):
		larger = self.levelsn > index
		#smaller = self.levelsn <= index
		llist = larger.tolist()
		if 1 in llist:
			index1 = llist.index(1) - 1
		else:
			index1 = len(self.colors)-1
		index1 = min(index1, len(self.colors)-1)
		import pdb
		#pdb.set_trace()
		#smaller = smaller.tolist()
		#smaller.reverse()
		#index2 = larger.index(1)
		#index2 = len(self.colors)-1-index2
		return self.colors[index1]

colormaps = {}
colormaps["whiterainbow"] = ColorMap([Color.white, Color.purple, Color.blue, Color.cyan, Color.green, Color.yellow, Color.red])
colormaps["rainbow"] = ColorMap([Color.purple, Color.blue, Color.cyan, Color.green, Color.yellow, Color.red])
colormaps["heat"] = ColorMap([Color.black, Color.red, Color.orange, Color.white])
colormaps["heat2"] = ColorMap([Color.black, Color.blue, Color.red, Color.white])
colormaps["cool"] = ColorMap([Color.black, Color.blue, Color.white])
colormaps["blackwhite"] = ColorMap([Color.black, Color.white])
colormaps["whiteblack"] = ColorMap([Color.white, Color.black])
colormaps["whiteblackred"] = ColorMap([Color.white, Color.black, Color.red])
colormaps["whiteblue"] = ColorMap([Color.white, Color.blue])
colormaps["whitered"] = ColorMap([Color.white, Color.red])
colormaps["redwhiteblue"] = ColorMap([Color.red, Color.white, Color.blue])
colormaps["bluewhitered"] = ColorMap([Color.blue, Color.white, Color.red])

for key, value in colormaps.items():
	setattr(ColorMap, key, value)