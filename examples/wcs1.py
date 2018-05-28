from kaplot import *
from numpy.random import normal, poisson
import kaplot.cext._gipsy as gipsy

mean = 0
std = 1
n = 10000
r = normal(mean, std, n)

x = arange(n) * 360.0 / n
y = r * 10
if False:
	xg, yg = gipsy.skyco(x, y, gipsy.GALACTIC, gipsy.EQUATORIAL_2000)
	xs, ys = gipsy.skyco(x, y, gipsy.SUPERGALACTIC, gipsy.EQUATORIAL_2000)
	xe, ye = gipsy.skyco(x, y, gipsy.ECLIPTIC, gipsy.EQUATORIAL_2000)

tgal = astro.transformation(skysystem_in=astro.gipsy.GALACTIC, skysystem_out=astro.gipsy.EQUATORIAL_2000)
tsgal = astro.transformation(skysystem_in=astro.gipsy.SUPERGALACTIC, skysystem_out=astro.gipsy.EQUATORIAL_2000)
teclip = astro.transformation(skysystem_in=astro.gipsy.ECLIPTIC, skysystem_out=astro.gipsy.EQUATORIAL_2000)
tgal = astro.transformation(skysystem_out=astro.gipsy.GALACTIC)
tsgal = astro.transformation(skysystem_out=astro.gipsy.SUPERGALACTIC)
teclip = astro.transformation(skysystem_out=astro.gipsy.ECLIPTIC)

b = wcsbox()
wcssphere()
wcssphere(transformation=tgal, color="red")
wcssphere(transformation=tsgal, color="blue")
wcssphere(transformation=teclip, color="green")
wcssymbols(x, y, 'dot', color="red", alpha=0.8, transformation=tgal)
wcssymbols(x, y, 'dot', color="blue", alpha=0.3, transformation=tsgal)
wcssymbols(x, y, 'dot', color="green", alpha=0.8, transformation=teclip)
#plot(x, x**2)
draw()