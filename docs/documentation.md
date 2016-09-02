# Project documentation and overview

This document describes the project architecture, implementation methods, code, training of the translation model and more. If one needs to get a general idea of what this does and how it does it, or there is a need to get some in-depth information, this is the right place to get started, before diving into the code.

What this document covers:

1. Overview of the project purpose
2. Overview of the architecture
3. Overview of the code
4. Training the Moses translator
5. Final web server and translation server daemon setup

### 1. Overview of the project purpose

This is a statistical translation frontend, written with Python+Flask bundle. Basically, the purpose of the whole system is to provide an easy and access to the translation server daemon running in the backgroun on the server side of the application. In short, we get a Google Translate like web page.

### 2. Overview of the architecture

#### TODO: Add diagrams

### 3. Overview of the code

The front end consists of the following files:

1. `decoder.py` - decoder decorator, this communicates with Moses server daemon via XMLRPC technology
2. `main.py` - main execution script that can translate sentences via command line
3. `moses.config.json` - configuration file
4. `post_process.py` - post processing mechanisms
5. `pre_process.py` - pre processing mechanisms
6. `static/index.html` - main web page for the front end
7. `static/keyboard.js` - a library that transliterates English letters to Hebrew ones
8. `static/main.js` - main Javascript for `index.html`
9. `static/style.css` - CSS styles for `index.html`
10. `webserver.py` - Flask web server application

Additionally, `xcleanup.sh` is a Bash script that makes it easy to pre process the parallel texts taken from the TED talks - basic XML-like tags clean up.

Below are short overviews of each file. Only object / function signatures are mentioned, along with some code. Note that not all the implementation is listed.

1. `decoder.py`

	```python
	class Decoder:
		def __init__(self):
		def init_server(self, config):
			self.server = xmlrpclib.ServerProxy(config['host']) # Created a server object for the decoder
		def decode(self, tokens):
			translation = self.server.translate({'text': tokens})
	```

2. `main.py` 

	```python
	from pre_process import pre_process
	from decoder import Decoder
	from post_process import post_process
	
	def translate(sentence):
	if(__name__ == '__main__'):
		print(translate(sentence))
	```

3. `moses.config.json`

	```python
	{
		"start_cmd": "( ~/mosesdecoder/bin/moses -f ~/working/binarised-model/moses.ini --daemon --server --server-log ~/moses.log 2>>~/moses.log & )",
		"check_cmd": "pidof moses"
	}
	```

4. `post_process.py` (This is only echo back, no logic here yet)

	```python
	def post_process(sentence):
		return sentence
	```

5. `pre_process.py`

	```python
	def pre_process(sentence):
		with open('moses.config.json') as config_file:
		tokenized_sentence = p.communicate(input=sentence.encode('utf8'))[0]
		return tokenized_sentence
	```

6. `static/index.html`

	```html
	<html>
		<head>
		</head>
		<body>
			<form id="tr">
				<textarea id="source" data-keyboard="he"></textarea>
			</form>
	
		</body>
	</html>
	```

7. `static/keyboard.js`

	```javasctipt
	str = 'aשbנcבdגeקfכgעhיiןjחkלlךmצnמoםpפq/rרsדtאuוvהw\'xסyטzז,ת.ץ/.;ף\','; // Preparing character transliteration
	
	defer(function(){ // Waiting for jQuery
		$("[data-keyboard=he]").keypress(function(evt) { // Overriding default key press to transliterate English key strokes to hebrew letters
		});
		$.prototype.paste = function(text){	// Defining a function that will paste into text areas, respecting selection
		};
	});
	```

8. `static/main.js`

	```javascrtpt
	defer(function(){ // Waiting for jQuery
		$("form#tr").submit(function(){	// Don't submit form, instead send AJAX to retrieve translation
			$.ajax({
				url: "/tr",
			});
		});
	});
	```

9. `static/style.css`

	```css
	#source{ direction: rtl; }
	form#tr{ height: 50px; }
	form#tr>*, form#tr textarea{ height: 100%; }
	form#tr textarea{ width: 300px; }
	```

10. `webserver.py`

	```python
	from main import translate
	from flask import Flask, request, json
	
	@app.route("/tr", methods=['POST', 'GET'])
	def tr():
		try:
			sentence = translate(sentence)	# Translating from the main.translate() function.
		except socket_error as error:
			print "Exception when translating '" + sentence + "', socket_error: " + str(error)
	
	if __name__ == "__main__":
	```

