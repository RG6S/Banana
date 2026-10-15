"""Interpreter for the Banana programming language (Part 4)."""

import sys
from pathlib import Path

from ast_nodes import (
    AssignmentNode,
    BinaryOpNode,
    IfNode,
    NumberNode,
    PrintNode,
    ProgramNode,
    UnaryOpNode,
    VariableNode,
    WhileNode,
)


class RuntimeErrorBanana(Exception):
    """Raised when a Banana program has a runtime error."""


class Interpreter:
    def __init__(self):
        self.environment = {}
        self.output = []

    def execute(self, node):
        """Execute a statement or program."""

        if isinstance(node, ProgramNode):
            for statement in node.statements:
                self.execute(statement)

        elif isinstance(node, AssignmentNode):
            self.execute_assignment(node)

        elif isinstance(node, PrintNode):
            value = self.evaluate(node.expression)
            self.output.append(str(value))
            print(value)

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

        else:
            raise RuntimeErrorBanana(
                f"Unsupported statement: {type(node).__name__}"
            )

    def execute_assignment(self, node):
        name = node.name
        operator = node.operator

        if node.is_declaration:
            if name in self.environment:
                raise RuntimeErrorBanana(
                    f"Variable '{name}' is already declared"
                )

            self.environment[name] = self.evaluate(node.value)
            return

        if name not in self.environment:
            raise RuntimeErrorBanana(
                f"Undefined variable '{name}'"
            )

        value = self.evaluate(node.value)

        if operator == "=":
            self.environment[name] = value
        elif operator == "+=":
            self.environment[name] += value
        elif operator == "-=":
            self.environment[name] -= value
        elif operator == "*=":
            self.environment[name] *= value
        elif operator == "/=":
            if value == 0:
                raise RuntimeErrorBanana("Division by zero")
            self.environment[name] /= value
        else:
            raise RuntimeErrorBanana(
                f"Unsupported assignment operator '{operator}'"
            )

    def evaluate(self, node):
        """Evaluate an expression and return its value."""

        if isinstance(node, NumberNode):
            return node.value

        if isinstance(node, VariableNode):
            if node.name not in self.environment:
                raise RuntimeErrorBanana(
                    f"Undefined variable '{node.name}'"
                )
            return self.environment[node.name]

        if isinstance(node, UnaryOpNode):
            value = self.evaluate(node.operand)

            if node.operator == "-":
                return -value

            raise RuntimeErrorBanana(
                f"Unsupported unary operator '{node.operator}'"
            )

        if isinstance(node, BinaryOpNode):
            left = self.evaluate(node.left)
            right = self.evaluate(node.right)
            operator = node.operator

            if operator == "+":
                return left + right
            elif operator == "-":
                return left - right
            elif operator == "*":
                return left * right
            elif operator == "/":
                if right == 0:
                    raise RuntimeErrorBanana("Division by zero")
                return left / right
            elif operator == "==":
                return left == right
            elif operator == "!=":
                return left != right
            elif operator == "<":
                return left < right
            elif operator == ">":
                return left > right
            elif operator == "<=":
                return left <= right
            elif operator == ">=":
                return left >= right

            raise RuntimeErrorBanana(
                f"Unsupported operator '{operator}'"
            )

        raise RuntimeErrorBanana(
            f"Unsupported expression: {type(node).__name__}"
        )


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

    except SyntaxError as error:
        print(f"Syntax error: {error}")
        return 1


if __name__ == "__main__":
    sys.exit(main())