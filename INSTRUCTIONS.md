# How to train Moses so this translator works:

For all the below steps - document each step, which files were used, which actions, etc.

### Download and clean the corpus:

* Download the corpus, I used http://wit3.fbk.eu/archive/2014-01//texts/he/en/he-en.tgz
* Extract it:
	* `tar -xzvf he-en.tgz`
* Change directory to the extracted location:
	* `cd he-en`
* Clean XML and tags files:
	* `~/translator/xcleanup.sh`
	* This will create a `he-en/clean/` directory with the cleaned files
* Divide the files by roles, take a side note. We will need files for:
	* Sentences for training (biggest set)
	* Sentences for tuning (smallest set)
	* Sentences for testing (validation, about 2-3% from training set)
 
### Prepare the corpus for Moses training:

* Tutorial taken from the [Moses website](http://www.statmt.org/moses/?n=Moses.Baseline)
	* In the tutorial, a French → English model was trained. We will train Hebrew → English instead.
* Tokenize the sentences:
	* ` ~/mosesdecoder/scripts/tokenizer/tokenizer.perl -l en \`
	* `< ~/corpus/training/news-commentary-v8.fr-en.en    \`
	* `> ~/corpus/news-commentary-v8.fr-en.tok.en`
	* `~/mosesdecoder/scripts/tokenizer/tokenizer.perl -l fr \`
	* `< ~/corpus/training/news-commentary-v8.fr-en.fr    \`
	* `> ~/corpus/news-commentary-v8.fr-en.tok.fr`
