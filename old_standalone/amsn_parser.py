
EVENT, CHAT= range(2)

class AmsnLine:
	def __init__(self, line):
		splitline= line.split('|"')[1:]
		if splitline[0][:5]=='LRED[':
			self.event(splitline)
		elif splitline[0][:5]=='LGRA[':
			self.chat(splitline)
		else:
			print "splitline:"+str(splitline)
			raise Exception('Unknown line type: '+line)
			
		

	def event(self, splitline):
		self.type= EVENT
		self.data= splitline[0][5:]

	def chat(self, splitline):
		self.type= CHAT
		assert splitline[1][:5]=='LTIME'
		assert splitline[1][15:17]==' ]'
		self.time= int(splitline[1][5:15])
		assert splitline[2][:4]=='LITA'
		self.sender= splitline[2][4:]
		assert splitline[3][:2]=='LC'
		self.color= splitline[3][2:8]
		self.data= splitline[3][9:]
		

class AmsnParser:
	def __init__(self, filename):
		self.tokens=[]
		file= open(filename, 'rb')
		for line in file:
			if line[0:2]=='|"':
				try:
					self.tokens.append(AmsnLine(line))
				except:
					pass
			else:
				if not line=='\n' and not line=='\n':
					print 'strange line: "'+line+'"'
					self.tokens[-1].data+=line
			
		

		

filename= 'tmp.log'
parser= AmsnParser(filename)

print parser.tokens[1].color
