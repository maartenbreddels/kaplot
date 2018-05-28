from kaplot import *
import kaplot
#print dir(kaplot.quickgen)

mozaic(type=box)
select(0, 0)
vectorfield("-y", "x", scale=0.5)
select(1, 0)
vectorfield("y", "x", scale=0.5)
select(0, 1)
vectorfield("x**2", "y**2", scale=0.5)
select(1, 1)
vectorfield("x/sqrt(x**2+y**2)", "y/sqrt(x**2+y**2)", scale=0.3)
draw()