'''
Decoder wrapper. This class is responsible for conversing with the translation model.
'''
class Decoder:
	'The decoder interface class for decoding ready sentences'
	def __init__(self):
		self.src = 'en'
		self.dest = 'he'

	'Gets tokens, returns translated tokens from the translation model'
	def decode(self, tokens):
		return tokens
