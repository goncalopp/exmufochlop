import re

from const import DECODER_BASECLASS
from chat_datatypes import *

class AmsnToken():
	'''A msn token. Make an object by passing the constructor a (line) string.
	If it throws no exception, the object will have the following Attributes:
	start: the index of the string where the whole token starts
	end: the index where the whole token (including Attribute, if it exists) ends
	inner_start: the index where the token name starts
	inner_end: the index where the token name ends
	token: the string representation of the token
	Attribute: the token's associated Attribute, if it exists (time, color...)
	'''
	TOKEN_BEGINNING= '|"L'
	TOKENS_STATIC= ['RED', 'GRA','NOR', 'ITA', 'GRE']
	TOKEN_COLOR= "C"
	TOKEN_TIME= "TIME"
	
	def __init__(self, line, start_looking_index=0):
		self.line= line
		self.search(start_looking_index)
		self.check()
		self.getAtribute()
	
	def search(self, startindex):
		'''searches for the first msn token in the line, after startindex.
		Raises ValueError if no token is present'''
		self.start= self.line.index(self.TOKEN_BEGINNING, startindex)	#raises ValueError if not found
		self.inner_start= self.start + len(self.TOKEN_BEGINNING)
		r= re.compile("[A-Z]+")
		m= r.search(self.line, self.inner_start)
		self.inner_end= m.end()
		self.token=m.group(0)

	def check(self):
		'''checks if the found region on the line is a valid token'''
		if self.token == self.TOKEN_COLOR:
			return
		if self.token == self.TOKEN_TIME:
			return
	
		#AMSN FORMAT IS LAME, since it may have an uppercase character
		#immediatelly next to the token, making the regex not work properly
		for tk in self.TOKENS_STATIC:
			if tk in self.token:
				self.inner_end= self.inner_start+len(tk)
				self.token= tk
				return
				
		raise Exception("Unknown token: "+self.token)
	
	def __repr__(self):
		return "%s(%s) [%d,%d]" % (self.token, self.Attribute, self.inner_start, self.inner_end)
		
	
	def getAtribute(self):
		'''if the token has an associated Attribute, get it'''
		if self.token==self.TOKEN_COLOR:
			r= re.compile("[0-9A-F]+")			#hex color
		elif self.token==self.TOKEN_TIME:
			r= re.compile("[0-9]+")					#unix time in decimal
		else:
			r= re.compile("")								#no Attribute
			
		m= r.search(self.line, self.inner_end)
		self.Attribute= m.group(0)
		self.end= m.end()


class AmsnTokenList():
	TYPE_MESSAGE, TYPE_EVENT= range(2)
	def __init__(self, line):
		self.line= line
		self.tks=[]
		end=0
		while True:
			try:
				tk= AmsnToken(line, end)	#throws ValueError if there are no more tokens
				self.tks.append(tk)
				end= tk.end
			except ValueError:
				return

	def getInterstitials(self):
			'''returns a ordered list of the non-tokens of the line'''
			inter=[]
			start=0
			for t in self.tks:
				inter.append(self.line[start:t.start])
				start= t.end
			inter.append(self.line[start:])
			return inter

	def __getitem__(self, i):
		return self.tks[i]

	def __len__(self):
		return len(self.tks)

	def __repr__(self):
		return str(self.tks)

	
		
class AMsnLogDecoder(DECODER_BASECLASS):
	NOTIMESTAMP= datetime.datetime.max
	@staticmethod
	def format_name():
		return "aMSN"
	
	@staticmethod
	def can_decode(lines):
		return lines[0][:3] == '|"L' 
	
	def decode(self, lines):
		message_list=[]
		last_timestamp= self.NOTIMESTAMP
		for line in lines:
			if line[0:3]!='|"L': #this is probably a message continuation...
				m.text+= line				#...so append to last message
			else:
				m= self.extract(line)
				if m.timestamp == self.NOTIMESTAMP:	#some events have no timestamp token...
					m.timestamp= last_timestamp				#make them keep the timestamp of last event
				message_list.append(m)
		return ChatLog([ChatConversation(message_list)])

	def extract_message(self, tokens, interstitials):
		'''a simple message, has a timestamp, a sender and a text'''
		i= interstitials
		assert i[0]==''
		assert i[1]=='['
		assert i[2]==' ] '
		assert i[3][-2:]==' :'
		
		displayname= i[3][:-2]
		message= i[4]
		timestamp= datetime.datetime.fromtimestamp(int(tokens[1].Attribute))
		return self.createmessage(timestamp, displayname, [], message)

	def extract_event1(self, tokens, interstitials):
		'''an event with timestamp and text'''
		i= interstitials
		assert i[0]==''
		assert i[1][:1]=='['
		assert i[2]==']\n'
		text= i[1][1:]
		timestamp= datetime.datetime.fromtimestamp(int(tokens[1].Attribute))
		return ChatEvent(timestamp, text)

	def extract_event2(self, tokens, interstitials):
		'''an event without timestamp'''
		i= interstitials
		assert i[0]==''
		assert i[1][:1]=='['
		assert i[1][-2:]==']\n'
		text= i[1][1:-2]+"\n"
		return ChatEvent(self.NOTIMESTAMP, text)

	def extract_filetransfer(self, tokens, interstitials):
		'''a file transfer event'''
		i= interstitials
		assert i[0]==i[1]==''
		assert i[2]==' '
		timestamp= datetime.datetime.fromtimestamp(int(tokens[1].Attribute))
		text= i[3]
		return ChatEvent(timestamp, text)
		
	def extract(self, line):
		print line
		t= tokens= AmsnTokenList(line)
		i= interstitials= tokens.getInterstitials()
		
		if len(t)==4 and t[0].token=='GRA' and t[1].token=='TIME' and t[2].token=='ITA' and t[3].token=='C':
			return self.extract_message(t, i)
		
		if len(t)==2 and t[0].token=='RED' and t[1].token=='TIME':
			return self.extract_event1(t, i)
		
		if len(t)==1 and t[0].token=='RED':
			return self.extract_event2(t, i)
		
		if len(t)==3 and t[0].token=='GRA' and t[1].token=='TIME' and t[2].token=='GRE':
			return self.extract_filetransfer(t, i)
			
		raise Exception("Could not detect line format.\nline:%s\ntokens:%s\ninterstitials:%s" % (line, tokens, interstitials))
		

