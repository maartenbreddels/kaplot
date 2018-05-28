import kaplot
#import kaplot.astro
import sys
import os
import numpy
#import numpy.nd_image
#import numpy.random_array
from numpy import *

def getFits(filename):
	fullfilename = getDataFilename("fits", filename)
	return kaplot.astro.fits.readImage(fullfilename)
	
def getDataFilename(*filenameParts):
	filename = os.path.join(*filenameParts)
	filenames = []
	filenames.append(os.path.join(os.path.dirname(kaplot.__file__), "..", "data", filename))
	filenames.append(os.path.join(sys.prefix, "share", "kaplot", filename))
	for name in filenames:
		if os.path.exists(name):
			return name
	raise Exception, "data file: %s not found" % filename

def perlin2dnoise(maxorder=9, seed=0):
	numpy.random_array.seed(seed, seed)
	image = numpy.zeros((2**maxorder, 2**maxorder), numpy.Float)


	for order in range(maxorder, 2, -1):
		dim = 2 ** order
		zoom = 2**(maxorder-order)
		newimage = numpy.random_array.random((dim,dim)) * zoom
		image += numpy.nd_image.zoom(newimage, (zoom, zoom), order=2)
	return image

def perlin1dnoise(maxorder=9, seed=0):
	numpy.random_array.seed(seed, seed)
	array = numpy.zeros((2**maxorder), numpy.Float)

	for order in range(maxorder, 2, -1):
		dim = 2 ** order
		zoom = 2**(maxorder-order)
		newarray = numpy.random_array.random((dim)) * zoom
		array += numpy.nd_image.zoom(newarray, (zoom), order=2)
	return array
	
def readtextcolumns(filename, columns, types):
	lines = file(filename).readlines()
	if len(columns) != len(types):
		raise ValueError, "inconsistent argmunents, columns and types should be of same length"
	data = [list() for k in range(len(columns))]
	for line in lines:
		line = line.strip() # remove spaces/tabs etc
		if not line.startswith("#"): # ignore comments
			allparts = line.split() # split by whitespace seperation
			parts = [type(allparts[index]) for index, type in zip(columns, types)] # get the columns and cast to proper type
			for i in xrange(len(columns)):
				data[i].append(parts[i])
	return data

def wmap():
	filename = getDataFilename("wmap", "powerspectrum_comb_yr1_v1p1.txt")
	moments, powers, errors = readtextcolumns(filename, [0, 1, 2], [float, float, float])

	return moments, powers, errors
	
def wmapbinned():
	filename = getDataFilename("wmap", "powerspectrum_binned_yr1_v1p1.txt")
	momentsBinned, powersBinned, errorsBinned = readtextcolumns(filename, [0, 3, 4], [float, float, float])
	return momentsBinned, powersBinned, errorsBinned


def gaussian2d(x, y, meanx, meany, sigma):
	return 1/(sqrt(2*pi)*sigma)*e**(-(((x-meanx)**2.+(y-meany)**2.))/(2*sigma**2))

def gaussian(x, mean=0., sigma=1.):
	return 1/(sqrt(2*pi)*sigma)*e**(-(((x-mean)**2))/(2*sigma**2))


worldpopulation = []
worldpopulation.append(("Africa", 221, 796, 851))
worldpopulation.append(("Asia", 1398, 3680, 3823))
worldpopulation.append(("Lat.Amer.+Caribbean", 167, 520, 543))
worldpopulation.append(("Europe", 547, 728, 726))
worldpopulation.append(("Northern America", 172, 316, 326))
worldpopulation.append(("Oceania", 13, 31, 32))

population1950 = [pop1950 for name, pop1950, pop2000, pop2003 in worldpopulation]
population2000 = [pop2000 for name, pop1950, pop2000, pop2003 in worldpopulation]
population2003 = [pop2003 for name, pop1950, pop2000, pop2003 in worldpopulation]
populationgroups = [population1950, population2000, population2003]
populationcontexts = [{"color":"blue"}, {"color":"red"}, {"color":"green"}]
populationlabels = [name for name, pop1950, pop2000, pop2003 in worldpopulation]
