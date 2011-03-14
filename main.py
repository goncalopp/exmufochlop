import sys
import const
import chat_codecs


def readFile(filename):
	f= open(filename, 'rb')
	lines= f.readlines()
	f.close()
	return lines

def include_codecs_path():
	sys.path.append(const.DECODERS_FOLDER)
	sys.path.append(const.ENCODERS_FOLDER)
	


include_codecs_path()
decoders= chat_codecs.get_decoder_list()
lines= readFile('test.xml')
capable= chat_codecs.capable_decoders(lines, decoders)

print "capable decoders:\n","\n".join([d.format_name() for d in capable])

decoder= capable[0]()
print decoder.decode(lines)
