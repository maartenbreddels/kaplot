from kaplot import *
import kaplot

class MyObject(kaplot.objects.PlotObject):
	def __init__(self, container, **kwargs):
		super(MyObject, self).__init__(container, **kwargs)
		self.xlist = [sin(k*pi/5)*0.4+0.5 for k in range(10)]
		self.ylist = [cos(k*pi/5)*0.3+0.5 for k in range(10)]
		
	def draw(self, device):
		device.pushContext(self.context)
		print "draw", self.xlist, self.ylist
		device.drawPolyLine(self.xlist, self.ylist, close=True)
		for i, (x, y) in enumerate(zip(self.xlist, self.ylist)):
			device.drawText(str(i+1), x, y)
		device.popContext()
		
	def handleKeyboardEvent(self, x, y, keycode, character, options, window):
		if character is not None:
			print character
			try:
				index = int(character)
				print "index =", index
				if index == 0:
					index = 10
				index -= 1
				wx, wy = self.container.windowToWorld(x, y)
				self.xlist[index] = wx
				self.ylist[index] = wy
				window.refreshPlot()
			except:
				pass # ignore other keys
				
			linestyles = {"Q":"normal", "W":"dot", "E":"dash", "R":"dotdash", "T":"dotdotdotdash"}
			linewidths = {"A":"1px", "S":"2px", "D":"4px", "F":"8px", "G":"16px"}
			if character in linestyles:
				self.context.linestyle = linestyles[character]
				window.refreshPlot()
			if character in linewidths:
				self.context.linewidth = linewidths[character]
				window.refreshPlot()
			text = ""
			if "linestyle" in self.context:
				text += "linestyle = %r\n" % self.context.linestyle
			if "linewidth" in self.context:
				text += "linewidth = %r\n" %  self.context.linewidth
			window.setInfoExtraText(text)
		

	def _handleMouseEvent(self, x, y, options, window):
		wx, wy = self.container.windowToWorld(x, y)
		if options["leftup"]:
			self.xlist.append(wx)
			self.ylist.append(wy)
			window.refreshPlot()
			print wx, wy
		if options["rightup"]:
			if len(self.xlist) > 0:
				self.xlist.pop()
				self.ylist.pop()
			window.refreshPlot()

#container(viewport=((0.1, 0.1), ()
box()

obj = MyObject(current.container, color="red")
guiselect(obj)

draw()