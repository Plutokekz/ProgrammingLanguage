from pprint import pprint

from Interpreter import Interpreter
from Lexer import Lex
from Parser import Parser

lex = Lex()
parser = Parser()
interpreter = Interpreter()
while True:
    string = input('> ')
    lex.lex_string(string)
    tokens = lex.tokenList
    node = parser.parse(tokens).node
    print(node)
    print(interpreter.visit(node))
