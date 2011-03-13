from abstract_parser import MsnLogParser
from msn_datatypes import *

from xml.dom import minidom

def attribute_list(xml, tag, atr):
	'''given a xml with several tags (tag) inside, builds a list of their atribute atr'''
	return [u.getAttribute(atr) for u in xml.getElementsByTagName(tag)]




class OfficialXMLParser(MsnLogParser):
	@staticmethod
	def can_parse(lines):
		line1, line2= lines[0].lower(), lines[1].lower()
		return "<" in line1 and ">" in line1 and "messagelog.xsl" in line2
		
	@staticmethod
	def format_name():
		return "Official client XML"
	
	
	def parse(self, lines):
		mapper= MsnFriendlyNameUserMapper()
		current_convo= MsnConversation()
		list_of_convos= [current_convo]
		
		xml= "".join(lines)
		xmldoc = minidom.parseString(xml)
		logs_xml= xmldoc.getElementsByTagName('Log')
		assert len(logs_xml)==1
		for log_xml in logs_xml:
			messages_xml= log_xml.getElementsByTagName('Message')
			for message_xml in messages_xml:
				msnmessage= self.xmlmessageToMsnMessage(message_xml)
				current_convo.addMessage(msnmessage)
		
		return list_of_convos
	
	def xmlmessageToMsnMessage(self, xmlmessage):
		datetime_xml= xmlmessage.getAttribute('DateTime')
		senders_xml = xmlmessage.getElementsByTagName('From')
		receivers_xml = xmlmessage.getElementsByTagName('To')
		
		timestamp= datetime.datetime.strptime(datetime_xml, "%Y-%m-%dT%H:%M:%S.%fZ")
		sender_fns =   attribute_list(senders_xml[0], 'User', 'FriendlyName')
		receiver_fns = attribute_list(receivers_xml[0], 'User', 'FriendlyName')
		text= xmlmessage.getElementsByTagName('Text')[0].firstChild.nodeValue
		text= text.encode('UTF-8')
		
		assert len(senders_xml)==1	#only one "From" section
		assert len(receivers_xml)==1	#only one "To" section
		assert len(sender_fns)==1	#only one sender
		
		message= self.createmessage(timestamp, sender_fns[0], receiver_fns, text)
		return message
	
	
	
	
