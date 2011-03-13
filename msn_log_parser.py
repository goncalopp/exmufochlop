import os
import sys
import itertools

from msn_datatypes import *
from abstract_parser import MsnLogParser

DECODERS_FOLDER= 'decoders/'
ENCODERS_FOLDER= 'encoders/'

DECODER_BASECLASS= MsnLogParser


def modules_list(directory):
	'''return the (imported) modules from a directory'''
	return  [__import__(f[:-3]) for f in os.listdir(directory) if f[-3:]==".py"]

def modules_atributes(list_of_modules):
	'''gives a flattened list of the modules attributes'''
	atrs_per_module= [[getattr(module, itmstr) for itmstr in dir(module)] for module in list_of_modules]
	flat_atrs= list(itertools.chain(*atrs_per_module))
	return flat_atrs
	
def detect_decoder(obj):
	'''given any object, detects if it is an encoder'''
	if (type(obj)==type(DECODER_BASECLASS)) \
		and issubclass(obj, DECODER_BASECLASS) \
		and (obj!=DECODER_BASECLASS):
		return (True)
	else:
		return False
		
def get_decoder_list(debug=False):
	'''searches for classes descendent of MsnLogParser in python modules in a certain directory, returns them as a list'''
	atrs= modules_atributes(modules_list(DECODERS_FOLDER))
	decoders= filter(detect_decoder, atrs)
	if debug:
		print 'imported the following decoders:'
		print "\t"+"\n\t".join([d.format_name() for d in decoders]),"\n"
	return decoders


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

sys.path.append(DECODERS_FOLDER)
sys.path.append(ENCODERS_FOLDER)



l= MsnLog('test.xml', get_decoder_list(debug=True), debug=True)
#print l
