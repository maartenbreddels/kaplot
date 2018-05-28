['/usr/X11R6/lib/X11/fonts/TTF', '/usr/X11R6/lib/X11/fonts/Type1', '/usr/share/fonts/kannada', '/usr/share/fonts/arabic', '/usr/share/fonts/hindi', '/usr/share/fonts/telugu', '/usr/share/fonts/KOI8-R', '/usr/share/fonts/oriya', '/usr/share/fonts/default', '/usr/share/fonts/punjabi', '/usr/share/fonts/chinese', '/usr/share/fonts/malayalam', '/usr/share/fonts/bengali', '/usr/share/fonts/ja', '/usr/share/fonts/bitstream-vera', '/usr/share/fonts/hebrew', '/usr/share/fonts/gujarati', '/usr/share/fonts/zh_TW', '/usr/share/fonts/liberation', '/usr/share/fonts/ISO8859-2', '/usr/share/fonts/dejavu-lgc', '/usr/share/fonts/sinhala', '/usr/share/fonts/japanese', '/usr/share/fonts/java', '/usr/share/fonts/bitmap-fonts', '/usr/share/fonts/tamil', '/usr/share/fonts/korean', '/usr/share/fonts/KOI8-R/100dpi', '/usr/share/fonts/KOI8-R/misc', '/usr/share/fonts/KOI8-R/75dpi', '/usr/share/fonts/default/Type1', '/usr/share/fonts/default/ghostscript', '/usr/share/fonts/chinese/TrueType', '/usr/share/fonts/chinese/misc', '/usr/share/fonts/ja/TrueType', '/usr/share/fonts/zh_TW/TrueType', '/usr/share/fonts/ISO8859-2/100dpi', '/usr/share/fonts/ISO8859-2/misc', '/usr/share/fonts/ISO8859-2/75dpi', '/usr/share/fonts/japanese/TrueType', '/usr/share/fonts/japanese/misc', '/usr/share/fonts/korean/TrueType', '/usr/share/fonts/korean/misc']
from kaplot.text.fonts import fontFamilies, FontFamily, \
     serif, sans_serif, monospace, cursive, fantasy, symbols, other, generics

import kaplot
kaplot.searchforfonts = False

fontFamilies['LKLUG'] = FontFamily(name='LKLUG', genericFontFamily=sans_serif, regular='/usr/share/fonts/sinhala/lklug.ttf', bold='/usr/share/fonts/sinhala/lklug.ttf', italic='/usr/share/fonts/sinhala/lklug.ttf', bolditalic='/usr/share/fonts/sinhala/lklug.ttf')
fontFamilies['KacstArt'] = FontFamily(name='KacstArt', genericFontFamily=sans_serif, regular='/usr/share/fonts/arabic/KacstArt.ttf', bold='/usr/share/fonts/arabic/KacstArt.ttf', italic='/usr/share/fonts/arabic/KacstArt.ttf', bolditalic='/usr/share/fonts/arabic/KacstArt.ttf')
fontFamilies['KacstTitle'] = FontFamily(name='KacstTitle', genericFontFamily=sans_serif, regular='/usr/share/fonts/arabic/KacstTitle.ttf', bold='/usr/share/fonts/arabic/KacstTitle.ttf', italic='/usr/share/fonts/arabic/KacstTitle.ttf', bolditalic='/usr/share/fonts/arabic/KacstTitle.ttf')
fontFamilies['Dingbats'] = FontFamily(name='Dingbats', genericFontFamily=symbols, regular='/usr/share/fonts/default/Type1/d050000l.pfb', bold='/usr/share/fonts/default/Type1/d050000l.pfb', italic='/usr/share/fonts/default/Type1/d050000l.pfb', bolditalic='/usr/share/fonts/default/Type1/d050000l.pfb')
fontFamilies['Baekmuk Gulim'] = FontFamily(name='Baekmuk Gulim', genericFontFamily=sans_serif, regular='/usr/share/fonts/korean/TrueType/gulim.ttf', bold='/usr/share/fonts/korean/TrueType/gulim.ttf', italic='/usr/share/fonts/korean/TrueType/gulim.ttf', bolditalic='/usr/share/fonts/korean/TrueType/gulim.ttf')
fontFamilies['Bitstream Vera Sans'] = FontFamily(name='Bitstream Vera Sans', genericFontFamily=sans_serif, regular='/usr/share/fonts/bitstream-vera/Vera.ttf', bold='/usr/share/fonts/bitstream-vera/VeraBd.ttf', italic='/usr/share/fonts/bitstream-vera/VeraIt.ttf', bolditalic='/usr/share/fonts/bitstream-vera/VeraBI.ttf')
fontFamilies['Liberation Serif'] = FontFamily(name='Liberation Serif', genericFontFamily=sans_serif, regular='/usr/share/fonts/liberation/LiberationSerif-Regular.ttf', bold='/usr/share/fonts/liberation/LiberationSerif-Bold.ttf', italic='/usr/share/fonts/liberation/LiberationSerif-Italic.ttf', bolditalic='/usr/share/fonts/liberation/LiberationSerif-BoldItalic.ttf')
fontFamilies['Nimbus Roman No9 L'] = FontFamily(name='Nimbus Roman No9 L', genericFontFamily=serif, regular='/usr/share/fonts/default/Type1/n021003l.pfb', bold='/usr/share/fonts/default/Type1/n021004l.pfb', italic='/usr/share/fonts/default/Type1/n021023l.pfb', bolditalic='/usr/share/fonts/default/Type1/n021024l.pfb')
fontFamilies['KacstDecorative'] = FontFamily(name='KacstDecorative', genericFontFamily=sans_serif, regular='/usr/share/fonts/arabic/KacstDecorative.ttf', bold='/usr/share/fonts/arabic/KacstDecorative.ttf', italic='/usr/share/fonts/arabic/KacstDecorative.ttf', bolditalic='/usr/share/fonts/arabic/KacstDecorative.ttf')
fontFamilies['Lohit Bengali'] = FontFamily(name='Lohit Bengali', genericFontFamily=sans_serif, regular='/usr/share/fonts/bengali/lohit_bn.ttf', bold='/usr/share/fonts/bengali/lohit_bn.ttf', italic='/usr/share/fonts/bengali/lohit_bn.ttf', bolditalic='/usr/share/fonts/bengali/lohit_bn.ttf')
fontFamilies['PakTypeTehreer'] = FontFamily(name='PakTypeTehreer', genericFontFamily=sans_serif, regular='/usr/share/fonts/arabic/PakTypeTehreer.ttf', bold='/usr/share/fonts/arabic/PakTypeTehreer.ttf', italic='/usr/share/fonts/arabic/PakTypeTehreer.ttf', bolditalic='/usr/share/fonts/arabic/PakTypeTehreer.ttf')
fontFamilies['Liberation Sans'] = FontFamily(name='Liberation Sans', genericFontFamily=sans_serif, regular='/usr/share/fonts/liberation/LiberationSans-Regular.ttf', bold='/usr/share/fonts/liberation/LiberationSans-Bold.ttf', italic='/usr/share/fonts/liberation/LiberationSans-Italic.ttf', bolditalic='/usr/share/fonts/liberation/LiberationSans-BoldItalic.ttf')
fontFamilies['URW Bookman L'] = FontFamily(name='URW Bookman L', genericFontFamily=serif, regular='/usr/share/fonts/default/Type1/b018012l.pfb', bold='/usr/share/fonts/default/Type1/b018015l.pfb', italic='/usr/share/fonts/default/Type1/b018032l.pfb', bolditalic='/usr/share/fonts/default/Type1/b018035l.pfb')
fontFamilies['KacstDigital'] = FontFamily(name='KacstDigital', genericFontFamily=sans_serif, regular='/usr/share/fonts/arabic/KacstDigital.ttf', bold='/usr/share/fonts/arabic/KacstDigital.ttf', italic='/usr/share/fonts/arabic/KacstDigital.ttf', bolditalic='/usr/share/fonts/arabic/KacstDigital.ttf')
fontFamilies['URW Chancery L'] = FontFamily(name='URW Chancery L', genericFontFamily=cursive, regular='/usr/share/fonts/default/Type1/z003034l.pfb', bold='/usr/share/fonts/default/Type1/z003034l.pfb', italic='/usr/share/fonts/default/Type1/z003034l.pfb', bolditalic='/usr/share/fonts/default/Type1/z003034l.pfb')
fontFamilies['AR PL ShanHeiSun Uni'] = FontFamily(name='AR PL ShanHeiSun Uni', genericFontFamily=sans_serif, regular='/usr/share/fonts/zh_TW/TrueType/bsmi00lp.ttf', bold='/usr/share/fonts/zh_TW/TrueType/bsmi00lp.ttf', italic='/usr/share/fonts/zh_TW/TrueType/bsmi00lp.ttf', bolditalic='/usr/share/fonts/zh_TW/TrueType/bsmi00lp.ttf')
fontFamilies['KacstBook'] = FontFamily(name='KacstBook', genericFontFamily=sans_serif, regular='/usr/share/fonts/arabic/KacstQura.ttf', bold='/usr/share/fonts/arabic/KacstQura.ttf', italic='/usr/share/fonts/arabic/KacstQura.ttf', bolditalic='/usr/share/fonts/arabic/KacstQura.ttf')
fontFamilies['Baekmuk Batang'] = FontFamily(name='Baekmuk Batang', genericFontFamily=sans_serif, regular='/usr/share/fonts/korean/TrueType/batang.ttf', bold='/usr/share/fonts/korean/TrueType/batang.ttf', italic='/usr/share/fonts/korean/TrueType/batang.ttf', bolditalic='/usr/share/fonts/korean/TrueType/batang.ttf')
fontFamilies['Lohit Oriya'] = FontFamily(name='Lohit Oriya', genericFontFamily=sans_serif, regular='/usr/share/fonts/oriya/lohit_or.ttf', bold='/usr/share/fonts/oriya/lohit_or.ttf', italic='/usr/share/fonts/oriya/lohit_or.ttf', bolditalic='/usr/share/fonts/oriya/lohit_or.ttf')
fontFamilies['Lucida Sans Typewriter'] = FontFamily(name='Lucida Sans Typewriter', genericFontFamily=sans_serif, regular='/usr/share/fonts/java/LucidaTypewriterRegular.ttf', bold='/usr/share/fonts/java/LucidaTypewriterBold.ttf', italic='/usr/share/fonts/java/LucidaTypewriterRegular.ttf', bolditalic='/usr/share/fonts/java/LucidaTypewriterRegular.ttf')
fontFamilies['URW Palladio L'] = FontFamily(name='URW Palladio L', genericFontFamily=serif, regular='/usr/share/fonts/default/Type1/p052003l.pfb', bold='/usr/share/fonts/default/Type1/p052004l.pfb', italic='/usr/share/fonts/default/Type1/p052023l.pfb', bolditalic='/usr/share/fonts/default/Type1/p052024l.pfb')
fontFamilies['Liberation Mono'] = FontFamily(name='Liberation Mono', genericFontFamily=sans_serif, regular='/usr/share/fonts/liberation/LiberationMono-Regular.ttf', bold='/usr/share/fonts/liberation/LiberationMono-Bold.ttf', italic='/usr/share/fonts/liberation/LiberationMono-Italic.ttf', bolditalic='/usr/share/fonts/liberation/LiberationMono-BoldItalic.ttf')
fontFamilies['Lohit Punjabi'] = FontFamily(name='Lohit Punjabi', genericFontFamily=sans_serif, regular='/usr/share/fonts/punjabi/lohit_pa.ttf', bold='/usr/share/fonts/punjabi/lohit_pa.ttf', italic='/usr/share/fonts/punjabi/lohit_pa.ttf', bolditalic='/usr/share/fonts/punjabi/lohit_pa.ttf')
fontFamilies['KacstQuran'] = FontFamily(name='KacstQuran', genericFontFamily=sans_serif, regular='/usr/share/fonts/arabic/KacstQuran.ttf', bold='/usr/share/fonts/arabic/KacstQuran.ttf', italic='/usr/share/fonts/arabic/KacstQuran.ttf', bolditalic='/usr/share/fonts/arabic/KacstQuran.ttf')
fontFamilies['Nimbus Sans L'] = FontFamily(name='Nimbus Sans L', genericFontFamily=sans_serif, regular='/usr/share/fonts/default/Type1/n019003l.pfb', bold='/usr/share/fonts/default/Type1/n019004l.pfb', italic='/usr/share/fonts/default/Type1/n019023l.pfb', bolditalic='/usr/share/fonts/default/Type1/n019024l.pfb')
fontFamilies['AR PL ZenKai Uni'] = FontFamily(name='AR PL ZenKai Uni', genericFontFamily=sans_serif, regular='/usr/share/fonts/chinese/TrueType/ukai.ttf', bold='/usr/share/fonts/chinese/TrueType/ukai.ttf', italic='/usr/share/fonts/chinese/TrueType/ukai.ttf', bolditalic='/usr/share/fonts/chinese/TrueType/ukai.ttf')
fontFamilies['DejaVu LGC Serif'] = FontFamily(name='DejaVu LGC Serif', genericFontFamily=sans_serif, regular='/usr/share/fonts/dejavu-lgc/DejaVuLGCSerif.ttf', bold='/usr/share/fonts/dejavu-lgc/DejaVuLGCSerif-Bold.ttf', italic='/usr/share/fonts/dejavu-lgc/DejaVuLGCSerif-Oblique.ttf', bolditalic='/usr/share/fonts/dejavu-lgc/DejaVuLGCSerif-BoldOblique.ttf')
fontFamilies['Nimbus Mono L'] = FontFamily(name='Nimbus Mono L', genericFontFamily=monospace, regular='/usr/share/fonts/default/Type1/n022003l.pfb', bold='/usr/share/fonts/default/Type1/n022004l.pfb', italic='/usr/share/fonts/default/Type1/n022023l.pfb', bolditalic='/usr/share/fonts/default/Type1/n022024l.pfb')
fontFamilies['KacstPoster'] = FontFamily(name='KacstPoster', genericFontFamily=sans_serif, regular='/usr/share/fonts/arabic/KacstPoster.ttf', bold='/usr/share/fonts/arabic/KacstPoster.ttf', italic='/usr/share/fonts/arabic/KacstPoster.ttf', bolditalic='/usr/share/fonts/arabic/KacstPoster.ttf')
fontFamilies['Sazanami Mincho'] = FontFamily(name='Sazanami Mincho', genericFontFamily=sans_serif, regular='/usr/share/fonts/japanese/TrueType/sazanami-mincho.ttf', bold='/usr/share/fonts/japanese/TrueType/sazanami-mincho.ttf', italic='/usr/share/fonts/japanese/TrueType/sazanami-mincho.ttf', bolditalic='/usr/share/fonts/japanese/TrueType/sazanami-mincho.ttf')
fontFamilies['Bitstream Vera Sans Mono'] = FontFamily(name='Bitstream Vera Sans Mono', genericFontFamily=sans_serif, regular='/usr/share/fonts/bitstream-vera/VeraMono.ttf', bold='/usr/share/fonts/bitstream-vera/VeraMoBd.ttf', italic='/usr/share/fonts/bitstream-vera/VeraMoIt.ttf', bolditalic='/usr/share/fonts/bitstream-vera/VeraMoBI.ttf')
fontFamilies['DejaVu LGC Sans Mono'] = FontFamily(name='DejaVu LGC Sans Mono', genericFontFamily=sans_serif, regular='/usr/share/fonts/dejavu-lgc/DejaVuLGCSansMono.ttf', bold='/usr/share/fonts/dejavu-lgc/DejaVuLGCSansMono-Bold.ttf', italic='/usr/share/fonts/dejavu-lgc/DejaVuLGCSansMono-Oblique.ttf', bolditalic='/usr/share/fonts/dejavu-lgc/DejaVuLGCSansMono-BoldOblique.ttf')
fontFamilies['URW Gothic L'] = FontFamily(name='URW Gothic L', genericFontFamily=sans_serif, regular='/usr/share/fonts/default/Type1/a010015l.pfb', bold='/usr/share/fonts/default/Type1/a010015l.pfb', italic='/usr/share/fonts/default/Type1/a010033l.pfb', bolditalic='/usr/share/fonts/default/Type1/a010015l.pfb')
fontFamilies['Lohit Kannada'] = FontFamily(name='Lohit Kannada', genericFontFamily=sans_serif, regular='/usr/share/fonts/kannada/lohit_kn.ttf', bold='/usr/share/fonts/kannada/lohit_kn.ttf', italic='/usr/share/fonts/kannada/lohit_kn.ttf', bolditalic='/usr/share/fonts/kannada/lohit_kn.ttf')
fontFamilies['KacstQuraFixed'] = FontFamily(name='KacstQuraFixed', genericFontFamily=sans_serif, regular='/usr/share/fonts/arabic/KacstQuraFixed.ttf', bold='/usr/share/fonts/arabic/KacstQuraFixed.ttf', italic='/usr/share/fonts/arabic/KacstQuraFixed.ttf', bolditalic='/usr/share/fonts/arabic/KacstQuraFixed.ttf')
fontFamilies['Lucida Sans'] = FontFamily(name='Lucida Sans', genericFontFamily=sans_serif, regular='/usr/share/fonts/java/LucidaSansRegular.ttf', bold='/usr/share/fonts/java/LucidaSansDemiBold.ttf', italic='/usr/share/fonts/java/LucidaSansRegular.ttf', bolditalic='/usr/share/fonts/java/LucidaSansRegular.ttf')
fontFamilies['Nimbus Sans L Condensed'] = FontFamily(name='Nimbus Sans L Condensed', genericFontFamily=sans_serif, regular='/usr/share/fonts/default/Type1/n019043l.pfb', bold='/usr/share/fonts/default/Type1/n019044l.pfb', italic='/usr/share/fonts/default/Type1/n019063l.pfb', bolditalic='/usr/share/fonts/default/Type1/n019064l.pfb')
fontFamilies['Lohit Malayalam'] = FontFamily(name='Lohit Malayalam', genericFontFamily=sans_serif, regular='/usr/share/fonts/malayalam/lohit_ml.ttf', bold='/usr/share/fonts/malayalam/lohit_ml.ttf', italic='/usr/share/fonts/malayalam/lohit_ml.ttf', bolditalic='/usr/share/fonts/malayalam/lohit_ml.ttf')
fontFamilies['Lohit Gujarati'] = FontFamily(name='Lohit Gujarati', genericFontFamily=sans_serif, regular='/usr/share/fonts/gujarati/lohit_gu.ttf', bold='/usr/share/fonts/gujarati/lohit_gu.ttf', italic='/usr/share/fonts/gujarati/lohit_gu.ttf', bolditalic='/usr/share/fonts/gujarati/lohit_gu.ttf')
fontFamilies['KacstTitleL'] = FontFamily(name='KacstTitleL', genericFontFamily=sans_serif, regular='/usr/share/fonts/arabic/KacstTitleL.ttf', bold='/usr/share/fonts/arabic/KacstTitleL.ttf', italic='/usr/share/fonts/arabic/KacstTitleL.ttf', bolditalic='/usr/share/fonts/arabic/KacstTitleL.ttf')
fontFamilies['Sazanami Gothic'] = FontFamily(name='Sazanami Gothic', genericFontFamily=sans_serif, regular='/usr/share/fonts/japanese/TrueType/sazanami-gothic.ttf', bold='/usr/share/fonts/japanese/TrueType/sazanami-gothic.ttf', italic='/usr/share/fonts/japanese/TrueType/sazanami-gothic.ttf', bolditalic='/usr/share/fonts/japanese/TrueType/sazanami-gothic.ttf')
fontFamilies['DejaVu LGC Sans'] = FontFamily(name='DejaVu LGC Sans', genericFontFamily=sans_serif, regular='/usr/share/fonts/dejavu-lgc/DejaVuLGCSans.ttf', bold='/usr/share/fonts/dejavu-lgc/DejaVuLGCSans-Bold.ttf', italic='/usr/share/fonts/dejavu-lgc/DejaVuLGCSans-Oblique.ttf', bolditalic='/usr/share/fonts/dejavu-lgc/DejaVuLGCSans-BoldOblique.ttf')
fontFamilies['Baekmuk Headline'] = FontFamily(name='Baekmuk Headline', genericFontFamily=sans_serif, regular='/usr/share/fonts/korean/TrueType/hline.ttf', bold='/usr/share/fonts/korean/TrueType/hline.ttf', italic='/usr/share/fonts/korean/TrueType/hline.ttf', bolditalic='/usr/share/fonts/korean/TrueType/hline.ttf')
fontFamilies['Standard Symbols L'] = FontFamily(name='Standard Symbols L', genericFontFamily=symbols, regular='/usr/share/fonts/default/Type1/s050000l.pfb', bold='/usr/share/fonts/default/Type1/s050000l.pfb', italic='/usr/share/fonts/default/Type1/s050000l.pfb', bolditalic='/usr/share/fonts/default/Type1/s050000l.pfb')
fontFamilies['KacstFarsi'] = FontFamily(name='KacstFarsi', genericFontFamily=sans_serif, regular='/usr/share/fonts/arabic/KacstFarsi.ttf', bold='/usr/share/fonts/arabic/KacstFarsi.ttf', italic='/usr/share/fonts/arabic/KacstFarsi.ttf', bolditalic='/usr/share/fonts/arabic/KacstFarsi.ttf')
fontFamilies['PakTypeNaqsh'] = FontFamily(name='PakTypeNaqsh', genericFontFamily=sans_serif, regular='/usr/share/fonts/arabic/PakTypeNaqsh.ttf', bold='/usr/share/fonts/arabic/PakTypeNaqsh.ttf', italic='/usr/share/fonts/arabic/PakTypeNaqsh.ttf', bolditalic='/usr/share/fonts/arabic/PakTypeNaqsh.ttf')
fontFamilies['KacstLetter'] = FontFamily(name='KacstLetter', genericFontFamily=sans_serif, regular='/usr/share/fonts/arabic/KacstLetter.ttf', bold='/usr/share/fonts/arabic/KacstLetter.ttf', italic='/usr/share/fonts/arabic/KacstLetter.ttf', bolditalic='/usr/share/fonts/arabic/KacstLetter.ttf')
fontFamilies['Baekmuk Dotum'] = FontFamily(name='Baekmuk Dotum', genericFontFamily=sans_serif, regular='/usr/share/fonts/korean/TrueType/dotum.ttf', bold='/usr/share/fonts/korean/TrueType/dotum.ttf', italic='/usr/share/fonts/korean/TrueType/dotum.ttf', bolditalic='/usr/share/fonts/korean/TrueType/dotum.ttf')
fontFamilies['Bitstream Vera Serif'] = FontFamily(name='Bitstream Vera Serif', genericFontFamily=sans_serif, regular='/usr/share/fonts/bitstream-vera/VeraSe.ttf', bold='/usr/share/fonts/bitstream-vera/VeraSeBd.ttf', italic='/usr/share/fonts/bitstream-vera/VeraSe.ttf', bolditalic='/usr/share/fonts/bitstream-vera/VeraSe.ttf')
fontFamilies['Lucida Bright'] = FontFamily(name='Lucida Bright', genericFontFamily=sans_serif, regular='/usr/share/fonts/java/LucidaBrightRegular.ttf', bold='/usr/share/fonts/java/LucidaBrightDemiBold.ttf', italic='/usr/share/fonts/java/LucidaBrightItalic.ttf', bolditalic='/usr/share/fonts/java/LucidaBrightDemiItalic.ttf')
fontFamilies['DejaVu Serif'] = FontFamily(name='DejaVu Serif', genericFontFamily=sans_serif, regular='/usr/share/fonts/dejavu-lgc/DejaVuLGCSerifCondensed.ttf', bold='/usr/share/fonts/dejavu-lgc/DejaVuLGCSerifCondensed-Bold.ttf', italic='/usr/share/fonts/dejavu-lgc/DejaVuLGCSerifCondensed-Oblique.ttf', bolditalic='/usr/share/fonts/dejavu-lgc/DejaVuLGCSerifCondensed-BoldOblique.ttf')
fontFamilies['Lohit Tamil'] = FontFamily(name='Lohit Tamil', genericFontFamily=sans_serif, regular='/usr/share/fonts/tamil/lohit_ta.ttf', bold='/usr/share/fonts/tamil/lohit_ta.ttf', italic='/usr/share/fonts/tamil/lohit_ta.ttf', bolditalic='/usr/share/fonts/tamil/lohit_ta.ttf')
fontFamilies['Century Schoolbook L'] = FontFamily(name='Century Schoolbook L', genericFontFamily=serif, regular='/usr/share/fonts/default/Type1/c059013l.pfb', bold='/usr/share/fonts/default/Type1/c059016l.pfb', italic='/usr/share/fonts/default/Type1/c059033l.pfb', bolditalic='/usr/share/fonts/default/Type1/c059036l.pfb')
fontFamilies['Lohit Hindi'] = FontFamily(name='Lohit Hindi', genericFontFamily=sans_serif, regular='/usr/share/fonts/hindi/lohit_hi.ttf', bold='/usr/share/fonts/hindi/lohit_hi.ttf', italic='/usr/share/fonts/hindi/lohit_hi.ttf', bolditalic='/usr/share/fonts/hindi/lohit_hi.ttf')
fontFamilies['Lohit Telugu'] = FontFamily(name='Lohit Telugu', genericFontFamily=sans_serif, regular='/usr/share/fonts/telugu/lohit_te.ttf', bold='/usr/share/fonts/telugu/lohit_te.ttf', italic='/usr/share/fonts/telugu/lohit_te.ttf', bolditalic='/usr/share/fonts/telugu/lohit_te.ttf')
fontFamilies['DejaVu Sans'] = FontFamily(name='DejaVu Sans', genericFontFamily=sans_serif, regular='/usr/share/fonts/dejavu-lgc/DejaVuLGCSansCondensed.ttf', bold='/usr/share/fonts/dejavu-lgc/DejaVuLGCSansCondensed-Bold.ttf', italic='/usr/share/fonts/dejavu-lgc/DejaVuLGCSansCondensed-Oblique.ttf', bolditalic='/usr/share/fonts/dejavu-lgc/DejaVuLGCSansCondensed-BoldOblique.ttf')
for generic in generics:
	generic.sort()
