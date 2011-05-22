#TODO:
#offer configuration options - save local username, locale (for ascii timestamp interpretation)
#
#

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

	def __init__(self):
		DECODER_BASECLASS.__init__(self)
		self.utc_offset= 0
		self.username= "local_username"
		
	def decode(self, lines):
		conversation_list=[]
		message_list=[]
		last_timestamp= self.NOTIMESTAMP
		for line_number,line in enumerate(lines):
			if line[0:3]!='|"L': #this is probably a message continuation...
				m.text+= line				#...so append to last message
			else:
				m= self.extract(line)
				if m.timestamp == self.NOTIMESTAMP:	#some events have no timestamp token...
					m.timestamp= last_timestamp				#make them keep the timestamp of last event
				if m.timestamp<last_timestamp and line_number>0:
					#anachronism; happens on connection problems (message doesn't get sent at first).
					#note this may also happen because the utc offset parameter is wrong (some dates are saved as UTC, other as local time)
					pass
				last_timestamp= m.timestamp
				if "Conversation started on" in m.text or "Started an Offline Instant Messaging conversation" in m.text:
					if line_number!=0:
						conversation_list.append(ChatConversation(message_list))
					message_list=[]
				message_list.append(m)
		conversation_list.append(ChatConversation(message_list))
		return ChatLog(conversation_list)


		
	def extract(self, line):
		t= tokens= AmsnTokenList(line)
		tn= [tok.token for tok in tokens]
		i= interstitials= tokens.getInterstitials()
		
		if tn==['GRA','TIME','ITA','C'] and i[0]=='' and i[1]=='[' and i[2]==' ] ' and i[3][-2:]==' :':
			#a simple message, has a timestamp, a sender and a text
			displayname= i[3][:-2]
			message= i[4]
			timestamp= datetime.datetime.fromtimestamp(int(tokens[1].Attribute))
			return self.createmessage(timestamp, displayname, [], message)
			
		if tn==['GRA','ITA','NOR'] and i[0]=='' and i[1][-2:]=='] ' and i[2][-2:]==' :':
			#a simple message, has a timestamp, a sender and a text
			displayname= i[3][:-2]
			message= i[3]
			timestamp= datetime.datetime.strptime(i[1], "[%m/%d/%y %H:%M:%S] ")
			timestamp+= datetime.timedelta(hours= -self.utc_offset)
			return self.createmessage(timestamp, displayname, [], message)
		
		if tn==['RED','TIME'] and i[0]=='' and i[1][:1]=='[':
			#an event with timestamp and text
			if i[2]==']\n':	#"normal" event
				text= i[1][1:]
			elif  i[2][-4:]==') ]\n' and i[1][-4:]==' on ':	#conference start
				text= i[1][1:-4]+i[2][-3]+'\n'
			timestamp= datetime.datetime.fromtimestamp(int(tokens[1].Attribute))
			return ChatEvent(timestamp, text)
		
		if tn==['RED'] and i[0]=='' and i[1][:1]=='[' and i[1][-2:]==']\n':
			#a chat event without timestamp
			text= i[1][1:-2]+"\n"
			return ChatEvent(self.NOTIMESTAMP, text)
		
		if tn==['GRA','TIME','GRE'] and i[0]==i[1]=='' and i[2]==' ':
			#a file transfer event
			timestamp= datetime.datetime.fromtimestamp(int(tokens[1].Attribute))
			text= i[3]
			return ChatEvent(timestamp, text)
		
		if tn==['GRA','TIME','ITA','RED'] and i[0]=='' and i[1]=='[' and i[2]==' ] ':
			#a message-not-delivered event'''
			text= i[3]+i[4]
			return ChatEvent(self.NOTIMESTAMP, text)
			
		raise Exception("Could not detect line format.\nline:%s\ntokens:%s\ninterstitials:%s" % (line, tokens, interstitials))
		

