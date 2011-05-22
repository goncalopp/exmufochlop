import datetime
import itertools


class ChatEvent():
	def __init__(self, timestamp, text=''):
		assert isinstance(timestamp, datetime.datetime)
		self.timestamp= timestamp
		self.text= text

	def __repr__(self):
		return (self.timestamp.isoformat() + " | " + self.text)


class ChatMessage(ChatEvent):
	def __init__(self, timestamp, from_dn, to_dns, text):
		'''accepts a datetime, a "from" DisplayName, a "to" [list of] DisplayName'''
		ChatEvent.__init__(self,timestamp, text)
		if isinstance(to_dns, DisplayName):
			to_dns= [to_dns]
			
		assert isinstance(from_dn, DisplayName)
		assert all([isinstance(dn, DisplayName) for dn in to_dns])
		assert isinstance(text, basestring)
		
		self.from_dn= from_dn
		self.to_dns= to_dns
	
	def __repr__(self):
		return (self.timestamp.isoformat() + " | " + str(self.from_dn) + " - " + self.text)

		
class ChatConversation():
	def __init__(self, list_of_messages):
		assert all([isinstance(m, ChatEvent) for m in list_of_messages])
		assert len(list_of_messages)>0
		self.messages= list_of_messages
		self.messages.sort(key=lambda m:m.timestamp)
		#timestamp of converstion is timestamp of first message
		self.timestamp= self.messages[0].timestamp	
		#self.participants= set(itertools.chain(*[m.users_involved() for m in messages]))
	
	def __getitem__(self, key):
		return self.messages[key]
	
	def __setitem__(self, key, value):
		self.messages[key]=value
	
	def __iter__(self):
		return self.messages.__iter__()
	
	def __repr__(self):
		return "\n".join([str(m) for m in self.messages])

class ChatLog():
	def __init__(self, conversation_list):
		self.conversations= conversation_list
	
	def __getitem__(self, key):
		return self.conversations[key]

	def __setitem__(self, key, value):
		self.conversations[key]=value

	def __iter__(self):
		return self.conversations.__iter__()
	
	def __repr__(self):
		return "Chat log with the following conversation dates:\n"+"\n".join([str(c.timestamp) for c in self.conversations])

class ChatUser():
	def __init__(self, realname):
		self.name= realname
		self.dn_list=[]
	
	def associateDisplayName(self, dn):
		if dn.user!=None:
			dn.user.dn_list.remove(dn)
		dn.user=self
		self.dn_list.append(dn)

class DisplayName():
	def __init__(self, dn_string, user=None):
		self.dn= dn_string
		self.user=user

	def __repr__(self):
		return self.dn

class ChatDisplayNameUserMapper:
	def __init__(self):
		self.str_to_dn={}

	def getOrAddDN(self, string):
		'''given a display name (string), returns the associated DisplayName, creating one if it doesn't exist'''
		if not string in self.str_to_dn:
			self.str_to_dn[string]=DisplayName(string)
		return self.str_to_dn[string]

	def getOrAddDNs(self, string_list):
		'''given a list of display names (strings), returns the associated DisplayName's, creating them if they doesn't exist'''
		return [self.getOrAddDN(string) for string in string_list]	
