from Lexer import Token
from Parser import NodeBinaryOperation, NodeNumber, NodeUnaryOperation


class RuntimeError(Exception):

    def __init__(self, context, message):
        super().__init__(str(context)+message)


class Number:

    def __init__(self, value, context=None, position=None):
        self.value = value
        self.position = position
        self.context = context

    def addition(self, other):
        if isinstance(other, Number):
            return Number(self.value + other.value, context=self.context, position=self.position), None  # TODO: position not right

    def subtraction(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value, context=self.context), None

    def multiply(self, other):
        if isinstance(other, Number):
            return Number(self.value * other.value, context=self.context), None

    def division(self, other):
        if isinstance(other, Number):
            if other.value == 0:
                return None, RuntimeError(self.context, f'at position {other.position} Division by zero')
            return Number(self.value / other.value, context=self.context), None

    def __repr__(self):
        return f'{self.value}'


class RuntimeResult:

    def __init__(self, error=None, value=None):
        self.error = error
        self.value = value

    def register(self, result):
        if result.error:
            self.error = result.error
        return result.value

    def success(self, value):
        self.value = value
        return self

    def failure(self, error):
        self.error = error
        return self


class Context:

    def __init__(self, display_name, parent=None, parent_entry_position=None):
        self.display_name = display_name
        self.parent = parent
        self.parent_entry_position = parent_entry_position

    def __repr__(self):
        p = self.parent if self.parent else ''
        return f"Traceback of the most recent Calls\nPosition       Name\n{self.parent_entry_position},      {self.display_name}\n{p}"


class Interpreter:

    def visit(self, node, context):
        method_name = f"visit_{type(node).__name__}"
        method = getattr(self, method_name, self.no_visit_method)
        return method(node, context)

    def no_visit_method(self, node):
        raise Exception(f"No visit_{type(node).__name__} method defined")

    def visit_NodeNumber(self, node: NodeNumber, context):
        runtime_result = RuntimeResult()
        return runtime_result.success(Number(node.token.value, context))

    def visit_NodeBinaryOperation(self, node: NodeBinaryOperation, context):
        runtime_result = RuntimeResult()
        left = runtime_result.register(self.visit(node.left_node, context))
        if runtime_result.error:
            return runtime_result
        right = runtime_result.register(self.visit(node.right_node, context))
        if runtime_result.error:
            return runtime_result
        method_name = f"{str(node.operation_token.type).split('.')[1].lower()}"
        result, error = getattr(left, method_name)(right)
        if error:
            return runtime_result.failure(error)
        return runtime_result.success(result)

    def visit_NodeUnaryOperation(self, node: NodeUnaryOperation, context):
        runtime_result = RuntimeResult()
        number = runtime_result.register(self.visit(node.node, context))

        if runtime_result.error:
            return runtime_result

        if node.operation_token.type == Token.SUBTRACTION:
            number, error = number.multiply(Number(-1))
            return runtime_result.failure(error)
        return runtime_result.success(number)
