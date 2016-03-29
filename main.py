#!/usr/local/bin/python2.7 -B
import pre_exec 
from decoder import Decoder
import post_exec

sentence = raw_input()

decoder = Decoder()
print(decoder.decode(sentence))
