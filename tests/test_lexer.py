import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from lexer import Lexer, LexerError


class TestBananaLexer(unittest.TestCase):

    def assertTypes(self, source, expected_types):
        tokens = Lexer(source).tokenize()
        self.assertEqual([t.type for t in tokens], expected_types)

    def test_variable_declaration(self):
        self.assertTypes(
            "let x = 10;",
            ["LET", "ID", "ASSIGN", "NUMBER", "SEMICOLON", "EOF"]
        )

    def test_arithmetic_expression(self):
        self.assertTypes(
            "let result = (10 + 5) * 2;",
            [
                "LET", "ID", "ASSIGN", "LPAREN", "NUMBER", "PLUS",
                "NUMBER", "RPAREN", "STAR", "NUMBER", "SEMICOLON", "EOF"
            ]
        )

    def test_print_statement(self):
        self.assertTypes(
            "print(x + 10);",
            [
                "PRINT", "LPAREN", "ID", "PLUS", "NUMBER",
                "RPAREN", "SEMICOLON", "EOF"
            ]
        )

    def test_control_structure(self):
        self.assertTypes(
            "if (x < 10) { print(x); } else { print(0); }",
            [
                "IF", "LPAREN", "ID", "LT", "NUMBER", "RPAREN",
                "LBRACE", "PRINT", "LPAREN", "ID", "RPAREN",
                "SEMICOLON", "RBRACE", "ELSE", "LBRACE", "PRINT",
                "LPAREN", "NUMBER", "RPAREN", "SEMICOLON", "RBRACE", "EOF"
            ]
        )

    def test_invalid_input(self):
        with self.assertRaisesRegex(LexerError, "invalid character"):
            Lexer("let x = 10 @ 5;").tokenize()

    def test_while_and_compound_assignment(self):
        self.assertTypes(
            "while (i < 10) { i += 1; }",
            [
                "WHILE", "LPAREN", "ID", "LT", "NUMBER", "RPAREN",
                "LBRACE", "ID", "PLUS_ASSIGN", "NUMBER",
                "SEMICOLON", "RBRACE", "EOF"
            ]
        )

    def test_function_and_return(self):
        self.assertTypes(
            "func square(n) { return n * n; }",
            [
                "FUNC", "ID", "LPAREN", "ID", "RPAREN", "LBRACE",
                "RETURN", "ID", "STAR", "ID", "SEMICOLON", "RBRACE", "EOF"
            ]
        )


if __name__ == "__main__":
    unittest.main()
