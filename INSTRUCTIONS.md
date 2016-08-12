# How to train Moses so this translator works:

* Download the corpus, I used [[//wit3.fbk.eu/archive/2014-01//texts/he/en/he-en.tgz]]
* Extract it:
	* `tar -xzvf he-en.tgz`
* Change directory to the extracted location:
	* `cd he-en`
* Clean XML and tags files:
	* `~/translator/xcleanup.sh`
	* This will create a `he-en/clean/` directory with the cleaned files
 
