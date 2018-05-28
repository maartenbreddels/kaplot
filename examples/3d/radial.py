from kaplot import *
import kaplot3d


page()
current.container = kaplot3d.Container3D(current.page, phi=10, theta=30, zoom=1)
def fr(theta, phi):
	return cos(theta)**2

#def fr(theta, phi):
#	return -1/sqrt(2)+cos(theta)*cos(phi)*sin(theta)

def frxa(theta, phi):
	# yx, U
	return (sin(theta)**2)*1

def frxb(theta, phi):
	# xz, U
	x = cos(theta)
	y = sin(phi) * sin(theta)
	z = cos(phi) * sin(theta)
	x, y, z = z, y, x
	costheta = x
	return (1-costheta**2)*1
	
def frza(theta, phi):
	# xy, U
	x = cos(theta)
	y = sin(phi) * sin(theta)
	z = cos(phi) * sin(theta)
	#x, y, z = y, x, z
	costheta = x
	return (1-costheta**2)*1
	
def frzb(theta, phi):
	# yz, L
	x = cos(theta)
	y = sin(phi) * sin(theta)
	z = cos(phi) * sin(theta)
	x, y, z = y, x, z
	costheta = x
	return (1-costheta**2)*1
	
def frya(theta, phi):
	# yz, L
	x = cos(theta)
	y = sin(phi) * sin(theta)
	z = cos(phi) * sin(theta)
	x, y, z = y, x, z
	costheta = x
	return (1-costheta**2)*3
	
def fryb(theta, phi):
	# xz, L 
	x = cos(theta)
	y = sin(phi) * sin(theta)
	z = cos(phi) * sin(theta)
	x, y, z = z, y, x
	costheta = x
	return (1-costheta**2)*3
	
fr = fryb
frc = fr

def fr(theta, phi):
	fs = [frxa, frxb, frya, fryb, frza, frzb]
	return sum([k(theta, phi) for k in fs],0)

def frc(theta, phi):
	fsU = [frxa, frxb, frya]
	fsL = [fryb, frza, frzb]
	U = sum([k(theta, phi) for k in fsU],0) / 5
	L = sum([k(theta, phi) for k in fsL],0) / 5
	print U.min(), U.max(), L.min(), L.max()
	return U
	#return arctan2(U, L)
	#I = (U+L)
	#return I - I.min()
	#	return abs(abs(U)-abs(L))
	#return sqrt(U**2-L**2)
fsX = [frya, frzb]
fsY = [frxa, frza]
fsZ = [frxb, fryb]
def fr(theta, phi):
	X = sum([k(theta, phi) for k in fsX],0)
	Y = sum([k(theta, phi) for k in fsY],0)
	Z = sum([k(theta, phi) for k in fsZ],0)
	I = (X+Y+Z)/4
	return I
	#return abs(I) - abs(I).min()
	#return frza(theta, phi) + frzb(theta, phi)
	return Y
def frc1(theta, phi):
	X = sum([k(theta, phi) for k in fsX],0)
	Y = sum([k(theta, phi) for k in fsY],0)
	Z = sum([k(theta, phi) for k in fsZ],0)
	I = (X-Y-Z)/3
	print X.min(), X.max(), Y.min(), Y.max(), Z.min(), Z.max(), I.min(), I.max()
	a = frya(theta, phi)
	b = fryb(theta, phi)
	U = a*cos(theta)+b*sin(theta)
	Q = a*cos(theta)+b*sin(theta)
	return 
	#return (Y-Z-X)
	#return X+Y+Z
	return (Y-X) - (Z-Y)
def frc2(theta, phi):
	X = sum([k(theta, phi) for k in fsX],0)
	Y = sum([k(theta, phi) for k in fsY],0)
	Z = sum([k(theta, phi) for k in fsZ],0)
	I = (X-Y-Z)/3
	return Y
	print X.min(), X.max(), Y.min(), Y.max(), Z.min(), Z.max(), I.min(), I.max()
	return (Y-X)
def frc3(theta, phi):
	X = sum([k(theta, phi) for k in fsX],0)
	Y = sum([k(theta, phi) for k in fsY],0)
	Z = sum([k(theta, phi) for k in fsZ],0)
	I = (X-Y-Z)/3
	return Z
	print X.min(), X.max(), Y.min(), Y.max(), Z.min(), Z.max(), I.min(), I.max()
	return (Z-Y)
	#I = (X-Z)
	#return I - I.min()
	#return abs(I) - abs(I).min()
	#return frza(theta, phi) + frzb(theta, phi)
	#return Y
#def frc(theta, phi):
#	return arctan2(fr2(theta, phi),fr1(theta, phi)) - sqrt(2)/2
	

#def fr(theta, phi):
#	return -0.5+sin(theta)**2

t = arange(0.0,2*pi/2, 0.005)
A = 0.15
x = 0*t
y = t
z = A * sin(t*20)
#phi = math.radians(rot)
#xr = cos(phi)*x + sin(phi)*z
#zr = -sin(phi)*x + cos(phi)*z
#yr = y
basealpha = 0.5


colormap = kaplot.ColorMap(["red", "green", "blue"], interpolate=False)
#kaplot3d.MeshPlotRadial(current.container, lambda x,y: 1, colorfunction=fr, color="black", 
#	linewidth="0.4px", colormap=colormap)
matrix = kaplot3d.Matrix3d.translate(0,4,0)
m = kaplot3d.MeshPlotRadial(current.container, fr, colorfunction=frc1, color="black", 
	linewidth="0.4px", colormap=colormap, solid=True, wireframe=False,
	dtheta=0.1/2, dphi=0.05/2, matrix=matrix)
matrix = kaplot3d.Matrix3d.translate(0,0,0)
m = kaplot3d.MeshPlotRadial(current.container, fr, colorfunction=frc2, color="black", 
	linewidth="0.4px", colormap=colormap, solid=True, wireframe=False,
	dtheta=0.1/2, dphi=0.05/2, matrix=matrix)
matrix = kaplot3d.Matrix3d.translate(0,-4,0)
m = kaplot3d.MeshPlotRadial(current.container, fr, colorfunction=frc3, color="black", 
	linewidth="0.4px", colormap=colormap, solid=True, wireframe=False,
	dtheta=0.1/2, dphi=0.05/2, matrix=matrix)
	
print "mm", m.colors.min(), m.colors.max()
for x,y,f in [(-6, 2, frxa), (-6, -2, frxb), (-4, 2, frya) , (-4, -2, fryb), (-2, 2, frza) , (-2, -2, frzb)][::-1]:
	matrix = kaplot3d.Matrix3d.translate(x,y,0)
	kaplot3d.MeshPlotRadial(current.container, f, color="black", linewidth="0.1px", matrix=matrix, alpha=0.5)
#kaplot3d.MeshPlotRadial(current.container, fr, color="black", linewidth="1px")
#kaplot3d.MeshPlotRadial(current.container, fr, color="black", linewidth="1px")
#def graph3d(
#line = kaplot3d.PolyLine3D(current.container, x, y, z, color="black", linewidth="1px")
#line = kaplot3d.PolyLine3D(current.container, z, y, x, color="black", linewidth="1px", linestyle="dot")
#line = kaplot3d.PolyLine3D(current.container, x, y, x, color="black", linewidth="1px")
draw()