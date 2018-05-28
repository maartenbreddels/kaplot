yformat = u"%(d1)i\xB0%(d2)02i'%(d3)02.2f''"
xformat = u"%(hour)ih%(minute)02im%(second)02.2fs"

def getFormatDict(tick):
	degree1 = int(tick)
	degree2 = int((tick * 100  - degree1 * 100))
	degree3 = ((tick * 10000 - degree1 * 10000 - degree2 * 100))
	tick = (tick + 360) % 360
	totalhours = float(tick * 24.0 / 360)
	hours = int(totalhours)
	minutes = int((totalhours*60 - hours*60))
	seconds = (totalhours * 3600 - hours * 3600 - minutes * 60)
	values = {"d1":degree1, "d2":degree2, "d3":degree3, "hour":hours, "minute":minutes, "second":seconds}
	return values

def formatX(tick):
	values = getFormatDict(tick)
	return xformat % values

def formatY(tick):
	values = getFormatDict(tick)
	return yformat % values
