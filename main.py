#!/usr/local/bin/python2.7 -B
from pre_process import pre_process
from decoder import Decoder
from post_process import post_process

def translate(sentence):
	sentence = pre_process(sentence)
	decoder = Decoder()
	sentence = decoder.decode(sentence)
	sentence = post_process(sentence)
	return sentence

if(__name__ == '__main__'):
	sentence = raw_input() # Got the one sentence
	print(translate(sentence))
