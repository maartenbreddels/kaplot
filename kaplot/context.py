import kaplot
from linestyle import linestyles
from kaplot.pattern import patterns
try:
	from kaplot.text.fontfamilies import fontFamilies
	fontnames = fontFamilies.keys()
except:
	fontnames = []

sampleValues = {}
sampleValues["color"] = ["red", "green", "blue"]
sampleValues["alpha"] = [k/10. for k in range(11)]
sampleValues["linestyle"] = linestyles.keys()
sampleValues["linewidth"] = ["1px", "2px", "4px", "2mm", "1cm"]
sampleValues["fontname"] = fontnames
sampleValues["fontsize"] = ["%ipt" % k for k in range(6, 25)]
sampleValues["fillstyle"] = patterns.keys()
sampleValues["patternsize"] = ["%imm" % (k*2.5) for k in range(5)]
sampleValues["symbolsize"] = ["%imm" % (k*2.5) for k in range(5)]

knownNames = sampleValues.keys()

class Context(dict):
	def __init__(self, *args, **kwargs):
		#for key, value in kwargs.items():
		#	setattr(self, key, value)
		dict.__init__(self, *args, **kwargs)
			
	def __getattr__(self, name):
		return self[name]
		
	def __setattr__(self, name, value):
		self._checkAttrName(name)
		self[name] = value

	def __setitem__(self, name, value):
		self._checkAttrName(name)
		super(Context, self).__setitem__(name, value)
		
	def _checkAttrName(self, name):
		if name not in knownNames:
			kaplot.info("Context.%s is not a known attribute, maybe it's misspelled" % name)
		
	def clone(self):
		#values = dict()
		#for key, value in self.__dict__.items():
			#if key not in ignore and not key.beginswith("__"):
			#if not key.startswith("__"):
		#	if key in knownValues:
		#		values[key] = value
		#return Context(**values)
		return Context(**dict(self))
		

