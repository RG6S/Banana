# Banana Grammar (Part 4)

This document describes the grammar implemented by the Banana Part 4 parser
and interpreter. It is consistent with the main project grammar in `GRAMMAR.md`.

## EBNF Grammar

Notation: `{ x }` means zero or more repetitions, `[ x ]` means optional,
and `|` means a choice. Quoted text represents literal tokens.

program        = { statement } , EOF ;

statement      = let_stmt
               | assign_stmt
               | print_stmt
               | if_stmt
               | while_stmt ;

let_stmt       = "let" , ID , "=" , expression , ";" ;
assign_stmt    = ID , assign_op , expression , ";" ;
print_stmt     = "print" , expression , ";" ;

assign_op      = "=" | "+=" | "-=" | "*=" | "/=" ;

if_stmt        = "if" , expression , block , [ "else" , block ] ;
while_stmt     = "while" , expression , block ;
block          = "{" , { statement } , "}" ;

expression     = comparison ;
comparison     = additive , [ comp_op , additive ] ;
comp_op        = "==" | "!=" | "<" | ">" | "<=" | ">=" ;

additive       = term , { ( "+" | "-" ) , term } ;
term           = unary , { ( "*" | "/" ) , unary } ;
unary          = "-" , unary | primary ;
primary        = NUMBER
               | ID
               | "(" , expression , ")" ;

## Operator Precedence

From highest to lowest:

1. Parentheses
2. Unary minus
3. Multiplication and division
4. Addition and subtraction
5. Comparison operators

Arithmetic operators follow the parser's associativity rules. Comparisons are
non-associative: an expression may contain only one comparison operator unless
parentheses are used to form separate expressions.

## Supported Features

- Integer numeric literals; division can produce decimal results.
- Variable declarations using `let`.
- Variable reassignment and compound assignments.
- Arithmetic operations: `+`, `-`, `*`, `/`.
- Comparison operators: `==`, `!=`, `<`, `>`, `<=`, `>=`.
- Print statements.
- `if` and optional `else` blocks.
- `while` loops.
- Runtime errors for undefined variables and division by zero.
- Lexical and syntax errors with line and column information.

## Current Limitations

Function declarations and return statements are not executable features in
the current Part 4 parser and interpreter. Keywords such as `func` and
`return` may be recognized by the lexer, but lexical recognition alone does
not mean the language supports executing functions.

Boolean values can result from comparison expressions. Boolean literals such
as `true` and `false` are not included in the primary-expression grammar above.

