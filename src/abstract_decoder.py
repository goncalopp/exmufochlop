#if you're creating a decoder, your class must descend from const.DECODER_BASECLASS

#uncomment the following line
#from const import DECODER_BASECLASS
from chat_datatypes import *

class ChatLogDecoder():
	'''Abstract class'''
	
	
	@staticmethod
	def format_name():
		'''returns this decoder's log format name'''
		raise NotImplementedError("LogDecoder is an abstract class")
		#return "My format name"
	
	@staticmethod
	def can_decode(lines):
		'''returns True if this decoder can understand the format of the given text'''
		raise NotImplementedError("LogDecoder is an abstract class")
		#return False

	def __init__(self):
		self.mapper= ChatDisplayNameUserMapper()
	
	def decode(self, lines):
		'''returns ChatLog'''
		raise NotImplementedError("LogDecoder is an abstract class")
		#return chatlog
		
	def createmessage(self, date, from_dn_str, to_dns_str, text):
		'''sugar function to deal with MsnDisplayNameUserMapper for you'''
		return ChatMessage(date, self.mapper.getOrAddDN(from_dn_str), self.mapper.getOrAddDNs(to_dns_str), text)
