from kaplot import *


def gaussian2d(x, y, meanx, meany, sigma):
	return 1/(sqrt(2*pi)*sigma)*e**(-((x**2.+y**2.))/(2*sigma**2))

document(size="35cm,20cm")
mozaic(2,2, type=container)

select(0,0)
spacer()
axes(xinteger=True, yinteger=True)	
function2d(gaussian2d, xrange=(-1, 1, 0.01), yrange=(-1, 1, 0.01), args=(0, 0, 0.5))

select(1,0)
function2d(gaussian2d, xrange=(-1, 1, 0.1), yrange=(-1, 1, 0.1),
	args=(0, 0, 3), array=True, colormap='cool')

select(0,1)
indexedimage(data.perlin2dnoise(8))
	
select(1,1)
f = "sin(r)*x*r"
spacer()
labels("x", "y", top=f)
spacer()
axes()	
function2d(f, xrange=(-25, 25, 0.1), yrange=(-25, 25, 0.1),
	args=(0, 0, 3), array=True, colormap='rainbow')


draw()