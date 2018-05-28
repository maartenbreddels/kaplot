"""
 * Font specification properties(from CSS2 specs - http://www.w3.org/TR/REC-CSS2/fonts.html)
  * fontfamily
   * a comma seperated list of family or generic family names (TODO: not implemented)
     * 'Verdana, sans-serif, serif'
   * family-names
    * 'Verdana'
    * 'Arial'
    * ..
   * generic-family
    * 'serif'
    * 'sans-serif'
    * 'cursive'
    * 'fantasy'
    * 'monospace'
  * fontstyle
   * 'normal'
   * 'italic'
   * 'bold'
   * 'bold' and 'italic'
  * fontsize
   * absolute size, like '10px', '18pt', '0.5i'
    * or 'xx-small', 'x-small', 'small', 'medium', 'large', 'x-large', 'xx-large'
   * relative size, like '150%'

  * Font variant - not needed
  * Font weight - not needed, use normal or bold
  * Font stretch - is this usefull?

 * Font matching:
  * first, if a generic family, return a default font
  * second, a normal lookup of the family
   * a case sensitive lookup
   * a case insensitive lookup with 'similar' names, if a name is a substring
     of the other, it will match
    * 'verdan' will match 'Verdana'
    *  'MS Verdana' will also match 'Verdana'
  * third, find a font with a similar generic family
  * at last, if nothing found, return a default font
 * fontstyle matching
  * if regular not found, return bold, italic of bold+italic
  * if bold not found return bold+italic, normal or italic
  * if italic not found return bold+italic, normal, bold
  * if bold+italic not found, return bold, italic, normal
 * font size should never be a problem with scalable fonts


"""

import kaplot.cext._pyfont as pyfont
import glob
import os
import sys
import re

import kaplot

fontFamilies = {}

class FontFamily(object):
	def __init__(self, name, genericFontFamily=None, regular=None, bold=None, italic=None, bolditalic=None):
		self.name = name
		self.genericFontFamily = genericFontFamily
		self.regular = regular
		self.bold = bold
		self.italic = italic
		self.bolditalic = bolditalic

		self.regularFont = None
		self.boldFont = None
		self.italicFont = None
		self.bolditalicFont = None
		if self.genericFontFamily is not None:
			self.genericFontFamily.append(self)

	def get(self, bold, italic):
		if bold and italic:
			return self.getBoldItalic()
		elif bold:
			return self.getBold()
		elif italic:
			return self.getItalic()
		else:
			return self.getRegular()

	def getRegular(self):
		if self.regularFont == None:
			self.regularFont = pyfont.Font(self.regular)
		return self.regularFont

	def getBold(self):
		if self.boldFont == None:
			self.boldFont = pyfont.Font(self.bold)
		return self.boldFont

	def getItalic(self):
		if self.italicFont == None:
			self.italicFont = pyfont.Font(self.italic)
		return self.italicFont

	def getBoldItalic(self):
		if self.bolditalicFont == None:
			self.bolditalicFont = pyfont.Font(self.bolditalic)
		return self.bolditalicFont

	def end(self):
		names = ["regular", "bold", "italic", "bolditalic"]
		existing = [getattr(self, name) for name in names if getattr(self, name) != None][0]
		for name in names:
			if getattr(self, name) == None:
				setattr(self, name, existing)

	def __repr__(self):
		famName = self.genericFontFamily.name.replace("-", "_")
		return "FontFamily(name=%r, genericFontFamily=%s, regular=%r, bold=%r, italic=%r, bolditalic=%r)" % \
				(self.name, famName, self.regular, self.bold, self.italic, self.bolditalic)

	def fuzzyMatch(self, fontFamily=None, fontFamilyName=None):
		if fontFamily:
			fontFamilyName = fontFamily.name
		return _fuzzyMatch(self.name, fontFamilyName)


	#def __setattr__(self, name, value):
	#	if name in self.__dict__ and self.__dict__[name] != None:
	#		raise Exception, "FontFamily.%s already set(%s)" % (name, self.name)
	#	self.__dict__[name] = value

class GenericFontFamily(list):
	def __init__(self, name, fontFamilyMemberNames):
		self.name = name
		self.fontFamilyMemberNames = fontFamilyMemberNames

	def memberOf(self, font=None, fontName=None, fuzzyMatch=False):
		if font != None:
			fontName = font.name

		for memberName in self.fontFamilyMemberNames:
			if fuzzyMatch and _fuzzyMatch(memberName, fontName):
				return True
			elif memberName == fontName:
				return True
		return False

	def sort(self):
		ffmn = self.fontFamilyMemberNames
		def cmpfunc(a, b):
			if a.name in ffmn:
				pos1 = ffmn.index(a.name)
			else:
				pos1 = len(ffmn)
			if b.name in ffmn:
				pos2 = ffmn.index(b.name)
			else:
				pos2 = len(ffmn)
			return cmp(pos1, pos2)

		super(GenericFontFamily, self).sort(cmpfunc)

# list taken from http://www.w3.org/Style/Examples/007/fonts.html
# some more are there: (but they prefix with company name, like 'MS Arial')
# http://www.w3.org/TR/REC-CSS2/fonts.html#generic-font-families
serifList = ['Times', 'Times New Roman', 'Palatino', 'Bookman', 'New Century Schoolbook',
		'cmmi10',
		'cmr10', 'Georgia', 'Palatino Linotype', 'Sylfaen',
		'URW Bookman L', 'Century Schoolbook L', 'Nimbus Roman No9 L',
		'NewMilleniumSchlbk', 'URW Palladio L']
sans_serifList = ['Arial', 'Arial Black', 'Helvetica', 'Gill Sans', 'Lucida', 'Helvetica Narrow',
		'Franklin Gothic Medium', 'Lucida Sans Unicode', 'Microsoft Sans Serif', 'Tahoma',
		'Trebuchet MS', 'Verdana', 'URW Gothic L',  'Nimbus Sans L']
monospaceList = ['Andale Mono', 'Courier New', 'Courier', 'Lucidatypewriter', 'Fixed',
	'Lucida Console', 'TeleText', 'TeleTextDH', 'Nimbus Mono L']
cursiveList = ['Comic Sans MS', 'Zapf Chancery', 'Coronetscript', 'Florence', 'Parkavenue', 'URW Chancery L']
fantasyList = ['Impact']
# fonts like TIX, teletext etc
uselessList = ['ATLAS97 Symbol 1', 'TeleTextLineDraw', 'TeleTextLineDrawDH']

mathList = ['cmex10', 'cmsy10']
for i in range(1,8):
	mathList.append("Mathematica%i" % i)
	mathList.append("Mathematica%iMono" % i)

symbolsList = ['ATLAS97 Symbol 1', 'Webdings', 'Wingdings', 'Dingbats',
		'Standard Symbols L', 'Symbol', 'Marlett']
symbolsList.extend(mathList)
otherList = ['Estrangelo Edessa', 'Gautami', 'Latha', 'Mangal', 'MV Boli',
		'Raavi' ,'Tunga', 'Shruti']

serif = GenericFontFamily("serif", serifList)
sans_serif = GenericFontFamily("sans-serif", sans_serifList)
monospace = GenericFontFamily("monospace", monospaceList)
cursive = GenericFontFamily("cursive", cursiveList)
fantasy = GenericFontFamily("fantasy", fantasyList)
symbols = GenericFontFamily("symbols", symbolsList)
other = GenericFontFamily("other", otherList)

generics = [serif, sans_serif, monospace, cursive, fantasy, symbols, other]
genericNames = [k.name for k in generics]


def getFontFilenames(dirnames=[]):
	if sys.platform == "win32":
		windir = os.environ.get("windir")
		if windir:
			dirnames.append(os.path.join(windir, "Fonts"))
	else:
		dirnames.append("/usr/X11R6/lib/X11/fonts/TTF")
		dirnames.append("/usr/X11R6/lib/X11/fonts/Type1")
		shareddir = "/usr/share/fonts"
		def walk(arg, dirname, filenames):
			for filename in list(filenames):
				fullname = os.path.join(dirname, filename)
				if os.path.isdir(fullname):
					arg.append(fullname)

		os.path.walk(shareddir, walk, dirnames)
                os.path.walk("/usr/X11R6/lib/X11/fonts", walk, dirnames)
		print dirnames
	extradirs = os.environ.get("FONT_DIR")
	if extradirs:
		dirnames.append(re.split("[~;~:]", extradirs))

	filenames = []
	for dirname in dirnames:
		filenames.extend(glob.glob(os.path.join(dirname, "*.ttf")))
		filenames.extend(glob.glob(os.path.join(dirname, "*.pfb")))
	return filenames

def findFontFamilies(dirnames=[]):
	filenames = getFontFilenames(dirnames)
	for filename in filenames:
		try:
			font = pyfont.Font(filename)
		except:
			continue
		style = font.style_name
		family = font.family_name

		if family not in uselessList:
			if not font.is_bold and not font.is_italic:
				_getFamily(family).regular = filename
			elif font.is_bold and font.is_italic:
				_getFamily(family).bolditalic = filename
			elif font.is_bold:
				_getFamily(family).bold = filename
			elif font.is_italic:
				_getFamily(family).italic = filename
			genericfamilyfound = False
			for generic in generics:
				if generic.memberOf(fontName=family):
					#generic_families[genericname].append(family)
					_getFamily(family).genericFontFamily = generic
					genericfamilyfound = True
					generic.append(_getFamily(family))
					break
			if not genericfamilyfound:
				kaplot.info("there is no generic family name found for font family %r," \
					" assuming it is a 'sans-serif' font" % family)
				#generic_families['sans-serif'].append(family)
				_getFamily(family).genericFontFamily = sans_serif
				sans_serif.append(_getFamily(family))

	for key, value in fontFamilies.items():
		value.end()

def _getFamily(name):
	if name in fontFamilies:
		return fontFamilies[name]
	else:
		fam = FontFamily(name)
		fontFamilies[name] = fam
		return fam


# list to prevent multiple font info msg'es
_fontmatches = {}

def findDefaultFontFamily():
	for generic in generics:
		if len(generic) > 0:
			fontFamily = generic[0]
			kaplot.debug("default font family %r, font %r will be used" % (generic.name, fontFamily.name), printonce=True)
			return fontFamily
	raise Exception, "no font found"

def _fuzzyMatch(string1, string2):
	return \
		(string1.lower() == string2.lower()) or \
		(string1.lower() in string2.lower()) or \
		(string2.lower() in string1.lower())

def _findFontFamily(fontFamilyName, fuzzy=False):
	for fontFamily in fontFamilies.values():
		if (fuzzy and fontFamily.fuzzyMatch(fontFamilyName)) or \
			(fontFamily.name == fontFamilyName):
			return fontFamily
	return None

def findGenericFontFamily(fontname):
	fontFamily = _findFontFamily(fontname)
	if fontFamily:
		return fontFamily.genericFontFamily
	else:
		return None

def findMatchingFontFamilies(fontname):
	firstGenericFontFamily = findGenericFontFamily(fontname)
	fontnameList = []
	if firstGenericFontFamily:
		kaplot.debug("font %r is part of generic family %r" % (fontname, firstGenericFontFamily.name), printonce=True)
		fontnameList.extend(list(firstGenericFontFamily))
		for generic in generics:
			if generic != firstGenericFontFamily:
				fontnameList.extend(list(generic))
	else:
		for generic in generics:
			fontnameList.extend(list(generic))
	return fontnameList

#def isPresent(fontname):
#	return fontname in fontFamilies

def findFontFamily(fontFamilyName):
	fontFamily = None

	# a case sensitive lookup
	if fontFamilyName in fontFamilies.keys():
		fontFamily = fontFamilies[fontFamilyName]

	# generic searching
	if fontFamily == None:
		for generic in generics:
			if generic.name == fontFamilyName.lower():
				if len(generic) > 0:
					fontFamily = generic[0]
					kaplot.debug("generic font family %r is found, font %r will be used" %\
						(generic.name, fontFamily.name), printonce=True)
				else:
					kaplot.debug("no font present for generic font family %r" % (fontFamilyName.lower()))
				break

	# a case insensitive sensitive lookup with substrings matching
	if fontFamily == None:
		for someFontFamily in fontFamilies.values():
			if someFontFamily.fuzzyMatch(fontFamilyName=fontFamilyName):
				fontFamily = someFontFamily
				kaplot.debug("font family %r not found, but %r matches it name" %\
					(fontFamilyName, fontFamily.name), printonce=True)
				break

	# find a font with a similar generic family
	if fontFamily == None:
		generic = findGenericFontFamily(fontFamilyName)
		if generic:
			# now take the first font in this family that is present
			if len(generic) > 0:
				fontFamily = generic[0]
				kaplot.debug("font family %r not found, but %r is part of the same font family(%r)" % \
						 (fontFamilyName, fontFamily.name, generic.name), printonce=True)

	if fontFamily == None:
		kaplot.debug("can't recognise or find font %r, using a default font" % fontFamilyName, printonce=True)
		fontFamily = findDefaultFontFamily()

	return fontFamily


def findFont(fontname, bold, italic):
	fontFamily = findFontFamily(fontname)
	return fontFamily.get(bold, italic)

if __name__ == "__main__":
	dirnames = sys.argv[1:]
	findFontFamilies(dirnames)
	print "from kaplot.text.fonts import fontFamilies, FontFamily, \\"
	print "     serif, sans_serif, monospace, cursive, fantasy, symbols, other, generics"
	print
	print "import kaplot"
	print "kaplot.searchforfonts = False"
	print
	for key, value in fontFamilies.items():
		print "fontFamilies[%r] = %r" % (key, value)

	print "for generic in generics:"
	print "	generic.sort()"
