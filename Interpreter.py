from Lexer import Token
from Parser import NodeBinaryOperation, NodeNumber, NodeUnaryOperation


class Number:

    def __init__(self, value, position=None):
        self.value = value
        self.position = position

    def addition(self, other):
        if isinstance(other, Number):
            return Number(self.value + other.value, self.position)  # TODO: position not right

    def subtraction(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value)

    def multiply(self, other):
        if isinstance(other, Number):
            return Number(self.value * other.value)

    def division(self, other):
        if isinstance(other, Number):
            return Number(self.value / other.value)

    def __repr__(self):
        return f'{self.value}'


class Interpreter:

    def visit(self, node):
        method_name = f"visit_{type(node).__name__}"
        method = getattr(self, method_name, self.no_visit_method)
        return method(node)

    def no_visit_method(self, node):
        raise Exception(f"No visit_{type(node).__name__} method defined")

    def visit_NodeNumber(self, node: NodeNumber):
        return Number(node.token.value)

    def visit_NodeBinaryOperation(self, node: NodeBinaryOperation):
        left = self.visit(node.left_node)
        right = self.visit(node.right_node)
        method_name = f"{str(node.operation_token.type).split('.')[1].lower()}"
        return getattr(left, method_name)(right)

    def visit_NodeUnaryOperation(self, node: NodeUnaryOperation):
        number = self.visit(node.node)
        if node.operation_token.type == Token.SUBTRACTION:
            number = number.multiply(Number(-1))
        return number
