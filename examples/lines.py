import kaplot
import kaplot.objects
import kaplot.astro
from numpy import *

m1 = kaplot.Matrix(2,3, 0, 0)
m2 = kaplot.Matrix(1,1, 10, 10)
print m1
print m2
print m1 * m2

plot = kaplot.objects.Plot()
page = kaplot.objects.Page(plot)
box = kaplot.objects.Box(page, viewport=((0.1, 0.1), (0.9, 0.9)))
line = kaplot.objects.Line(box, 1, 1, 9, 5)
x = arange(0.01,10,0.1)
y = sin(x)/x * 5 + 3
pline = kaplot.objects.PolyLine(box, x, y, color="green")
pline = kaplot.objects.PolyLine(box, x, y*0.9, color="green")
sphere = kaplot.astro.WcsSphere(box)

device = kaplot.device()
device.draw(plot)
device.close()
