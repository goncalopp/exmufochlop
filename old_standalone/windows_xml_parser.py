#windows msn xml parser...
from xml.dom import minidom
import codecs

def getText(nodelist):
	rc = []
	for node in nodelist:
		rc.append(node.data)
	return ''.join(rc)


xmldoc = minidom.parse('yuna_ayame570657228.xml')
messages= xmldoc.getElementsByTagName('Message')
#f=open('outfile','w')
f = codecs.open( "outfile", "w", "utf-8" )



for message in messages:
	date= message.getAttribute('Date')
	receiver = message.getElementsByTagName('From')[0].getElementsByTagName('User')[0].getAttribute('FriendlyName')
	sender = message.getElementsByTagName('From')[0].getElementsByTagName('User')[0].getAttribute('FriendlyName')
	text= message.getElementsByTagName('Text')[0].firstChild.nodeValue
	f.write(date+'\t'+sender[:10]+':\t'+text+'\n')

