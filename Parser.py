from Lexer import Token, TokenInfo


class NodeNumber:

    def __init__(self, token):
        self.token = token

    def __repr__(self):
        return f"NodeNumber(token: {self.token})"


class NodeBinaryOperation:

    def __init__(self, left_node, operation_token, right_node):
        self.left_node = left_node
        self.right_node = right_node
        self.operation_token = operation_token

    def __repr__(self):
        return f"NodeBinaryOperation(left: {self.left_node}, operation: {self.operation_token}, right: {self.right_node})"


class Parser:

    def __init__(self, tokens):
        self.tokens = tokens
        self.token_index = -1
        self.current_token = None
        self.advance()

    def advance(self):
        self.token_index += 1
        if self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index]
        return self.current_token

    def parse(self):
        return self.expression()

    def factor(self):
        if self.current_token.type in (Token.INTEGER, Token.FLOAT):
            token = self.current_token
            self.advance()
            return NodeNumber(token)

    def term(self):
        return self._operation(self.factor, (Token.MULTIPLY, Token.DIVISION))

    def _operation(self, func, token_types):
        left = func()
        while self.current_token.type in token_types:
            operation_token = self.current_token
            self.advance()
            right = func()
            left = NodeBinaryOperation(left, operation_token, right)
        return left

    def expression(self):
        return self._operation(self.term, (Token.ADDITION, Token.SUBTRACTION))


if __name__ == "__main__":
    tokens = [TokenInfo(Token.INTEGER, "1", None), TokenInfo(Token.ADDITION, "+", None),
              TokenInfo(Token.INTEGER, "2", None), TokenInfo(Token.MULTIPLY, "*", None),
              TokenInfo(Token.INTEGER, "3", None)]
    parser = Parser(tokens)
    print(parser.parse())
