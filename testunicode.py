import xml.sax
import xml.dom.pulldom
from cStringIO import StringIO
encoding = "utf-16"
xmlstring = u"<?xml version='1.0' encoding='%s'?><b>hoeba</b>" % encoding
parser = xml.sax.make_parser()
buf = StringIO(xmlstring.encode(encoding))
bufsize = len(xmlstring)
events = xml.dom.pulldom.DOMEventStream(buf, parser, bufsize)
toktype, rootNode = events.getEvent()