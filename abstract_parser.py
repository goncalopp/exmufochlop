#uncomment this if you're creating a parser:
#from abstract_parser import MsnLogParser   
from msn_datatypes import *

class MsnLogParser():
	'''Abstract class'''
	
	
	@staticmethod
	def format_name():
		'''returns this parser's log format name'''
		raise NotImplementedError("MsnLogParser is an abstract class")
		#return "My format name"
	
	@staticmethod
	def can_parse(lines):
		'''returns True if this parser can understand the format of the given text'''
		raise NotImplementedError("MsnLogParser is an abstract class")
		#return False

	def __init__(self):
		self.mapper= MsnFriendlyNameUserMapper()
	
	def parse(self, lines):
		'''returns list_of_MsnConversation)'''
		raise NotImplementedError("MsnLogParser is an abstract class")
		#return convos
		
	def createmessage(self, date, from_fn_str, to_fns_str, text):
		'''sugar function to deal with MsnFriendlyNameUserMapper for you'''
		return MsnMessage(date, self.mapper.getOrAddFN(from_fn_str), self.mapper.getOrAddFNs(to_fns_str), text)
