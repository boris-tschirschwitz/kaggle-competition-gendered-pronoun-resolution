import os.path

class WordVectors:
    def __init__(self, algorithm, dimensions):
        self.algorithm = algorithm
        self.dimensions = dimensions
        self.sorted_words = []
        self.vectors = []

    def init(self):
        if self.algorithm == 'glove' and ensure_glove_files_exist():
            if len(self.sorted_words)>0:
                return True

            # read words from glove file and sort them by length
            cur_index = 0;
            with open('glove/glove.6B.' + str(self.dimensions) + 'd.txt') as f:
                for line in f:
                    word, *vector = line.split()
                    self.sorted_words.append([word, cur_index])
                    self.vectors.append(list(map(lambda v: float(v), vector)))
                    cur_index += 1
            self.sorted_words.sort(key=lambda x: len(x[0]), reverse=True)
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
