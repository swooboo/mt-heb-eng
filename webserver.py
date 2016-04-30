#!/usr/bin/python2 -B
import sys
sys.dont_write_bytecode = True # Don't want cluttering .pyc files.
from main import translate
from flask import Flask, request, json
app = Flask(__name__, static_url_path='')

@app.route("/")
def index():
	return app.send_static_file('index.html') # Serving the index file.

@app.route("/tr", methods=['POST', 'GET'])
def tr():
	sentence = request.form.get("sentence")	# Got the sentence.
	sentence = translate(sentence)	# Translating from the main.translate() function.
	return json.jsonify(sentence=sentence)

if __name__ == "__main__":
	app.debug = True	# Debugging.
	app.run()

