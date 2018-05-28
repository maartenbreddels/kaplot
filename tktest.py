#!/usr/bin/env python

from Tkinter import *

class App:

	def __init__(self, master):
		frame = Frame(master)
		frame.pack()
		self.frame = frame
		
		self.button = Button(frame, text="QUIT", fg="red", command=frame.quit)
		self.button.pack(side=LEFT)
		
		self.hi_there = Button(frame, text="Hello", command=self.say_hi)
		self.hi_there.pack(side=LEFT)
		self.menus = []

	def say_hi(self):
		#print "hi there, everyone!"
		_tkmenu = Menu(self.frame, tearoff=1)
		def bla(*args):
			print "hoeba!"
		def popupFocusOut(event, _tkmenu=_tkmenu):
			print "HOEEEEEEEEEEEEEEBA!"
			_tkmenu.unpost()
		_tkmenu.bind("<FocusOut>", popupFocusOut)
		_tkmenu.bind("<FocusIn>", popupFocusOut)
		_tkmenu.add_command(label="dsadsa", command=bla)
		_tkmenu.post(100, 100)
		self.menus.append(_tkmenu)

#root = Tk()
#app = App(root)
#root.mainloop()

from Tkinter import *

root = Tk()

def hello():
        print "hello!"
def hello1():
        print "hello1!"
def hello2():
        print "hello2!"

def popup(event):
        menu.post(event.x_root, event.y_root)
        menu.focus_set()

def popupFocusOut(self,event=None):
        menu.unpost()

# create a canvas
frame = Frame(root, width=512, height=512)
frame.pack()

# create a popup menu
menu = Menu(frame, tearoff=0)
menu.add_command(label="Undo", command=hello)
menu.add_command(label="Redo", command=hello)

submenu = Menu(menu, tearoff=0)
submenu.add_command(label="Undo", command=hello1)
submenu.add_command(label="Redo", command=hello2)
menu.add_cascade(label="sub", menu=submenu)
#menu.bind("<FocusOut>",popupFocusOut)

# attach popup to canvas
frame.bind("<Button-3>", popup)
frame.bind("<Button-1>", popupFocusOut)

mainloop()