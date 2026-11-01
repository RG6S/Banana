"""Interpreter for the Banana programming language, Part 5."""

import sys
from pathlib import Path

from ast_nodes import (
    AssignmentNode,
    BinaryOpNode,
    ForNode,
    FunctionCallNode,
    FunctionDefNode,
    IfNode,
    NumberNode,
    PrintNode,
    ProgramNode,
    ReturnNode,
    UnaryOpNode,
    VariableNode,
    WhileNode,
)


class RuntimeErrorBanana(Exception):
    """Raised when a Banana program has a runtime error."""


class ReturnSignal(Exception):
    """Internal signal used to return a value from a function."""

    def __init__(self, value):
        super().__init__()
        self.value = value


class Interpreter:
    def __init__(self):
        # The global environment remains available as self.environment.
        self.environment = {}
        self.scopes = [self.environment]
        self.functions = {}
        self.output = []

    def find_variable_scope(self, name):
        """Find a variable in the current function scope or global scope."""
        current_scope = self.scopes[-1]

        if name in current_scope:
            return current_scope

        # Functions can access global variables, but not caller-local variables.
        if len(self.scopes) > 1 and name in self.environment:
            return self.environment

        return None

    def execute(self, node):
        """Execute a statement or program node."""

        if isinstance(node, ProgramNode):
            for statement in node.statements:
                self.execute(statement)

        elif isinstance(node, AssignmentNode):
            self.execute_assignment(node)

        elif isinstance(node, PrintNode):
            value = self.evaluate(node.expression)
            text = str(value)
            print(text)
            self.output.append(text)

        elif isinstance(node, IfNode):
            if self.evaluate(node.condition):
                for statement in node.then_branch:
                    self.execute(statement)
            else:
                for statement in node.else_branch:
                    self.execute(statement)

        elif isinstance(node, WhileNode):
            while self.evaluate(node.condition):
                for statement in node.body:
                    self.execute(statement)

        elif isinstance(node, ForNode):
            self.execute_for(node)

        elif isinstance(node, FunctionDefNode):
            if node.name in self.functions:
                raise RuntimeErrorBanana(
                    f"Function '{node.name}' is already defined"
                )
            self.functions[node.name] = node

        elif isinstance(node, FunctionCallNode):
            # A function call may be used as a standalone statement.
            self.evaluate(node)

        elif isinstance(node, ReturnNode):
            if len(self.scopes) == 1:
                raise RuntimeErrorBanana(
                    "'return' cannot be used outside a function"
                )
            raise ReturnSignal(self.evaluate(node.expression))

        else:
            raise RuntimeErrorBanana(
                f"Unsupported statement: {type(node).__name__}"
            )

    def execute_assignment(self, node):
        """Execute declarations, assignments, and compound assignments."""

        name = node.name
        operator = node.operator
        current_scope = self.scopes[-1]

        if node.is_declaration:
            if name in current_scope:
                raise RuntimeErrorBanana(
                    f"Variable '{name}' is already declared in this scope"
                )

            value = self.evaluate(node.value)
            current_scope[name] = value
            return

        target_scope = self.find_variable_scope(name)

        if target_scope is None:
            raise RuntimeErrorBanana(
                f"Undefined variable '{name}'"
            )

        value = self.evaluate(node.value)

        if operator == "=":
            target_scope[name] = value

        elif operator == "+=":
            target_scope[name] += value

        elif operator == "-=":
            target_scope[name] -= value

        elif operator == "*=":
            target_scope[name] *= value

        elif operator == "/=":
            if value == 0:
                raise RuntimeErrorBanana("Division by zero")
            target_scope[name] /= value

        else:
            raise RuntimeErrorBanana(
                f"Invalid assignment operator '{operator}'"
            )

    def execute_for(self, node):
        """Execute a for loop with initialization, condition, and increment."""

        self.execute(node.initializer)

        while self.evaluate(node.condition):
            for statement in node.body:
                self.execute(statement)

            self.execute(node.increment)

    def evaluate(self, node):
        """Evaluate an expression and return its value."""

        if isinstance(node, NumberNode):
            return node.value

        if isinstance(node, VariableNode):
            scope = self.find_variable_scope(node.name)

            if scope is None:
                raise RuntimeErrorBanana(
                    f"Undefined variable '{node.name}'"
                )

            return scope[node.name]

        if isinstance(node, UnaryOpNode):
            value = self.evaluate(node.operand)

            if node.operator == "-":
                return -value

            raise RuntimeErrorBanana(
                f"Invalid unary operator '{node.operator}'"
            )

        if isinstance(node, BinaryOpNode):
            return self.evaluate_binary(node)

        if isinstance(node, FunctionCallNode):
            return self.call_function(node)

        raise RuntimeErrorBanana(
            f"Unsupported expression: {type(node).__name__}"
        )

    def evaluate_binary(self, node):
        """Evaluate arithmetic and comparison expressions."""

        operator = node.operator
        left = self.evaluate(node.left)
        right = self.evaluate(node.right)

        if operator == "+":
            return left + right

        if operator == "-":
            return left - right

        if operator == "*":
            return left * right

        if operator == "/":
            if right == 0:
                raise RuntimeErrorBanana("Division by zero")
            return left / right

        if operator == "==":
            return left == right

        if operator == "!=":
            return left != right

        if operator == "<":
            return left < right

        if operator == ">":
            return left > right

        if operator == "<=":
            return left <= right

        if operator == ">=":
            return left >= right

        raise RuntimeErrorBanana(
            f"Invalid operator '{operator}'"
        )

    def call_function(self, node):
        """Call a function using a new local environment."""

        if node.name not in self.functions:
            raise RuntimeErrorBanana(
                f"Undefined function '{node.name}'"
            )

        function = self.functions[node.name]

        if len(node.arguments) != len(function.parameters):
            raise RuntimeErrorBanana(
                f"Function '{node.name}' expects "
                f"{len(function.parameters)} argument(s), "
                f"but received {len(node.arguments)}"
            )

        # Evaluate arguments in the caller's scope.
        argument_values = [
            self.evaluate(argument) for argument in node.arguments
        ]

        # Parameters and local variables belong to this call's scope.
        local_scope = dict(
            zip(function.parameters, argument_values)
        )
        self.scopes.append(local_scope)

        try:
            for statement in function.body:
                self.execute(statement)

        except ReturnSignal as signal:
            return signal.value

        finally:
            # Always remove the local scope, even if execution fails.
            self.scopes.pop()

        # A function without an explicit return produces None.
        return None


def run(source):
    """Parse and execute Banana source code."""

    part3_path = str(Path(__file__).parent / "part3")

    if part3_path not in sys.path:
        sys.path.insert(0, part3_path)

    from banana_parser import parse

    interpreter = Interpreter()
    tree = parse(source)
    interpreter.execute(tree)

    return interpreter.output


def main():
    """Run a Banana source file from the command line."""

    if len(sys.argv) != 2:
        print("Usage: python interpreter.py <source_file>")
        return 1

    filename = sys.argv[1]

    try:
        with open(filename, "r", encoding="utf-8") as source_file:
            source_code = source_file.read()

        run(source_code)
        return 0

    except RuntimeErrorBanana as error:
        print(f"Runtime error: {error}")
        return 1

    except OSError as error:
        print(f"File error: {error}")
        return 1

    except Exception as error:
        error_name = type(error).__name__

        if error_name == "LexerError":
            print(f"Lexical error: {error}")
            return 1

        if error_name in ("ParserError", "SyntaxError"):
            print(f"Syntax error: {error}")
            return 1

        raise


if __name__ == "__main__":
    sys.exit(main())