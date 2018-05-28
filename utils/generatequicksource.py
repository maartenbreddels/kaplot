import kaplot
import kaplot.objects
#import kaplot.astro
import inspect
import sys
#import kaplot.astro

quickdoc = """"""

initcode = """from kaplot.quick import *
import kaplot
import kaplot.objects
#import kaplot.astro
from kaplot.quick import _checkPage, _checkContainer
"""


def isPlotObject(o):
	return type(o) == type and issubclass(o, kaplot.objects.PlotObject)

def isContainer(o):
	return type(o) == type and issubclass(o, kaplot.objects.Container)

def isDecorator(o):
	return type(o) == type and issubclass(o, kaplot.objects.Decorator)

def getObjects(module):
	names = dir(module)
	objects = [getattr(module, name) for name in names]
	items = zip(names, objects)
	return [(name, object) for name, object in items]

#allobjects = getPlotObjects(kaplot.objects) + getPlotObjects(kaplot.astro)
#allobjects = getPlotObjects(kaplot.objects)
#allobjects.sort(lambda a,b: cmp(a[0], b[0]))
#allobjects.remove(PlotObject)
#allobjects.remove(Decorator)
#allobjects.remove(Container)
#containers = [(name, object) for (name, object) in allobjects if isContainer(object)]
#decorators = [(name, object) for (name, object) in allobjects if isDecorator(object)]
#plotobjects = [k for k in allobjects if k not in containers and k not in decorators]
#plotobjects = [k for k in allobjects if k not in containers]
allObjects = []
allObjects.extend(getObjects(kaplot.objects))
#allObjects.extend(getObjects(kaplot.astro))
plotObjects = [(name, object) for (name, object) in allObjects if isPlotObject(object)]
containers = [(name, object) for (name, object) in allObjects if isContainer(object)]
decorators = [(name, object) for (name, object) in allObjects if isDecorator(object)]
#print allObjects
#print containers, plotObjects

def printcode(name, plotobject):
	arguments = inspect.getargspec(plotobject.__init__)
	#print >>sys.stderr, arguments
	parentName = arguments[0][1]
	if len(arguments[0]) > 2 and arguments[0][2] == "wcs":
		hasWcs = False
	else:
		hasWcs = False
	#print parentName
	if isContainer(plotobject) and parentName != "page":
		raise NameError, "container should have 'page' as first argument, not: %r, for contructor of %r" % (parentName, plotobject)
	elif isPlotObject(plotobject) and parentName != "container":
		raise NameError, "PlotObject should have 'container' as first argument, not: %r, for contructor of %r" % (parentName, plotobject)
	elif isDecorator(plotobject) and parentName != "container":
		raise NameError, "Decorator should have 'container' as first argument, not: %r, for contructor of %r" % (parentName, plotobject)

	#print arguments
	#print arguments
	for argname in ["self"]: #, "lock", "context"]:
		if argname in arguments[0]:
			arguments[0].remove(argname)
	#print arguments
	orgarguments = arguments
	#hasWcs
	#(['container', 'data2d', 'mask2d', 'colormap', 'datamin', 'datamax', 'function', 'lock', 'context'], 
	#	None, 'kwargs', 
	#	(None, 'rainbow', None, None, 'linear', True, None))
	keywordValues = []
	if arguments[3]:
		keywordValues = list(arguments[3])
	
	keywordValues.append(None) # container/parent
	if hasWcs:
		keywordValues.append(None) # wcs/projection

	if hasWcs:
		argumentNames = arguments[0][2:]
	else:
		argumentNames = arguments[0][1:]
	
	argumentNames.append(parentName)
	if hasWcs:
		argumentNames.append("wcs")
	

	arguments = (argumentNames, arguments[1], arguments[2], tuple(keywordValues))
	#print arguments

	ctorformat = inspect.formatargspec(*arguments)
	print "def %s%s:" % (name.lower(), ctorformat)
	if hasattr(plotobject, "__fdoc__"):
		print '\t\"""%s"""' % plotobject.__fdoc__
	else:
		print >>sys.stderr, "object %r has no docstring(__fdoc__)" % name
		
	arguments = orgarguments

	defaults = arguments[3]
	if defaults and len(defaults) > 0:
		defaults = arguments[0][-len(defaults):]
		#print `defaults`
		arguments = arguments[0], arguments[1], arguments[2], defaults
	args, varargs, varkw, defaults = arguments
	#if isContainer(plotobject):
	#	args = ["current.plot"] + args
	#else:
	#	args = ["current.container"] + args
	ctorformat = inspect.formatargspec(args, varargs, varkw, defaults, str, lambda x: "*"+x, lambda x: "**"+x, lambda x: "="+x)

	packageName = ".".join(plotobject.__module__.split(".")[:2])
	#print "\t_checkPlot()"

	if isContainer(plotobject):
		print "\tif page is None:"
		print "\t\t_checkPage()"
		print "\t\tpage = current.page"
	elif isDecorator(plotobject):
		print "\tif container is None:"
		print "\t\t_checkContainer()"
		print "\t\tcontainer = current.container"
	else:
		print "\tif container is None:"
		print "\t\t_checkContainer()"
		print "\t\tcontainer = current.container"
	if hasWcs:
		print "\tif wcs is None:"
		print "\t\t_checkWcs()"
		print "\t\twcs = current.wcs"

	if isPlotObject(plotobject):
		print "\tcurrent.object = %s.%s%s" % (packageName, name, ctorformat)
		print "\treturn current.object"
	if isDecorator(plotobject):
		print "\tcurrent.object = %s.%s%s" % (packageName, name, ctorformat)
		print "\treturn current.object"
	if isContainer(plotobject):
		print "\tcurrent.container = %s.%s%s" % (packageName, name, ctorformat)
		#print "\tcurrent.container = current.object"
		print "\treturn current.container"
		#print "\tcurrent.plot.add(current.object)"
	#elif isDecorator(plotobject):
	#	print "\tcurrent.container.addDecorator(current.object)"
	#else:
		#print "\tcurrent.container.add(current.object)"
	print

# printing begins here
print '"""%s"""' % quickdoc
print initcode
print "# from plotobjects"
for name, plotobject in plotObjects:
	if name != "PlotObject":
		printcode(name, plotobject)

print "# from decorators"
for name, decorator in decorators:
	if name != "Decorator":
		printcode(name, decorator)

print "# from containers"
for name, plotobject in containers:
	printcode(name, plotobject)

#print "# from decorators"
#for name, plotobject in decorators:
#	printcode(name, plotobject)
