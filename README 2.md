# Banana Parser (Part 3)

Converts the lexer's tokens into an Abstract Syntax Tree. Written in
Python 3 using only the standard library (no installs needed).

## Files

| File | Purpose |
|------|---------|
| `lexer.py` | Updated lexer (one change, see below) |
| `ast_nodes.py` | AST node classes + `format_tree` / `to_sexpr` printers |
| `banana_parser.py` | Recursive-descent parser and `ParserError` |
| `GRAMMAR.md` | Updated EBNF and BNF grammar |
| `test_parser.py` | 22 parser tests (`unittest`) |
| `demo.py` | Prints tokens + AST for three programs, plus error examples |
| `ast_output.txt` | Saved output of `demo.py` |

(The parser is `banana_parser.py` rather than `parser.py` because older
Python versions have a built-in module called `parser` that would be
imported instead.)

## How to run (VS Code, no terminal needed)

1. Put all files in one folder and open that folder in VS Code.
2. **AST demo:** open `demo.py` and press the ▶ Run button (top right).
3. **Tests:** open `test_parser.py` and press ▶ Run, or use the Testing
   (beaker) icon in the sidebar. Expected result: `Ran 22 tests ... OK`.

To parse your own code:

```python
from banana_parser import parse
from ast_nodes import format_tree
print(format_tree(parse("let x = 1 + 2 * 3; print x;")))
```

## Language supported in this part

```
let x = 5;           // declaration
x = x + 1;           // reassignment
x += 2 * 3;          // compound assignment (+=  -=  *=  /=)
print (x + 1) * -2;  // print statement, parentheses, unary minus
```

Statements end with `;`. Whitespace and `// comments` are ignored.

## AST design

- `ProgramNode(statements)`
- `AssignmentNode(name, operator, value, is_declaration)` covers `let x = e;`,
  `x = e;` and `x += e;`
- `PrintNode(expression)`
- `BinaryOpNode(operator, left, right)`
- `UnaryOpNode(operator, operand)` (added so that `-5` works)
- `NumberNode(value)`, `VariableNode(name)`

Parentheses do not get their own node; they only affect the tree shape.
Compound assignments are stored as written (`+=`), not rewritten to
`x = x + e`.

## Precedence

Implemented by one parsing function per level (`expression` -> `term` ->
`unary` -> `primary`), matching the grammar. `2 + 3 * 4` becomes
`+(2, *(3, 4))`.

## Error handling

The parser stops at the first error and reports its position and what it
expected:

```
let x = ;      -> Syntax error at line 1, column 9: expected an expression but found ';'
print (1 + 2;  -> Syntax error at line 1, column 13: expected ')' to close the '(' but found ';'
```

Lexer problems still raise `LexerError`. Both error types are caught in
`demo.py`.

## Changes to the lexer

One change: a number immediately followed by a letter or underscore
(e.g. `12abc`) now raises a `LexerError`. Before, it lexed as `NUMBER(12)`
then `ID(abc)`, which produced a confusing parser error later.