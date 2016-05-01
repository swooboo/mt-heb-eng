import json
import urllib2

'''
Decoder wrapper. This class is responsible for conversing with the translation model.
'''
class Decoder:
	'The decoder interface class for decoding ready sentences'
	def __init__(self):
		self.src = 'en'
		self.dest = 'he'
		with open('decoder.config.json') as config_file:
			config = json.load(config_file)	# Loaded the configuration JSON.
		self.init_server(config)	# Checking whether the server is up and starting if needed.
	
	def init_server(self, config):
		response = urllib2.urlopen(config['host'] + ':' + str(config['port']))
		html = response.read()

	'Gets tokens, returns translated tokens from the translation model'
	def decode(self, tokens):
		return tokens
