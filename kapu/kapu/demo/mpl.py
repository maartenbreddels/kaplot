from pylab import *
from matplotlib.ticker import Locator
#from kapu.wcslocators import *
from kapu.wcsplot import *

class TestLocator(Locator):
	def __call__(self):
		#print self.viewInterval.__file__
		print dir(self.viewInterval)
		print self.viewInterval.get_bounds()
		print self.viewInterval.val1()
		print self.viewInterval.val2()
		print self.dataInterval
		print dir(self)

t = arange(-10.0, 10.0, 0.01)
s = sin(2*pi*t) * 50
#r = arange(0,1,0.001)
#theta = 2*2*pi*r

#ax = wcsplot(theta, r, linewidth=1.0)
ax = wcsplot(t, s, linewidth=1.0)
#ax = polar(theta, r, lw=3.0)
#polar(theta, r, color='#ee8d18', lw=3)
#ax = axes()
#print ax.xaxis
#wcsl = WcsLocators()
#wcsl.init(ax)
#ax.xaxis.set_major_locator(tl)
#xlabel('time (s)')
#ylabel('voltage (mV)')
title('About as simple as it gets, folks')
grid(False)
show()