import os.path

class WordVectors:
    def __init__(self, algorithm, dimensions):
        self.algorithm = algorithm
        self.dimensions = dimensions
        self.sorted_words = []
        self.vectors = []

    def init(self):
        if self.algorithm == 'glove':
            # TODO ensure existence of glove files and initialize words and vectors
            return True
        return False

    def tokenize(self, text):
        if self.init():
            # TODO tokenize properly
            return text.split()
        else:
            return []
