""""""
from kaplot.quick import *
import kaplot
import kaplot.objects
#import kaplot.astro
from kaplot.quick import _checkPage, _checkContainer

# from plotobjects
def barchart(datalist, autoscale=True, contexts=None, barwidth=0.80000000000000004, groupspacing=0.10000000000000001, sortbars=False, container=None, **kwargs):
	if container is None:
		_checkContainer()
		container = current.container
	current.object = kaplot.objects.BarChart(container, datalist, autoscale=autoscale, contexts=contexts, barwidth=barwidth, groupspacing=groupspacing, sortbars=sortbars, **kwargs)
	return current.object

def contour(data2d, levels, matrix=None, container=None, **kwargs):
	"""HIDE"""
	if container is None:
		_checkContainer()
		container = current.container
	current.object = kaplot.objects.Contour(container, data2d, levels, matrix=matrix, **kwargs)
	return current.object

def contourfill(data2d, level1, level2, container=None, **kwargs):
	"""HIDE"""
	if container is None:
		_checkContainer()
		container = current.container
	current.object = kaplot.objects.ContourFill(container, data2d, level1, level2, **kwargs)
	return current.object

def errorbars(x, y, size='3mm', xerr=None, yerr=None, xpos=None, xneg=None, ypos=None, yneg=None, container=None, **kwargs):
	"""Draws errorbar at (x[n],y[n]) locations
	
	Arguments:
	 * xerr -- error in x direction, both positive and negative
	 * xpos -- positive error in x, overriding xerr
	 * xneg, ypos, yerr -- ...
	
	"""
	if container is None:
		_checkContainer()
		container = current.container
	current.object = kaplot.objects.ErrorBars(container, x, y, size=size, xerr=xerr, yerr=yerr, xpos=xpos, xneg=xneg, ypos=ypos, yneg=yneg, **kwargs)
	return current.object

def errorrange(x, y, err, pos=None, neg=None, fill=True, caps=False, container=None, **kwargs):
	"""Fills between the errors instead of drawing error bars (see errorbars)
	
	Arguments:
	 * x, y -- arrays or sequences containing the locations
	 * err -- the error in y, both positive and negative
	 * pos, neg -- the positive and negative error in y, overriding err
	 * fill -- if False, doesn't fill, but draws a line at the edges
	 * caps -- if fill is False, and caps is False, the 'caps' at the left and right end are not drawn
	"""
	if container is None:
		_checkContainer()
		container = current.container
	current.object = kaplot.objects.ErrorRange(container, x, y, err, pos=pos, neg=neg, fill=fill, caps=caps, **kwargs)
	return current.object

def fillrange(x, y, level=0, container=None, **kwargs):
	"""Draws a polygon between the y values and level"""
	if container is None:
		_checkContainer()
		container = current.container
	current.object = kaplot.objects.FillRange(container, x, y, level=level, **kwargs)
	return current.object

def grid(subgrid=False, xinterval=None, xinteger=False, xstart=None, xsubticks=4, xlogarithmic=False, yinterval=None, yinteger=False, ystart=None, ysubticks=4, ylogarithmic=False, container=None, **kwargs):
	"""Draws a grid on the whole of the container

	Arguments:
	 * subgrid == if True, only draw the gridlines of the minor ticks
	 * xinterval -- if specified, the major tick seperation for the x axis
	 * xinteger -- if True, x will always be an integer, so no floating point strings in your plot
	 * xstart -- if specified, the start value for the major ticks
	 * xsubticks -- the number of subticks (minor ticks) between mayor ticks
	 * xlogarithmic -- if True, the minor subticks will be seperated as on logarithmic paper.
	 		Note that you have to take the logarithm of your data yourself. Also, labels will
	 		be draws as the base (currently only 10 is supported) with the x-value as superscript
	 * yinterval and the rest -- same, but now for y
	 		
	 TODO: example and explain how to do custom labeling and tick locations
	"""
	if container is None:
		_checkContainer()
		container = current.container
	current.object = kaplot.objects.Grid(container, subgrid=subgrid, xinterval=xinterval, xinteger=xinteger, xstart=xstart, xsubticks=xsubticks, xlogarithmic=xlogarithmic, yinterval=yinterval, yinteger=yinteger, ystart=ystart, ysubticks=ysubticks, ylogarithmic=ylogarithmic, **kwargs)
	return current.object

def histogramline(bins, data, binned=True, bincount=10, fill=True, drawverticals=True, drawsides=True, container=None, **kwargs):
	"""Draws a histogram line
	
	Arguments:
	 * bins -- values of the bins, the first bin will be drawn between bins[0] and bins[1]
	 * data -- the binned or unbinned data. If unbinned, the height of the bin, otherwise the raw data
	 * binned -- if False, data will be binned according to bincount
	 * fill -- boolean, fill or just draw the outline
	 * drawverticals -- if fill is False, this determines if the vertical lines between bins are also drawn
	 * drawsides -- if fill is False, this determines if the outer left and right line are drawn
	"""
	if container is None:
		_checkContainer()
		container = current.container
	current.object = kaplot.objects.HistogramLine(container, bins, data, binned=binned, bincount=bincount, fill=fill, drawverticals=drawverticals, drawsides=drawsides, **kwargs)
	return current.object

def indexedimage(data2d, matrix=None, mask2d=None, colormap='rainbow', datamin=None, datamax=None, function='linear', resize=None, context=None, container=None, **kwargs):
	"""Draws an intensity image using the colormap to map the intensity to a color
	
	Example:
	 * {{{#!python
    x, y = meshgrid()
    I = e**-(x**2+y**2)
    indexedimage(I, colormap='cool')}}}
	"""
	if container is None:
		_checkContainer()
		container = current.container
	current.object = kaplot.objects.IndexedImage(container, data2d, matrix=matrix, mask2d=mask2d, colormap=colormap, datamin=datamin, datamax=datamax, function=function, resize=resize, context=context, **kwargs)
	return current.object

def innercolorbar(label=None, image=None, levels=[], direction='up', location='right, top', labelposition=None, size=None, colormap='rainbow', datamin=None, datamax=None, edgespacing='10mm', container=None, **kwargs):
	"""HIDE"""
	if container is None:
		_checkContainer()
		container = current.container
	current.object = kaplot.objects.InnerColorbar(container, label=label, image=image, levels=levels, direction=direction, location=location, labelposition=labelposition, size=size, colormap=colormap, datamin=datamin, datamax=datamax, edgespacing=edgespacing, **kwargs)
	return current.object

def legend(types, labels, objects, location='right, top', spacing='2mm', edgespacing='10mm', borderspacing='2mm', linelength='1cm', container=None, **kwargs):
	"""Draws a legend, as information for graphs for instance
	
	Arguments:
	 * types -- a list of string, specifing the marker that should be drawn
	 * labels -- a list of string
	 * location -- specifies where the legend is drawn.
	 		Format is "<hloc>, <vloc>", where <hloc> is 'left', 'center' or 'top'
	 		and <vloc> is  'bottom', 'center' or 'top'
	 * spacing -- the horizontal seperation between the symbols and the labels
	 * edgespacing -- the displacement from the edge, specified by 'location'
	 * borderspacing -- the seperation of the text and symbols, and the border drawn
	 		around it
	 * linelength -- if type contains a line, it's length will be specified by this
	 		arguments. (dotted or dashed lines sometimes need to be longer to be
	 		clearly visible)
	 	
	 	
	"""
	if container is None:
		_checkContainer()
		container = current.container
	current.object = kaplot.objects.Legend(container, types, labels, objects, location=location, spacing=spacing, edgespacing=edgespacing, borderspacing=borderspacing, linelength=linelength, **kwargs)
	return current.object

def line(x1, y1, x2=1, y2=2, container=None, **kwargs):
	"""Draws a line from x1,y1 to x2,y2
	Example:
	 * line(0, 0, 10, 5)
	 * line(20, -5, 2, 50)
	"""
	if container is None:
		_checkContainer()
		container = current.container
	current.object = kaplot.objects.Line(container, x1, y1, x2=x2, y2=y2, **kwargs)
	return current.object

def pointer(x1, y1, x2, y2, text, offset='3mm', halign=None, valign=None, container=None, **kwargs):
	if container is None:
		_checkContainer()
		container = current.container
	current.object = kaplot.objects.Pointer(container, x1, y1, x2, y2, text, offset=offset, halign=halign, valign=valign, **kwargs)
	return current.object

def polyline(x, y, close=False, container=None, **kwargs):
	"""Draws a polyline from (x[0],y[0]) to (x[1],y[1]) ... to (x[n],y[n])
	
	Arguments:
	 * x -- an array or other sequence
	 * y -- idem
	 * close -- if True, the begin and endpoint will be connected
	 
	Example:
	 * polyline([0, 1, 2, 3], [0, 1, 4, 9], color='red')
	 * {{{#!python
    x = arange(0, 5, 0.1)
    y = sin(x*3) * x**2
    polyline(x, y, linestyle='dotdash')
    }}}
	"""
	if container is None:
		_checkContainer()
		container = current.container
	current.object = kaplot.objects.PolyLine(container, x, y, close=close, **kwargs)
	return current.object

def polygon(x, y, close=True, container=None, **kwargs):
	"""Same as polyline but now the interior will be filled.
	"""
	if container is None:
		_checkContainer()
		container = current.container
	current.object = kaplot.objects.Polygon(container, x, y, close=close, **kwargs)
	return current.object

def rectangle(x1, y1, x2, y2, solid=False, gridsnap=True, container=None, **kwargs):
	"""Draws a rectangle from x1,y1 to x2,y2
	
	Arguments:
	 * solid -- if True, the rectangle will be filled

	Example:
	 * rectangle(0, 0, 10, 5)
	 * rectangle(20, -5, 2, 50)

	"""
	if container is None:
		_checkContainer()
		container = current.container
	current.object = kaplot.objects.Rectangle(container, x1, y1, x2, y2, solid=solid, gridsnap=gridsnap, **kwargs)
	return current.object

def symbols(x, y, symbolName='x', xscales=None, yscales=None, angles=None, colors=None, colormap='rainbow', datamin=None, datamax=None, container=None, **kwargs):
	"""Draws symbols at locations (x[n], y[n])
	
	Example:
	{{{#!python
    x = arange(0.001, 10, 0.1)
    y = sin(x)/x
    symbols(x, y, symbolName='triangle')
    }}}
	"""
	if container is None:
		_checkContainer()
		container = current.container
	current.object = kaplot.objects.Symbols(container, x, y, symbolName=symbolName, xscales=xscales, yscales=yscales, angles=angles, colors=colors, colormap=colormap, datamin=datamin, datamax=datamax, **kwargs)
	return current.object

def text(text, x=0.5, y=0.5, halign='center', valign='center', textangle=0, container=None, **kwargs):
	"""Draws a text string
	
	Arguments:
	 * halign -- horizontal placement of text relative to location
	 * valign -- vertical placement of text relative to location
	 
	Example:
	 * Text("Hello", 0.5, 0.5, "left", "center")
	 	This will draw the text "Hello" to the right of location (0.5, 0.5)
	
	"""
	if container is None:
		_checkContainer()
		container = current.container
	current.object = kaplot.objects.Text(container, text, x=x, y=y, halign=halign, valign=valign, textangle=textangle, **kwargs)
	return current.object

# from decorators
def axes(viewport=((0, 0), (1, 1)), xinterval=None, xinteger=False, xstart=None, xsubticks=4, xlogarithmic=False, yinterval=None, yinteger=False, ystart=None, ysubticks=4, ylogarithmic=False, ticklength='3mm', labeloffset='1mm', linestyle='normal', linewidth='1px', container=None, **kwargs):
	"""Adds axes around the container

	Arguments:
	 * xinterval -- if specified, the major tick seperation for the x axis
	 * xinteger -- if True, x will always be an integer, so no floating point strings in your plot
	 * xstart -- if specified, the start value for the major ticks
	 * xsubticks -- the number of subticks (minor ticks) between mayor ticks
	 * xlogarithmic -- if True, the minor subticks will be seperated as on logarithmic paper.
	 		Note that you have to take the logarithm of your data yourself. Also, labels will
	 		be draws as the base (currently only 10 is supported) with the x-value as superscript
	 * yinterval and the rest -- same, but now for y
	 * ticklength -- length of the mayor ticks, if negative, ticks are drawn to the outside
	 * labeloffset -- length of the seperation between the label and the axis or tickmark (whichever is closer)
	 * linestyle and linewidth -- are added so that axes always look normal, ie your change the default
	 		linewidth of the page
	 		
	 TODO: example and explain how to do custom labeling and tick locations
	"""
	if container is None:
		_checkContainer()
		container = current.container
	current.object = kaplot.objects.Axes(container=container, viewport=viewport, xinterval=xinterval, xinteger=xinteger, xstart=xstart, xsubticks=xsubticks, xlogarithmic=xlogarithmic, yinterval=yinterval, yinteger=yinteger, ystart=ystart, ysubticks=ysubticks, ylogarithmic=ylogarithmic, ticklength=ticklength, labeloffset=labeloffset, linestyle=linestyle, linewidth=linewidth, **kwargs)
	return current.object

def axes2(linestyle='normal', linewidth='1px', container=None, **kwargs):
	"""Adds axes around the container

	Arguments:
	 * xinterval -- if specified, the major tick seperation for the x axis
	 * xinteger -- if True, x will always be an integer, so no floating point strings in your plot
	 * xstart -- if specified, the start value for the major ticks
	 * xsubticks -- the number of subticks (minor ticks) between mayor ticks
	 * xlogarithmic -- if True, the minor subticks will be seperated as on logarithmic paper.
	 		Note that you have to take the logarithm of your data yourself. Also, labels will
	 		be draws as the base (currently only 10 is supported) with the x-value as superscript
	 * yinterval and the rest -- same, but now for y
	 * ticklength -- length of the mayor ticks, if negative, ticks are drawn to the outside
	 * labeloffset -- length of the seperation between the label and the axis or tickmark (whichever is closer)
	 * linestyle and linewidth -- are added so that axes always look normal, ie your change the default
	 		linewidth of the page
	 		
	 TODO: example and explain how to do custom labeling and tick locations
	"""
	if container is None:
		_checkContainer()
		container = current.container
	current.object = kaplot.objects.Axes2(container, linestyle=linestyle, linewidth=linewidth, **kwargs)
	return current.object

def axis(location='left', interval=None, integer=False, start=None, ticks=4, subticks=4, logarithmic=False, ticklength='3mm', labeloffset='1mm', linestyle='normal', linewidth='1px', intersects=None, halign=None, valign=None, intersection=None, spacing='3mm', container=None, **kwargs):
	"""A decorator 'decorates' a container, like axes add axes to it"""
	if container is None:
		_checkContainer()
		container = current.container
	current.object = kaplot.objects.Axis(container, location=location, interval=interval, integer=integer, start=start, ticks=ticks, subticks=subticks, logarithmic=logarithmic, ticklength=ticklength, labeloffset=labeloffset, linestyle=linestyle, linewidth=linewidth, intersects=intersects, halign=halign, valign=valign, intersection=intersection, spacing=spacing, **kwargs)
	return current.object

def border(container=None, **kwargs):
	"""Adds a solid border around the container"""
	if container is None:
		_checkContainer()
		container = current.container
	current.object = kaplot.objects.Border(container, **kwargs)
	return current.object

def labels(bottom=None, left=None, right=None, top=None, spacing='2mm', container=None, **kwargs):
	"""Adds 4 labels around the container"""
	if container is None:
		_checkContainer()
		container = current.container
	current.object = kaplot.objects.Labels(container, bottom=bottom, left=left, right=right, top=top, spacing=spacing, **kwargs)
	return current.object

def spacer(space='5pt', bottom='0cm', right='0cm', top='0cm', left='0cm', container=None, **kwargs):
	"""Adds some space around the container"""
	if container is None:
		_checkContainer()
		container = current.container
	current.object = kaplot.objects.Spacer(container, space=space, bottom=bottom, right=right, top=top, left=left, **kwargs)
	return current.object

def title(text='', spacing='2mm', container=None, **kwargs):
	"""Adds a title in the top/center location of the container"""
	if container is None:
		_checkContainer()
		container = current.container
	current.object = kaplot.objects.Title(container, text=text, spacing=spacing, **kwargs)
	return current.object

# from containers
def box(viewport=((0, 0), (1, 1)), world=None, title='', bottomlabel=None, leftlabel=None, rightlabel=None, toplabel=None, xinterval=None, xinteger=False, xstart=None, xsubticks=4, xlogarithmic=False, yinterval=None, yinteger=False, ystart=None, ysubticks=4, ylogarithmic=False, ticklength='3mm', labeloffset='1mm', page=None, **kwargs):
	"""Creates a box, which is a container, with axes around it
	
	Arguments:
	 * viewport -- the viewport for this container, in normalized page coordinates
	 * world -- the world tuple, specifying range and domain
	 * title -- title (a string) with will be displayed at the top of the container
	 * xxx-label -- a string/label that will be placed as indicated by 'xxx'
	
	For the rest of the arguments, see 'axes'
	
	"""
	if page is None:
		_checkPage()
		page = current.page
	current.container = kaplot.objects.Box(page, viewport=viewport, world=world, title=title, bottomlabel=bottomlabel, leftlabel=leftlabel, rightlabel=rightlabel, toplabel=toplabel, xinterval=xinterval, xinteger=xinteger, xstart=xstart, xsubticks=xsubticks, xlogarithmic=xlogarithmic, yinterval=yinterval, yinteger=yinteger, ystart=ystart, ysubticks=ysubticks, ylogarithmic=ylogarithmic, ticklength=ticklength, labeloffset=labeloffset, **kwargs)
	return current.container

def box2(viewport=((0, 0), (1, 1)), world=None, title='', bottomlabel=None, leftlabel=None, rightlabel=None, toplabel=None, xinterval=None, xinteger=False, xstart=None, xsubticks=4, xlogarithmic=False, yinterval=None, yinteger=False, ystart=None, ysubticks=4, ylogarithmic=False, ticklength='3mm', labeloffset='1mm', page=None, **kwargs):
	"""Creates a box, which is a container, with axes around it
	
	Arguments:
	 * viewport -- the viewport for this container, in normalized page coordinates
	 * world -- the world tuple, specifying range and domain
	 * title -- title (a string) with will be displayed at the top of the container
	 * xxx-label -- a string/label that will be placed as indicated by 'xxx'
	
	For the rest of the arguments, see 'axes'
	
	"""
	if page is None:
		_checkPage()
		page = current.page
	current.container = kaplot.objects.Box2(page, viewport=viewport, world=world, title=title, bottomlabel=bottomlabel, leftlabel=leftlabel, rightlabel=rightlabel, toplabel=toplabel, xinterval=xinterval, xinteger=xinteger, xstart=xstart, xsubticks=xsubticks, xlogarithmic=xlogarithmic, yinterval=yinterval, yinteger=yinteger, ystart=ystart, ysubticks=ysubticks, ylogarithmic=ylogarithmic, ticklength=ticklength, labeloffset=labeloffset, **kwargs)
	return current.container

def container(viewport=((0, 0), (1, 1)), world=None, page=None, **kwargs):
	"""Container holds objects which can be drawn on the page.
	
	It can also have decorators (they 'decorate' the container). Which will
	normally be drawn on the borders of the container, like 'labels' and 'axis' do.
	They shrink the viewport, resulting in an shrunk inner viewport so that your labels
	are always visible. 

	Arguments:
	 * viewport -- the viewport for this container, in normalized page coordinates
	 * world -- the world tuple, specifying range and domain
	"""
	if page is None:
		_checkPage()
		page = current.page
	current.container = kaplot.objects.Container(page, viewport=viewport, world=world, **kwargs)
	return current.container

