import const
import itertools
import os


def modules(directory):
	'''return the (imported) modules from a directory'''
	return  [__import__(f[:-3]) for f in os.listdir(directory) if f[-3:]==".py"]

def atributes(list_of_modules):
	'''gives a flattened list of the modules attributes'''
	atrs_per_module= [[getattr(module, itmstr) for itmstr in dir(module)] for module in list_of_modules]
	flat_atrs= list(itertools.chain(*atrs_per_module))
	return flat_atrs
	
def is_decoder(obj):
	'''given any object, detects if it is an encoder'''
	if (type(obj)==type(const.DECODER_BASECLASS)) \
		and issubclass(obj, const.DECODER_BASECLASS) \
		and (obj!=const.DECODER_BASECLASS):
		return (True)
	else:
		return False
		
def get_decoder_list(debug=False):
	'''searches for classes descendent of ChatLogDecoder in python modules in a certain directory, returns them as a list'''
	atrs= atributes(modules(const.DECODERS_FOLDER))
	decoders= filter(is_decoder, atrs)
	if debug:
		print 'imported the following decoders:'
		print "\t"+"\n\t".join([d.format_name() for d in decoders]),"\n"
	return decoders

def capable_decoders(file_lines, decoder_list):
	return [dec for dec in decoder_list if dec.can_decode(file_lines)]
