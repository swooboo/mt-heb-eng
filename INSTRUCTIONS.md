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
	for file in ~/corpus/*he-en.en*clean.tok
	do
	  ~/mosesdecoder/scripts/recaser/truecase.perl \
	    --model ~/corpus/truecase-model.en \
	    <$file \
	    >${file//he-en.??/he-en}.true.en
	done
	
	for file in ~/corpus/*he-en.he*clean.tok
	do
	  ~/mosesdecoder/scripts/recaser/truecase.perl \
	    --model ~/corpus/truecase-model.he \
	    <$file \
	    >${file//he-en.??/he-en}.true.he
	done
	```
 * Note that we added `.en` and `.he` to the `.true`, and removed the language infix from `.he-en.??` we will need this for the next step - the file name pairs should be identical up until the suffix that denotes the language.
* Clean and limit to 80 tokens:

	```bash
	for file in ~/corpus/*he-en*clean.tok.true.en
	do
	  common_filename=${file//true.en/true}
	  ~/mosesdecoder/scripts/training/clean-corpus-n.perl \
	    $common_filename he en \
	    $common_filename.clean 1 80
	done
	```
* Summing up: we have prepared our corpus for training. The final files are listed with the following command - `ls ~/corpus/*clean.??`

### Training the language model

* Train a 3-gram model for English language:

	```bash
	mkdir -p ~/working/lm
 	cd ~/working/lm
 	~/mosesdecoder/bin/lmplz -o 3 \
 	  <~/corpus/train.tags.he-en.clean.tok.true.clean.en \
 	  >~/working/lm/train.tags.he-en.clean.tok.true.clean.arpa.en
 	```
* Binarise the model for faster queries:

	```bash
	~/mosesdecoder/bin/build_binary \
   	  ~/working/lm/train.tags.he-en.clean.tok.true.clean.arpa.en \
   	  ~/working/lm/train.tags.he-en.clean.tok.true.clean.blm.en
   	```
