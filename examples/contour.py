from kaplot import *

def func2d(x, y):
    return (x**3+y**5-x**8/100-y**4/300)*e**(-x**2-y**2)
    
levels = arange(-1.1, 1, 0.24)

image = function2d(func2d, xrange=(-3, 3, 0.05), yrange=(-3, 3, 0.05), colormap="rainbow")
contour(image.data2d, levels, color="red", linewidth="3px")
innercolorbar(image, levels=list(levels), location="right, bottom")

draw()