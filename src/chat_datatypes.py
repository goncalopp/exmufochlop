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
	def __init__(self):
		self.messages=[]
	
	def __getitem__(self, key):
		return self.messages[key]
	
	def __setitem__(self, key, value):
		self.messages[key]=value
	
	def __iter__(self):
		return self.messages.__iter__()

	def addEvent(self, event):
		assert isinstance(event, ChatEvent)
		self.messages.append(event)

	def finish(self):
		self.messages.sort(key=lambda m:m.timestamp)
		self.start_timestamp= self.messages[0].timestamp
		self.end_timestamp= self.messages[-1].timestamp
		#self.participants= set(itertools.chain(*[m.users_involved() for m in messages]))
	
	def __repr__(self):
		return "\n".join([str(m) for m in self.messages])

class ChatLog():
	def __init__(self):
		self.conversations= []
		self.mapper= ChatDisplayNameUserMapper()
	
	def __getitem__(self, key):
		return self.conversations[key]

	def __setitem__(self, key, value):
		self.conversations[key]=value

	def __iter__(self):
		return self.conversations.__iter__()
	
	def __repr__(self):
		return "Chat log with the following conversation dates:\n"+"\n".join([str(c.start_timestamp) for c in self.conversations])

	def createConversation(self):
		self.conversations.append( ChatConversation() )

	def createMessage(self, *args, **kwargs):
		'''adds a new message to last conversation'''
		return self.mapper.create_message(*args, **kwargs)
		self.conversations[-1].addEvent(m)

	def createEvent(self, *args, **kwargs):
		return ChatEvent(*args, **kwargs)

	def addEvent(self, m):
		assert isinstance(m,ChatEvent)
		self.conversations[-1].addEvent(m)

	
	def finish(self):
		for c in self.conversations:
			c.finish()
		self.start_timestamp= min([c.start_timestamp for c in self.conversations])
		self.start_timestamp= max([c.end_timestamp for c in self.conversations])
		

	
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
		self.str_to_user={}

	def getOrAddUser(self, username):
		if not username in self.str_to_user:
			self.str_to_user[username]= ChatUser(username)
		return self.str_to_user[username]

	def getOrAddDN(self, dn_string, username_str=None):
		'''given a display name (dn_string), returns the associated
		DisplayName, if it exists. If it doesn't, a new one is created;
		in this case, if no username_str is given, a
		new user will be created with the same string as the DN,
		otherwise the DN will be associated with the given user'''
		if not dn_string in self.str_to_dn:
			self.str_to_dn[dn_string]= DisplayName(dn_string, self.str_to_user.get(username_str))
		return self.str_to_dn[dn_string]

	def create_message(self, date, text, from_dn_str, to_dns_str, from_user_str=None, to_users_str=None):
		'''creates a message given DisplayNames (and possibly the matching
		usernames) as strings'''
		if to_users_str==None:
			to_users_str= (None,)*len(to_dns_str)
		assert len(to_dns_str)==len(to_users_str)
		
		from_dn= self.getOrAddDN(from_dn_str, from_user_str)
		to_dns= tuple(DisplayName(d, u) for d,u in zip(to_dns_str, to_users_str))
		return ChatMessage(date, from_dn, to_dns, text)

