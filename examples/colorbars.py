from kaplot import *

image = indexedimage(data.perlin2dnoise(8))
for hloc in ["left", "center", "right"]:
	for vloc in ["top", "center", "bottom"]:
		location = "%s, %s" % (hloc, vloc)
		innercolorbar(image, direction="down", location=location,
			edgespacing="1cm")
draw()
