"""Performs projections using the WCSLIB library.

I as not totally sure i get the whole WCSLIB library, so you might want to
test your results with another program like ds9 (though i found a bug in
it's skysystem transformations).

The simpelest way to use this class is to generate if from a FITS file.

proj = fromFits("m81.fits")
x, y = proj.forward(10, 20)


"""
from kapu._wcslib import Wcs
from numpy import *

def fromFitsFile(filename):
	from fits import FITS
	fits = FITS(filename)
	header = fits.headers
	return fromDict(header)

def fromDict(header, fixcd=False):
	# TODO: fixcd should not be an argument, it should be done automagicly,
	# just recontruct the cdmatrix from CROTA2(2?) and CDELTi
	#header = fits.headers
	ctype = [header["CTYPE1"], header["CTYPE2"]]
	projectiontype1 = ctype[0].split("-")[-1].replace("'", "")
	projectiontype2 = ctype[1].split("-")[-1].replace("'", "")
	#print "projection type found", projectiontype1
	altlin = 0
	if projectiontype1 != projectiontype2:
		raise Exception, "mixed projection type"
	else:
		projectiontype = projectiontype1
	crval = [float(header["CRVAL1"]), float(header["CRVAL2"])]
	if header.has_key("PC001001"):
		altlin |= 1
		pcmatrix = [	float(header["PC001001"]),
				float(header["PC001002"]),
				float(header["PC002001"]),
				float(header["PC002002"])]
	elif header.has_key("PC1_1"):
		altlin |= 1
		pcmatrix = [	float(header["PC1_1"]),
				float(header["PC1_2"]),
				float(header["PC2_1"]),
				float(header["PC2_2"])]
	else:
		#raise Exception, "unable to find pc matrix"
		pcmatrix = [1.0, 0.0, 0.0, 1.0]

	if header.has_key("CD001001"):
		altlin |= 2
		cdmatrix = [	float(header["CD001001"]),
				float(header["CD001002"]),
				float(header["CD002001"]),
				float(header["CD002002"])]
	elif header.has_key("CD1_1"):
		altlin |= 2
		cdmatrix = [	float(header["CD1_1"]),
				float(header["CD1_2"]),
				float(header["CD2_1"]),
				float(header["CD2_2"])]
	else:
		#raise Exce	ption, "unable to find cd matrix"
		cdmatrix = [1.0, 0.0, 0.0, 1.0]
	cdelt = [float(header["CDELT1"]), float(header["CDELT2"])]
	crpix = [float(header["CRPIX1"]), float(header["CRPIX2"])]
	if "CROTA1" in header or "CROTA2" in header and not altlin&2:
		altlin |= 4;
		crota = [float(header.get("CROTA1", 0)), float(header.get("CROTA2", 0))]
	else:
		crota = [0.0, 0.0]

	if fixcd:
		#kapu.debug("WARNING: had to fix the cd matrix")
		cdmatrix = [cdmatrix[0] * cdelt[0], cdmatrix[1] * cdelt[1], cdmatrix[2] * cdelt[0], cdmatrix[3] * cdelt[1]]

	return Wcs(crval, ctype, pcmatrix, cdelt, crpix, crota, cdmatrix, altlin)
