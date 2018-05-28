class PlotWindow(object):
	pass
	
	
class WxPlotFrame(wx.Frame):
	def __init__(self):
		wx.Frame.__init__(self, -1, "kaplot - wxPython")
		self.leftBar = wx.Panel

class WxPlotWindow(wx.Panel):
	def __init__(self, parent, device):
		wx.Panel.__init__(self, parent, -1, size=(300, 300))
		self.setBackgroup("red")
		
	
