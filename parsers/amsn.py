from abstract_parser import MsnLogParser   
from msn_datatypes import *

class MsnLogParser(MsnLogParser):
	'''Abstract class'''
	
	@staticmethod
	def format_name():
		return "aMSN"
	
	@staticmethod
	def can_parse(lines):
		line1= lines[0].lower()
		return '|"lred' in line1

	
	def parse(self, lines):
		convo= MsnConversation()
		for line in lines:
			if line[0:2]=='|"':
					convo.addMessage(self.amsn_line(line))
			else:
				if not line=='\n':
					raise Exception("Can't parse line: "+line+'"')
		return [convo]


	def amsn_line(self, line):
		splitline= line.split('|"')[1:]
		if splitline[0][:5]=='LRED[':
			return self.event(splitline)
		elif splitline[0][:5]=='LGRA[':
			return self.message(splitline)
		else:
			print "splitline:"+str(splitline)
			raise Exception("Can't parse line: "+line+'"')
			
		

	def event(self, splitline):
		text= splitline[0][5:]
		return MsnEvent(datetime.datetime.now())

	def message(self, splitline):
		print splitline
		assert splitline[1][:5]=='LTIME'
		assert splitline[1][15:17]==' ]'
		assert splitline[2][:4]=='LITA'
		if splitline[3][:2]=='LC':
			text= splitline[3][9:]
		elif splitline[3][:4]=='LRED':
			text= splitline[3][5:]
		
		timestamp= datetime.datetime.fromtimestamp(int(splitline[1][5:15]))
		sender= splitline[2][4:]
		color= splitline[3][2:8]
		
		
		return self.createmessage(timestamp, sender, [], text)
