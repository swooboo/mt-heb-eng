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

Below are short overviews of each file.

1. `decoder.py`
```python

```
