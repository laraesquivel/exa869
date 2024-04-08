from reader import Reader
from tokenization import Tokenization
from writer import Writer

a = Reader()
a.list_files()

g= a.read_file()

exp = next(g)
t = Tokenization(exp[1],exp[0])
t.tokenization_file()

print(t.token_file)
#w = Writer(t.token_file,t.input_file_name)

#w.write()