from lexer import Lexer

class Tokenization:
    def __init__(self, file,input_file_name):
        self.readed_file = file
        self.token_file = []
        self.input_file_name = input_file_name


    def tokenization_line(self):
        for line in self.reded_file:
            yield list(' '.join(line))

    def tokenization_file(self):
        for index,line in enumerate(self.readed_file):
            lemma = Lexer(line)
            lemma.lemma()
            for token in lemma.token_list:
                self.token_file.append((token, index))