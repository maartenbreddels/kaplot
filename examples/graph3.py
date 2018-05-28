from kaplot import *

p1 = "t+1j*sin(t)"
p2 = "t/3*e**(1j*t*2*pi)"
f1 = "cos(x)"
parametric(p1, range=(-pi, pi, 0.1), color="blue", linestyle="dash")
parametric(p2, range=(0, 3+0.001, 0.05), color="orange", linestyle="dot")
function(f1, range=(-pi, pi, 0.1), color="red", linestyle="dotdash")

p2text = "<fraction><text>t</text><text>3</text></fraction>e<sup>i2&pi;t</sup>"
autolegend([p1, p2text, f1], location="left, top", fontsize="20pt")


show()
