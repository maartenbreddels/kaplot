from kaplot.objects import PlotObject
import numarray
import kaplot
import kaplot.context
import kaplot.vector

class WcsGrid(PlotObject):
	def __init__(self, xticks, yticks, projection, longitudeoffset, lock=True, context=None, **kwargs):
		PlotObject.__init__(self, lock=False, context=kaplot.context.mergeDicts(context, kwargs))

		self.xticks = xticks
		self.yticks = yticks
		self.projection = projection
		self.longitudeoffset = longitudeoffset

		self.context = kaplot.context.buildContext(kwargs)
		self.callback = self.notifyChange
		self.context.addWeakListener(self.callback)

		if lock:
			self._lock()


	def plot(self, device):
		#xticks = self.xticks
		#yticks = self.yticks
		#xmask = (xticks >= lomin) == (xticks <= lomax)
		#ymask = (yticks >= lamin) == (yticks <= lamax)
		#xticks = compress(xmask, xticks)
		#yticks = compress(ymask, yticks)
		#la
		#yticks = arange(lamin, lamax, lagran)
		#xticks = arange(lomin, lomax, logran)
		lines = []
		xticks = numarray.array(self.xticks)
		yticks = numarray.array(self.yticks)
		#xticks = (xticks + 180) % 360 - 180
		lomin, lomax = min(xticks), max(xticks)
		lamin, lamax = min(yticks), max(yticks)

		logran = (lomax - lomin) / 40
		lagran = (lamax - lamin) / 40
		#print lomin, lomax
		#print lamin, lamax
		#print lomin, lomax, lamin, lamax
		#print xticks, yticks
		#print xticks, yticks
		#print dev.transformation.transform(xticks, yticks)
		#print "PHAT", lomin, lomax, len(yticks)
		for latitude  in yticks[:]: #arange(lamin, lamax+lagran/2, lagran):
			x = numarray.arange(lomin, lomax+logran/2.0, logran)
			y = numarray.zeros(len(x)) + float(latitude)
			nx, ny = self.projection.forwardarray(x, y)
			#print "latitude", latitude
			#print "x=",x, "y=",y
			#print "new"
			#print "nx=",nx, "ny=",ny
			nx = []
			ny = []
			longoffset = self.longitudeoffset
			offset = 0 #(int(self.longitudeoffset) / 180) * 180
			longitudebegin = -180
			while ((x[0]-offset) >= (longitudebegin+longoffset)):
				offset += 180
			#print "offset", offset
			sigma = 0.0001
			for x, y in zip(x, y):
				if ((x-offset) >= (longitudebegin+longoffset)):
					#print "jump", longoffset
					p = self.projection.forward(longitudebegin+(longoffset-sigma)-offset, y)
					if p != None:
						nx.append(p[0])
						ny.append(p[1])
					offset += (180)
					if len(nx) >= 2:
						#print "plot", nx, ny
						device.plotPolyline(nx, ny)
					nx = []
					ny = []
					p = self.projection.forward(longitudebegin+(longoffset+sigma)-(offset-180), y)
					if p != None:
						nx.append(p[0])
						ny.append(p[1])
				#else:
				#	print "no jump"
				p = self.projection.forward(x, y)
				if p != None:
					nx.append(p[0])
					ny.append(p[1])
			#p = self.projection.forward(lomax, y)
			#if p != None:
			#	nx.append(p[0])
			#	ny.append(p[1])
			if len(nx) >= 2:
				#print "plot", nx, ny
				device.plotPolyline(nx, ny)

		for longitude in xticks: #arange(lomin, lomax+logran/2, logran):
			y = numarray.arange(lamin, lamax+lagran/2, lagran)
			x = numarray.zeros(len(y)) + float(longitude)
			nx, ny = self.projection.forwardarray(x, y)
			device.plotPolyline(nx, ny)
			#line = Polyline(x, y, linestyle="normal", linewidth=self.linewidth, color=self.color)
			#lines.append(line)


