from kaplot import *
import pymedia
interval = 0.01
#interval = 0.1
x = arange(0, 4.+interval/2, interval)
x = arange(0, 1, interval)
y = 1+sin(x*2*pi) + sin(x*30*2*pi) + sin(x*10*2*pi)
#y = 0.1+sin(x *2.5 * 2 * pi)
b = box()
#plot(x, y)
ftspectrum(y, T=interval)
b.grow(1.1)
b.xinterval = 10
b.xinteger = True
draw()