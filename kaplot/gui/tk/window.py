# -*- coding: utf-8 -*-
import kaplot
from kaplot.gui.window import Window, Menu
hastk = True
try:
	import Tkinter
	import _tkinter
	import tkFont
	import PIL.ImageTk
except:
	pass # temp fix
	hastk = False
	class Fake(object):
		def __init__(self, *args, **kwargs):
			pass
	Tkinter = Fake()
	Tkinter.Frame = Fake()
#else:
if 1:
	import PIL.Image
	import PIL.ImageDraw
	import time
	import threading, Queue
	
	class GuiThread(threading.Thread):
		def __init__(self):
			threading.Thread.__init__(self)
			self.createMutex = threading.Semaphore(1)
			self.startEvent = threading.Event()
			self.producerQueue = Queue.Queue(1)
			self.productQueue = Queue.Queue(1)
			self.setDaemon(True)
	
			#self.getPages() = []
			self.start()
			self.startEvent.wait()
			time.sleep(0.05)
	
		def _generateGuiEvent(self):
			"""Implement a gui specific event to check the producer queue"""
			pass
	
		def _checkProductions(self, *args, **kwargs):
			"""Bind the custom gui-event to this function, all arguments will be ignored"""
			if not self.producerQueue.empty():
				callable, args, kwargs = self.producerQueue.get()
				product = callable(*args, **kwargs)
				self.productQueue.put(product)
				kaplot.debug("product is produced")
	
		def executeFromThread(self, callable, *args, **kwargs):
			#self.createMutex.acquire()
			if threading.currentThread() == self: # these can be executed directly
				kaplot.debug("calling executeFromThread from gui thread, returning directly")
				return callable(*args, **kwargs)
			else:
				self.producerQueue.put((callable, args, kwargs))
				kaplot.debug("generating event to execute a function in the gui thread")
				self._generateGuiEvent()
				kaplot.debug("waiting for reply from the gui thread")
				result = self.productQueue.get()
				kaplot.debug("got return value from gui thread")
	
			#self.createMutex.release()
			return result
	
	class TkGuiThread(GuiThread):
		def run(self):
			self.testMutex = threading.Semaphore(1)
			self.root = Tkinter.Tk()
			self.root.withdraw()
			self.root.bind('<<Other-Thread-Event>>', self._checkProductions)
			self.startEvent.set()
			kaplot.debug("running tk mainloop")
			self.root.mainloop()
			kaplot.debug("end of tk mainloop")
	
		def _generateGuiEvent(self):
			self.root.event_generate('<<Other-Thread-Event>>', when='tail')
			self.testMutex.release()
	
	tkMaster = None
	def getTkMaster():
		global tkMaster
		if tkMaster == None:
			tkMaster = Tkinter.Tk()
			tkMaster.withdraw()
		return tkMaster 
	
	def createFrame(master):
			tl = Tkinter.Toplevel(master, )
			tl.title("kaplot")
			return tl
			
	class MenuTk(Menu):
		def __init__(self, window, root):
			super(MenuTk, self).__init__(window)
			self._root = root
			self._tkmenu = Tkinter.Menu(self._root, tearoff=1)
	
		def _getTkArguments(self, bold=False):
			kwargs = {}
			tempmenu = Tkinter.Menu(self._root)
			if bold:
				family, size = str(tempmenu["font"]).split()[0:2]
				font = tkFont.Font(family=family, size=int(size), weight=tkFont.BOLD)
				kwargs["font"] = font
			tempmenu.destroy()
			return kwargs
			
		def _tkhide(self):
			self._tkmenu.destroy()
	
		def _tkshow(self, x, y):
			self._tkmenu.post(x, y)
			def kill():
				self._tkmenu.destroy()
				#for submenu in allmenus[::-1]:
				#	if submenu:
				#		submenu.destroy()
				#		print ".",
			#self._root.after_idle(kill)
	
		def addCommand(self, text, callback, bold=False, args=[], kwargs={}):
			def commandWrapper(callback=callback, args=args, kwargs=kwargs, text=text):
				print "command executed", text
				allargs = [self.window] + list(args)
				callback(*allargs, **kwargs)
			self._tkmenu.add_command(label=text, command=commandWrapper, **self._getTkArguments(bold=bold))
	
		def addSubMenu(self, text, menu, bold=False):
			#**getExtraArguments(options)
			#subMenu = MenuTk(self._root)
			def activate(menu=menu):
				print "activate"
				menu._tkmenu.activate()
			self._tkmenu.add_cascade(label=text, menu=menu._tkmenu, command=activate, **self._getTkArguments(bold=bold))
			#return subMenu
			
		def addSeparator(self):
			self._tkmenu.add_separator()
			
			
			#allmenus = []
			#def createMenu(menuList):
			#	menu = Tkinter.Menu(self.canvas, tearoff=0)
			#	#print menuList
			#	if menuList is None:
			#		return menu
			#	for menuItem in menuList:
			#		if menuItem is None:
			#			allmenus.append(menu.add_separator())
			#		else:
			#			menuName, other = menuItem[:2]
			#			if callable(other):
			#				callback = other
			#				args = list([self])
			#				kwargs = {}
			#				options = {}
			#				if len(menuItem) > 2:
			#					args += list(menuItem[2])
			#				if len(menuItem) > 3:
			#					kwargs = menuItem[3]
			#				if len(menuItem) > 4:
			#					options = menuItem[4]
			#				def command(callback=callback, args=args, kwargs=kwargs, menuName=menuName):
			#					callback(*args, **kwargs)
			#				allmenus.append(menu.add_command(label=menuName, command=command, **getExtraArguments(options)))
			#			else:
			#				subMenu = createMenu(other) # recursive
			#				options = {}
			#				if len(menuItem) > 2:
			#					options = menuItem[2]
			#				allmenus.append(menu.add_cascade(label=menuName, menu=subMenu, **getExtraArguments(options)))
			#	return menu
			#menu = createMenu(menuList)
			#x, y = self.lastMousePos
			#x += self.canvas.winfo_rootx()
			#y += self.canvas.winfo_rooty()
			#menu.post(x, y)
			#
			#def kill(menu=menu, allmenus=allmenus):
			#	menu.destroy()
			#	for submenu in allmenus[::-1]:
			#		if submenu:
			#			submenu.destroy()
			#			print ".",
			#self.root.after_idle(kill)
	
	class TkWindow(Tkinter.Frame, Window):
		def __init__(self, parent, width, height, pageCount, threaded=False, **kw):
			Tkinter.Frame.__init__(self, parent, **kw)
			Window.__init__(self)
			self.parent = parent
			self.root = parent
			self.width = width
			self.height = height
			self.pageCount = pageCount
			self.threaded = threaded
			kaplot.debug("treaded = %s" % threaded)
	
			root = parent
	
			self.currentDisplayPage = 0
			self.currentPage = 0
			def image():
				return PIL.Image.fromstring("RGB", (self.width, self.height), "\x00\x00\x00" * width * height)
			self.pageImages = [image() for k in range(self.pageCount)]
			
			self.tkimage = PIL.ImageTk.PhotoImage(self.pageImages[self.currentPage])
			#self.label = Tkinter.Label(self, image=self.tkimage, relief=Tkinter.SUNKEN, bd=2)
			#self.label.grid(row=1, column=0, columnspan=4, rowspan=2, sticky="NE")#Tkinter.W+Tkinter.E+Tkinter.N+Tkinter.S)
			self.canvas = Tkinter.Canvas(self, relief=Tkinter.SUNKEN, bd=0, takefocus=True)
			self.canvas.grid(row=10, column=0, columnspan=4, rowspan=2, sticky="NW")
	
			self.zoomwidth, self.zoomheight = 128, 128
			self.zoomimage = PIL.Image.fromstring("RGB", (self.zoomwidth, self.zoomheight), "\x00\x00\x00" * self.zoomwidth * self.zoomheight)#, "raw", "RGB", gs.width*3, 1)
			self.zoomtkimage = PIL.ImageTk.PhotoImage(self.zoomimage)
			self.zoomlabel = Tkinter.Label(self, image=self.zoomtkimage, relief=Tkinter.SUNKEN, bd=2)
			self.zoomlabel.grid(row=0, column=0, columnspan=1, rowspan=2,sticky="W")#Tkinter.W+Tkinter.E+Tkinter.N+Tkinter.S)
			
			self.infoText = Tkinter.Text(self, width=30, height=7, wrap=Tkinter.NONE, takefocus=False)
			self.infoText.grid(row=0, column=1)
	
			self.infoTextCopy = Tkinter.Text(self, width=30, height=7, wrap=Tkinter.NONE, takefocus=False)
			self.infoTextCopy.grid(row=0, column=2)
	
			self.infoTextExtra = Tkinter.Text(self, width=30, height=7, wrap=Tkinter.NONE, takefocus=False)
			self.infoTextExtra.grid(row=0, column=3)
			
			if 0:
				self.button1 = Tkinter.Button(self, text="Test", bd=2)
				self.button1.grid(row=1, column=1, columnspan=1, sticky="W")#Tkinter.W+Tkinter.E+Tkinter.N+Tkinter.S)
				
				self.scale1label = Tkinter.Label(self, text="E:", bd=2)
				self.scale1label.grid(row=2, column=0, columnspan=1, sticky="E")#Tkinter.W+Tkinter.E+Tkinter.N+Tkinter.S)
				def test(*args, **kwargs):
					print args, kwargs
				self.scale1 = Tkinter.Scale(self, from_=0, to=100, bd=2, orient=Tkinter.HORIZONTAL, length=500, command=test)
				self.scale1.grid(row=2, column=1, columnspan=3, sticky="W")#Tkinter.W+Tkinter.E+Tkinter.N+Tkinter.S)
				
				self.scale2label = Tkinter.Label(self, text="L:", bd=2)
				self.scale2label.grid(row=3, column=0, columnspan=1, sticky="E")#Tkinter.W+Tkinter.E+Tkinter.N+Tkinter.S)
				self.scale2 = Tkinter.Scale(self, from_=0, to=1000, bd=2, orient=Tkinter.HORIZONTAL, length=500)
				self.scale2.grid(row=3, column=1, columnspan=3, sticky="W")#Tkinter.W+Tkinter.E+Tkinter.N+Tkinter.S)
	
			self.frameCount = 0
			#self.label.bind("<Button-1>", self._onMouseClick)
			self.bind('<<refresh>>', self._refresh)
			#self.bind('<Destroy>', self._handleDeleteWindow)
			self.root.protocol("WM_DELETE_WINDOW", self._handleDeleteWindow)
			self.bind("<Key>", self.keyEvent)
			self.canvas.bind("<Key>", self.keyEvent)
			self.canvas.bind("<Motion>", self.mouseEvent)
			self.canvas.bind("<Enter>", self.mouseEventEnter)
			self.canvas.bind("<Button-1>", self.mouseEvent)
			self.canvas.bind("<Button-2>", self.mouseEvent)
			self.canvas.bind("<Button-3>", self.mouseEvent)
			self.canvas.bind("<ButtonRelease-1>", self.mouseEvent)
			self.canvas.bind("<ButtonRelease-2>", self.mouseEvent)
			self.canvas.bind("<ButtonRelease-3>", self.mouseEvent)
			self.canvas.bind("<Double-Button-1>", self.mouseEventDouble)
			self.canvas.bind("<Double-Button-2>", self.mouseEventDouble)
			self.canvas.bind("<Double-Button-3>", self.mouseEventDouble)
			
	
			self.mouseOptions = {}
			self.mouseOptions["dragposition"] = (0, 0)
			self.mouseOptions["moving"] = False
			self.mouseOptions["dragging"] = False
			self.mouseOptions["wasdragging"] = False
			self.mouseOptions["leftdouble"] = False
			self.mouseOptions["leftup"] = False
			self.mouseOptions["leftdown"] = False
			self.mouseOptions["leftisdown"] = False
			self.mouseOptions["middledouble"] = False
			self.mouseOptions["middleup"] = False
			self.mouseOptions["middledown"] = False
			self.mouseOptions["middleisdown"] = False
			self.mouseOptions["rightdouble"] = False
			self.mouseOptions["rightup"] = False
			self.mouseOptions["rightdown"] = False
			self.mouseOptions["rightisdown"] = False
			self.mouseOptions["shift"] = False
			self.mouseOptions["control"] = False
			self.mouseOptions["alt"] = False
			self.lastMousePos = (0, 0)
			self._canvasItems = []
			self.keeprunning = True
			self.defaultCursor = self.getMouseCursor()
			self.menus = []
			if threaded:
				self.closelock = threading.Event(0)
			#self.mainMenu = Tkinter.Menu(self.
			self.canvas.focus_set()
			
		#def setRubberBand(self, *args, **kwargs):
		#	super(TkWindow, self).setRubberBand(*args)
		#	#self._updateRubberBand()
		#	self._refreshDocument()
		
		def isValid(self):
			try:
				self.root.state()
				return True
			except:
				return False
			
		def clone(self):
			return createImageWindow()
			
		def refreshDocument(self):
			kaplot.debug("refresh document requested")
			def _refreshDocument():
				kaplot.debug("refreshing document")
				self.document.draw(self.device)
			self.root.after_idle(_refreshDocument)
	
		def refreshWindow(self):
			kaplot.debug("refresh window requested")
			self.root.after_idle(self._refreshDocument)
			
		#def setRubberBand(self, xlist, ylist, close=False):
		#	super
		
		def updateRegions(self):
			for name, region in self.regions.items():
				if hasattr(region, "item"):
					self.canvas.delete(region.item)
				#kwargs = {"fill":"red", "stipple":"gray50"}
				x = region.xlist
				y = [self.image.height - 1 - y for y in region.ylist]
				if len(x) > 0:
					region.item = self.canvas.create_polygon(zip(x, y), fill="red", stipple="gray12", outline="black")
				#self._canvasItems.append(item)
				
			
		def setFlashRegion(self, *args, **kwargs):
			def flashEnd():
				for item in self._canvasItems:
					self.canvas.delete(item)
			def flash():
				for item in self._canvasItems:
					self.canvas.delete(item)
				x = self.flashRegion.xlist
				y = [self.image.height - 1 - k for k in self.flashRegion.ylist]
				if self.flashRegion.close:
					x.append(x[0])
					y.append(y[0])
				args = zip(x, y)
				kwargs = {"fill":"red", "stipple":"gray50"}
				item = self.canvas.create_line(*args, **kwargs)
				self._canvasItems.append(item)
			def flash3():
				flash()
				self.root.after(300, flashEnd)
			def flash2():
				flashEnd()
				self.root.after(300, flash3)
			def flash1():
				flash()
				self.root.after(300, flash2)
			super(TkWindow, self).setFlashRegion(*args, **kwargs)
			self.root.after_idle(flash1)
	
		def createMenu(self, parentMenu=None):
			if parentMenu:
				return MenuTk(self, parentMenu._tkmenu)
			else:
				return MenuTk(self, self.root)
	
		def getMainMenu(self, menu):
			self.config(menu=menu)
			
		def showPopupMenu(self, menu):
			x, y = self.lastMousePos
			x += self.canvas.winfo_rootx()
			y += self.canvas.winfo_rooty()
	
			menu._tkshow(x, y)
			self.menus.append(menu)
			
			#for submenu in allmenus[::-1]:
			#	if submenu:
			#		submenu.destroy()
			#		print ".",
			#menu.destroy()
			#print dir(menu)
			#menu.delete(Tkinter.ALL)
	
		def setClipboardText(self, text):
			self.root.clipboard_clear()
			self.root.clipboard_append(text)
			
		def _handleDeleteWindow(self):
			#self.root.quit()
			kaplot.debug("closing window")
			self.root.withdraw()
			if self.threaded:
				self.closelock.set()
			else:
				self.keeprunning = False
		
		def setImage(self, image):
			def _setImage():
				kaplot.debug("setting image")
				self.image = image
			if self.threaded:
				guiThread = getGuiThread()
				guiThread.executeFromThread(_setImage)
			else:
				_setImage()
			
			#self._refreshDocument()
			
		def updateImage(self):
			def _updateImage():
				kaplot.debug("updating image")
				self.pageImages[self.currentPage] = \
					PIL.Image.fromstring("RGB", (self.image.width, self.image.height), self.image.get_rgb_string(), "raw", "RGB", 0, 0)
				current = self.pageImages[self.currentDisplayPage]
				#self.overlay = current.copy()
				self.canvas.delete(Tkinter.ALL)
				self.tkimage = PIL.ImageTk.PhotoImage(current)
				width, height = self.image.width, self.image.height
				self.canvas.create_image(width/2., height/2., image=self.tkimage)
				self.canvas["width"] = self.image.width
				self.canvas["height"] = self.image.height
				self.canvas.update()
				#self.label["image"]  = self.tkimage
				self._refreshDocument()
				self.root.deiconify()
			if self.threaded:
				guiThread = getGuiThread()
				guiThread.executeFromThread(_updateImage)
			else:
				_updateImage()
	
		def keyEvent(self, event):
			#print event.char, event.type, event.keycode, dir(event)
			keycode = event.keycode
			character = None
			x, y = self.lastMousePos
			try:
				#character = chr(keycode)
				character = event.char
			except:
				pass
			#if event.keycode == 16:
			#	self.mouseOptions["alt"] = True
			if self.selectedObject is not None:
				self.selectedObject.handleKeyboardEvent(x, self.image.height - 1 - y, keycode, character, self.mouseOptions, self)
			#self.device.onKeyboardEvent(x, self.height-y-1, keycode, character, self.mouseOptions,
			#	self.currentDisplayPage, self, self.getSelectedObject())
	
		def mouseEventEnter(self, event):
			self.canvas.focus()
			#print self.canvas
			#print self.focus_get()
			#self.canvas.focus_force()
			#print self.canvas
			#print self.focus_get()
	
		def mouseEventDouble(self, event):
			#print "double", `event.type`, event.num, event.delta, event.x, event.y
			if event.num == 1:
				self.mouseOptions["leftdouble"] = True
			if event.num == 2:
				self.mouseOptions["middledouble"] = True
			if event.num == 3:
				self.mouseOptions["rightdouble"] = True
			if self.selectedObject is not None:
				self.selectedObject.handleMouseEvent(event.x, self.image.height - 1 - event.y, self.mouseOptions, self)
			self.mouseOptions["leftdouble"] = False
			self.mouseOptions["middledouble"] = False
			self.mouseOptions["rightdouble"] = False
			
				
		def mouseEvent(self, event):
			#print `event.type`, event.num, event.delta, event.x, event.y
	
			isdown = event.type == "4"
	
			if event.type in ["4", "5"]:
				for menu in self.menus[:]:
					menu._tkhide()
					self.menus.remove(menu)
				if event.num == 1:
					if isdown:
						self.mouseOptions["leftdown"] = True
					else:
						self.mouseOptions["leftup"] = True
					self.mouseOptions["leftisdown"] = isdown
	
				if event.num == 2:
					if isdown:
						self.mouseOptions["middledown"] = True
					else:
						self.mouseOptions["middleup"] = True
					self.mouseOptions["middleisdown"] = isdown
	
				if event.num == 3:
					if isdown:
						self.mouseOptions["rightdown"] = True
					else:
						self.mouseOptions["rightup"] = True
					self.mouseOptions["rightisdown"] = isdown
	
			prevx, prevy = self.lastMousePos
			dx = prevx - event.x
			dy = prevy - event.y
			if dx != 0 or dy != 0:
				self.mouseOptions["moving"] = True
			else:
				self.mouseOptions["moving"] = False
	
			if self.mouseOptions["moving"] and \
				(self.mouseOptions["rightisdown"] and not self.mouseOptions["rightdown"]) or  \
				(self.mouseOptions["middleisdown"] and not self.mouseOptions["middledown"]) or \
				(self.mouseOptions["leftisdown"] and not self.mouseOptions["leftdown"]):
				if not self.mouseOptions["dragging"]:
					self.mouseOptions["dragposition"] = (prevx, self.image.height - 1 - prevy)
				self.mouseOptions["dragging"] = True
			else:
				if self.mouseOptions["dragging"]:
					self.mouseOptions["wasdragging"] = True
				self.mouseOptions["dragging"] = False
	
			#self.device.onMouseEvent(event.x, self.height-event.y-1, self.mouseOptions,
			#	self.currentDisplayPage, self, self.getSelectedObject())
	
			#options["shift"] = event.ShiftDown()
			#options["control"] = event.ControlDown()
			#options["alt"] = event.AltDown()
			#guiThread = getGuiThread()
			if self.mouseOptions["moving"]:
				#self._drawZoomed()
				#def blabla():
				self.root.after_idle(self._drawZoomed)
				#guiThread.executeFromThread(blabla)
				
	
			if event.num == 1:
				self.root.after_idle(self._copyInfo)
	
			self.lastMousePos = event.x, event.y
			if self.selectedObject is not None:
				self.selectedObject.handleMouseEvent(event.x, self.image.height - 1 - event.y, self.mouseOptions, self)
	
			self.mouseOptions["leftup"] = False
			self.mouseOptions["leftdown"] = False
			self.mouseOptions["middleup"] = False
			self.mouseOptions["middledown"] = False
			self.mouseOptions["rightup"] = False
			self.mouseOptions["rightdown"] = False
			self.mouseOptions["wasdragging"] = False
	
		def _drawZoomed(self):
			#self.onMouseMove(event.x, event.y)
			#import pdb
			#pdb.set_trace()
			x, y = self.lastMousePos
			zoomedimage = self.getZoomedImage(self.pageImages[self.currentDisplayPage],
							x, y, 128, 128)
			self.zoomtkimage.paste(zoomedimage, (0,0))#(-50, -55))
			self.update()
	
		def setWaitMouseCursor(self):
			self.setMouseCursor("watch")
	
		def setCrosshairMouseCursor(self):
			self.setMouseCursor("crosshair")
	
		def setXMouseCursor(self):
			self.setMouseCursor("sb_h_double_arrow")
			
		def setYMouseCursor(self):
			self.setMouseCursor("sb_v_double_arrow")
			
		def setMouseCursor(self, cursor):
			self.configure(cursor=cursor)
			self.update()
			
		def getMouseCursor(self):
			return self.root["cursor"]
	
		def setDefaultCursor(self):
			self.setMouseCursor(self.defaultCursor)
	
		def refresh(self, pixmap):
			self.pixmap = pixmap
			if self.threaded:
				guiThread = getGuiThread()
				guiThread.executeFromThread(self._refresh)
				#self.event_generate("<<refresh>>", when="tail")
			else:
				self._refresh()
	
		def _refresh(self, *args):
			#self.tree.refreshTree()
			self._refreshDocument()
	
		def _refreshDocument(self):
			current = self.pageImages[self.currentDisplayPage]
			for item in self._canvasItems:
				self.canvas.delete(item)
			
			#self.canvas.create_image(0, 0, image=
			if self.rubberBand:
				x = self.rubberBand.xlist
				y = [self.image.height - 1 - k for k in self.rubberBand.ylist]
				if self.rubberBand.close:
					x.append(x[0])
					y.append(y[0])
				args = zip(x, y)
				kwargs = {"fill":"red", "stipple":"gray50"}
				item = self.canvas.create_line(*args, **kwargs)
				self._canvasItems.append(item)
			
			
		def __refreshDocument(self):
			# is this line really needed
			current = self.pageImages[self.currentDisplayPage]
			#self.overlay.paste(current)
			#self.tkimage.paste(current)
	
			#mask = PIL.Image.new("L", current.size, -1)
			#print dir(self.tkimage._PhotoImage__photo)
			draw = PIL.ImageDraw.Draw(self.overlay)
			if self.rubberBand:
				x = self.rubberBand.xlist
				y = [self.image.height - 1 - k for k in self.rubberBand.ylist]
				if self.rubberBand.close:
					x.append(x[0])
					y.append(y[0])
				draw.line(zip(x, y), fill="red")
			self.label["image"]  = self.tkimage
			#self.currentOverlayObject.draw(draw)
			#del draw
			#import pdb
			#pdb.set_trace()
			#image = PIL.Image.Image.(current)._makeself(current.im.chop_xor(mask.im))
			#self.label.update()
			#self.tkimage.resize((self.image.width, self.image.height))
			#sizex, sizey = copy.size
			#if self.currentImageHandle != None:
			#	self.label.delete(self.currentImageHandle)
			#self.currentImageHandle = self.label.create_image(sizex/2, sizey/2, image=self.tkimage)
			#self.update()
			#import pdb
			#pdb.set_trace()
	
		def about(self):
			tkMessageBox.showinfo("About", "coded by blabla");
	
		def help(self):
			tkMessageBox.showinfo("Help", "visit http://www.astro.rug.nl/~kplot");
	
	
		def _exitMainLoop(self):
			self.root.quit()
	
		def mainloop(self):
			self.root.deiconify()
			if not self.threaded:
				self.keeprunning = True
		# 		#clear(self.root.mainloop()
				#return False
				#self.root.iconify()
				try:
					while self.keeprunning:
						self.update()
						self.parent.state() # this might throw an exception if app is destoyed.. which is what we want
						time.sleep(0.02)
				except _tkinter.TclError:
					kaplot.debug("exit mainloop")
				#tkMaster.mainloop()
				#self.root.mainloop()
			else:
				kaplot.debug("waiting for window to close")
				self.closelock.clear()
				self.closelock.wait()
	
		def close(self):
			if self.threaded:
				kaplot.debug("waiting for deleteEvent")
				self.deleteEvent.wait()
			else:
				try:
					while True:
						self.update()
						self.parent.state() # this might throw an exception if app is destoyed.. which is what we want
						time.sleep(0.02)
				except _tkinter.TclError:
					pass
	
		def _copyInfo(self):
			#self.onMouseClick(event.x, event.y)
			self.setInfoCopyText(self.infoText.get("1.0", Tkinter.END))
	
		def setInfoText(self, text):
			#text.delete(1.0, END)
			self.infoText.delete("1.0", Tkinter.END)
			self.infoText.insert(Tkinter.END, text)
			
		def setInfoCopyText(self, text):
			self.infoTextCopy.delete("1.0", Tkinter.END)
			self.infoTextCopy.insert(Tkinter.END, text)
	
		def setInfoExtraText(self, text):
			self.infoTextExtra.delete("1.0", Tkinter.END)
			self.infoTextExtra.insert(Tkinter.END, text)
			
			
	tkThread = None
	def getGuiThread():
		global tkThread
		if tkThread == None:
			tkThread = TkGuiThread()
		return tkThread
	
	def createImageWindow(threaded=False):
		kaplot.debug("creating window, threaded=%r" % threaded)
		if threaded:
			def createPlotWindow(root):
				frame = createFrame(root)
				window = TkWindow(frame, 500, 400, 1, threaded=True)
				window.grid(row=0, column=0, sticky="NWSE")
				frame.columnconfigure(0, weight=1)
				frame.rowconfigure(0, weight=1)
				return window
			windowThread = getGuiThread()
			window = windowThread.executeFromThread(createPlotWindow, windowThread.root)
			return window
		else:
			tkMaster = getTkMaster()
			frame = createFrame(tkMaster)
			window = TkWindow(frame, 500, 400, 1, threaded=False)
			window.grid(row=0, column=0, sticky="NWSE")
			frame.columnconfigure(0, weight=1)
			frame.rowconfigure(0, weight=1)
			return window

if __name__ == "__main__":
	guiThread = getGuiThread()
	def bla():
		print "bla1"
	guiThread.executeFromThread(bla)
	guiThread.executeFromThread(bla)
 