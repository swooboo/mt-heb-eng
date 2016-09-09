# Aleph-null Statistical Translation System

## Abstract

Statistical translation system is a translation model trained using statistical analysis methods. We'll use parallel text method to achieve Hebrew to English translation of reasonable quality. Training the model is done by the Moses open source tool. For the front end of the translation and the communication with Moses model, Python is used in cunjunction with a Flask web server. Moses will be run in daemon-server mode, and Python program will communicate with it via XML-RPC protocol.

## Approach

A parallel corpus was aquired from Ted talks, which are conveniently translated, albeit some cleanup (XML and XML-like tags) was needed, and a tool was created for this, `xcleanup.sh`. The model was trained by Moses on a 24-core server. The training process is well-documented, and semi-automatic, meaning that one will only need to copy and paste Bash commands from the documentation into the shell, and the training will be done virtually without user interferance. Another part is setting up the web server for outside usage. In our case, the server was hidden behind a firewall, so outbound connections were tricky, but with some clever SSH tunnels, full Internet exposure was achieved. For this, another server was used, which is under control and outside of the aforementioned firewall, and in addition, dynamic DNS solution was used. Python was chosen as the language for the web server back end and front end. Specifically, web pages were served by Flask, which is a lightweight web framework Python, derived from Jango.

![Aleph-null](https://rawgit.com/swooboo/mt-heb-eng/master/docs/aleph0.svg)
