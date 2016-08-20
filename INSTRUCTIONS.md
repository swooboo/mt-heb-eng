# How to train Moses so this translator works:

For all the below steps - document each step, which files were used, which actions, etc.

### Download and clean the corpus:

* `mkdir ~/corpus ;cd ~corpus`
* Download the corpus, I used [this HE-EN corpus](http://wit3.fbk.eu/archive/2014-01//texts/he/en/he-en.tgz):
	* `wget https://wit3.fbk.eu/archive/2014-01//texts/he/en/he-en.tgz`
* Extract it:
	* `tar -xzvf he-en.tgz ;mv he-en training`
* Change directory to the extracted location:
	* `cd training`
* Clean XML and tags files:
	* `~/translator/xcleanup.sh`
	* This will create a `trainig/clean/` directory with the cleaned files
* Divide the files by roles, take a side note. We will need files for:
	* Sentences for training (biggest set)
	* Sentences for tuning (smallest set)
	* Sentences for testing (validation, about 2-3% from training set)
 
### Prepare the corpus for Moses training:

* Tutorial taken from the [Moses website](http://www.statmt.org/moses/?n=Moses.Baseline)
	* In the tutorial, a French → English model was trained. We will train Hebrew → English instead.
	* Assuming Moses is installed in `~/mosesdecoder` directory.
* Tokenize the sentences:

	```bash
	for file in ~/corpus/training/clean/*he-en.en*
	do
	  ~/mosesdecoder/scripts/tokenizer/tokenizer.perl -l en \
	    <$file \
	    >~/corpus/`basename $file`.tok
	done
	```
	```bash
	for file in ~/corpus/training/clean/*he-en.he*
	do
	  ~/mosesdecoder/scripts/tokenizer/tokenizer.perl -l he \
	    <$file \
	    >~/corpus/`basename $file`.tok
	done
	```
* Train and apply the true casing:

	```bash
	~/mosesdecoder/scripts/recaser/train-truecaser.perl \
	  --model ~/corpus/truecase-model.en --corpus \
	  ~/corpus/train.tags.he-en.en.clean.tok
	
	~/mosesdecoder/scripts/recaser/train-truecaser.perl \
	  --model ~/corpus/truecase-model.he --corpus \
	  ~/corpus/train.tags.he-en.he.clean.tok
	```
	```bash
	for file in ~/corpus/*he-en.en*
	do
	  ~/mosesdecoder/scripts/recaser/truecase.perl \
	    --model ~/corpus/truecase-model.en \
	    <$file \
	    >~/corpus/`basename $file`.true.en
	done
	
	for file in ~/corpus/*he-en.he*
	do
	  ~/mosesdecoder/scripts/recaser/truecase.perl \
	    --model ~/corpus/truecase-model.he \
	    <$file \
	    >~/corpus/`basename $file`.true.he
	done
	```
 * Note that we added `.en` and `.he` to the `.true`, we will need this for the next step.
* Clean and limit to 80 tokens:

	```bash
	for file in ~/corpus/*he-en.en*clean.tok.true*
	do
	  mv $file ${file//he-en.??/he-en}
	done
	```
	```bash
	for file in ~/corpus/*he-en*clean.tok.true.en
	do
	  common_filename=${file//true.en/true}
	  ~/mosesdecoder/scripts/training/clean-corpus-n.perl \
	    $common_filename he en \
	    $common_filename.clean 1 80
	done
	```
 * Note that first code segment renames files so `he-en.en` and `he-en.he` will turn to `he-en`, because we need the language suffix to appear only in the end of the file name for the second code segment.
