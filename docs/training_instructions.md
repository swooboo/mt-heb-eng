# How to train your Moses:

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
* We will divide our data as described in the table below:

| File name                                                                    | # of sentences | Lang.    | Role   |
|------------------------------------------------------------------------------|----------------|:--------:|:------:|
| `~/corpus/training/clean/IWSLT14.TED.dev2010.he-en.en.xml.clean`             | 949            | EN       | tune   |
| `~/corpus/training/clean/IWSLT14.TED.dev2010.he-en.he.xml.clean`             | 949            | HE       | tune   |
| `~/corpus/training/clean/IWSLT14.TED.tst2010.he-en.en.xml.clean`             | 1650           | EN       | test   |
| `~/corpus/training/clean/IWSLT14.TED.tst2010.he-en.he.xml.clean`             | 1650           | HE       | test   |
| `~/corpus/training/clean/IWSLT14.TED.tst2011.he-en.en.xml.clean`             | 1553           | EN       | test   |
| `~/corpus/training/clean/IWSLT14.TED.tst2011.he-en.he.xml.clean`             | 1553           | HE       | test   |
| `~/corpus/training/clean/IWSLT14.TED.tst2012.he-en.en.xml.clean`             | 1812           | EN       | test   |
| `~/corpus/training/clean/IWSLT14.TED.tst2012.he-en.he.xml.clean`             | 1812           | HE       | test   |
| `~/corpus/training/clean/train.tags.he-en.en.clean`                          | 192185         | EN       | train  |
| `~/corpus/training/clean/train.tags.he-en.he.clean`                          | 192185         | HE       | train  |

### Prepare the corpus for Moses training:

* Tutorial taken from the [Moses website](http://www.statmt.org/moses/?n=Moses.Baseline)
	* In the tutorial, a French to English model was trained. We will train Hebrew to English instead.
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

### Training the Language Model

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
* Test the language model with a simple English sentence:

	```bash
	echo "is this an English sentence ?" \
	  | ~/mosesdecoder/bin/query ~/working/lm/train.tags.he-en.clean.tok.true.clean.blm.en
	```
 * The example above should yield the output below:
 
		```
		$ echo "is this an English sentence ?" \
		>   | ~/mosesdecoder/bin/query ~/working/lm/train.tags.he-en.clean.tok.true.clean.blm.en
		is=18 2 -2.7017515      this=65 3 -0.8656755    an=188 3 -2.3518038     English=3600 2 -2.768621 sentence=7252 2 -2.3785648        ?=73 2 -2.4919968       </s>=2 3 -0.22995311    Total: -13.788365 OOV: 0
		Perplexity including OOVs:      93.27526264042754
		Perplexity excluding OOVs:      93.27526264042754
		OOVs:   0
		Tokens: 7
		Name:query      VmPeak:74968 kB VmRSS:1676 kB   RSSMax:52468 kB user:0  sys:0.012998    CPU:0.012998 real:0.0114762
		```

### Training, Tuning and Testing the Translation System

* Train the translation model:

	```bash
	mkdir -p ~/working
	cd ~/working
	nohup nice ~/mosesdecoder/scripts/training/train-model.perl -root-dir ~/working/train \
	 -corpus ~/corpus/train.tags.he-en.clean.tok.true.clean \
	 -f he -e en -alignment grow-diag-final-and -reordering msd-bidirectional-fe \
	 -lm 0:3:$HOME/working/lm/train.tags.he-en.clean.tok.true.clean.blm.en:8 \
	 -cores 24 \
	 -external-bin-dir ~/mosesdecoder/tools >& training.out &
	```
	* Note that `-cores 24` is for 24-core server, choose the number of cores correctly.
* Tune the translation model:

	```bash
	cd ~/working
	nohup nice ~/mosesdecoder/scripts/training/mert-moses.pl \
	  ~/corpus/IWSLT14.TED.dev2010.he-en.xml.clean.tok.true.clean.he \
	  ~/corpus/IWSLT14.TED.dev2010.he-en.xml.clean.tok.true.clean.en  \
	  ~/mosesdecoder/bin/moses ~/working/train/model/moses.ini --mertdir ~/mosesdecoder/bin/ \
	  --decoder-flags="-threads 24" \
	  &> mert.out &
	```
	* Note the `--decoder-flags="-threads 24"` is set for 24 cores, adjust accordingly.
* Test the translation system with a simple sentence. Run the following and then enter a sentence in Hebrew:

	```bash
	~/mosesdecoder/bin/moses -f ~/working/mert-work/moses.ini
	```
	* The system loads somewhat slowly, next step - we binarise the model for faster queries.
* Binarise the translation model:

	```bash
	mkdir ~/working/binarised-model
	cd ~/working
	~/mosesdecoder/bin/processPhraseTableMin \
	  -in ~/working/train/model/phrase-table.gz -nscores 4 \
	  -out ~/working/binarised-model/phrase-table
	~/mosesdecoder/bin/processLexicalTableMin \
	  -in ~/working/train/model/reordering-table.wbe-msd-bidirectional-fe.gz \
	  -out ~/working/binarised-model/reordering-table
	```
	```bash
	sed \
	  's/PhraseDictionaryMemory/PhraseDictionaryCompact/;
	    s/train.model.phrase-table.gz/binarised-model\/phrase-table.minphr/;
	    s/train.model.reordering-table.wbe-msd-bidirectional-fe.gz/binarised-model\/reordering-table/' \
	  ~/working/mert-work/moses.ini \
	  >~/working/binarised-model/moses.ini
	```
	* [OPTIONAL READING - this is an explanation of the `sed` command] The second code segment will modify the moses configuration file (the `moses.ini` that was generated as a result of training the translation system) to the binarised model directory after making the following edits:
		1. Change `PhraseDictionaryMemory` to `PhraseDictionaryCompact`
		2. Set the path of the `PhraseDictionary` feature to point to `$HOME/working/binarised-model/phrase-table.minphr`
		3. Set the path of the `LexicalReordering` feature to point to `$HOME/working/binarised-model/reordering-table`
		4. Exit the editor and save with the following keystrokes: `^O ENTER ^X`
* Now we can load faster and test with our favorite Hebrew sentence. Run Moses with the binarised model (faster) as follows:

	```bash
	~/mosesdecoder/bin/moses -f ~/working/binarised-model/moses.ini
	```

### Evaluating the translation system

* As noted in the table in the beginning of this document, we have multiple files for testing. First, we need to 'clump' them together:

	```bash
	cd ~/working
	mkdir -p ~/working/testing
	cat ~/corpus/*tst*tok.true.clean.en >~/working/testing/testset.en
	cat ~/corpus/*tst*tok.true.clean.he >~/working/testing/testset.he
	```
* Filter our translation model only for the sentences we want to translate - for faster results:

	```bash
	~/mosesdecoder/scripts/training/filter-model-given-input.pl \
	  ~/working/testing/filtered-testset ~/working/mert-work/moses.ini ~/working/testing/testset.he \
	  -Binarizer ~/mosesdecoder/bin/processPhraseTableMin
	  -threads 24
	```
	* Again, `-threads 24` - adjust accordingly.
* Now, we want to translate the Hebrew test set into English, and compare the translation to the 'original' translations:

	```bash
	nohup nice ~/mosesdecoder/bin/moses \
	  -f ~/working/testing/filtered-testset/moses.ini \
	  < ~/working/testing/testset.he \
	  > ~/working/testing/testset.translated.en \
	  2> ~/working/testing/moses-testset.out
	```
* So far we have the set we translated with Moses, and the one we got from 'outside', which is supposed to be very good. Let's test how good our translation is, in comparison with this 'very good' one, using BLEU evaluation:

	```bash
	~/mosesdecoder/scripts/generic/multi-bleu.perl \
	  -lc ~/working/testing/testset.en \
	  <~/working/testing/testset.translated.en
	```
	* The command should yield the following output (we should get a BLEU score of 30.31):
	
		```bash
		$ ~/mosesdecoder/scripts/generic/multi-bleu.perl   -lc ~/working/testing/testset.en   <~/working/testing/testset.translated.en
		BLEU = 30.31, 63.2/36.4/23.5/15.6 (BP=1.000, ratio=1.023, hyp_len=95620, ref_len=93431)
		```
