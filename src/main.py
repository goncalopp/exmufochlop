import sys
import const
import chat_codecs
import ui


def readFile(filename):
	f= open(filename, 'rb')
	lines= f.readlines()
	f.close()
	return lines

def include_codecs_path():
	sys.path.append(const.DECODERS_FOLDER)
	sys.path.append(const.ENCODERS_FOLDER)

def decodeFile(filename):
	global decoders
	lines= readFile(filename)
	decoder= chat_codecs.choose_decoder_for( lines, decoders )
	return decoder.decode(lines)


include_codecs_path()
decoders= chat_codecs.get_decoder_list()


log= decodeFile('../kairi_s_heart@hotmail.com.log')
for con in log.conversations:
	print con.messages[0].text
