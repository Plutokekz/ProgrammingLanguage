from enum import Enum

UNDERSCORE = '_'
NEWLINE = '\n'
HASHTAG = '#'
WHITESPACE = ' '
OPERATOR = '+-*/'
SEPARATOR = ';,(){}:'


class Token(Enum):
    EoF = 0
    IDENTIFIER = 1
    INTEGER = 2
    ERRONEOUS = 3
    OPERATOR = 4
    SEPARATOR = 5


class PositionInFile:
    file_name: str
    line_number: int
    char_number: int

    def __init__(self, file_name, line_number, char_number):
        self.file_name: str = file_name
        self.line_number: int = line_number
        self.char_number: int = char_number

    def __repr__(self):
        return f"PositionInFile(name: {self.file_name}, line: {self.line_number}, character: {self.char_number})"


class TokenType:
    type: Token
    _repr: str
    position_in_file: PositionInFile

    def __init__(self, _type, _repr, position_in_file):
        self.type = _type
        self._repr = _repr
        self.position_in_file = position_in_file

    def __repr__(self):
        return f"TokenType(type: {self.type}, repr: <{self._repr}>, position: {self.position_in_file})"


class Lexer:
    dot: int
    line: int
    char: int
    current_char: chr
    input: str
    input_length: int
    done: bool

    def __init__(self, file_name):
        self.dot = 0
        self.char = 1
        self.line = 1
        self.done = False
        self.file_name = file_name
        self._read_file()

    def _read_file(self):
        with open(self.file_name, "r", encoding="utf-8") as fp:
            self.input = fp.read()
            self.input_length = len(self.input)
            self.current_char = self.input[0]

    def __iter__(self):
        self.dot = 0
        self.char = 1
        self.line = 1
        self.done = False
        self.current_char = self.input[0]
        self.input_length = len(self.input)
        return self

    def __next__(self):
        t = lexer.get_next_token()
        if self.done:
            raise StopIteration
        if t.type == Token.EoF:
            self.done = True
        return t

    def next_char(self):
        if self.dot + 1 < self.input_length:
            self.dot += 1
            self.char += 1
            self.current_char = self.input[self.dot]
            if self.current_char == '\n':
                self.line += 1
                self.char = 0

    def previous_char(self):
        self.dot -= 1
        self.current_char = self.input[self.dot]

    def _is_end_of_input(self):
        return self.dot + 1 >= len(self.input)

    def _is_letter(self):
        return self.current_char.isalpha()

    def _is_digit(self):
        return self.current_char.isdigit()

    def _is_operator(self):
        return self.current_char in OPERATOR

    def _is_separator(self):
        return self.current_char in SEPARATOR

    def _is_layout(self):
        return not self._is_end_of_input() and self.current_char <= WHITESPACE

    def _is_comment_starter(self):
        return self.current_char == HASHTAG

    def _is_comment_stopper(self):
        return self._is_comment_starter() or self.current_char == NEWLINE

    def _is_letter_or_digit(self):
        return self._is_letter() or self._is_digit()

    def _is_underscore(self):
        return self.current_char == UNDERSCORE

    def skip_layout_and_comment(self):
        while self._is_layout():
            self.next_char()
        while self._is_comment_starter():
            self.next_char()
            while not self._is_comment_stopper():
                if self._is_end_of_input():
                    return
                self.next_char()
            self.next_char()
            while self._is_layout():
                self.next_char()

    def note_token_position(self):
        return PositionInFile(self.file_name, self.line, self.char)

    def _piek(self, func):
        self.next_char()
        x = func()
        self.previous_char()
        return x

    def recognize_identifier(self):
        self.next_char()
        while self._is_letter_or_digit():
            self.next_char()
        while self._is_underscore() and self._piek(self._is_letter_or_digit):
            self.next_char()
            while self._is_letter_or_digit():
                self.next_char()
        return Token.IDENTIFIER

    def recognize_integer(self):
        while self._is_digit():
            self.next_char()
        return Token.INTEGER

    def get_next_token(self) -> TokenType:
        _token: TokenType = TokenType(None, None, None)
        start_dot: int
        self.skip_layout_and_comment()
        _token.position_in_file = self.note_token_position()
        start_dot = self.dot
        if self._is_end_of_input():
            _token.type = Token.EoF
            _token.repr = "<EoF>"
        elif self._is_letter():
            _token.type = self.recognize_identifier()
        elif self._is_digit():
            _token.type = self.recognize_integer()
        elif self._is_operator():
            _token.type = Token.OPERATOR
            self.next_char()
        elif self._is_separator():
            _token.type = Token.SEPARATOR
            self.next_char()
        else:
            _token.type = Token.ERRONEOUS
            self.next_char()
        _token._repr = self.input[start_dot: self.dot]
        return _token


"""CREATE TABLE """

if __name__ == "__main__":
    lexer = Lexer("input.txt")
    for token in lexer:
        print(token)
