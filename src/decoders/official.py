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
		self.log= ChatLog()
		xmldoc = minidom.parseString("".join(lines))
		
		logs_xml= xmldoc.getElementsByTagName('Log')
		assert len(logs_xml)==1
		log_xml= logs_xml[0]
		
		for entry_xml in log_xml.childNodes:
			event= self.addXmlEvent(entry_xml)

		for conversation in self.sessions.values():
			self.log.createConversation()
			for m in conversation:
				self.log.addEvent(m)
		return self.log

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
		elif xml.tagName=="Join":
			return self.invitation(xml)
		elif xml.tagName=="Leave":
			return self.invitation(xml)
		else:
			raise Exception('unrecognized element: "'+xml.tagName+'"')

	def message(self, xmlmessage):
		timestamp, text, sender_dns, receiver_dns= self.common_atributes_and_elements(xmlmessage)
		assert len(sender_dns)==1	#only one sender
		assert len(receiver_dns)>=1	#one or more receivers
		message= self.log.createMessage(timestamp, text, sender_dns[0], receiver_dns)
		return message

	def common_atributes_and_elements(self, xml):
		'''returns timestamp, text, sender_dn and receivers_dns, if available'''
		datetime_xml= xml.getAttribute('DateTime')
		timestamp= datetime.datetime.strptime(datetime_xml, "%Y-%m-%dT%H:%M:%S.%fZ")
		
		senders_xml = xml.getElementsByTagName('From')
		receivers_xml = xml.getElementsByTagName('To')
		sender_dns = attribute_list(senders_xml[0], 'User', 'FriendlyName') if len(senders_xml) else []
		receiver_dns = attribute_list(receivers_xml[0], 'User', 'FriendlyName') if len(receivers_xml) else []
		map(lambda a:a.encode('UTF-8'), sender_dns)
		map(lambda a:a.encode('UTF-8'), receiver_dns)
		
		text= xml.getElementsByTagName('Text')[0].firstChild.nodeValue
		text= text.encode('UTF-8')
		return (timestamp, text, sender_dns, receiver_dns)
		
	def invitation(self, xmlmessage):
		timestamp, text, sender_dns, receiver_dns= self.common_atributes_and_elements(xmlmessage)
		return self.log.createEvent(timestamp, text)
	
	
	
	
