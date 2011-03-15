#TODO:
#text style
#invitation types
#correct invitation responses representation

from const import DECODER_BASECLASS
from chat_datatypes import *

from xml.dom import minidom

def attribute_list(xml, tag, atr):
	'''given a xml with several tags (tag) inside, builds a list of their atribute atr'''
	return [u.getAttribute(atr) for u in xml.getElementsByTagName(tag)]




class OfficialXMLParser(DECODER_BASECLASS):
	@staticmethod
	def can_decode(lines):
		line1, line2= lines[0].lower(), lines[1].lower()
		return "<" in line1 and ">" in line1 and "messagelog.xsl" in line2
		
	@staticmethod
	def format_name():
		return "Official client XML"
	
	
	def decode(self, lines):
		self.sessions= {}	#dictionary of sessionnumeber, list_of_messages
		xmldoc = minidom.parseString("".join(lines))
		
		logs_xml= xmldoc.getElementsByTagName('Log')
		assert len(logs_xml)==1
		log_xml= logs_xml[0]
		
		for entry_xml in log_xml.childNodes:
			event= self.addXmlEvent(entry_xml)
		
		conversations= [ChatConversation(self.sessions[ml]) for ml in self.sessions.keys()]
		return ChatLog(conversations)

	def addXmlEvent(self, xml):
		session_number= int(xml.getAttribute('SessionID'))
		if not session_number in self.sessions:
			self.sessions[session_number]=[]
		msnevent= self.xmlEventToChatEvent(xml)
		self.sessions[session_number].append(msnevent)
		
	def xmlEventToChatEvent(self, xml):
		if xml.tagName=="Message":
			return self.message(xml)
		elif xml.tagName=="Invitation":
			return self.invitation(xml)
		elif xml.tagName=="InvitationResponse":
			return self.invitation(xml)
		else:
			raise Exception('unrecognized element: "'+xml.tagName+'"')

	def message(self, xmlmessage):
		timestamp, text, sender_fns, receiver_fns= self.common_atributes_and_elements(xmlmessage)
		assert len(sender_fns)==1	#only one sender
		assert len(receiver_fns)>=1	#one or more receivers
		message= self.createmessage(timestamp, sender_fns[0], receiver_fns, text)
		return message

	def common_atributes_and_elements(self, xml):
		'''returns timestamp, text, sender_fn and receivers_fns, if available'''
		datetime_xml= xml.getAttribute('DateTime')
		timestamp= datetime.datetime.strptime(datetime_xml, "%Y-%m-%dT%H:%M:%S.%fZ")
		
		senders_xml = xml.getElementsByTagName('From')
		receivers_xml = xml.getElementsByTagName('To')
		sender_fns = attribute_list(senders_xml[0], 'User', 'FriendlyName') if len(senders_xml) else []
		receiver_fns = attribute_list(receivers_xml[0], 'User', 'FriendlyName') if len(receivers_xml) else []
		map(lambda a:a.encode('UTF-8'), sender_fns)
		map(lambda a:a.encode('UTF-8'), receiver_fns)
		
		text= xml.getElementsByTagName('Text')[0].firstChild.nodeValue
		text= text.encode('UTF-8')
		return (timestamp, text, sender_fns, receiver_fns)
		
	def invitation(self, xmlmessage):
		timestamp, text, sender_fns, receiver_fns= self.common_atributes_and_elements(xmlmessage)
		return ChatEvent(timestamp, text)
	
	
	
	
