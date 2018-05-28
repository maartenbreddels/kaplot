from kaplot import *

box()
title("filled sinc functions")
spacer()
border() 

x = arange(0.01, 10, 0.1)
y1 = sin(x)/x
y2 = sin(x)/x/2

fillrange(x, y1, alpha=0.3, color="green")
fillrange(x, y2, alpha=0.3, color="blue")
polyline(x, y1)
polyline(x, y2)

x = arange(2, 5, 0.1)
y = sin(x)/x

fillrange(x, y, alpha=0.5, color="black")
polyline(x, y, color="red", linewidth="4px", linestyle="dash")

grow(1.1)
draw()