from Lexer import Token, TokenInfo


class NodeNumber:

    def __init__(self, token):
        self.token = token

    def __repr__(self):
        return f"{self.token.value}"


class NodeBinaryOperation:

    def __init__(self, left_node, operation_token, right_node):
        self.left_node = left_node
        self.right_node = right_node
        self.operation_token = operation_token

    def __repr__(self):
        return f"({self.left_node} {self.operation_token.value} {self.right_node})"


class NodeUnaryOperation:

    def __init__(self, operation_token, node):
        self.operation_token = operation_token
        self.node = node

    def __repr__(self):
        return f"({self.operation_token.value} {self.node})"


class InvalidSyntaxError(SyntaxError):
    pass


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
        result = self.expression()
        if not result.error and self.current_token.type != Token.EOF:
            return result.failure(InvalidSyntaxError(
                f"at position {self.current_token.position} Expected end of input, got {self.current_token.type}"))
        return result

    def factor(self):
        result = ParserResult()
        token = self.current_token

        # einzelnes plus oder minus vor der zahl bindet am meisten
        if token.type in (Token.ADDITION, Token.SUBTRACTION):
            result.register(self.advance())
            node = result.register(self.factor())
            if result.error:
                return result
            return result.success(NodeUnaryOperation(token, node))

        elif token.type in (Token.INTEGER, Token.FLOAT):
            result.register(self.advance())
            return result.success(NodeNumber(token))

        elif token.type == Token.LPAREN:
            result.register(self.advance())
            node = result.register(self.expression())
            if result.error:
                return result
            if self.current_token.type == Token.RPAREN:
                result.register(self.advance())
                return result.success(node)
            else:
                return result.failure(InvalidSyntaxError(
                    f"at position {self.current_token.position} Expected ')', got {self.current_token.type}"))

        return result.failure(InvalidSyntaxError(
            f"at position {self.current_token.position} Expected a number, got {self.current_token.type}"))

    def term(self):
        return self._operation(self.factor, (Token.MULTIPLY, Token.DIVISION))

    def _operation(self, func, token_types):
        result = ParserResult()
        left = result.register(func())
        if result.error:
            return result
        while self.current_token.type in token_types:
            operation_token = self.current_token
            result.register(self.advance())
            right = result.register(func())
            if result.error:
                return result
            left = NodeBinaryOperation(left, operation_token, right)
        return result.success(left)

    def expression(self):
        return self._operation(self.term, (Token.ADDITION, Token.SUBTRACTION))


class ParserResult:

    def __init__(self):
        self.error = None
        self.node = None

    def register(self, result):
        if isinstance(result, ParserResult):
            if result.error:
                self.error = result.error
            return result.node
        return result

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        self.error = error
        return self


if __name__ == "__main__":
    tokens = [TokenInfo(Token.INTEGER, "1", None), TokenInfo(Token.ADDITION, "+", None),
              TokenInfo(Token.INTEGER, "2", None), TokenInfo(Token.MULTIPLY, "*", None),
              TokenInfo(Token.INTEGER, "3", None)]
    parser = Parser(tokens)
    print(parser.parse())
