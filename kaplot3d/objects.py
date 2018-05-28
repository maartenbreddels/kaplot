import kaplot
import math
from kaplot3d.matrix3d import Matrix3d
from kaplot3d.vector3d import Vector3d
from numpy import *
import kaplot.cext._ext3d

def bbox2points(bbox):
	(x1, y1, z1), (x2, y2, z2) = bbox
	vectors = []
	vectors.append(Vector3d(x1, y1, z1))
	vectors.append(Vector3d(x1, y2, z1))
	vectors.append(Vector3d(x2, y2, z1))
	vectors.append(Vector3d(x2, y1, z1))
	vectors.append(Vector3d(x1, y1, z2))
	vectors.append(Vector3d(x1, y2, z2))
	vectors.append(Vector3d(x2, y2, z2))
	vectors.append(Vector3d(x2, y1, z2))
	return vectors

class Container3D(kaplot.objects.Container):
	def __init__(self, page, viewpos=(0,10,10), phi=0, theta=0, zoom=1, **kwargs):
		super(Container3D, self).__init__(page, **kwargs)
		self.world3D = (-1,-1,-1), (1,1,1)
		self.viewpos = viewpos
		#viewAngle = math.radians(45)
		self.theta = math.radians(theta)
		self.phi = math.radians(phi)
		self.zoom = zoom
		#self.viewMatrix = create
		self.updateViewMatrix()
		self.bpoints = None
		
	def updateViewMatrix(self):
		bpoints = []
		if self.world3D:
			bpoints = bbox2points(self.world3D)
			#(x1, y1, z1), (x2, y2, z2) = self.world3D
			#dx = abs(x2-x1)
			#dy = abs(y2-y1)
			#dz = abs(z2-z1)
			#print "dx..", dx, dy, dz
		matrix = \
			Matrix3d._projection(3) * Matrix3d.translate(0,2, 120.2) * Matrix3d.rotateX(self.theta) * Matrix3d.rotateY(self.phi)
		if bpoints:
			tpoints = [matrix*p for p in bpoints]
			xmin, xmax = min([p.x for p in tpoints]), max([p.x for p in tpoints])
			ymin, ymax = min([p.y for p in tpoints]), max([p.y for p in tpoints])
			#zmin, zmax = min([p.z for p in tpoints]), max([p.z for p in tpoints])
			xs = xmax - xmin
			ys = ymax - ymin
			#zs = zmax - zmin
			s = 1.0/max(xs, ys) * self.zoom
			if False:
				s = 1
				matrix = Matrix3d.scale(s,s,s)  * matrix *\
					Matrix3d.translate(0,0, -10)
				#Matrix3d.translate(-min([p.x for p in tpoints]),
			else:
				matrix = \
				Matrix3d.translate(0.5, 0.5, 0) * \
				Matrix3d.scale(s, s, 1) *\
				Matrix3d.translate(-(xmax+xmin)/2, -(ymax+ymin)/2, 0) * \
				matrix
		self.bpoints = bpoints
		self.viewMatrix = matrix
		#kaplot.debug("updatedMatrix: %r", self.viewMatrix)
		
	def fit3D(self, bbox3D):
		if self.world3D is None:
			self.world3D = bbox3D
		else:
			(x1a, y1a, z1a), (x2a, y2a, z2a) = bbox3D
			(x1b, y1b, z1b), (x2b, y2b, z2b) = self.world3D
			flippedx = x1b > x2b
			flippedy = y1b > y2b
			flippedx = z1b > z2b
			x = [x1a, x2a, x1b, x2b]
			y = [y1a, y2a, y1b, y2b]
			z = [z1a, z2a, z1b, z2b]
			self.world3D = (min(x), min(y), min(z)), (max(x), max(y), max(z))
			self.updateViewMatrix()
			#if flippedx:
			#	self.flipx()
			#if flippedy:
			#	self.flipy()
			
	def draw(self, device):
		self.preDraw(device)
		self.drawObjects(device)
		if self.bpoints and False:
			bottom = self.bpoints[0:4] * 2
			top = self.bpoints[4:] * 2
			plist = []
			plist.extend(zip(bottom[:4], bottom[1:5]))
			plist.extend(zip(top[:4], top[1:5]))
			for i in range(4):
				plist.append((bottom[i], top[i]))
			for p1, p2 in plist:
				matrix = self.viewMatrix
				x1, y1, _ = matrix * Vector3d(p1.x, p1.y, p1.z)
				x2, y2, _ = matrix * Vector3d(p2.x, p2.y, p2.z)
				device.drawLine(x1, y1, x2, y2)
		self.drawDecorators(device)
		self.postDraw(device)

	def fitChildren(self):
		super(Container3D, self).fitChildren()
		for object in self.objects:
			if isinstance(object, PlotObject3D):
				bbox3D = object.getBBox3D()
				#if hasattr(bbox3D, "matrix"):
					#p1, p2 = bbox3D
					#p1 = object.matrix * Vector3d(*p1)
					#p2 = object.matrix * Vector3d(*p1)
					#bbox3D = (p1.
				if bbox3D:
					self.fit3D(bbox3D)


class PlotObject3D(kaplot.objects.PlotObject):
	def __init__(self, container, **kwargs):
		if not isinstance(container, Container3D):
			raise TypeError, "PlotObject parent should be a 3d container, (not '%r')" % (container)
		super(PlotObject3D, self).__init__(container, **kwargs)
		bbox3D = self.getBBox3D()
		if bbox3D is not None:
			self.container.fit3D(bbox3D)

	def getBBox3D(self):
		return None

class Line3D(PlotObject3D):
	def __init__(self, container, x1, y1, z1, x2, y2, z2, matrix=None, **kwargs):
		self.x1 = x1
		self.y1 = y1
		self.z1 = z1
		self.x2 = x2
		self.y2 = y2
		self.z2 = z2
		if matrix is not None:
			self.matrix = matrix
		else:
			self.matrix = Matrix3d()
		super(Line3D, self).__init__(container, **kwargs)
		
	def draw(self, device):
		device.pushContext(self.context)
		matrix = self.container.viewMatrix * self.matrix
		x1, y1, _ = matrix * Vector3d(self.x1, self.y1, self.z1)
		x2, y2, _ = matrix * Vector3d(self.x2, self.y2, self.z2)
		device.drawLine(x1, y1, x2, y2)
		#print "%.2f, %.2f, %.2f, %.2f" % (x1, y1, x2, y2)
		device.popContext()

	def getBBox3D(self):
		p1 = self.matrix * Vector3d(self.x1, self.y1, self.z1)
		p2 = self.matrix * Vector3d(self.x2, self.y2, self.z2)
		return p1, p2
				
class Text3D(PlotObject3D):
	def __init__(self, container, text, x=0.5, y=0.5, z=0.0, halign="center", valign="center", textangle=0, matrix=None, **kwargs):
		self.text = text
		self.x = x
		self.y = y
		self.z = z
		self.halign = halign
		self.valign = valign
		self.textangle = textangle
		if matrix is not None:
			self.matrix = matrix
		else:
			self.matrix = Matrix3d()
		super(Text3D, self).__init__(container, **kwargs)
		
	def draw(self, device):
		device.pushContext(self.context)
		matrix = self.container.viewMatrix * self.matrix
		x, y, _ = matrix * Vector3d(self.x, self.y, self.z)
		device.drawText(self.text, x, y, self.halign, self.valign, textangle=self.textangle)
		device.popContext()

	def getBBox3D(self):
		#p1 = self.matrix * Vector3d(x, y, z)
		#return p1, p2
		return None
				
class PolyLine3D(PlotObject3D):

	def __init__(self, container, x, y, z, close=False, matrix=None, **kwargs):
		self.x = x
		self.y = y
		self.z = z
		self.close = close
		if matrix is not None:
			self.matrix = matrix
		else:
			self.matrix = Matrix3d()
		super(PolyLine3D, self).__init__(container, **kwargs)
		
	def draw(self, device):
		device.pushContext(self.context)
		matrix = self.container.viewMatrix * self.matrix
		x, y, _ = matrix.mulXYZ(self.x, self.y, self.z)
		#print x, y
		device.drawPolyLine(x, y, close=self.close)
		device.popContext()
		
	def getBBox3D(self):
		p1 = self.matrix * Vector3d(min(self.x), min(self.y), min(self.z))
		p2 = self.matrix * Vector3d(max(self.x), max(self.y), max(self.z))
		return p1, p2

class MeshPlotRadial(PlotObject3D):
	def __init__(self, container, function, colorfunction=None, close=False, 
				dtheta=0.05, dphi=0.1, matrix=None,
				wireframe=True, solid=True, colormap="rainbow", **kwargs):
		self.function = function
		self.wireframe = wireframe
		self.solid = solid
		self.matrix = matrix
		self.colormap = kaplot.utils.getColormap(colormap)
		theta, phi = meshgrid(arange(0, math.pi+dtheta/2, dtheta), arange(0, 2*math.pi+dphi/2, dphi))
		r = function(theta, phi)
		self.x = r * sin(phi)* sin(theta)
		self.y = r * cos(theta)
		self.z = r * cos(phi)* sin(theta)
		if colorfunction is None:
			self.colors = r
		else:
			self.colors = colorfunction(theta, phi)
		super(MeshPlotRadial, self).__init__(container, **kwargs)
		
	def draw(self, device):
		device.pushContext(self.context)
		if self.matrix:
			matrix = self.container.viewMatrix * self.matrix
		else:
			matrix = self.container.viewMatrix 
		n1, n2 = self.x.shape
		colors = array(self.colors);
		datamin = colors.min()
		datamax = colors.max()
		colors = (colors - datamin) / (datamax - datamin)
		r, g, b = device.getColor().getRGB()

		kaplot.cext._ext3d.mesh3d(self.x, self.y, self.z, matrix.matrix,
			device.getCInterface(),
			shading=False, colors=colors, colorfunction=self.colorfunction,
			wirecolor=(r, g, b),
			 wireframe=self.wireframe, solid=self.solid)
			 #, 
		device.popContext()
		
	def colorfunction(self, v):
		color = self.colormap(v)
		return color.r, color.g, color.b


	def getBBox3D(self):
		if self.matrix is None:
			x, y, z = self.x, self.y, self.z
		else:
			x, y, z = self.matrix.mulXYZ(array(self.x.flat), array(self.y.flat), array(self.z.flat))
		return (min(x.flat), min(y.flat), min(z.flat)),\
		 (max(x.flat), max(y.flat), max(z.flat))
