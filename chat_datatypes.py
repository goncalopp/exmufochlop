import datetime
import itertools


class ChatEvent():
	def __init__(self, date):
		assert isinstance(date, datetime.datetime)
		self.date= date

class ChatMessage(ChatEvent):
	def __init__(self, date, from_fn, to_fns, text):
		'''accepts a date, a "from" FriendlyName, a "to" [list of] FrienlyName'''
		ChatEvent.__init__(self,date)
		if isinstance(to_fns, FriendlyName):
			to_fns= [to_fns]
			
		assert isinstance(from_fn, FriendlyName)
		assert all([isinstance(fn, FriendlyName) for fn in to_fns])
		assert isinstance(text, basestring)
		
		self.from_fn= from_fn
		self.to_fns= to_fns
		self.text= text
	
	def __repr__(self):
		return (self.date.isoformat() + " | " + str(self.from_fn) + " - " + self.text)

		
class ChatConversation():
	def __init__(self, messages=[]):
		assert all([isinstance(m, ChatEvent) for m in messages])
		
		self.messages= messages
		#self.participants= set(itertools.chain(*[m.users_involved() for m in messages]))
	
	def addMessage(self, message):
		assert isinstance(message, ChatEvent)
		#self.participants= self.participants.union(message.users_involved())
		self.messages.append(message)

	def __repr__(self):
		return "\n".join([str(m) for m in self.messages])

class ChatLog():
	def __init__(self, conversation_list):
		self.conversations= conversation_list

class ChatUser():
	def __init__(self, realname):
		self.name= realname
		self.default_friendly_name= realname

class FriendlyName():
	def __init__(self, string):
		self.fn= string

	def __repr__(self):
		return self.fn.encode('UTF-8')

class ChatFriendlyNameUserMapper:
	def __init__(self):
		self.str_to_fn={}
		self.fn_to_str={}
		self.fn_to_user= {}

	def getOrAddFN(self, string):
		'''given a friendly name (string), returns the associated FriendlyName, creating one if it doesn't exist'''
		if not string in self.str_to_fn:
			self.str_to_fn[string]=FriendlyName(string)
		return self.str_to_fn[string]

	def getOrAddFNs(self, string_list):
		'''given a list of friendly names (strings), returns the associated FriendlyName's, creating them if they doesn't exist'''
		return [self.getOrAddFN(string) for string in string_list]	
