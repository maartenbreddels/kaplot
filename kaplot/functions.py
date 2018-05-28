import math
from numpy import *
functions = {}
functions["linear"] = lambda x: x
functions["inverse"] = lambda x: 1-x
functions["sqrt"] = lambda x: math.sqrt(x)
functions["log"] = lambda x: math.log(x+1) / math.log(2)
functions["inversesqrt"] = lambda x: 1-math.sqrt(x)
functions["inverselog"] = lambda x: 1-math.log(x+1) / math.log(2)
	
