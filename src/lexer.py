from dataclasses import dataclass
from typing import List


KEYWORDS = {
    "let": "LET",
    "print": "PRINT",
    "if": "IF",
    "else": "ELSE",
    "while": "WHILE",
    "func": "FUNC",
    "return": "RETURN",
    "true": "TRUE",
    "false": "FALSE",
}

TWO_CHAR_OPERATORS = {
    "==": "EQ",
    "!=": "NE",
    "<=": "LE",
    ">=": "GE",
    "+=": "PLUS_ASSIGN",
    "-=": "MINUS_ASSIGN",
    "*=": "STAR_ASSIGN",
    "/=": "SLASH_ASSIGN",
}

ONE_CHAR_TOKENS = {
    "+": "PLUS",
    "-": "MINUS",
    "*": "STAR",
    "/": "SLASH",
    "<": "LT",
    ">": "GT",
    "=": "ASSIGN",
    "(": "LPAREN",
    ")": "RPAREN",
    "{": "LBRACE",
    "}": "RBRACE",
    ",": "COMMA",
    ";": "SEMICOLON",
}


@dataclass(frozen=True)
class Token:
    type: str
    lexeme: str
    line: int
    column: int

    def __str__(self) -> str:
        return f"{self.type}({self.lexeme})"


class LexerError(Exception):
    """Raised when the lexer finds an invalid character or malformed token."""

    def __init__(self, message: str, line: int, column: int, character: str):
        super().__init__(f"Lexical error at line {line}, column {column}: "
                         f"{message} {character!r}")
        self.line = line
        self.column = column
        self.character = character


class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.current = 0
        self.line = 1
        self.column = 1

    def tokenize(self) -> List[Token]:
        tokens = []

        while not self.is_at_end():
            char = self.peek()

            # Whitespace
            if char in " \t\r":
                self.advance()
                continue
            if char == "\n":
                self.advance()
                continue

            # Line comments: // comment
            if char == "/" and self.peek_next() == "/":
                self.skip_comment()
                continue

            # Two-character operators
            two = char + self.peek_next()
            if two in TWO_CHAR_OPERATORS:
                start_line, start_col = self.line, self.column
                self.advance()
                self.advance()
                tokens.append(Token(TWO_CHAR_OPERATORS[two], two,
                                    start_line, start_col))
                continue

            # One-character operators and delimiters
            if char in ONE_CHAR_TOKENS:
                start_line, start_col = self.line, self.column
                self.advance()
                tokens.append(Token(ONE_CHAR_TOKENS[char], char,
                                    start_line, start_col))
                continue

            # Identifier / keyword
            if char.isalpha() or char == "_":
                tokens.append(self.identifier_or_keyword())
                continue

            # Integer number
            if char.isdigit():
                tokens.append(self.number())
                continue

            raise LexerError(
                "invalid character",
                self.line,
                self.column,
                char,
            )

        tokens.append(Token("EOF", "", self.line, self.column))
        return tokens

    def identifier_or_keyword(self) -> Token:
        start_line, start_col = self.line, self.column
        start = self.current

        self.advance()
        while (not self.is_at_end()
               and (self.peek().isalnum() or self.peek() == "_")):
            self.advance()

        lexeme = self.source[start:self.current]
        token_type = KEYWORDS.get(lexeme, "ID")
        return Token(token_type, lexeme, start_line, start_col)

    def number(self) -> Token:
        start_line, start_col = self.line, self.column
        start = self.current

        while not self.is_at_end() and self.peek().isdigit():
            self.advance()

        # Banana Part 1 defines <number> as one or more digits.
        # A decimal point is therefore not accepted by this lexer.
        return Token("NUMBER", self.source[start:self.current],
                     start_line, start_col)

    def skip_comment(self) -> None:
        while not self.is_at_end() and self.peek() != "\n":
            self.advance()

    def peek(self) -> str:
        if self.is_at_end():
            return "\0"
        return self.source[self.current]

    def peek_next(self) -> str:
        if self.current + 1 >= len(self.source):
            return "\0"
        return self.source[self.current + 1]

    def advance(self) -> str:
        char = self.source[self.current]
        self.current += 1
        if char == "\n":
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        return char

    def is_at_end(self) -> bool:
        return self.current >= len(self.source)


def lex(source: str) -> List[Token]:
    """Convenience function for tokenizing Banana source code."""
    return Lexer(source).tokenize()


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python lexer.py <source-file>")
        sys.exit(1)

    source_file = sys.argv[1]
    try:
        source = open(source_file, "r", encoding="utf-8").read()
        for token in lex(source):
            print(token)
    except LexerError as error:
        print(error)
        sys.exit(1)
    except OSError as error:
        print(f"Could not read source file: {error}")
        sys.exit(1)
