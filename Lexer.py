from collections import namedtuple
from enum import Enum

TokenInfo = namedtuple("Tokens", ["type", "value", "position"])


class Token(Enum):
    INTEGER = "0123456789"
    FLOAT = INTEGER + "." + INTEGER
    SUBTRACTION = "-"
    ADDITION = "+"
    MULTIPLY = "*"
    DIVISION = "/"
    INVALID = "INV"
    EOF = "EOF"
    LPAREN = "("
    RPAREN = ")"
    # EXPRESSION = TERM or UNARYOP + TERM or TERM + BINARYOP + TERM


class Lex:
    myInput = None
    dot: int = None
    input_char = None
    tokenList = []

    def __init__(self, file_name):
        self.file_name = file_name
        self.start_lex()

    def get_input(self, file_name):
        with open(file_name, 'r') as file:
            self.myInput = file.read().replace('\n', ' ')

    def start_lex(self):
        self.get_input(self.file_name)
        self.dot = 0
        self.input_char = self.myInput[self.dot]

    def lex(self):
        while self.input_char != "EOF":
            self.identify_token()

    def get_next_char(self):
        try:
            self.dot += 1
            self.input_char = self.myInput[self.dot]
        except IndexError:
            self.input_char = "EOF"

    def get_next_string_of_ints(self):
        number = ""
        while True:
            number += self.input_char
            self.get_next_char()
            if self.input_char not in "0123456789":
                break
        return number

    def identify_token(self):
        start_dot = self.dot
        if self.input_char in "0123456789":
            input_number = self.get_next_string_of_ints()

            if self.input_char == ".":
                input_number += self.get_next_string_of_ints()
                self.tokenList.append(TokenInfo(Token.FLOAT, input_number, start_dot))
            else:
                self.tokenList.append(TokenInfo(Token.INTEGER, input_number, start_dot))

        elif self.input_char == "+":
            self.tokenList.append(TokenInfo(Token.ADDITION, self.input_char, start_dot))
            self.get_next_char()
        elif self.input_char == "-":
            self.tokenList.append(TokenInfo(Token.SUBTRACTION, self.input_char, start_dot))
            self.get_next_char()
        elif self.input_char == "*":
            self.tokenList.append(TokenInfo(Token.MULTIPLY, self.input_char, start_dot))
            self.get_next_char()
        elif self.input_char == "/":
            self.tokenList.append(TokenInfo(Token.DIVISION, self.input_char, start_dot))
            self.get_next_char()
        elif self.input_char == "(":
            self.tokenList.append(TokenInfo(Token.LPAREN, self.input_char, start_dot))
            self.get_next_char()
        elif self.input_char == ")":
            self.tokenList.append(TokenInfo(Token.RPAREN, self.input_char, start_dot))
            self.get_next_char()
        else:
            self.tokenList.append(TokenInfo(Token.INVALID, self.input_char, start_dot))
            self.get_next_char()

        if self.input_char == "EOF":
            self.tokenList.append(TokenInfo(Token.EOF, "EOF", start_dot))


if __name__ == "__main__":
    lex = Lex("input.txt")

    lex.start_lex()

    while True:
        while lex.input_char != "EOF":
            lex.identify_token()

        print("Die Geparsten Tokens lauten: ")
        for obj in lex.tokenList:
            print(obj.value, end=" AND ")
        print()
        print(lex.tokenList)
        break
