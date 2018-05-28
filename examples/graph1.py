from kaplot import *

x = arange(0.01,20,0.1)
y = sin(x*1.8)/x * 5 + 3
green = colors["green"]

N = 2
b = box()
#container()

line(0, 0, 1,1)
for i in range(1, N):
	g = graph(x, y*0.3*i, color="red")
#for i in range(1, N):
#	s = symbols(x, y*0.3*i, symbolName='dot', color=green * (i/float(N)))
#b.grow(x=1.25,y=1.25)
#for hloc in ["left", "center", "right"]:
#	for vloc in ["top", "center", "bottom"]:
#		location = "%s, %s" % (hloc, vloc)
#		legend(["line", "dot"], ["graph", "symbols"], [g, s], location=location)
draw()
