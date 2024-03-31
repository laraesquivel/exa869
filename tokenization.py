

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
                for word in line.split():
                    l = list(' '.join(word))
                    self.token_file.append((l, index))