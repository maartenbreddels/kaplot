from kaplot import *
import kaplot.astro


image = data.getFits("m81.fits")
wcs = astro.projection.fromDict(image.headers).wcs
epoch = image.headers["EQUINOX"]

tgal = astro.transformation(skysystem_out=astro.gipsy.GALACTIC)
sgal = astro.transformation(skysystem_out=astro.gipsy.SUPERGALACTIC)
t1950 = astro.transformation(epoch_in=epoch, epoch_out=1950)

w = wcsbox(wcs=wcs)
#spacer("10pt")
#wcsaxes()

indexedimage(image.data, colormap='whiteblack')

wcsgrid()
wcsgrid(transformation=t1950, color="red", linestyle="dot")
wcsgrid(transformation=tgal, color="orange", linestyle="dash", xinterval=0.05, yinterval=0.05)

wcsaxis("right", format="%(degree)s")
wcsaxis("left", transformation=t1950, format="%(degree)s", color="red")

labels(left="&delta;", color="red", fontsize="16pt", fontname="serif")

wcsaxis("top", transformation=tgal, format="%(value).3f", color="orange", interval=0.05)
wcsaxis("bottom", transformation=tgal, format="%(value).3f", color="orange", interval=0.05)
labels(bottom="l", color="orange", fontsize="16pt", fontname="serif")
spacer()
wcsaxis("left", transformation=tgal, format="%(value).3f", color="orange", interval=0.05)
labels(left="b", color="orange", fontsize="16pt", fontname="serif")
wcsaxis("bottom", format="%(time)s")
wcsaxis("bottom", format="%(time)s", transformation=t1950, color="red")
labels(bottom="&alpha;", color="red", fontsize="16pt", fontname="serif")
spacer()
title("<text>object: %s <text color='red'>1950</text>/"\
"<text color='black'>2000</text>/<text color='orange'>Galactic</text></text>" % image.headers["OBJECT"])
spacer()
border()
spacer()
w.addTransformationInfo("1950", t1950)
w.addTransformationInfo("Gal", tgal, str, str)
w.addTransformationInfo("SGal", sgal, str, str)

draw()
