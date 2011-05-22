import chat_codecs

def readFile(filename):
	f= open(filename, 'rb')
	lines= f.readlines()
	f.close()
	return lines


def decodeFile(filename):
	lines= readFile(filename)
	decoder= chat_codecs.choose_decoder_for( lines, chat_codecs.decoders )()
	return decoder.decode(lines)



log= decodeFile('../kairi_s_heart@hotmail.com.log')
encoder= chat_codecs.encoders[0]()
result= encoder.encode(log)


f=open('../result.html', 'w')
f.write(result)
