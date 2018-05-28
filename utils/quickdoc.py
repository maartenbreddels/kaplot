import Kdoc
from Kdoc.reflect import *
import kaplot
rootpackage = load(["kaplot", "kaplot.quick", "kaplot.quickgen"])
functions = []
for name, module in rootpackage.modules.items():
	#print "module", name
	#print "\tfunctions", module.functions.keys()
	functions.extend(module.functions.items())

print "[[TableOfContents()]]"
print """= Introduction =
/!\ This document it generated, so please don't edit it.

Some arguments for functions are not specified. For example, your will see '**kwargs' alot in the plot functions.
These are keyword arguments, and should (usually) be graphics context arguments, like 'color'. See KaplotContext for a description on the arguments.

Example:
{{{#!python
line(0, 0, 1, 1, color='red', linestyle='dash')
}}}

It is also assumed that your read KaplotDocQuickIntroduction!

"""

dev = ["device", "guidevice", "document", "page", "box", "container", "clear", "draw", "setdevice", "export"]
container = [
"grow", "setdomain", "setrange",
"vsplit", "hsplit", "mozaic", "select",
]
plot = ["function", "parametric", "graph", "function2d", "ftspectrum", "vectorfield",
"polyline", "line", "polygon", "indexedimage", "histogramline", "symbols", "errorbars", "errorrange", "fillrange", 
"contour", "contourfill", "innercolorbar", "legend", "autolegend", "clearautolegend",
"wcstext", "wcssphere", "wcssymbols",
]
decorator = [
"spacer", "border", "axes", "title", "labels", 
]

notothers = dev + container + plot + decorator
def printdoc(name, function):
	docstring = function.doc #function.argumentstring
	if "HIDE" not in docstring:
		print "== %s ==" % name
		print "'''%s%s'''\n\n" % (name, function.argumentstring.replace("''", "\"\""))
		print docstring.replace("''", "\"\"")

def printlist(list):
	for name in list:
		printdoc(name, dict(functions)[name])
	

print "= Device/document/page functions ="
printlist(dev)
print "= Container functions ="
printlist(container)
print "= Plot functions ="
printlist(plot)
print "= Decorator functions ="
printlist(decorator)
rest = [(name, function) for name, function in functions if name not in notothers]
if rest:
	print "= Other functions ="
	for name, function in rest:
		printdoc(name, function)
