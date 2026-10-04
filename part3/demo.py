"""Prints the AST for several example programs (press Run in VS Code)."""

from ast_nodes import format_tree, to_sexpr
from banana_parser import ParserError, parse
from lexer import LexerError, lex

EXAMPLES = [
    ("Example 1: operator precedence", "print 2 + 3 * 4;"),
    ("Example 2: parentheses and unary minus",
     "let x = (2 + 3) * -4;\nprint x;"),
    ("Example 3: multiple statements, reassignment, compound assignment",
     "let total = 10;\ntotal += 5 * 2;\ntotal = total - 1;\nprint total / 3;"),
]

ERRORS = [
    "let x = ;",
    "print (1 + 2;",
    "let x = 5\nprint x;",
]


def main() -> None:
    for title, source in EXAMPLES:
        print("=" * 60)
        print(title)
        print("-" * 60)
        print("Source:")
        print(source)
        print("\nTokens:")
        print(" ".join(str(t) for t in lex(source)))
        tree = parse(source)
        print("\nAST:")
        print(format_tree(tree))
        print("\nS-expression:", to_sexpr(tree))
        print()

    print("=" * 60)
    print("Syntax error examples")
    print("-" * 60)
    for source in ERRORS:
        print("Source:", repr(source))
        try:
            parse(source)
        except (LexerError, ParserError) as error:
            print("  ->", error)
        print()


if __name__ == "__main__":
    main()
