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
		with open('moses.config.json') as config_file:
			config = json.load(config_file)	# Loaded the configuration JSON.
		self.init_server(config)	# Checking whether the server is up and starting if needed.
	
	def init_server(self, config):
		if 0 != os.system(config['check_cmd']):	# Checking if there is a moses process running
			print("Moses daemon appears to be down. Attempting to start with command `" + config['start_cmd'] + "`.")
			exit_status = os.system(config['start_cmd'])>>8 # Making sure Moses server is up, shift right to get exit status
			if 0 != exit_status:	# Checking exit status of startup command
				print("Could not start Moses daemon. Starting command returned exit status " + str(exit_status) + ". Please check the Moses log file, or try to run manually without the --server switch.")
		time.sleep(0.2)
		self.server = xmlrpclib.ServerProxy(config['host']) # Created a server object for the decoder

	'Gets tokens, returns translated tokens from the translation model'
	def decode(self, tokens):
		translation = self.server.translate({'text': tokens})
		return translation['text']
