#!/usr/bin/env python
from distutils.core import setup, Extension
from distutils.sysconfig import get_python_inc, get_python_lib
import os
import sys
import glob

name = "kapu"
version = "0.1"
description = "Python bindings to c routines for handling coordinate projections"
author = "M.A. Breddels"
author_email = "maartenbreddels .. at .. gmail.com"
url = "http://www.astro.rug.nl/~breddels/"


basedir = os.path.join(os.path.dirname(__file__), "src")

gipsy = True
wcslib = True

extensions = []

if wcslib:
	defines = []
	extra_compile_args = []
	include_dirs = []
	library_dirs = []
	data_files = []
	libraries = []

	import numpy
	numdir = os.path.dirname(numpy.__file__)
	ipath = os.path.join(numdir, "numarray", "numpy")
	print ipath
	include_dirs.append(ipath)
	ipath = os.path.join(numdir, "core", "include")
	print ipath
	include_dirs.append(ipath)

	include_dirs.append(os.path.join(basedir, "wcslib"))
	defines.append(("__STDC__", "1"))
	sources = [os.path.join(basedir, "wcslib", k) for k in "lin.c prj.c sph.c cel.c spx.c spc.c wcs.c cylfix.c wcstrig.c pywcsmodule.c pywcs.c reproj.c".split(" ")]
	#sources.append("wcsmodule.c")

	wcslibExtension = Extension("kapu._wcslib", sources,
		include_dirs=include_dirs,
		library_dirs=library_dirs,
		libraries=libraries,
		define_macros=defines,
		extra_compile_args=extra_compile_args
		)
	extensions.append(wcslibExtension)
	
if gipsy:
	defines = []
	extra_compile_args = []
	include_dirs = []
	library_dirs = []
	data_files = []
	libraries = []

	import numpy
	numdir = os.path.dirname(numpy.__file__)
	ipath = os.path.join(numdir, "numarray", "numpy")
	print ipath
	include_dirs.append(ipath)
	ipath = os.path.join(numdir, "core", "include")
	print ipath
	include_dirs.append(ipath)

	include_dirs.append(os.path.join(basedir, "gipsy"))
	sources = [os.path.join(basedir, "gipsy", k) for k in "eclipco.c julianday.c skyco.c gipsy.c".split(" ")]

	gipsyExtension = Extension("kapu._gipsy", sources,
		include_dirs=include_dirs,
		library_dirs=library_dirs,
		libraries=libraries,
		define_macros=defines,
		extra_compile_args=extra_compile_args
		)
	extensions.append(gipsyExtension)
	
	
if __name__ == "__main__":
	setup(name=name,
		packages=["kapu"],
		version=version,
		description=description,
		author=author,
		author_email=author_email,
		url=url,
		ext_modules=extensions,
		data_files=data_files
		)
	