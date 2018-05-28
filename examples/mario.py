from kaplot import *

mozaic(2,2, type=box)

select(0, 0)
function("x*x")

select(1, 0)
function("x**1.8")

select(0, 1)
function("1-log(1.3-x)/log(1.1)")

select(1, 1)
function("1-sqrt(1-x)")

draw()
