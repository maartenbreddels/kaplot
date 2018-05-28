from kaplot import *

h = 6.62e-34
k = 1.3807e-23
c = 3e8
nm = 1e-9
T = 6000
L = arange(200*nm, 3000*nm, nm)
I = 2*h*c**2/L**5 * 1 / (e**(h*c/(L*k*T))-1)
logI = log(I)/log(10)

def tofrequency(l):
	return "%g" % (c/l/1e9)
	
def tonanometer(nu):
	return "%g" % (nu/nm)

b = box(ylogarithmic=True)
b.xaxis.label = tonanometer
a = axis("top", ticklength="-3mm")
a.label = tofrequency
#labels(top="frequency, &nu; [Thz]", bottom="wavelength, &lambda; [nm]", left="log(I(&lambda;, T))")
labels(top="frequency, &nu; [Thz]", bottom="wavelength, &lambda; [nm]", left="log(I(&lambda;, T))")
title("Plank spectrum for temperature of %i K" % T, fontsize="18pt")
spacer()
grid(subgrid=True, color="lightgrey", ylogarithmic=True)

fillrange(L[200:600], logI[200:600], level=11.5, alpha=0.5, color='blue')
pointer(800*nm, 12, 1800*nm, 12.8, "Optical region", color='green')
line(400*nm, 12, 1800*nm, 12.8, color='green')
grid()
graph(L, logI)


draw()

