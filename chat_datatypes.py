import datetime
import itertools


class ChatEvent():
	def __init__(self, timestamp):
		assert isinstance(timestamp, datetime.datetime)
		self.timestamp= timestamp

class ChatMessage(ChatEvent):
	def __init__(self, timestamp, from_fn, to_fns, text):
		'''accepts a datetime, a "from" FriendlyName, a "to" [list of] FrienlyName'''
		ChatEvent.__init__(self,timestamp)
		if isinstance(to_fns, FriendlyName):
			to_fns= [to_fns]
			
		assert isinstance(from_fn, FriendlyName)
		assert all([isinstance(fn, FriendlyName) for fn in to_fns])
		assert isinstance(text, basestring)
		
		self.from_fn= from_fn
		self.to_fns= to_fns
		self.text= text
	
	def __repr__(self):
		return (self.timestamp.isoformat() + " | " + str(self.from_fn) + " - " + self.text)

		
class ChatConversation():
	def __init__(self, list_of_messages):
		assert all([isinstance(m, ChatEvent) for m in list_of_messages])
		assert len(list_of_messages)>0
		self.messages= list_of_messages
		self.messages.sort(key=lambda m:m.timestamp)

		#timestamp of converstion is timestamp of first message
		self.timestamp= self.messages[0].timestamp	
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
	
	def __repr__(self):
		return "Chat log with the following conversation dates:\n"+"\n".join([str(c.timestamp) for c in self.conversations])

class ChatUser():
	def __init__(self, realname):
		self.name= realname
		self.fn_list=[]
	
	def associateFrindlyName(self, fn):
		if fn.user!=None:
			fn.user.fn_list.remove(fn)
		fn.user=self
		self.fn_list.append(fn)

class FriendlyName():
	def __init__(self, fn_string, user=None):
		self.fn= fn_string
		self.user=user

	def __repr__(self):
		return self.fn.encode('UTF-8')

class ChatFriendlyNameUserMapper:
	def __init__(self):
		self.str_to_fn={}

	def getOrAddFN(self, string):
		'''given a friendly name (string), returns the associated FriendlyName, creating one if it doesn't exist'''
		if not string in self.str_to_fn:
			self.str_to_fn[string]=FriendlyName(string)
		return self.str_to_fn[string]

	def getOrAddFNs(self, string_list):
		'''given a list of friendly names (strings), returns the associated FriendlyName's, creating them if they doesn't exist'''
		return [self.getOrAddFN(string) for string in string_list]	
