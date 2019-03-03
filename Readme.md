# kaggle-competition-gendered-pronoun-resolution

Kaggle site: [Gendered Pronoun Resolution](https://www.kaggle.com/c/gendered-pronoun-resolution).
After the Google AI repository is cloned, have a look at its [Readme](data/raw/gap-coreference/README.md), direct repository link: [Readme](https://github.com/google-research-datasets/gap-coreference/blob/master/README.md).

## Preparation

The `kaggle` command used to download the Kaggle data requires the local file `~/.kaggle/kaggle.json` for authentication.

To create this file log into your account at [kaggle](https://www.kaggle.com),
go to "My account" and  Click on "Create new API Token".
This will download the file 'kaggle.json'.

Copy this file to `~/.kaggle/kaggle.json`.

## Build

```bash
cd kaggle-competition-gendered-pronoun-resolution
make
```

Now the raw Kaggle data can be found in 'data/raw'.
Switch to the project's virtual environment with

```bash
source activate.
```

You'll want to add more Python packages to your project
by adjusting 'requirements.txt'. Then call make again to
run pip.

The idea now is to next add new targets to the Makefile
to process the raw data, etc.

To remove all processed data call:

```bash
make clean
```

To update the installed Python packages run

```bash
make pipupgrade
```
