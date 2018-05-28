#!/usr/bin/env python
from distutils.core import setup, Extension
from distutils.sysconfig import get_python_inc, get_python_lib
import os
import sys
sys.path.append(os.path.dirname(__file__))

pjoin = os.path.join
from extensions import extensions
#import kaplot
#version = kaplot.__version__
version = "0.3"

data_files = [
				#(pjoin("share", "kaplot", "fits"), [pjoin("data", "fits", "*.fits")]),
				#(pjoin("share", "kaplot", "wmap"), [pjoin("data", "wmap", "m81.fits")]),
			]

if sys.platform == "win32":
	data_files.append(("", [r"h:\python\cairo\lib\cairo.dll"]))

packages = [
		"kaplot",
		"kaplot.objects",
		"kaplot.astro",
		"kaplot.cext",
		"kaplot.text",
		#"kaplot.doc",
		#"kaplot.kaplot3d",
		"kaplot.gui",
		"kaplot.gui.tk",
		"kaplot.devices",
		#"kaplot.devices.cairo",
		#"kaplot.devices.gs",
		#"kaplot.devices.pdf",
		#"kaplot.demo",
		#"kaplot.demo.astro",
		#"kaplot.demo.basics",
		#"kaplot.demo.containers",
		#"kaplot.demo.examples",
		#"kaplot.demo.more",
		#"kaplot.demo.plot3d",
		]

full = False
for arg in sys.argv[:]:
	print `arg`
	if arg == "full":
		print "found"
		#sys.argv.remove(arg)
		full = True

#scripts = ['scripts/kaplotdemo.py', 'scripts/postinstallwin32.py']

def main():
	setup(
		name="kaplot",
		version=version,
		author="Maarten Breddels",
		author_email="maartenbreddels@gmail.nl",
		url="http://www.astro.rug.nl/~breddels/cgi-bin/moin.cgi/KaplotPage",
		description="vector based plotting library, targeted but not limited to astronomical plotting",
		#scripts=scripts,
		data_files=data_files,
		ext_modules=extensions,
		packages=packages
		)

if __name__ == "__main__":
	main()