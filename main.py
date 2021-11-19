from pprint import pprint
from Lexer import Lex
from Parser import Parser

lex = Lex("input.txt")
lex.lex()
tokens = lex.tokenList
pprint(tokens)
parser = Parser(tokens)
pprint(parser.parse().node)
