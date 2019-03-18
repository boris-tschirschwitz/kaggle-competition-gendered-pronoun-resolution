SHELL := /bin/bash

.DELETE_ON_ERROR:
.PHONY: all pipupgrade

all: processdata kaggle env/.requirements.lastrun .git | env data data/raw data/raw/gap-coreference

env:
	python3 -m venv $@
	ln -s $@/bin/activate activate

env/.requirements.lastrun: requirements.txt | env
	source activate && pip install --upgrade pip
	source activate && pip install -r requirements.txt
	touch $@

.git:
	git init
	git add .
	git commit -m "Initial commit"

pipupgrade: env/.requirements.lastrun
	source activate && pip install --upgrade pip
	source activate && pip install -U -r requirements.txt

data:
	mkdir $@

data/raw: | data
	mkdir $@

# Kaggle commands

.PHONY: kaggle processdata

kaggle: | data/raw env/.requirements.lastrun
ifeq (, $(wildcard data/raw/test_stage_1.tsv.zip))
	source activate && kaggle competitions download -c gendered-pronoun-resolution -p data/raw/
endif

data/raw/test_stage_1.tsv.zip: kaggle

# Download raw data from google-research-datasets/gap-coreference

data/raw/gap-coreference: | data/raw
	cd data/raw && git clone https://github.com/google-research-datasets/gap-coreference.git

# Preprocess data
data/processed: | data/raw
	mkdir $@

# unzip the test data into the processed data folder
data/processed/test_stage_1.tsv: data/raw/test_stage_1.tsv.zip | data/processed
	cd $(dir $@) && unzip ../../$< && chmod 0644 $(notdir $@) && touch $(notdir $@)

data/raw/gap-coreference/gap-development.tsv: | data/raw/gap-coreference

data/raw/gap-coreference/gap-test.tsv: | data/raw/gap-coreference

data/processed/gap.tsv: data/raw/gap-coreference/gap-development.tsv data/raw/gap-coreference/gap-test.tsv
	cp $< $@ && tail -n +2 $(word 2,$^) >> $@

data/processed/gap_with_types.tsv: data/processed/gap.tsv add_pronoun_types.py
	source activate && python add_pronoun_types.py $< $@

data/processed/single_match_with_types.tsv: data/processed/gap_with_types.tsv create_single_match_data.py
	source activate && python create_single_match_data.py $< $@

processdata: data/processed/test_stage_1.tsv data/processed/single_match_with_types.tsv

# Clean commands

.PHONY: envclean gitclean dataclean rawclean

# clean everything that can be recreated from raw data
clean: processeddataclean

envclean:
	rm -f activate
	rm -rf env

gitclean:
	rm -rf .git

alldataclean: rawclean
ifneq (, $(wildcard data))
	rm -rf data
endif

rawclean:
ifneq (, $(wildcard data/raw))
	rm -rf data/raw
endif

allbutraw := $(filter-out data/raw,$(wildcard data/*))
processeddataclean:
ifneq (, $(allbutraw))
	rm -rf $(allbutraw)
endif
