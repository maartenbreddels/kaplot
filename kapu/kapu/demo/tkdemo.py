from Tkinter import *
from kapu.stereographic import *
from kapu.aitoff import *
from kapu.hammer import *
import kapu

class ProjectionWindow(Frame):
	def __init__(self, parent=None, **kw):
		Frame.__init__(self, parent, **kw)
		self.canvas = Canvas(self, width=400, height=400)
		
		self.projections = {}
		self.projections["stereographic"] = StereoGraphicProjection(phi0=pi/2)
		self.projections["aitoff"] = AitoffProjection()
		ref = (0, 0)
		s = 50
		wcs = kapu.Wcs(ref, ["RA---AIT", "DEC--AIT"], [s,0,0, s], (1,1), (0, 0), (0,0), [1,0,0,1], 1|2|4, [(1,0,1), (2,1,1)] )
		#self.projections["hammer"] = HammerProjection()
		self.projections["aitoff(wcs)"] = wcs
		
		
		
		self.projectionVar = StringVar()
		self.projectionVar.set("aitoff(wcs)")
		
		i = 0
		for text, value in self.projections.items():
			b = Radiobutton(self, text=text, variable=self.projectionVar, value=text, command=self.redraw)
			b.grid(row=0, column=i)
			i += 1


		self.equatorial = BooleanVar()
		self.equatorialButton = Checkbutton(self, text="equatorial", variable=self.equatorial, command=self.redraw)
		self.equatorialButton.grid(row=1, column=0)
		
		self.galactic = BooleanVar()
		self.galacticButton = Checkbutton(self, text="galactic", variable=self.galactic, command=self.redraw)
		self.galacticButton.grid(row=1, column=1)
		
		self.superGalactic = BooleanVar()
		self.superGalactic.set(True)
		self.superGalacticButton = Checkbutton(self, text="super galactic", variable=self.superGalactic, command=self.redraw)
		self.superGalacticButton.grid(row=1, column=2)
		
		self.canvas.grid(row=2, column=0, columnspan=3)
		self.pack()
		self.redraw()
		
	def redraw(self):
		print "redraw"
		self.projection = self.projections[self.projectionVar.get()]
		self.draw_projection()
		
	def draw_projection(self):
		self.canvas.delete(ALL) # delete all items
		thetarange = range(-170, 181, 10) + [-180, -170]
		phirange = range(-90, 91, 10)
		#thetarange = range(-10, 171, 10)
		#phirange = range(0, 90, 10)
		
		cx, cy = 200, 200
		scale = 70
		print self.equatorial.get()
		if self.equatorial.get():
			for phi1, phi2 in zip(phirange[:-1], phirange[1:]):
				for theta1, theta2 in zip(thetarange[:-1], thetarange[1:]):
					try:
						x1, y1 = self.projection.to_pixel(theta1, phi1)
						x2, y2 = self.projection.to_pixel(theta2, phi1)
						x3, y3 = self.projection.to_pixel(theta2, phi2)
						x4, y4 = self.projection.to_pixel(theta1, phi2)
						self.canvas.create_line(cx+x1*scale, cy+y1*scale, cx+x2*scale, cy+y2*scale)
						self.canvas.create_line(cx+x2*scale, cy+y2*scale, cx+x3*scale, cy+y3*scale)
						self.canvas.create_line(cx+x3*scale, cy+y3*scale, cx+x4*scale, cy+y4*scale)
						self.canvas.create_line(cx+x4*scale, cy+y4*scale, cx+x1*scale, cy+y1*scale)
						print x1, y1
					except:
						pass # ignore errors
				
		# same, but with other sky coordinates
		
		try:
			if self.galactic.get():
				self.draw_skyco(thetarange, phirange, kapu.EQUATORIAL_1950, kapu.GALACTIC, "blue")
		except:
			print "error drawing galactic projection"
		try:
			if self.superGalactic.get():
				self.draw_skyco(thetarange, phirange, kapu.EQUATORIAL_1950, kapu.SUPERGALACTIC, "red")
		except:
			print "error drawing super galactic projection"
		
	def draw_skyco(self, thetarange, phirange, from_system, to_system, color):
		cx, cy = 200, 200
		scale = 70

		for phi1, phi2 in zip(phirange[:-1], phirange[1:]):
			for theta1, theta2 in zip(thetarange[:-1], thetarange[1:]):
				#print phi1, phi2
				#print theta1, theta2
				alpha1, beta1 = kapu.skyco(theta1, phi1, from_system, to_system)
				alpha2, beta2 = kapu.skyco(theta2, phi1, from_system, to_system)
				alpha3, beta3 = kapu.skyco(theta2, phi2, from_system, to_system)
				alpha4, beta4 = kapu.skyco(theta1, phi2, from_system, to_system)
				def angle_range(angle):
					# makes sure it's in [-180, 180) range
					return (angle+360+180) % 360 - 180
				x1, y1 = self.projection.to_pixel(angle_range(alpha1), angle_range(beta1))
				x2, y2 = self.projection.to_pixel(angle_range(alpha2), angle_range(beta2))
				x3, y3 = self.projection.to_pixel(angle_range(alpha3), angle_range(beta3))
				x4, y4 = self.projection.to_pixel(angle_range(alpha4), angle_range(beta4))
				#print theta1, alpha1, phi1, beta1

				self.canvas.create_line(cx+x1*scale, cy+y1*scale, cx+x2*scale, cy+y2*scale, fill=color)
				self.canvas.create_line(cx+x2*scale, cy+y2*scale, cx+x3*scale, cy+y3*scale, fill=color)
				self.canvas.create_line(cx+x3*scale, cy+y3*scale, cx+x4*scale, cy+y4*scale, fill=color)
				self.canvas.create_line(cx+x4*scale, cy+y4*scale, cx+x1*scale, cy+y1*scale, fill=color)
				
				
		


root = Tk()
root.title("Projection/Transformation demo")

window = ProjectionWindow()
window.mainloop()