# Statistical Translation System

## Abstract

Statistical translation system is a translation model trained using statistical analysis methods. We'll use parallel text method to achieve Hebrew to English translation of reasonable quality. Training the model is done by the Moses open source tool. For the front end of the translation and the communication with Moses model, Python is used in cunjunction with a Flask web server. Moses will be run in daemon-server mode, and Python program will communicate with it via XML-RPC protocol.
