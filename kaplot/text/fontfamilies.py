['/usr/X11R6/lib/X11/fonts/TTF', '/usr/X11R6/lib/X11/fonts/Type1', '/usr/share/fonts/culmus', '/usr/share/fonts/liberation', '/usr/share/fonts/dejavu', '/usr/share/fonts/default', '/usr/share/fonts/wqy-zenhei', '/usr/share/fonts/stix', '/usr/share/fonts/opensymbol', '/usr/share/fonts/google-crosextra-caladea', '/usr/share/fonts/abattis-cantarell', '/usr/share/fonts/google-crosextra-carlito', '/usr/share/fonts/lohit-gujarati', '/usr/share/fonts/lohit-bengali', '/usr/share/fonts/khmeros', '/usr/share/fonts/lohit-devanagari', '/usr/share/fonts/paratype-pt-sans', '/usr/share/fonts/thai-scalable', '/usr/share/fonts/paktype-naskh-basic', '/usr/share/fonts/lohit-assamese', '/usr/share/fonts/lklug', '/usr/share/fonts/lohit-nepali', '/usr/share/fonts/lohit-kannada', '/usr/share/fonts/nhn-nanum', '/usr/share/fonts/sil-abyssinica', '/usr/share/fonts/sil-nuosu', '/usr/share/fonts/cjkuni-uming', '/usr/share/fonts/lohit-tamil', '/usr/share/fonts/overpass', '/usr/share/fonts/smc', '/usr/share/fonts/vlgothic', '/usr/share/fonts/lohit-marathi', '/usr/share/fonts/lohit-telugu', '/usr/share/fonts/wqy-microhei', '/usr/share/fonts/lohit-malayalam', '/usr/share/fonts/gnu-free', '/usr/share/fonts/lohit-punjabi', '/usr/share/fonts/open-sans', '/usr/share/fonts/madan', '/usr/share/fonts/lohit-oriya', '/usr/share/fonts/ucs-miscfixed', '/usr/share/fonts/jomolhari', '/usr/share/fonts/sil-padauk', '/usr/share/fonts/msttcore', '/usr/share/fonts/default/Type1', '/usr/share/fonts/default/ghostscript']
from kaplot.text.fonts import fontFamilies, FontFamily, \
     serif, sans_serif, monospace, cursive, fantasy, symbols, other, generics

import kaplot
kaplot.searchforfonts = False

fontFamilies['Lohit Devanagari'] = FontFamily(name='Lohit Devanagari', genericFontFamily=sans_serif, regular='/usr/share/fonts/lohit-devanagari/Lohit-Devanagari.ttf', bold='/usr/share/fonts/lohit-devanagari/Lohit-Devanagari.ttf', italic='/usr/share/fonts/lohit-devanagari/Lohit-Devanagari.ttf', bolditalic='/usr/share/fonts/lohit-devanagari/Lohit-Devanagari.ttf')
fontFamilies['Miriam Mono CLM'] = FontFamily(name='Miriam Mono CLM', genericFontFamily=sans_serif, regular='/usr/share/fonts/culmus/MiriamMonoCLM-Book.ttf', bold='/usr/share/fonts/culmus/MiriamMonoCLM-Bold.ttf', italic='/usr/share/fonts/culmus/MiriamMonoCLM-BookOblique.ttf', bolditalic='/usr/share/fonts/culmus/MiriamMonoCLM-BoldOblique.ttf')
fontFamilies['FreeMono'] = FontFamily(name='FreeMono', genericFontFamily=sans_serif, regular='/usr/share/fonts/gnu-free/FreeMono.ttf', bold='/usr/share/fonts/gnu-free/FreeMonoBold.ttf', italic='/usr/share/fonts/gnu-free/FreeMonoOblique.ttf', bolditalic='/usr/share/fonts/gnu-free/FreeMonoBoldOblique.ttf')
fontFamilies['Arial'] = FontFamily(name='Arial', genericFontFamily=sans_serif, regular='/usr/share/fonts/msttcore/arial.ttf', bold='/usr/share/fonts/msttcore/arialbd.ttf', italic='/usr/share/fonts/msttcore/ariali.ttf', bolditalic='/usr/share/fonts/msttcore/arialbi.ttf')
fontFamilies['Stam Sefarad CLM'] = FontFamily(name='Stam Sefarad CLM', genericFontFamily=sans_serif, regular='/usr/share/fonts/culmus/StamSefaradCLM.ttf', bold='/usr/share/fonts/culmus/StamSefaradCLM.ttf', italic='/usr/share/fonts/culmus/StamSefaradCLM.ttf', bolditalic='/usr/share/fonts/culmus/StamSefaradCLM.ttf')
fontFamilies['Trebuchet MS'] = FontFamily(name='Trebuchet MS', genericFontFamily=sans_serif, regular='/usr/share/fonts/msttcore/trebuc.ttf', bold='/usr/share/fonts/msttcore/trebucbd.ttf', italic='/usr/share/fonts/msttcore/trebucit.ttf', bolditalic='/usr/share/fonts/msttcore/trebucbi.ttf')
fontFamilies['PT Sans Narrow'] = FontFamily(name='PT Sans Narrow', genericFontFamily=sans_serif, regular='/usr/share/fonts/paratype-pt-sans/PTN57F.ttf', bold='/usr/share/fonts/paratype-pt-sans/PTN77F.ttf', italic='/usr/share/fonts/paratype-pt-sans/PTN57F.ttf', bolditalic='/usr/share/fonts/paratype-pt-sans/PTN57F.ttf')
fontFamilies['Courier New'] = FontFamily(name='Courier New', genericFontFamily=monospace, regular='/usr/share/fonts/msttcore/cour.ttf', bold='/usr/share/fonts/msttcore/courbd.ttf', italic='/usr/share/fonts/msttcore/couri.ttf', bolditalic='/usr/share/fonts/msttcore/courbi.ttf')
fontFamilies['Georgia'] = FontFamily(name='Georgia', genericFontFamily=serif, regular='/usr/share/fonts/msttcore/georgia.ttf', bold='/usr/share/fonts/msttcore/georgiab.ttf', italic='/usr/share/fonts/msttcore/georgiai.ttf', bolditalic='/usr/share/fonts/msttcore/georgiaz.ttf')
fontFamilies['DejaVu Sans Mono'] = FontFamily(name='DejaVu Sans Mono', genericFontFamily=sans_serif, regular='/usr/share/fonts/dejavu/DejaVuSansMono.ttf', bold='/usr/share/fonts/dejavu/DejaVuSansMono-Bold.ttf', italic='/usr/share/fonts/dejavu/DejaVuSansMono-Oblique.ttf', bolditalic='/usr/share/fonts/dejavu/DejaVuSansMono-BoldOblique.ttf')
fontFamilies['Liberation Serif'] = FontFamily(name='Liberation Serif', genericFontFamily=sans_serif, regular='/usr/share/fonts/liberation/LiberationSerif-Regular.ttf', bold='/usr/share/fonts/liberation/LiberationSerif-Bold.ttf', italic='/usr/share/fonts/liberation/LiberationSerif-Italic.ttf', bolditalic='/usr/share/fonts/liberation/LiberationSerif-BoldItalic.ttf')
fontFamilies['Verdana'] = FontFamily(name='Verdana', genericFontFamily=sans_serif, regular='/usr/share/fonts/msttcore/verdana.ttf', bold='/usr/share/fonts/msttcore/verdanab.ttf', italic='/usr/share/fonts/msttcore/verdanai.ttf', bolditalic='/usr/share/fonts/msttcore/verdanaz.ttf')
fontFamilies['Frank Ruehl CLM'] = FontFamily(name='Frank Ruehl CLM', genericFontFamily=sans_serif, regular='/usr/share/fonts/culmus/FrankRuehlCLM-Medium.ttf', bold='/usr/share/fonts/culmus/FrankRuehlCLM-Bold.ttf', italic='/usr/share/fonts/culmus/FrankRuehlCLM-MediumOblique.ttf', bolditalic='/usr/share/fonts/culmus/FrankRuehlCLM-BoldOblique.ttf')
fontFamilies['Caladea'] = FontFamily(name='Caladea', genericFontFamily=sans_serif, regular='/usr/share/fonts/google-crosextra-caladea/Caladea-Regular.ttf', bold='/usr/share/fonts/google-crosextra-caladea/Caladea-Bold.ttf', italic='/usr/share/fonts/google-crosextra-caladea/Caladea-Italic.ttf', bolditalic='/usr/share/fonts/google-crosextra-caladea/Caladea-BoldItalic.ttf')
fontFamilies['Nuosu SIL'] = FontFamily(name='Nuosu SIL', genericFontFamily=sans_serif, regular='/usr/share/fonts/sil-nuosu/NuosuSIL.ttf', bold='/usr/share/fonts/sil-nuosu/NuosuSIL.ttf', italic='/usr/share/fonts/sil-nuosu/NuosuSIL.ttf', bolditalic='/usr/share/fonts/sil-nuosu/NuosuSIL.ttf')
fontFamilies['Lohit Bengali'] = FontFamily(name='Lohit Bengali', genericFontFamily=sans_serif, regular='/usr/share/fonts/lohit-bengali/Lohit-Bengali.ttf', bold='/usr/share/fonts/lohit-bengali/Lohit-Bengali.ttf', italic='/usr/share/fonts/lohit-bengali/Lohit-Bengali.ttf', bolditalic='/usr/share/fonts/lohit-bengali/Lohit-Bengali.ttf')
fontFamilies['Dingbats'] = FontFamily(name='Dingbats', genericFontFamily=symbols, regular='/usr/share/fonts/default/Type1/d050000l.pfb', bold='/usr/share/fonts/default/Type1/d050000l.pfb', italic='/usr/share/fonts/default/Type1/d050000l.pfb', bolditalic='/usr/share/fonts/default/Type1/d050000l.pfb')
fontFamilies['Liberation Sans'] = FontFamily(name='Liberation Sans', genericFontFamily=sans_serif, regular='/usr/share/fonts/liberation/LiberationSans-Regular.ttf', bold='/usr/share/fonts/liberation/LiberationSans-Bold.ttf', italic='/usr/share/fonts/liberation/LiberationSans-Italic.ttf', bolditalic='/usr/share/fonts/liberation/LiberationSans-BoldItalic.ttf')
fontFamilies['URW Bookman L'] = FontFamily(name='URW Bookman L', genericFontFamily=serif, regular='/usr/share/fonts/default/Type1/b018012l.pfb', bold='/usr/share/fonts/default/Type1/b018015l.pfb', italic='/usr/share/fonts/default/Type1/b018032l.pfb', bolditalic='/usr/share/fonts/default/Type1/b018035l.pfb')
fontFamilies['Waree'] = FontFamily(name='Waree', genericFontFamily=sans_serif, regular='/usr/share/fonts/thai-scalable/Waree.ttf', bold='/usr/share/fonts/thai-scalable/Waree-Bold.ttf', italic='/usr/share/fonts/thai-scalable/Waree-Oblique.ttf', bolditalic='/usr/share/fonts/thai-scalable/Waree-BoldOblique.ttf')
fontFamilies['NanumGothic'] = FontFamily(name='NanumGothic', genericFontFamily=sans_serif, regular='/usr/share/fonts/nhn-nanum/NanumGothicExtraBold.ttf', bold='/usr/share/fonts/nhn-nanum/NanumGothicBold.ttf', italic='/usr/share/fonts/nhn-nanum/NanumGothicExtraBold.ttf', bolditalic='/usr/share/fonts/nhn-nanum/NanumGothicExtraBold.ttf')
fontFamilies['URW Palladio L'] = FontFamily(name='URW Palladio L', genericFontFamily=serif, regular='/usr/share/fonts/default/Type1/p052003l.pfb', bold='/usr/share/fonts/default/Type1/p052004l.pfb', italic='/usr/share/fonts/default/Type1/p052023l.pfb', bolditalic='/usr/share/fonts/default/Type1/p052024l.pfb')
fontFamilies['PakType Naskh Basic'] = FontFamily(name='PakType Naskh Basic', genericFontFamily=sans_serif, regular='/usr/share/fonts/paktype-naskh-basic/PakTypeNaskhBasic.ttf', bold='/usr/share/fonts/paktype-naskh-basic/PakTypeNaskhBasic.ttf', italic='/usr/share/fonts/paktype-naskh-basic/PakTypeNaskhBasic.ttf', bolditalic='/usr/share/fonts/paktype-naskh-basic/PakTypeNaskhBasic.ttf')
fontFamilies['VL Gothic'] = FontFamily(name='VL Gothic', genericFontFamily=sans_serif, regular='/usr/share/fonts/vlgothic/VL-Gothic-Regular.ttf', bold='/usr/share/fonts/vlgothic/VL-Gothic-Regular.ttf', italic='/usr/share/fonts/vlgothic/VL-Gothic-Regular.ttf', bolditalic='/usr/share/fonts/vlgothic/VL-Gothic-Regular.ttf')
fontFamilies['Hadasim CLM'] = FontFamily(name='Hadasim CLM', genericFontFamily=sans_serif, regular='/usr/share/fonts/culmus/HadasimCLM-Regular.ttf', bold='/usr/share/fonts/culmus/HadasimCLM-Bold.ttf', italic='/usr/share/fonts/culmus/HadasimCLM-RegularOblique.ttf', bolditalic='/usr/share/fonts/culmus/HadasimCLM-BoldOblique.ttf')
fontFamilies['Lohit Marathi'] = FontFamily(name='Lohit Marathi', genericFontFamily=sans_serif, regular='/usr/share/fonts/lohit-marathi/Lohit-Marathi.ttf', bold='/usr/share/fonts/lohit-marathi/Lohit-Marathi.ttf', italic='/usr/share/fonts/lohit-marathi/Lohit-Marathi.ttf', bolditalic='/usr/share/fonts/lohit-marathi/Lohit-Marathi.ttf')
fontFamilies['Lohit Oriya'] = FontFamily(name='Lohit Oriya', genericFontFamily=sans_serif, regular='/usr/share/fonts/lohit-oriya/Lohit-Oriya.ttf', bold='/usr/share/fonts/lohit-oriya/Lohit-Oriya.ttf', italic='/usr/share/fonts/lohit-oriya/Lohit-Oriya.ttf', bolditalic='/usr/share/fonts/lohit-oriya/Lohit-Oriya.ttf')
fontFamilies['Stam Ashkenaz CLM'] = FontFamily(name='Stam Ashkenaz CLM', genericFontFamily=sans_serif, regular='/usr/share/fonts/culmus/StamAshkenazCLM.ttf', bold='/usr/share/fonts/culmus/StamAshkenazCLM.ttf', italic='/usr/share/fonts/culmus/StamAshkenazCLM.ttf', bolditalic='/usr/share/fonts/culmus/StamAshkenazCLM.ttf')
fontFamilies['Open Sans'] = FontFamily(name='Open Sans', genericFontFamily=sans_serif, regular='/usr/share/fonts/open-sans/OpenSans-Semibold.ttf', bold='/usr/share/fonts/open-sans/OpenSans-Bold.ttf', italic='/usr/share/fonts/open-sans/OpenSans-SemiboldItalic.ttf', bolditalic='/usr/share/fonts/open-sans/OpenSans-BoldItalic.ttf')
fontFamilies['Webdings'] = FontFamily(name='Webdings', genericFontFamily=symbols, regular='/usr/share/fonts/msttcore/webdings.ttf', bold='/usr/share/fonts/msttcore/webdings.ttf', italic='/usr/share/fonts/msttcore/webdings.ttf', bolditalic='/usr/share/fonts/msttcore/webdings.ttf')
fontFamilies['Liberation Mono'] = FontFamily(name='Liberation Mono', genericFontFamily=sans_serif, regular='/usr/share/fonts/liberation/LiberationMono-Regular.ttf', bold='/usr/share/fonts/liberation/LiberationMono-Bold.ttf', italic='/usr/share/fonts/liberation/LiberationMono-Italic.ttf', bolditalic='/usr/share/fonts/liberation/LiberationMono-BoldItalic.ttf')
fontFamilies['Times New Roman'] = FontFamily(name='Times New Roman', genericFontFamily=serif, regular='/usr/share/fonts/msttcore/times.ttf', bold='/usr/share/fonts/msttcore/timesbd.ttf', italic='/usr/share/fonts/msttcore/timesi.ttf', bolditalic='/usr/share/fonts/msttcore/timesbi.ttf')
fontFamilies['Meera'] = FontFamily(name='Meera', genericFontFamily=sans_serif, regular='/usr/share/fonts/smc/Meera.ttf', bold='/usr/share/fonts/smc/Meera.ttf', italic='/usr/share/fonts/smc/Meera.ttf', bolditalic='/usr/share/fonts/smc/Meera.ttf')
fontFamilies['Lohit Punjabi'] = FontFamily(name='Lohit Punjabi', genericFontFamily=sans_serif, regular='/usr/share/fonts/lohit-punjabi/Lohit-Punjabi.ttf', bold='/usr/share/fonts/lohit-punjabi/Lohit-Punjabi.ttf', italic='/usr/share/fonts/lohit-punjabi/Lohit-Punjabi.ttf', bolditalic='/usr/share/fonts/lohit-punjabi/Lohit-Punjabi.ttf')
fontFamilies['Khmer OS System'] = FontFamily(name='Khmer OS System', genericFontFamily=sans_serif, regular='/usr/share/fonts/khmeros/KhmerOS_sys.ttf', bold='/usr/share/fonts/khmeros/KhmerOS_sys.ttf', italic='/usr/share/fonts/khmeros/KhmerOS_sys.ttf', bolditalic='/usr/share/fonts/khmeros/KhmerOS_sys.ttf')
fontFamilies['Nimbus Sans L'] = FontFamily(name='Nimbus Sans L', genericFontFamily=sans_serif, regular='/usr/share/fonts/default/Type1/n019043l.pfb', bold='/usr/share/fonts/default/Type1/n019044l.pfb', italic='/usr/share/fonts/default/Type1/n019063l.pfb', bolditalic='/usr/share/fonts/default/Type1/n019064l.pfb')
fontFamilies['Madan2'] = FontFamily(name='Madan2', genericFontFamily=sans_serif, regular='/usr/share/fonts/madan/madan.ttf', bold='/usr/share/fonts/madan/madan.ttf', italic='/usr/share/fonts/madan/madan.ttf', bolditalic='/usr/share/fonts/madan/madan.ttf')
fontFamilies['Nimbus Mono L'] = FontFamily(name='Nimbus Mono L', genericFontFamily=monospace, regular='/usr/share/fonts/default/Type1/n022003l.pfb', bold='/usr/share/fonts/default/Type1/n022004l.pfb', italic='/usr/share/fonts/default/Type1/n022023l.pfb', bolditalic='/usr/share/fonts/default/Type1/n022024l.pfb')
fontFamilies['Miriam CLM'] = FontFamily(name='Miriam CLM', genericFontFamily=sans_serif, regular='/usr/share/fonts/culmus/MiriamCLM-Book.ttf', bold='/usr/share/fonts/culmus/MiriamCLM-Bold.ttf', italic='/usr/share/fonts/culmus/MiriamCLM-Book.ttf', bolditalic='/usr/share/fonts/culmus/MiriamCLM-Book.ttf')
fontFamilies['Simple CLM'] = FontFamily(name='Simple CLM', genericFontFamily=sans_serif, regular='/usr/share/fonts/culmus/SimpleCLM-Medium.ttf', bold='/usr/share/fonts/culmus/SimpleCLM-Bold.ttf', italic='/usr/share/fonts/culmus/SimpleCLM-MediumOblique.ttf', bolditalic='/usr/share/fonts/culmus/SimpleCLM-BoldOblique.ttf')
fontFamilies['Impact'] = FontFamily(name='Impact', genericFontFamily=fantasy, regular='/usr/share/fonts/msttcore/impact.ttf', bold='/usr/share/fonts/msttcore/impact.ttf', italic='/usr/share/fonts/msttcore/impact.ttf', bolditalic='/usr/share/fonts/msttcore/impact.ttf')
fontFamilies['Khmer OS'] = FontFamily(name='Khmer OS', genericFontFamily=sans_serif, regular='/usr/share/fonts/khmeros/KhmerOS.ttf', bold='/usr/share/fonts/khmeros/KhmerOS.ttf', italic='/usr/share/fonts/khmeros/KhmerOS.ttf', bolditalic='/usr/share/fonts/khmeros/KhmerOS.ttf')
fontFamilies['FreeSerif'] = FontFamily(name='FreeSerif', genericFontFamily=sans_serif, regular='/usr/share/fonts/gnu-free/FreeSerif.ttf', bold='/usr/share/fonts/gnu-free/FreeSerifBold.ttf', italic='/usr/share/fonts/gnu-free/FreeSerifItalic.ttf', bolditalic='/usr/share/fonts/gnu-free/FreeSerifBoldItalic.ttf')
fontFamilies['PT Sans'] = FontFamily(name='PT Sans', genericFontFamily=sans_serif, regular='/usr/share/fonts/paratype-pt-sans/PTS55F.ttf', bold='/usr/share/fonts/paratype-pt-sans/PTS75F.ttf', italic='/usr/share/fonts/paratype-pt-sans/PTS56F.ttf', bolditalic='/usr/share/fonts/paratype-pt-sans/PTS76F.ttf')
fontFamilies['Lohit Kannada'] = FontFamily(name='Lohit Kannada', genericFontFamily=sans_serif, regular='/usr/share/fonts/lohit-kannada/Lohit-Kannada.ttf', bold='/usr/share/fonts/lohit-kannada/Lohit-Kannada.ttf', italic='/usr/share/fonts/lohit-kannada/Lohit-Kannada.ttf', bolditalic='/usr/share/fonts/lohit-kannada/Lohit-Kannada.ttf')
fontFamilies['Khmer OS Content'] = FontFamily(name='Khmer OS Content', genericFontFamily=sans_serif, regular='/usr/share/fonts/khmeros/KhmerOS_content.ttf', bold='/usr/share/fonts/khmeros/KhmerOS_content.ttf', italic='/usr/share/fonts/khmeros/KhmerOS_content.ttf', bolditalic='/usr/share/fonts/khmeros/KhmerOS_content.ttf')
fontFamilies['DejaVu Sans'] = FontFamily(name='DejaVu Sans', genericFontFamily=sans_serif, regular='/usr/share/fonts/dejavu/DejaVuSansCondensed.ttf', bold='/usr/share/fonts/dejavu/DejaVuSansCondensed-Bold.ttf', italic='/usr/share/fonts/dejavu/DejaVuSansCondensed-Oblique.ttf', bolditalic='/usr/share/fonts/dejavu/DejaVuSansCondensed-BoldOblique.ttf')
fontFamilies['LKLUG'] = FontFamily(name='LKLUG', genericFontFamily=sans_serif, regular='/usr/share/fonts/lklug/lklug.ttf', bold='/usr/share/fonts/lklug/lklug.ttf', italic='/usr/share/fonts/lklug/lklug.ttf', bolditalic='/usr/share/fonts/lklug/lklug.ttf')
fontFamilies['Lohit Nepali'] = FontFamily(name='Lohit Nepali', genericFontFamily=sans_serif, regular='/usr/share/fonts/lohit-nepali/Lohit-Nepali.ttf', bold='/usr/share/fonts/lohit-nepali/Lohit-Nepali.ttf', italic='/usr/share/fonts/lohit-nepali/Lohit-Nepali.ttf', bolditalic='/usr/share/fonts/lohit-nepali/Lohit-Nepali.ttf')
fontFamilies['URW Gothic L'] = FontFamily(name='URW Gothic L', genericFontFamily=sans_serif, regular='/usr/share/fonts/default/Type1/a010015l.pfb', bold='/usr/share/fonts/default/Type1/a010015l.pfb', italic='/usr/share/fonts/default/Type1/a010035l.pfb', bolditalic='/usr/share/fonts/default/Type1/a010015l.pfb')
fontFamilies['Arial Black'] = FontFamily(name='Arial Black', genericFontFamily=sans_serif, regular='/usr/share/fonts/msttcore/ariblk.ttf', bold='/usr/share/fonts/msttcore/ariblk.ttf', italic='/usr/share/fonts/msttcore/ariblk.ttf', bolditalic='/usr/share/fonts/msttcore/ariblk.ttf')
fontFamilies['Comic Sans MS'] = FontFamily(name='Comic Sans MS', genericFontFamily=cursive, regular='/usr/share/fonts/msttcore/comic.ttf', bold='/usr/share/fonts/msttcore/comicbd.ttf', italic='/usr/share/fonts/msttcore/comic.ttf', bolditalic='/usr/share/fonts/msttcore/comic.ttf')
fontFamilies['Lohit Malayalam'] = FontFamily(name='Lohit Malayalam', genericFontFamily=sans_serif, regular='/usr/share/fonts/lohit-malayalam/Lohit-Malayalam.ttf', bold='/usr/share/fonts/lohit-malayalam/Lohit-Malayalam.ttf', italic='/usr/share/fonts/lohit-malayalam/Lohit-Malayalam.ttf', bolditalic='/usr/share/fonts/lohit-malayalam/Lohit-Malayalam.ttf')
fontFamilies['Lohit Gujarati'] = FontFamily(name='Lohit Gujarati', genericFontFamily=sans_serif, regular='/usr/share/fonts/lohit-gujarati/Lohit-Gujarati.ttf', bold='/usr/share/fonts/lohit-gujarati/Lohit-Gujarati.ttf', italic='/usr/share/fonts/lohit-gujarati/Lohit-Gujarati.ttf', bolditalic='/usr/share/fonts/lohit-gujarati/Lohit-Gujarati.ttf')
fontFamilies['Abyssinica SIL'] = FontFamily(name='Abyssinica SIL', genericFontFamily=sans_serif, regular='/usr/share/fonts/sil-abyssinica/AbyssinicaSIL-R.ttf', bold='/usr/share/fonts/sil-abyssinica/AbyssinicaSIL-R.ttf', italic='/usr/share/fonts/sil-abyssinica/AbyssinicaSIL-R.ttf', bolditalic='/usr/share/fonts/sil-abyssinica/AbyssinicaSIL-R.ttf')
fontFamilies['Overpass'] = FontFamily(name='Overpass', genericFontFamily=sans_serif, regular='/usr/share/fonts/overpass/Overpass_Regular.ttf', bold='/usr/share/fonts/overpass/Overpass_Bold.ttf', italic='/usr/share/fonts/overpass/Overpass_Regular.ttf', bolditalic='/usr/share/fonts/overpass/Overpass_Regular.ttf')
fontFamilies['Padauk'] = FontFamily(name='Padauk', genericFontFamily=sans_serif, regular='/usr/share/fonts/sil-padauk/Padauk.ttf', bold='/usr/share/fonts/sil-padauk/Padauk-bold.ttf', italic='/usr/share/fonts/sil-padauk/Padauk.ttf', bolditalic='/usr/share/fonts/sil-padauk/Padauk.ttf')
fontFamilies['Nimbus Roman No9 L'] = FontFamily(name='Nimbus Roman No9 L', genericFontFamily=serif, regular='/usr/share/fonts/default/Type1/n021003l.pfb', bold='/usr/share/fonts/default/Type1/n021004l.pfb', italic='/usr/share/fonts/default/Type1/n021023l.pfb', bolditalic='/usr/share/fonts/default/Type1/n021024l.pfb')
fontFamilies['Standard Symbols L'] = FontFamily(name='Standard Symbols L', genericFontFamily=symbols, regular='/usr/share/fonts/default/Type1/s050000l.pfb', bold='/usr/share/fonts/default/Type1/s050000l.pfb', italic='/usr/share/fonts/default/Type1/s050000l.pfb', bolditalic='/usr/share/fonts/default/Type1/s050000l.pfb')
fontFamilies['Jomolhari'] = FontFamily(name='Jomolhari', genericFontFamily=sans_serif, regular='/usr/share/fonts/jomolhari/Jomolhari-alpha3c-0605331.ttf', bold='/usr/share/fonts/jomolhari/Jomolhari-alpha3c-0605331.ttf', italic='/usr/share/fonts/jomolhari/Jomolhari-alpha3c-0605331.ttf', bolditalic='/usr/share/fonts/jomolhari/Jomolhari-alpha3c-0605331.ttf')
fontFamilies['FreeSans'] = FontFamily(name='FreeSans', genericFontFamily=sans_serif, regular='/usr/share/fonts/gnu-free/FreeSans.ttf', bold='/usr/share/fonts/gnu-free/FreeSansBold.ttf', italic='/usr/share/fonts/gnu-free/FreeSansOblique.ttf', bolditalic='/usr/share/fonts/gnu-free/FreeSansBoldOblique.ttf')
fontFamilies['OpenSymbol'] = FontFamily(name='OpenSymbol', genericFontFamily=sans_serif, regular='/usr/share/fonts/opensymbol/opens___.ttf', bold='/usr/share/fonts/opensymbol/opens___.ttf', italic='/usr/share/fonts/opensymbol/opens___.ttf', bolditalic='/usr/share/fonts/opensymbol/opens___.ttf')
fontFamilies['Tahoma'] = FontFamily(name='Tahoma', genericFontFamily=sans_serif, regular='/usr/share/fonts/msttcore/tahoma.ttf', bold='/usr/share/fonts/msttcore/tahoma.ttf', italic='/usr/share/fonts/msttcore/tahoma.ttf', bolditalic='/usr/share/fonts/msttcore/tahoma.ttf')
fontFamilies['David CLM'] = FontFamily(name='David CLM', genericFontFamily=sans_serif, regular='/usr/share/fonts/culmus/DavidCLM-Medium.ttf', bold='/usr/share/fonts/culmus/DavidCLM-Bold.ttf', italic='/usr/share/fonts/culmus/DavidCLM-MediumItalic.ttf', bolditalic='/usr/share/fonts/culmus/DavidCLM-BoldItalic.ttf')
fontFamilies['Carlito'] = FontFamily(name='Carlito', genericFontFamily=sans_serif, regular='/usr/share/fonts/google-crosextra-carlito/Carlito-Regular.ttf', bold='/usr/share/fonts/google-crosextra-carlito/Carlito-Bold.ttf', italic='/usr/share/fonts/google-crosextra-carlito/Carlito-Italic.ttf', bolditalic='/usr/share/fonts/google-crosextra-carlito/Carlito-BoldItalic.ttf')
fontFamilies['DejaVu Serif'] = FontFamily(name='DejaVu Serif', genericFontFamily=sans_serif, regular='/usr/share/fonts/dejavu/DejaVuSerifCondensed.ttf', bold='/usr/share/fonts/dejavu/DejaVuSerifCondensed-Bold.ttf', italic='/usr/share/fonts/dejavu/DejaVuSerifCondensed-Italic.ttf', bolditalic='/usr/share/fonts/dejavu/DejaVuSerifCondensed-BoldItalic.ttf')
fontFamilies['Andale Mono'] = FontFamily(name='Andale Mono', genericFontFamily=monospace, regular='/usr/share/fonts/msttcore/andalemo.ttf', bold='/usr/share/fonts/msttcore/andalemo.ttf', italic='/usr/share/fonts/msttcore/andalemo.ttf', bolditalic='/usr/share/fonts/msttcore/andalemo.ttf')
fontFamilies['Lohit Tamil'] = FontFamily(name='Lohit Tamil', genericFontFamily=sans_serif, regular='/usr/share/fonts/lohit-tamil/Lohit-Tamil.ttf', bold='/usr/share/fonts/lohit-tamil/Lohit-Tamil.ttf', italic='/usr/share/fonts/lohit-tamil/Lohit-Tamil.ttf', bolditalic='/usr/share/fonts/lohit-tamil/Lohit-Tamil.ttf')
fontFamilies['Lohit Assamese'] = FontFamily(name='Lohit Assamese', genericFontFamily=sans_serif, regular='/usr/share/fonts/lohit-assamese/Lohit-Assamese.ttf', bold='/usr/share/fonts/lohit-assamese/Lohit-Assamese.ttf', italic='/usr/share/fonts/lohit-assamese/Lohit-Assamese.ttf', bolditalic='/usr/share/fonts/lohit-assamese/Lohit-Assamese.ttf')
fontFamilies['Century Schoolbook L'] = FontFamily(name='Century Schoolbook L', genericFontFamily=serif, regular='/usr/share/fonts/default/Type1/c059013l.pfb', bold='/usr/share/fonts/default/Type1/c059016l.pfb', italic='/usr/share/fonts/default/Type1/c059033l.pfb', bolditalic='/usr/share/fonts/default/Type1/c059036l.pfb')
fontFamilies['URW Chancery L'] = FontFamily(name='URW Chancery L', genericFontFamily=cursive, regular='/usr/share/fonts/default/Type1/z003034l.pfb', bold='/usr/share/fonts/default/Type1/z003034l.pfb', italic='/usr/share/fonts/default/Type1/z003034l.pfb', bolditalic='/usr/share/fonts/default/Type1/z003034l.pfb')
fontFamilies['Lohit Telugu'] = FontFamily(name='Lohit Telugu', genericFontFamily=sans_serif, regular='/usr/share/fonts/lohit-telugu/Lohit-Telugu.ttf', bold='/usr/share/fonts/lohit-telugu/Lohit-Telugu.ttf', italic='/usr/share/fonts/lohit-telugu/Lohit-Telugu.ttf', bolditalic='/usr/share/fonts/lohit-telugu/Lohit-Telugu.ttf')
for generic in generics:
	generic.sort()
