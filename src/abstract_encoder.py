#if you're creating a encoder, your class must descend from const.ENCODER_BASECLASS

#uncomment the following line
#from const import ENCODER_BASECLASS
from chat_datatypes import *

class ChatLogEncoder():
	'''Abstract class'''
	
	
	@staticmethod
	def format_name():
		'''returns this encoder's log format name'''
		raise NotImplementedError("LogEncoder is an abstract class")
		#return "My format name"

	def __init__(self):
		self.mapper= ChatDisplayNameUserMapper()
	
	def encode(self, chatlog):
		'''returns a string'''
		raise NotImplementedError("LogEncoder is an abstract class")
		#return string
