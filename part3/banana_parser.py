
"""Recursive-descent parser for Banana Part 4."""

from typing import List

from ast_nodes import (
    AssignmentNode,
    BinaryOpNode,
    IfNode,
    Node,
    NumberNode,
    PrintNode,
    ProgramNode,
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
            return self.assignment_statement()

        if token.type == "IF":
            return self.if_statement()

        if token.type == "WHILE":
            return self.while_statement()

        if token.type in {"ELSE", "FUNC", "RETURN"}:
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
        name = self.expect("ID", "a variable name after 'let'")
        self.expect("ASSIGN", "'=' after the variable name")
        value = self.expression()
        self.expect("SEMICOLON", "';' at the end of the statement")

        return AssignmentNode(
            name.lexeme,
            "=",
            value,
            is_declaration=True,
        )

    def assignment_statement(self) -> AssignmentNode:
        name = self.advance()

        if not self.check(*ASSIGN_OPERATORS):
            raise ParserError(
                f"expected '=' or a compound assignment operator after "
                f"'{name.lexeme}' but found {describe(self.peek())}",
                self.peek(),
            )

        operator = self.advance()
        value = self.expression()
        self.expect("SEMICOLON", "';' at the end of the statement")

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
