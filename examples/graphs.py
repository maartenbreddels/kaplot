from kaplot import *

document(size="30cm, 15cm")
mozaic(2,2, type=box)

for x in range(2):
	for y in range(2):
		select(x,y)
		pass
		#border("5pt")
select(0,0)
function("numpy.sin(x)*x", (-10, 10, 0.1), linestyle="dot")
grow(1.2)

select(0,1)
function("10*numpy.e**(numpy.sin(x/3)*x/10)", (-15, 15, 0.1), color="green")
grow(1.2)

select(1,0)
parametric("t/3*numpy.e**(1j*t*2*numpy.pi)", range=(0, 3+0.001, 0.05), symbolName='x', color="orange", linestyle="normal")
grow(y=0.8)

select(1,1)
parametric("t+1j*numpy.sin(t)", range=(-pi, pi, 0.1), color="blue", linestyle="dash")
parametric("t", "numpy.cos(t)", range=(-pi, pi, 0.1), color="red", linestyle="dash")
ylabel("blaat")
grow(x=4)

draw()
