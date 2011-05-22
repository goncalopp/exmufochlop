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
	
def decodeFile(decoders, filename):
	lines= readFile(filename)
	capable= chat_codecs.capable_decoders(lines, decoders)
	format_names_list= [d.format_name() for d in capable]
	if len(capable)<=0:
		raise Exception("No capable decoder found for this file")
	if len(capable)>1:
		choice= ui.choice("more than one decoder is capable of processing this file. Please choose one", format_names_list)
		decoder=capable[choice]()
	else:
		decoder= capable[0]()
	print 'decoding "%s" with "%s" decoder'%(filename, decoder.format_name())
	return decoder.decode(lines)


include_codecs_path()
decoders= chat_codecs.get_decoder_list()


log= decodeFile(decoders, '../kairi_s_heart@hotmail.com.log')
for con in log.conversations:
	print con.messages[0].text
