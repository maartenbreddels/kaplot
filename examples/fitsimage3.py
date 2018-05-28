from kaplot import *
import kaplot.astro


image = data.getFits("m81.fits")
wcs = astro.projection.fromDict(image.headers).wcs
epoch = image.headers["EQUINOX"]

tgal = astro.transformation(skysystem_out=astro.gipsy.GALACTIC)
sgal = astro.transformation(skysystem_out=astro.gipsy.SUPERGALACTIC)
t1950 = astro.transformation(epoch_in=epoch, epoch_out=1950)

w = wcsbox(wcs=wcs)
indexedimage(image.data, colormap='whiteblack')

# native, J2000
wcsgrid()
wcsaxis("left", format="%(degree)s")
wcsaxis("bottom", format="%(time)s")
labels(left="&delta;",  bottom="&alpha;", fontsize="16pt", fontname="serif")

# B1950
wcsgrid(transformation=t1950, color="red", linestyle="dot")
wcsaxis("right", format="%(degree)s", transformation=t1950, color="red")
wcsaxis("top", format="%(time)s", transformation=t1950, color="red")
labels(right="&delta;", top="&alpha;", color="red", fontsize="16pt", fontname="serif")

# galactic
wcsgrid(transformation=tgal, color="orange", linestyle="dash", ticks=8)
wcsaxis("left", format="%(value).3f", transformation=tgal, color="orange", ticks=8)
wcsaxis("bottom", format="%(value).3f", transformation=tgal, color="orange", ticks=8)
labels(left="l",  bottom="b", color="orange", fontsize="16pt", fontname="serif")

title("<text>object: %s <text color='red'>1950</text>/"\
"<text color='black'>2000</text>/<text color='orange'>Galactic</text></text>" % image.headers["OBJECT"])
spacer()
border()
spacer()
w.addTransformationInfo("1950", t1950)
w.addTransformationInfo("Gal", tgal, str, str)
w.addTransformationInfo("SGal", sgal, str, str)

draw()
