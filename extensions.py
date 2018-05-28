#!/usr/bin/env python
# -*- coding: utf-8 -*-
from distutils.core import setup, Extension
from distutils.sysconfig import get_python_inc, get_python_lib
import os
import sys
import glob

#basedir = os.path.dirname(__file__)
basedir = os.path.join(os.path.dirname(__file__), "src")
#sys.path.append(os.path.abspath(os.path.join(basedir, "..")))

wcslib = False
contour = True
cairo = False
pyfont = True
ext3d = True
kaplot = True
gipsy = True #False
image = True
agg = True

extensions = []

import numpy
numdir = os.path.dirname(numpy.__file__)
print ">>>", numdir
#dsa
numpyinc = os.path.join(numdir, "numarray", "numpy")
numpyinc2 = os.path.join(numdir, "core", "include")
#numpyinc3 = os.path.join(numdir, "core")
numpyinc3 = os.path.join(numdir, "numarray", "include", "numpy")


if wcslib:
	defines = []
	extra_compile_args = []
	include_dirs = []
	library_dirs = []
	data_files = []
	libraries = []

	include_dirs.append(os.path.join(get_python_inc(plat_specific=1), "numpy"))
	include_dirs.append(os.path.join(basedir, "wcslib"))
	defines.append(("__STDC__", "1"))
	sources = [os.path.join(basedir, "wcslib", k) for k in "lin.c prj.c sph.c cel.c spx.c spc.c wcs.c cylfix.c wcstrig.c pywcsmodule.c pywcs.c reproj.c".split(" ")]
	#sources.append("wcsmodule.c")

	wcslibExtension = Extension("kaplot.cext._wcslib", sources,
		include_dirs=include_dirs,
		library_dirs=library_dirs,
		libraries=libraries,
		define_macros=defines,
		extra_compile_args=extra_compile_args
		)
	extensions.append(wcslibExtension)

if contour:
	defines = []
	extra_compile_args = []
	include_dirs = []
	library_dirs = []
	data_files = []
	libraries = []

	#include_dirs.append(os.path.join(get_python_inc(plat_specific=1), "numpy"))
	include_dirs.append(numpyinc)
	include_dirs.append(numpyinc2)
	include_dirs.append(numpyinc3)
	include_dirs.append(os.path.join(basedir, "contour"))
	include_dirs.append(os.path.join(basedir, "kaplot"))
	sources = [os.path.join(basedir, "contour", k) for k in "contour.c pgcn01.c pgconx.c pgcnsc.c".split(" ")]

	contourExtension = Extension("kaplot.cext._contour", sources,
		include_dirs=include_dirs,
		library_dirs=library_dirs,
		libraries=libraries,
		define_macros=defines,
		extra_compile_args=extra_compile_args
		)
	extensions.append(contourExtension)

if cairo:
	defines = []
	extra_compile_args = []
	include_dirs = []
	library_dirs = []
	data_files = []
	libraries = []
	if sys.platform == "win32":
		defines.append(("WIN32", 1))

	include_dirs.append(os.path.join(get_python_inc(plat_specific=1), "numpy"))
	include_dirs.append(os.path.join(basedir, "cairo"))
	include_dirs.append(os.path.join(basedir, "contour"))
	include_dirs.append(os.path.join(basedir, "ext3d"))
	include_dirs.append(os.path.join(basedir, "font"))
	include_dirs.append(os.path.join(basedir, "kaplot"))
	include_dirs.append(r"h:\python\cairo\pycairo\cairo")
	include_dirs.append(r"h:\python\cairo\cairo\src")
	include_dirs.append(r"h:\python\cairo\libpixman\src")
	include_dirs.append(r"h:\python\cairo\include")
	include_dirs.append(r"h:\python\cairo\freetype-2.1.8\include")
	#include_dirs.append("h:\python\cairo")
	#include_dirs.append("h:\python\cairo\libpixregion\src")
	#include_dirs.append("h:\python\cairo\slim\src")

	if sys.platform == "win32":
		buildstatic = False
		libraries.append("user32")
		libraries.append("gdi32")
		libraries.append("advapi32")
		if buildstatic:
			libraries.append("cairostatic")
			libraries.append("libpixman")
			libraries.append("libpng")
			libraries.append("libpng")
		else:
			libraries.append("cairo")
		library_dirs.append("h:\python\cairo\lib")
	else:
		libraries.append("cairo")

	#libraries.append("cairo")
	sources = [os.path.join("cairo", k) for k in "cairo.c".split(" ")]

	cairoExtension = Extension("kaplot.cext._cairo", sources,
		include_dirs=include_dirs,
		library_dirs=library_dirs,
		libraries=libraries,
		define_macros=defines,
		extra_compile_args=extra_compile_args
		)
	extensions.append(cairoExtension)

if pyfont:
	defines = []
	extra_compile_args = []
	include_dirs = []
	library_dirs = []
	data_files = []
	libraries = []
	if "linux" in sys.platform:
		include_dirs.append("/usr/include/freetype2")
	else:
	#include_dirs.append(os.path.join(get_python_inc(plat_specific=1), "numpy"))
		#include_dirs.append("h:\python\cairo\include")
		include_dirs.append(r"f:\misc\python\cairo\freetype-2.1.8\include")
		library_dirs.append("f:\misc\python\cairo\lib")
	
	include_dirs.append(os.path.join(basedir, "font"))
	include_dirs.append(os.path.join(basedir, "kaplot"))
	sources = [os.path.join(basedir, "font", k) for k in "pyfont.c".split(" ")]
	libraries.append("freetype")

	pyfontExtension = Extension("kaplot.cext._pyfont", sources,
		include_dirs=include_dirs,
		library_dirs=library_dirs,
		libraries=libraries,
		define_macros=defines,
		extra_compile_args=extra_compile_args
		)
	extensions.append(pyfontExtension)

if ext3d:
	defines = []
	extra_compile_args = []
	include_dirs = []
	library_dirs = []
	data_files = []
	libraries = []

	sources = [os.path.join(basedir, "ext3d", k) for k in "ext3d.c".split(" ")]
	include_dirs.append(os.path.join(get_python_inc(plat_specific=1), "numpy"))
	include_dirs.append(os.path.join(basedir, "ext3d"))
	include_dirs.append(os.path.join(basedir, "kaplot"))
	include_dirs.append(numpyinc)
	include_dirs.append(numpyinc2)
        include_dirs.append(numpyinc3)


	ext3dExtension = Extension("kaplot.cext._ext3d", sources,
		include_dirs=include_dirs,
		library_dirs=library_dirs,
		libraries=libraries,
		define_macros=defines,
		extra_compile_args=extra_compile_args
		)
	extensions.append(ext3dExtension)

if kaplot:
	defines = []
	extra_compile_args = []
	include_dirs = []
	library_dirs = []
	data_files = []
	libraries = []

	#include_dirs.append(os.path.join(get_python_inc(plat_specific=1), "numpy"))
	include_dirs.append(numpyinc)
	include_dirs.append(numpyinc2)
	include_dirs.append(numpyinc3)
	include_dirs.append(os.path.join(basedir, "kaplot"))
	sources = [os.path.join(basedir, "kaplot", k) for k in "kaplot.c matrix.c vector.c vector4.c".split(" ")]

	kaplotExtension = Extension("kaplot.cext._kaplot", sources,
		include_dirs=include_dirs,
		library_dirs=library_dirs,
		libraries=libraries,
		define_macros=defines,
		extra_compile_args=extra_compile_args
		)
	extensions.append(kaplotExtension)

if gipsy:
	defines = []
	extra_compile_args = []
	include_dirs = []
	library_dirs = []
	data_files = []
	libraries = []

	include_dirs.append(numpyinc)
	include_dirs.append(numpyinc2)
	include_dirs.append(numpyinc3)
	#include_dirs.append(os.path.join(get_python_inc(plat_specific=1), "numpy"))
	include_dirs.append(os.path.join(basedir, "gipsy"))
	sources = [os.path.join(basedir, "gipsy", k) for k in "eclipco.c julianday.c skyco.c gipsy.c".split(" ")]

	gipsyExtension = Extension("kaplot.cext._gipsy", sources,
		include_dirs=include_dirs,
		library_dirs=library_dirs,
		libraries=libraries,
		define_macros=defines,
		extra_compile_args=extra_compile_args
		)
	extensions.append(gipsyExtension)

if image:
	defines = []
	extra_compile_args = []
	include_dirs = []
	library_dirs = []
	data_files = []
	libraries = []

	#include_dirs.append(os.path.join(get_python_inc(plat_specific=1), "numpy"))
	include_dirs.append(numpyinc)
	include_dirs.append(numpyinc2)
        include_dirs.append(numpyinc3)

	include_dirs.append(os.path.join(basedir, "image"))
	sources = [os.path.join(basedir, "image", k) for k in "image.c".split(" ")]

	imageExtension = Extension("kaplot.cext._image", sources,
		include_dirs=include_dirs,
		library_dirs=library_dirs,
		libraries=libraries,
		define_macros=defines,
		extra_compile_args=extra_compile_args
		)
	extensions.append(imageExtension)

if agg:
	defines = []
	extra_compile_args = []
	if sys.platform == "win32": # should be a msvc compiler check
		extra_compile_args.append("/Od") # don't optimize! (compiler bug?)
		extra_compile_args.append("/MDd")
		extra_compile_args.append("/FR\"src/agg/\"")
		extra_compile_args.append("/Fp\"src/agg/_agg.pch\"")
		extra_compile_args.append("/YX")
		#extra_compile_args.append("/Fo\"agg\"")
		#extra_compile_args.append("/Fd\"agg\"")
		extra_compile_args.append("/FD")
		extra_compile_args.append("/GZ")
		extra_compile_args.append("/ZI")
		extra_compile_args.append("/debug")
		
		
		#" /Fp"Debug/6df.pch" /YX /Fo"Debug/" /Fd"Debug/" /FD /GZ /c 
	else:
		extra_compile_args.append("-fstrict-aliasing") # for gcc (compiler bug?)
	include_dirs = []
	library_dirs = ["../../"	]
	data_files = []
	#libraries = ["./agg"]
	include_dirs.append(os.path.join(basedir, "agg/agg23/include"))

	#include_dirs.append(os.path.join(get_python_inc(plat_specific=1), "numpy"))
	include_dirs.append(numpyinc)
	include_dirs.append(numpyinc2)
        include_dirs.append(numpyinc3)
	include_dirs.append(os.path.join(basedir, "agg"))
	include_dirs.append(os.path.join(basedir, "kaplot"))
	sources = [os.path.join(basedir, "agg", k) for k in "pyagg23.cpp".split(" ")]
	sources += glob.glob(os.path.join(basedir, "agg", "agg23", "src", "*.cpp"))

	aggExtension = Extension("kaplot.cext._agg", sources,
		include_dirs=include_dirs,
		library_dirs=library_dirs,
		libraries=libraries,
		define_macros=defines,
		extra_compile_args=extra_compile_args
		)
	extensions.append(aggExtension)

version = "0.1"
description = "Python bindings to c routines for kaplot"
author = "M.A. Breddels"
author_email = "dmon at xs4all dot nl"
url = "http://?"

if __name__ == "__main__":
	setup(name="kaplot",
		packages=[],
		version=version,
		description=description,
		author=author,
		author_email=author_email,
		url=url,
		ext_modules=extensions,
		data_files=data_files
		)
