from kaplot import *
#from numpy.random_array import normal
from kaplot.objects.plotobjects import bindata

def gaussian(x, mean, sigma):
	return 1/(sqrt(2*pi)*sigma)*e**(-(x-mean)**2/(2*sigma**2))

mean = 0
stddev = 1
N = 500
data = random.normal(mean, stddev, N)

bincount=60
bins, bindata = bindata(data, bincount=bincount, datamin=min(data), datamax=max(data)+1)
binwidth = (bins[1] - bins[0])
bindata = bindata.astype(float) / (sum(bindata) * binwidth) # normalize
x = arange(min(bins), max(bins), 0.01, dtype=float)
yreal = gaussian(x, mean=0, sigma=stddev)
ydata = gaussian(x, mean=data.mean(), sigma=data.std())

box()
title("Histogram of a random normal distribution:\n&sigma;=%g N=%i" % (stddev, N))
xlabel("x")
ylabel("y")
h1 = histogramline(bins, bindata, color="red", fillstyle="crosshatch")
histogramline(bins, bindata, fill=False, color="black", linewidth="2px")
histogramline(bins, bindata, fill=False, drawverticals=False, color="blue", linewidth="3px")
graph(x, yreal, color="black", linewidth="2px")
graph(x, ydata, color="darkgreen", linewidth="2px", linestyle="dash")
autolegend('theory', 'measurements')
text("Blaat", 0, 0.3, fontsize="20pt", color="red", textangle=0.2)
grow(top=1.1, x=1.2)
draw()
