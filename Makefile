SHELL := /bin/bash

.DELETE_ON_ERROR:
.PHONY: all pipupgrade

all: kaggle env/.requirements.lastrun .git | env data data/raw

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

# Kaggle commands

.PHONY: kaggle

kaggle: | data/raw env/.requirements.lastrun
ifeq (, $(wildcard data/raw/*))
	source activate && kaggle competitions download -c gendered-pronoun-resolution -p data/raw/
endif
