import json
from subprocess import Popen, PIPE, STDOUT

def pre_process(sentence):
	with open('decoder.config.json') as config_file:
		config = json.load(config_file) # Loaded the configuration JSON.
	p = Popen(config['tokenize_cmd'].split(' '), stdout=PIPE, stdin=PIPE, stderr=PIPE, shell=True) # Using command defined in the config.
	tokenized_sentence = p.communicate(input=sentence.encode('utf8'))[0]

	return tokenized_sentence
