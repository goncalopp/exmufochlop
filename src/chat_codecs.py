import itertools
import os
import sys

import const

EBC, DBC= const.ENCODER_BASECLASS, const.DECODER_BASECLASS
ED, DD= const.ENCODERS_DIRECTORY, const.DECODERS_DIRECTORY

def include_codecs_path():
	sys.path.extend([DD, ED])

def modules(directory):
	'''return the (imported) modules from a directory'''
	return  [__import__(f[:-3]) for f in os.listdir(directory) if f[-3:]==".py"]

def atributes(list_of_modules):
	'''gives a flattened list of the modules attributes'''
	atrs_per_module= [[getattr(module, itmstr) for itmstr in dir(module)] for module in list_of_modules]
	flat_atrs= list(itertools.chain(*atrs_per_module))
	return flat_atrs

def descends(class1, class2):
	c1, c2= class1, class2
	return c1!=c2 and type(c1)==type(c2) and issubclass(c1, c2)

def is_decoder(obj):
	'''given any object, detects if it is an decoder'''
	return descends(obj, DBC)

def is_encoder(obj):
	'''given any object, detects if it is an encoder'''
	return descends(obj, EBC)

def get_subclasses_in_directory(directory, baseclass, filter_f= lambda a:True):
	'''searches for classes descendent of baselass in python modules
	present in directory; returns them as a list, optionally filtered by
	the filter_f function'''
	atrs= atributes(modules(directory))
	atrs= filter(filter_f, atrs)
	return atrs

def get_decoder_list(debug=False):
	decoders= get_subclasses_in_directory(DD, DBC, is_decoder)
	if debug:
		print 'imported the following decoders:'
		print "\t"+"\n\t".join([d.format_name() for d in decoders]),"\n"
	return decoders

def get_encoder_list(debug=False):
	encoders= get_subclasses_in_directory(ED, EBC, is_encoder)
	if debug:
		print 'imported the following encoders:'
		print "\t"+"\n\t".join([d.format_name() for d in encoders]),"\n"
	return encoders

def capable_decoders(file_lines, decoder_list):
	return [dec for dec in decoder_list if dec.can_decode(file_lines)]

def choose_decoder_for(file_content, decoder_list, debug=False):
	capable= capable_decoders(file_content, decoder_list)
	if len(capable)<=0:
		raise Exception("No capable decoder found for this file")
	if len(capable)>1:
		format_names_list= [d.format_name() for d in capable]
		choice= ui.choice("more than one decoder is capable of processing this file. Please choose one", format_names_list)
		decoder=capable[choice]()
	else:
		decoder= capable[0]
	if debug :	print 'found suitable decoder for "%s": "%s"'%(filename, decoder.format_name())
	return decoder



#this code executes as the module is imported
include_codecs_path()
decoders= get_decoder_list( debug=True )
encoders= get_encoder_list( debug=True )
