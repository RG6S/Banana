
"""Recursive-descent parser for Banana Part 5."""

from typing import List

from ast_nodes import (
    AssignmentNode,
    BinaryOpNode,
    ForNode,
    FunctionCallNode,
    FunctionDefNode,
    IfNode,
    Node,
    NumberNode,
    PrintNode,
    ProgramNode,
    ReturnNode,
    UnaryOpNode,
    VariableNode,
    WhileNode,
)
from lexer import Token, lex


ASSIGN_OPERATORS = {
    "ASSIGN",
    "PLUS_ASSIGN",
    "MINUS_ASSIGN",
    "STAR_ASSIGN",
    "SLASH_ASSIGN",
}

COMPARISON_OPERATORS = {"EQ", "NE", "LT", "GT", "LE", "GE"}


class ParserError(Exception):
    """Raised when the token stream does not match the grammar."""

    def __init__(self, message: str, token: Token):
        super().__init__(
            f"Syntax error at line {token.line}, "
            f"column {token.column}: {message}"
        )
        self.message = message
        self.line = token.line
        self.column = token.column
        self.token = token


def describe(token: Token) -> str:
    if token.type == "EOF":
        return "end of input"
    return f"'{token.lexeme}'"


class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0

    def peek(self) -> Token:
        return self.tokens[self.pos]

    def peek_next(self) -> Token:
        return self.tokens[min(self.pos + 1, len(self.tokens) - 1)]

    def check(self, *types: str) -> bool:
        return self.peek().type in types

    def advance(self) -> Token:
        token = self.tokens[self.pos]
        if token.type != "EOF":
            self.pos += 1
        return token

    def expect(self, token_type: str, what: str) -> Token:
        if self.check(token_type):
            return self.advance()

        raise ParserError(
            f"expected {what} but found {describe(self.peek())}",
            self.peek(),
        )

    def parse_program(self) -> ProgramNode:
        statements = []

        while not self.check("EOF"):
            statements.append(self.statement())

        return ProgramNode(statements)

    def statement(self) -> Node:
        token = self.peek()

        if token.type == "LET":
            return self.let_statement()

        if token.type == "PRINT":
            return self.print_statement()

        if token.type == "ID":
            if self.peek_next().type == "LPAREN":
                call = self.function_call()
                self.expect("SEMICOLON", "';' after the function call")
                return call
            return self.assignment_statement()

        if token.type == "IF":
            return self.if_statement()

        if token.type == "WHILE":
            return self.while_statement()

        if token.type == "FUNC":
            return self.function_definition()

        if token.type == "RETURN":
            return self.return_statement()

        if token.type == "FOR":
            return self.for_statement()

        if token.type in {"ELSE"}:
            raise ParserError(
                f"'{token.lexeme}' is not supported here",
                token,
            )

        raise ParserError(
            f"expected a statement but found {describe(token)}",
            token,
        )

    def let_statement(self) -> AssignmentNode:
        self.advance()
        node = self.declaration_core()
        self.expect("SEMICOLON", "';' at the end of the statement")
        return node

    def declaration_core(self) -> AssignmentNode:
        name = self.expect("ID", "a variable name after 'let'")
        self.expect("ASSIGN", "'=' after the variable name")
        value = self.expression()

        return AssignmentNode(
            name.lexeme,
            "=",
            value,
            is_declaration=True,
        )

    def assignment_statement(self) -> AssignmentNode:
        node = self.assignment_core()
        self.expect("SEMICOLON", "';' at the end of the statement")
        return node

    def assignment_core(self) -> AssignmentNode:
        name = self.expect("ID", "a variable name")

        if not self.check(*ASSIGN_OPERATORS):
            raise ParserError(
                f"expected '=' or a compound assignment operator after "
                f"'{name.lexeme}' but found {describe(self.peek())}",
                self.peek(),
            )

        operator = self.advance()
        value = self.expression()

        return AssignmentNode(name.lexeme, operator.lexeme, value)

    def print_statement(self) -> PrintNode:
        self.advance()
        value = self.expression()
        self.expect("SEMICOLON", "';' at the end of the statement")
        return PrintNode(value)

    def if_statement(self) -> IfNode:
        self.advance()
        condition = self.expression()
        then_branch = self.block()
        else_branch = []

        if self.check("ELSE"):
            self.advance()
            else_branch = self.block()

        return IfNode(condition, then_branch, else_branch)

    def while_statement(self) -> WhileNode:
        self.advance()
        condition = self.expression()
        body = self.block()
        return WhileNode(condition, body)

    def function_definition(self) -> FunctionDefNode:
        self.advance()
        name = self.expect("ID", "a function name")
        self.expect("LPAREN", "'(' after the function name")

        parameters = []

        if not self.check("RPAREN"):
            parameters.append(
                self.expect("ID", "a parameter name").lexeme
            )

            while self.check("COMMA"):
                self.advance()
                parameters.append(
                    self.expect("ID", "a parameter name").lexeme
                )

        if len(parameters) != len(set(parameters)):
            raise ParserError(
                "duplicate parameter name",
                self.peek(),
            )

        self.expect("RPAREN", "')' after the parameters")
        body = self.block()

        return FunctionDefNode(name.lexeme, parameters, body)

    def function_call(self) -> FunctionCallNode:
        name = self.expect("ID", "a function name")
        self.expect("LPAREN", "'(' after the function name")

        arguments = []

        if not self.check("RPAREN"):
            arguments.append(self.expression())

            while self.check("COMMA"):
                self.advance()
                arguments.append(self.expression())

        self.expect("RPAREN", "')' after the arguments")

        return FunctionCallNode(name.lexeme, arguments)

    def return_statement(self) -> ReturnNode:
        self.advance()
        value = self.expression()
        self.expect("SEMICOLON", "';' after the return value")
        return ReturnNode(value)

    def for_statement(self) -> ForNode:
        self.advance()
        self.expect("LPAREN", "'(' after 'for'")

        if self.check("LET"):
            self.advance()
            initializer = self.declaration_core()
        elif self.check("ID"):
            initializer = self.assignment_core()
        else:
            raise ParserError(
                "expected a variable declaration or assignment "
                "to initialize the for loop",
                self.peek(),
            )

        self.expect("SEMICOLON", "';' after the for-loop initializer")

        condition = self.expression()
        self.expect("SEMICOLON", "';' after the for-loop condition")

        increment = self.assignment_core()
        self.expect("RPAREN", "')' after the for-loop increment")

        body = self.block()

        return ForNode(initializer, condition, increment, body)

    def block(self) -> List[Node]:
        self.expect("LBRACE", "'{' to begin a block")
        statements = []

        while not self.check("RBRACE", "EOF"):
            statements.append(self.statement())

        self.expect("RBRACE", "'}' to close a block")
        return statements

    def expression(self) -> Node:
        return self.comparison()

    def comparison(self) -> Node:
        node = self.term()

        if self.check(*COMPARISON_OPERATORS):
            operator = self.advance()
            node = BinaryOpNode(
                operator.lexeme,
                node,
                self.term(),
            )

            if self.check(*COMPARISON_OPERATORS):
                raise ParserError(
                    "chained comparisons are not supported",
                    self.peek(),
                )

        return node

    def term(self) -> Node:
        node = self.factor()

        while self.check("PLUS", "MINUS"):
            operator = self.advance()
            node = BinaryOpNode(
                operator.lexeme,
                node,
                self.factor(),
            )

        return node

    def factor(self) -> Node:
        node = self.unary()

        while self.check("STAR", "SLASH"):
            operator = self.advance()
            node = BinaryOpNode(
                operator.lexeme,
                node,
                self.unary(),
            )

        return node

    def unary(self) -> Node:
        if self.check("MINUS"):
            operator = self.advance()
            return UnaryOpNode(
                operator.lexeme,
                self.unary(),
            )

        return self.primary()

    def primary(self) -> Node:
        token = self.peek()

        if token.type == "NUMBER":
            self.advance()
            return NumberNode(int(token.lexeme))

        if token.type == "ID":
            if self.peek_next().type == "LPAREN":
                return self.function_call()

            self.advance()
            return VariableNode(token.lexeme)

        if token.type == "LPAREN":
            self.advance()
            node = self.expression()
            self.expect("RPAREN", "')' to close the '('")
            return node

        raise ParserError(
            f"expected an expression but found {describe(token)}",
            token,
        )


def parse_tokens(tokens: List[Token]) -> ProgramNode:
    return Parser(tokens).parse_program()


def parse(source: str) -> ProgramNode:
    """Lex and parse Banana source code."""
    return parse_tokens(lex(source))
