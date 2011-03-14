#if you're creating a parser, your class must descend from const.const.DECODER_BASECLASS
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
		self.mapper= ChatFriendlyNameUserMapper()
	
	def decode(self, lines):
		'''returns ChatLog'''
		raise NotImplementedError("LogDecoder is an abstract class")
		#return chatlog
		
	def createmessage(self, date, from_fn_str, to_fns_str, text):
		'''sugar function to deal with MsnFriendlyNameUserMapper for you'''
		return ChatMessage(date, self.mapper.getOrAddFN(from_fn_str), self.mapper.getOrAddFNs(to_fns_str), text)
