class CnnInput:
    def __init__(self, word_vectors):
        self.word_vectors = word_vectors
        self.window_left = 100
        self.window_right = 60

    def prepare_input(self, text, pronoun, pronoun_offset, a, a_offset, b, b_offset):
        tokens = self.word_vectors.tokenize(text)
        tokens_size = len(tokens)
        pronoun_index, _ = get_token_annotations(tokens, pronoun, pronoun_offset)
        a_index, a_size = get_token_annotations(tokens, a, a_offset)
        b_index, b_size = get_token_annotations(tokens, b, b_offset)
        input_offset = self.window_left - pronoun_index
        input_size = self.window_left + self.window_right
        input = []
        for i in range(input_size):
            if i >= input_offset and i < input_offset + tokens_size:
                text_annotation = 1
                word_vector_index = tokens[i - input_offset][1]
            else:
                text_annotation = 0
                word_vector_index = -1
            if i >= input_offset + a_index and i < input_offset + a_index + a_size:
                a_annotation = 1
            else:
                a_annotation = 0
            if i >= input_offset + b_index and i < input_offset + b_index + b_size:
                b_annotation = 1
            else:
                b_annotation = 0
            row = [text_annotation, a_annotation, b_annotation] + self.word_vectors.get_vector_from_index(word_vector_index)
            input.append(row)
        return input


def get_token_annotations(tokens, t, t_offset):
    t_index = next(i for i,t in enumerate(tokens) if t[2] == t_offset)
    t_text = t.replace(' ', '')
    t_size = 1
    t_words = tokens[t_index][0]
    while len(t_words)<len(t_text):
        t_words += tokens[t_index + t_size][0]
        t_size += 1
    return t_index, t_size
