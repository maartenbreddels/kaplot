from kaplot import *
import pymedia.audio.acodec as acodec
import pymedia.muxer as muxer
import sys
import wave


if False:
	file = open(sys.argv[1], 'rb')
	rawdata = file.read()
	wfile = wave.open('test.wav', 'wb')
	
	print muxer.extensions
	demuxer = muxer.Demuxer('mp3')
	frames = demuxer.parse(rawdata)
	decoder = acodec.Decoder(demuxer.streams[0]) # mp3 always got 1 audio stream
	
	audio = decoder.decode(frames[0][1])
	print audio.sample_rate, audio.channels
	wfile.setparams((audio.channels, 2, audio.sample_rate, 0, 'NONE', ''))
	
	for frame in frames[:10]:
		#import pdb; pdb.set_trace()
		audio = decoder.decode(frame[1])
		wfile.writeframes(audio.data)
	sys.exit(0)

wavefile = wave.open(sys.argv[1], 'rb')
print "channels: ", wavefile.getnchannels()
print "getsampwidth: ", wavefile.getsampwidth()
print "getframerate: ", wavefile.getframerate()
print "getnframes: ", wavefile.getnframes()
print "getparams: ", wavefile.getparams()

length = 1 # seconds

if wavefile.getsampwidth() == 2:
	rawdata = wavefile.readframes(length*wavefile.getframerate() * wavefile.getnchannels())
	data = fromstring(rawdata, Int16)
	datal = data[arange(len(data)/2) * 2]
	datar = data[arange(len(data)/2) * 2+1]
else:
	print "unsupported sample width", wavefile.getsampwidth()
	sys.exit(0)

interval = 1.0/wavefile.getframerate()
#interval = 0.1
#x = arange(0, 4.+interval/2, interval)
#x = arange(0, 1, interval)
#y = 1+sin(x*2*pi) + sin(x*30*2*pi) + sin(x*10*2*pi)
#y = 0.1+sin(x *2.5 * 2 * pi)
b = box()
#plot(x, y)
ftspectrum(datal, T=interval, shifted=False, logarithmic=False)
#b.world = (0,0), (2000, 0.05)
b.setRange(0, 2000)
b.grow(1.1)
print b.world
#b.ylogarithmic = True
#b.xinterval = 10
#b.xinteger = True
show()