# Web server deployment instructions

The front end of the project is a Flask-based web service, written in Python. This document describes the web server deployment process.

### Prequisites:

* A Linux server on which the server will run. Should be exposed to the Internet, with the ability to open ports
	* If the server is not exposed, but connected to the internet, there is a way to tunnel the ports with SSH.
* Flask web server installed on the aforementioned server
* The source code of the service [here](https://github.com/swooboo/mt-heb-eng.git):
* Translation model trained by moses, [instructions](https://github.com/swooboo/mt-heb-eng/blob/master/docs/training_instructions.md)
* Patience

### Working plan:

1. Get the source code
2. Apply the configurations
3. Run the server
4. (Optional) Set up SSH tunneling, in case the server is not exposed

### Get the source code

* Clone from Git:
	
	```bash
	git clone https://github.com/swooboo/mt-heb-eng.git
	cd mt-heb-eng
	```
* Check the configuration file, defaults should be fine:

	```
	$ cat ./moses.config.json
	{
			"name": "moses",
			"host": "http://localhost:8080/RPC2",
			"start_cmd": "( ~/mosesdecoder/bin/moses -f ~/working/binarised-model/moses.ini --daemon --server --server-log ~/moses.log 2>>~/moses.log & )",
			"check_cmd": "pidof moses",

			"tokenize_cmd": "~/mosesdecoder/scripts/tokenizer/tokenizer.perl -l en"
	}
	```
