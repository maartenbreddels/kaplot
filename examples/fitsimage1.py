from kaplot import *
import kaplot.astro


image = data.getFits("m81.fits")
wcs = astro.wcs.fromDict(image.headers)

wcsbox(wcs=wcs)
indexedimage(image.data, colormap='whiteblack')
wcsgrid()
wcsaxis("left", format="%(degree)s")
wcsaxis("bottom", format="%(time)s")
labels(bottom="&alpha;", left="&delta;", fontsize="16pt", fontname="serif")
title("Object: " +image.headers["OBJECT"])
spacer(right="5mm")
border()
spacer()

draw()
