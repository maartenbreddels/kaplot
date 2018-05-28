from kaplot import *
nx = 2
ny = 2

x = arange(nx*ny, shape=(ny,nx)) % nx * 1.0
y = repeat(reshape(arange(ny),(ny,1)), nx,1)
x = x * 1.
y = y * 1.

def gaussian(x_v, mean, sigma):
	return 1/(sqrt(2*pi)*sigma)*e**(-(x_v-mean)**2/(2*sigma**2))
def gaussian(x_v, mean, sigma):
	return 1/(sqrt(2*pi)*sigma)*e**(-(x_v-mean)**2/(2*sigma**2))

	
#I = gaussian(v, 5, 5)
sigma = 40
I = gaussian(x, nx/2, sigma) * gaussian(y, ny/2, sigma)
#I = sin(x/10)*10 + y

b = box(viewport=((0.1, 0.1), (0.9, 0.9))) #, world=((0.5,0.5), (nx+0.5, ny+0.5)))
b.xinteger = True
b.yinteger = True
matrix = kaplot.Matrix.translate(-0.5, -0.5) * kaplot.Matrix.scale(3, 6)
#matrix = kaplot.Matrix.scale(1, 1)
indexedimage(I, matrix=matrix)
x = arange(0,3.8, 0.001)
polyline(x, x**2)
grow(1.1)
draw()