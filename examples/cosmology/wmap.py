from kaplot import *

moments, powers, errors = data.wmap()
momentsBinned, powersBinned, errorsBinned = data.wmapbinned()

logarithmic = False
if logarithmic:
	momentsBinned = log(array(momentsBinned)) / log(10)
	moments = log(array(moments)) / log(10)

momentsBinned = array(momentsBinned)
powersBinned = array(powersBinned)
#print powersBinned.size, momentsBinned.size
#powersBinned = powersBinned / (momentsBinned*(momentsBinned+1))
#print momentsBinned
errorsBinned = array(errorsBinned)

box(xlogarithmic=logarithmic, xinteger=True, bottomlabel="Multipole moment (<i>l</i>)",
fontname="serif", fontsize="14pt",
title="WMAP spectrum data\nshowing 1,2 and 3 sigma error ranges")

alpha = 0.3
for sigma in [3,2,1]:
	errorrange(momentsBinned, powersBinned, err=errorsBinned*sigma, color="green", alpha=alpha)
#	errorrange(momentsBinned, powersBinned, err=errorsBinned*sigma, fill=False, caps=True, alpha=alpha)

#symbols(moments, powers, symbolName="dot")
#symbols(momentsBinned, powersBinned, symbolName="dot", color="blue")

polyline(momentsBinned, powersBinned, symbolName="dot", color="red")

#setrange(0, 7000)
grow(x=1.1)
draw()
