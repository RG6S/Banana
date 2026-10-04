"""Parser tests. Run this file directly, or use VS Code's Testing panel."""

import unittest

from ast_nodes import (AssignmentNode, BinaryOpNode, NumberNode, PrintNode,
                       ProgramNode, UnaryOpNode, VariableNode, to_sexpr)
from banana_parser import ParserError, parse
from lexer import LexerError


def expr(text: str) -> str:
    """Parse a single expression (wrapped in a print) and return its s-expr."""
    program = parse(f"print {text};")
    return to_sexpr(program.statements[0].expression)


class PrecedenceTests(unittest.TestCase):
    def test_multiplication_binds_tighter_than_addition(self):
        self.assertEqual(expr("2 + 3 * 4"), "(+ 2 (* 3 4))")

    def test_multiplication_first_on_the_left_too(self):
        self.assertEqual(expr("2 * 3 + 4"), "(+ (* 2 3) 4)")

    def test_parentheses_override_precedence(self):
        self.assertEqual(expr("(2 + 3) * 4"), "(* (+ 2 3) 4)")

    def test_subtraction_is_left_associative(self):
        self.assertEqual(expr("10 - 4 - 3"), "(- (- 10 4) 3)")

    def test_division_is_left_associative(self):
        self.assertEqual(expr("100 / 10 / 2"), "(/ (/ 100 10) 2)")

    def test_unary_minus_binds_tighter_than_multiplication(self):
        self.assertEqual(expr("-2 * 3"), "(* (neg 2) 3)")

    def test_nested_parentheses(self):
        self.assertEqual(expr("((1 + 2)) * (3 - x)"),
                         "(* (+ 1 2) (- 3 x))")


class StatementTests(unittest.TestCase):
    def test_let_declaration_node_structure(self):
        program = parse("let x = 5;")
        self.assertEqual(program, ProgramNode([
            AssignmentNode("x", "=", NumberNode(5), is_declaration=True)]))

    def test_reassignment_without_let(self):
        stmt = parse("x = y + 1;").statements[0]
        self.assertEqual(stmt, AssignmentNode(
            "x", "=", BinaryOpNode("+", VariableNode("y"), NumberNode(1))))
        self.assertFalse(stmt.is_declaration)

    def test_compound_assignment(self):
        self.assertEqual(to_sexpr(parse("x += 2 * 3;")), "(program (+= x (* 2 3)))")
        self.assertEqual(to_sexpr(parse("x /= 2;")), "(program (/= x 2))")

    def test_print_statement(self):
        self.assertEqual(parse("print x;").statements[0],
                         PrintNode(VariableNode("x")))

    def test_multiple_statements_keep_order(self):
        program = parse("let a = 1;\nlet b = a + 2;\nprint b * 3;")
        self.assertEqual(len(program.statements), 3)
        self.assertEqual(to_sexpr(program),
                         "(program (let= a 1) (let= b (+ a 2)) "
                         "(print (* b 3)))")

    def test_comments_and_empty_program(self):
        self.assertEqual(parse("// nothing here\n").statements, [])
        self.assertEqual(parse("").statements, [])


class SyntaxErrorTests(unittest.TestCase):
    def test_missing_expression_after_equals(self):
        with self.assertRaises(ParserError) as ctx:
            parse("let x = ;")
        self.assertEqual((ctx.exception.line, ctx.exception.column), (1, 9))
        self.assertIn("expected an expression but found ';'", str(ctx.exception))

    def test_missing_semicolon(self):
        with self.assertRaises(ParserError) as ctx:
            parse("let x = 5\nprint x;")
        self.assertEqual(ctx.exception.line, 2)
        self.assertIn("expected ';'", str(ctx.exception))

    def test_missing_closing_parenthesis(self):
        with self.assertRaises(ParserError) as ctx:
            parse("print (1 + 2;")
        self.assertIn("expected ')'", str(ctx.exception))

    def test_missing_variable_name(self):
        with self.assertRaises(ParserError) as ctx:
            parse("let = 5;")
        self.assertIn("variable name", str(ctx.exception))

    def test_dangling_operator(self):
        with self.assertRaises(ParserError) as ctx:
            parse("print 2 + ;")
        self.assertIn("expected an expression", str(ctx.exception))

    def test_two_expressions_without_operator(self):
        with self.assertRaises(ParserError):
            parse("print 2 3;")

    def test_identifier_without_assignment_operator(self):
        with self.assertRaises(ParserError) as ctx:
            parse("x;")
        self.assertIn("assignment operator", str(ctx.exception))

    def test_unsupported_keyword_gives_clear_message(self):
        with self.assertRaises(ParserError) as ctx:
            parse("while x { }")
        self.assertIn("not supported", str(ctx.exception))

    def test_lexer_errors_still_propagate(self):
        with self.assertRaises(LexerError):
            parse("let x = 5 @ 3;")
        with self.assertRaises(LexerError):
            parse("let x = 12abc;")


if __name__ == "__main__":
    unittest.main(verbosity=2)
