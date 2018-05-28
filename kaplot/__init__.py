__version__ = "0.3"
from numpy import *

class size(object):
	default = "25cm, 15cm"
	
papersize = {}
width = 841
height = 1189
for format in range(11):
	papersize["A%i" % format] = "%imm, %imm" % (width, height)
	papersize["A%iL" % format] = "%imm, %imm" % (height, width)
	width, height = height/2, width
	
#print papersize
	
defaultDpi = 72
import kaplot.text as textmod
import kaplot.objects
from kaplot.cext._kaplot import Matrix, Vector
from kaplot.context import Context
from kaplot.devices.aggdevice import AggDeviceBase, AggDeviceWindow
#from kaplot.gui.tk.window import createImageWindow
from color import Color, colors, nicecolors
import kaplot.markers
from kaplot.functions import functions
from kaplot.pattern import patterns
from kaplot.colormaps import colormaps, ColorMap
from linestyle import linestyles, alllinestyles
import kaplot.data
import kaplot.utils


def window(interactive=False):
	return createImageWindow(interactive)



defaultContext = kaplot.Context()
defaultContext.color = "black"
defaultContext.alpha = 1.
defaultContext.linestyle = "normal"
defaultContext.linewidth = "1px"
defaultContext.fontname = "Verdana"
defaultContext.fontsize = "10mm"
defaultContext.fillstyle = "fill"
defaultContext.patternsize = "5mm"
defaultContext.symbolsize = "3mm"

printInfo = True
printDebug = False
indentString = "\t"

# lists to prevent msg'es to repeat
_infoMsgs = []
_debugMsgs = []

import time
import sys

from quick import *


def info(*args, **kwargs):
	if printInfo:
		timestr = time.strftime("%H:%M:%S")
		timestr = "%06.3f" % time.clock()
		msg = " ".join([str(k) for k in args])
		if "printonce" in kwargs:
			if msg in _infoMsgs:
				return
			else:
				_infoMsgs.append(msg)
		print >>sys.stderr, "INFO [%s]:" % timestr, msg

def debug(*args, **kwargs):
	if printDebug:
		timestr = time.strftime("%H:%M:%S")
		timestr = "%06.3f" % time.clock()
		msg = " ".join([str(k) for k in args])
		if "printonce" in kwargs:
			if msg in _debugMsgs:
				return
			else:
				_debugMsgs.append(msg)
		print >>sys.stderr, "DEBUG[%s]:" % timestr, msg




#import kaplot.text.fontfamilies
#import kaplot.text.fonts
#kaplot.text.fonts.findFontFamilies()

