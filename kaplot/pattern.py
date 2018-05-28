from kaplot.markers import SimpleSymbol, symbols
import math

class Pattern(object):
	def __init__(self, angle, solid):
		self.angle = angle
		self.solid = solid
		self.parts = 1

	def getXY(self, part):
		raise NotImplementedError

class SymbolPattern(Pattern):
	def __init__(self, angle, symbol):
		Pattern.__init__(self, angle, symbol.solid)
		self.symbol = symbol
		self.parts = symbol.parts

	def getXY(self, part):
		x, y = self.symbol.getXY(part)
		return [x],[y]

class BrickPattern(Pattern):
	def __init__(self, angle):
		Pattern.__init__(self, angle, False)

	def getXY(self, part):
		x = [[0, 1], [0.5, 0.5], [0, 1, 1]]
		y = [[0, 0], [0, 0.5], [0.5, 0.5, 1]]
		return x, y


patterns = {}
patterns["crosshatch"] = SymbolPattern(math.radians(45), symbols["plus"])
patterns["hatch"] = SymbolPattern(math.radians(45), symbols["line"])
patterns["hlines"] = SymbolPattern(0, symbols["line"])
patterns["vlines"] = SymbolPattern(0, symbols["vline"])
patterns["star"] = SymbolPattern(0, symbols["star"])
patterns["tristar"] = SymbolPattern(0, symbols["tristar"])
patterns["circle"] = SymbolPattern(0, symbols["circle"])
patterns["circlesolid"] = SymbolPattern(0, symbols["circlesolid"])
patterns["dot"] = SymbolPattern(0, symbols["dot"])
patterns["brick"] = BrickPattern(0)
patterns["brickdiagonal"] = BrickPattern(math.radians(45))

