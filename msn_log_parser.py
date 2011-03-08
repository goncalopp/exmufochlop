import os
import sys

from msn_datatypes import *
from abstract_parser import MsnLogParser

def get_parser_list(debug=False):
	'''searches for classes descendent of MsnLogParser in python modules in a certain directory, returns them as a list'''
	directory='parsers/'
	sys.path.append(directory)
	parsers= []
	for f in os.listdir(directory):
		if f[-3:]==".py":
			parser_module= __import__(f[:-3])
			for item in [getattr(parser_module, itmstr) for itmstr in dir(parser_module)]:
				if type(item)==type(MsnLogParser) and  issubclass(item, MsnLogParser) and item!=MsnLogParser:
						parsers.append(item)
						if debug:
							print 'imported "'+item.format_name()+'" parser.'
	return parsers


class MsnLog():
	def __init__(self, filename, parsers, debug=False):
		if debug: print "Reading",filename
		lines= self.readfile(filename)
		for parser in parsers:
			if debug: print "trying parser for", parser.format_name()
			if parser.can_parse(lines):
				parser_instance= parser()
				if debug: print "The format is", parser.format_name()
				self.conversations= parser_instance.parse(lines)
				break
		
	def readfile(self, filename):
		f= open(filename, 'rb')
		lines= f.readlines()
		f.close()
		return lines

	def __repr__(self):
		return str(self.conversations[0])


l= MsnLog('test.xml', get_parser_list(), debug=True)
print l
