import json
import xmlrpclib
import os 

'''
Decoder wrapper. This class is responsible for conversing with the translation model.
'''
class Decoder:
	def __init__(self):
		self.src = 'en'
		self.dest = 'he'
		with open('decoder.config.json') as config_file:
			config = json.load(config_file)	# Loaded the configuration JSON.
		self.init_server(config)	# Checking whether the server is up and starting if needed.
	
	def init_server(self, config):
		os.system(config['start_cmd']) # Making sure Moses server is up
		self.server = xmlrpclib.ServerProxy(config['host']) # Created a server object for the decoder

	'Gets tokens, returns translated tokens from the translation model'
	def decode(self, tokens):
		translation = self.server.translate({'text': tokens})
		return translation['text']
