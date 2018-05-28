import numpy

class FitsImage(object):
	def __init__(self, headers, data, headerList=None, comments=None):
		self.headers = headers
		self.data = data
		self.headerList = headerList
		if self.headerList == None:
			self.headerList = self.headers.keys()
		self.comments = comments
		if self.comments:
			self.comments = {}

		# make sure the mandatory headers exist, and are in order
		if "SIMPLE" not in self.headerList:
			self.headerList.insert("SIMPLE")
			self.headers["SIMPLE"] = "T"
			self.comments["SIMPLE"] = "Fits header"

		if "BITPIX" not in self.headerList:
			self.headerList.insert("BITPIX")
			self.headers["BITPIX"] = "16"
			self.comments["BITPIX"] = "No.Bits per pixel"
		
		for i in range(self.data.rank):
			headerName = "NAXIS%i" % (i+1)
			axis = {0:"X", 1:"Y", 2:"Z"}.get(i, "#"+str(i))
			comment = "Length %s axis" % axis
			axisLength = self.data.shape[-(i+1)]
			if headerName not in self.headerList:
				self.headerList.insert(headerName)
				self.headers[headerName] = axisLength
				self.comments[headerName] = comment

		orderList = ["SIMPLE", "BITPIX"]
		for i in range(self.data.rank):
			orderList.append("NAXIS%i" % (i+1))
		for index, headerName in enumerate(orderList):
			if self.headerList.index(headerName) != 0:
				self.headerList.remove(headerName)
				self.headerList.insert(index, headerName)
		#print self.headerList
				
		
	
	def writeImage(self, fileName):
		file = open(fileName, "rb")
		return self.writeImageFromFile(file)
	
	def writeImageFromFile(self, file):
		for headerName in self.headerList:
			value = str(self.headers[headerName]).jlust(20, " ")
			comment = self.comments.get(header, "")
			if comment == None:
				comment = ""
			comment = comment.ljust(50-2)
			line = headerName.ljust(8, " ") + "= " + value + " /" + comment
			if len(line) != 80:
				_debug("length of line !-= 80, it's " +len(line))
			file.write(line)
		file.write("END".ljust(80, " "))
		_nextBlock(file)
		data = data.copy()
		data = data.astype(numpy.Int16)
		file.write(data.tostring())
		
			
	
def readImages(filename):
	file = open(filename, "rb")
	
	images = []
	while len(file.read(1)) == 1:
		file.seek(file.tell()-1)
		image = readImageFromFile(file)
		images.append(image)
		_nextBlock(file)

	return images

def readImage(filename):
	file = open(filename, "rb")
	return readImageFromFile(file)
	
def readImageFromFile(file):
	headers = {}
	headersList = []
	finished = False
	while not finished:
		key, value = _readLine(file)
		if key == None:
			# skip comments
			pass
		elif key == "END":
			_debug("end")
			finished = True
		else:
			#_debug("headers:", key, value)
			headers[key] = value
			headersList.append(key)
	
	_nextBlock(file) # seek to a multitude of 2880
	
	datatype = int(headers["BITPIX"])
	typemap = {8:numpy.Byte, 16:numpy.Int16, 32:numpy.Int32, -32:numpy.Float32, -64:numpy.Float64}
	lengthmap = {8:1, 16:2, 32:4, -32:4, -64:8}
	if datatype not in typemap:
		raise Exception, "unknown BITPIX: %i" % datatype
	
	axisCount = int(headers["NAXIS"])
	shape = [int(headers["NAXIS%i" % (k+1)]) for k in range(axisCount)]
	shape.reverse()
	_debug("shape", shape)
	length = lengthmap[datatype] * reduce(lambda x,y: x*y, shape, 1)
	#print length
	numpydatatype = typemap[datatype]
	data = numpy.fromstring(file.read(length), numpydatatype, shape)
	data.togglebyteorder()
	image = FitsImage(headers, data, headersList)
	return image
		
def _debug(*args):
	pass
	#print "fits debug: ", ", ".join(map(str, args))
				
def _readLine(file):
	line = file.read(80)
	key = line[:8].strip()
	value = line[9:]
	if line[8] != "=" and key != "END":
		_debug("comment", line)
		return None, None
	#print "->", value
	if "/" in value:
		pos = value.find("/")
		value, comment = value[:pos], value[pos+1:]
		#print "   ->", `value`, `comment`
		if line[9] == ' ' and line[10] == "'":
			# string
			endquote = value.rfind("'")
			value = value[2:endquote].rstrip()
			_debug("fixed string", key, `value`)
		elif line[29] == 'T':
			value = True
			_debug("boolean true", key, `value`)
		elif line[29] == 'F':
			_debug("boolean false", key, `value`)
			value = False
		else:
			try:
				value = int(value)
				_debug("int value", key, `value`)
			except:
				try:
					value = float(value)
					_debug("float value", key, `value`)
				except:
					try:
						value = complex(value)
						_debug("complex value", key, `value`)
					except:
						_debug("uknown value", key, `value`)
	return key, value
				
def _nextBlock(file):
	if (file.tell() % 2880) != 0:
		file.seek(2880 * (file.tell() / 2880 + 1))
			
				
		
		