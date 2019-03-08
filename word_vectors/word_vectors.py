import os.path

class WordVectors:
    def __init__(self, algorithm, dimensions):
        self.algorithm = algorithm
        self.dimensions = dimensions
        self.sorted_words = []
        self.vectors = []

    def init(self):
        if self.algorithm == 'glove' and ensure_glove_files_exist():
            # TODO initialize words and vectors
            return True
        return False

    def tokenize(self, text):
        if self.init():
            # TODO tokenize properly
            return text.split()
        else:
            return []


def ensure_glove_files_exist():
    if (not(os.path.isfile('./glove/glove.6B.50d.txt')) or
        not(os.path.isfile('./glove/glove.6B.100d.txt')) or
        not(os.path.isfile('./glove/glove.6B.200d.txt')) or
        not(os.path.isfile('./glove/glove.6B.300d.txt'))):
        print("""

        Note: Please download the pre-trained GloVe word vectors from
        http://nlp.stanford.edu/data/glove.6B.zip, unzip them and copy
        the files into a 'glove' folder relative to this file.

        """)
        return False
    else:
        return True
