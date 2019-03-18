import os.path
import re

LETTER_REGEX = re.compile(r'[a-zA-Z]')
NON_LETTER_REGEX = re.compile(r'[^a-zA-Z]')
DIGIT_REGEX = re.compile(r'[0-9]')
NON_DIGIT_REGEX = re.compile(r'[^0-9]')
LETTER_DIGIT_SPACE_REGEX = re.compile(r'[a-zA-Z0-9\s]');

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
            # read words from glove text file and sort them by length
            with open('glove/glove.6B.' + str(self.dimensions) + 'd.txt') as f:
                for i, line in enumerate(f):
                    word, *vector = line.split()
                    self.sorted_words.append([word, i])
                    self.vectors.append(list(map(lambda v: float(v), vector)))
            self.sorted_words.sort(key=lambda x: len(x[0]), reverse=True)
            print('Words initialized: ' + str(len(self.sorted_words)))
            return True
        return False

    def tokenize(self, text):
        if self.init():
            text = text.lower()
            tokens = []
            offset = 0
            while len(text)>0:
                word_with_index = self.get_first_word(text)
                word_with_index.append(offset)
                tokens.append(word_with_index)
                word_length = len(word_with_index[0])
                offset += word_length
                text = text[word_length:]
                if text.startswith(' '):
                    text = text[1:]
                    offset += 1
            return tokens
        else:
            return []

    def get_first_word(self, text):
        for word_with_index in self.sorted_words:
            if text == word_with_index[0]:
                return word_with_index.copy()
            if text.startswith(word_with_index[0]):
                last_char_of_word = text[len(word_with_index[0]) - 1]
                next_char = text[len(word_with_index[0])]
                if LETTER_REGEX.search(last_char_of_word) and LETTER_REGEX.search(next_char):
                    # A split between letters is not allowed. Return the word
                    # until the next non-letter chararecter as an unknown word.
                    return self.get_first_unknow_word(text, NON_LETTER_REGEX)
                elif DIGIT_REGEX.search(last_char_of_word) and DIGIT_REGEX.search(next_char):
                    # A split between digits is not allowed. Return the word
                    # until the next non-digit chararecter as an unknown word.
                    return self.get_first_unknow_word(text, NON_DIGIT_REGEX)
                else:
                    return word_with_index.copy()
        # handle an unknown first words
        first_char = text[0]
        if LETTER_REGEX.search(first_char):
            return self.get_first_unknow_word(text, NON_LETTER_REGEX)
        elif DIGIT_REGEX.search(first_char):
            return self.get_first_unknow_word(text, NON_DIGIT_REGEX)
        else:
            return self.get_first_unknow_word(text, LETTER_DIGIT_SPACE_REGEX)

    def get_first_unknow_word(self, text, next_token_regex):
        search_text = text[1:]
        next_token_position = next_token_regex.search(search_text).start() + 1
        word = text[:next_token_position]
        print('Word not found: ' + word)
        return [word, -1]

    def get_vector_from_index(self, index):
        if index == -1:
            return [0] * self.dimensions
        else:
            return self.vectors[index]

    def get_vector_columns(self):
        return list(map(lambda i: 'v' + str(i), range(self.dimensions)))


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
