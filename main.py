from pprint import pprint

from Interpreter import Interpreter, Context
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
    context = Context('<Calculator>')
    result = interpreter.visit(node, context)
    if result.error:
        print(result.error)
    else:
        pprint(result.value)
