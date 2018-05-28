import kaplot
import PIL.Image
#from kaplot.cext._agg import Agg

class RubberBand(object):
	def __init__(self, xlist, ylist, close):
		self.xlist = xlist
		self.ylist = ylist
		self.close = close
		
class Region(object):
	def __init__(self, xlist, ylist, close, fill):
		self.xlist = xlist
		self.ylist = ylist
		self.close = close
		self.fill = fill
		
class Menu(object):
	def __init__(self, window):
		self.window = window
		
	def addCommand(self, text, callback, bold=False, args=[], kwargs={}):
		pass
		
	def addSubMenu(self, text, bold=False):
		pass
		
	def addSeparator(self):
		pass
	
		
#	def draw(self, agg):
#		dashlength = 5
#		dasharray = [dashlength, dashlength]
#		agg.set_color(0, 0, 0)
#		agg.set_linedash(dasharray)
#		agg.polyline(self.xlist, self.ylist)
#		if self.close:
#			agg.close()
#		agg.stroke()
		
class Window(object):
	def __init__(self):
		self.image = None
		self.document = None
		self.device = None
		self.selectedObject = None
		self.rubberBand = None
		self.overlay = None
		self.flashRegion = None
		self.regions = {}
		
	def isValid(self):
		raise Exception, "not implemented"
	
	def setImage(self, image):
		self.image = image
		self.overlay = Agg(self.image.width, self.image.height)
		
	def updateImage(self):
		pass
		
	def refreshDocument(self):
		pass
		
	def setDocument(self, document, device):
		self.document = document
		self.device = device
		
	def setInfoText(self, text):
		pass
		
	def setInfoCopyText(self, text):
		pass
		
	def setClipboardText(self, text):
		pass
		
	def setRubberBand(self, xlist, ylist, close=False):
		self.rubberBand = RubberBand(xlist, ylist, close)
		
	def setFlashRegion(self, xlist, ylist, close=False, fill=False):
		self.flashRegion = Region(xlist, ylist, close, fill)
		
	def getRegion(self, name):
		if name in self.regions:
			return self.regions[name]
		else:
			region = Region([], [], True, True)
			self.regions[name] = region
			return region
		
	def removeRubberBand(self):
		self.rubberBand = None
		
	def select(self, object):
		kaplot.debug("selected", object)
		self.selectedObject = object
		
	def getSelected(self):
		return self.selectedObject
		
	def createMenu(self, parentMenu=None):
		pass
		
	def showPopupMenu(self, menu):
		pass
		
	def getZoomedImage(self, image, mousex, mousey, zoomwidth, zoomheight):
		zoom = 4
		hwidth = zoomwidth / (2 * zoom)
		hheight = zoomwidth / (2 * zoom)
		#image = self.pageImages[self.currentPage]
		imwidth, imheight = image.size
		#if event.x >= hwidth and event.y >= hheight and event.x < imwidth - hwidth  and event.y < imheight - hheight:
		#if True:
		x = mousex
		y = mousey
		x = min(max(x, hwidth), imwidth-hwidth)
		y = min(max(y, hheight), imheight-hheight)
		bbox = (x - hwidth, y - hheight, x + hwidth, y + hheight)
		image = image.crop(bbox)
		zoomedimage = image.resize((zoomwidth, zoomheight), PIL.Image.NEAREST)
		#zoomedimage.paste((0,0,0), (0,0,self.zoomwidth,self.zoomheight))
		px = mousex - x + hwidth
		py = mousey - y + hheight
		zimwidth, zimheight = zoomedimage.size
		for i in range(zoom+1):
			x = px*zoom+i
			y = py*zoom
			if x >= 0 and y >= 0 and x < zimwidth and y < zimheight:
				r,g,b = zoomedimage.getpixel((x, y))
				zoomedimage.putpixel((x, y), (r^255,g^255,b^255))

			x = px*zoom+i
			y = py*zoom + zoom
			if x >= 0 and y >= 0 and x < zimwidth and y < zimheight:
				r,g,b = zoomedimage.getpixel((x, y))
				zoomedimage.putpixel((x, y), (r^255,g^255,b^255))

			x = px*zoom
			y = py*zoom+i
			if x >= 0 and y >= 0 and x < zimwidth and y < zimheight:
				r,g,b = zoomedimage.getpixel((x, y))
				zoomedimage.putpixel((x, y), (r^255,g^255,b^255))

			x = px*zoom + zoom
			y = py*zoom +i
			if x >= 0 and y >= 0 and x < zimwidth and y < zimheight:
				r,g,b = zoomedimage.getpixel((x, y))
				zoomedimage.putpixel((x, y), (r^255,g^255,b^255))

		#self.zoomtkimage.paste(zoomedimage, (-50, -55))
		#self.update()
		return zoomedimage

		