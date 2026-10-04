# Banana Grammar (Part 2)

## EBNF

Notation: `{ x }` = zero or more, `[ x ]` = optional, `|` = choice,
quoted text and UPPERCASE names are tokens from the lexer.

```ebnf
program     = { statement } , EOF ;

statement   = let_stmt
            | assign_stmt
            | print_stmt ;

let_stmt    = "let" , ID , "=" , expression , ";" ;
assign_stmt = ID , assign_op , expression , ";" ;
print_stmt  = "print" , expression , ";" ;

assign_op   = "=" | "+=" | "-=" | "*=" | "/=" ;

expression  = term , { ( "+" | "-" ) , term } ;
term        = unary , { ( "*" | "/" ) , unary } ;
unary       = "-" , unary
            | primary ;
primary     = NUMBER
            | ID
            | "(" , expression , ")" ;
```

Each precedence level is its own rule, which is what makes `2 + 3 * 4`
parse as `2 + (3 * 4)`. The `{ ... }` loops in `expression` and `term`
make `+ - * /` left-associative: `10 - 4 - 3` is `(10 - 4) - 3`.

## BNF equivalent

```bnf
<program>     ::= <statements> EOF
<statements>  ::= <statement> <statements> | ""
<statement>   ::= <let_stmt> | <assign_stmt> | <print_stmt>
<let_stmt>    ::= "let" ID "=" <expression> ";"
<assign_stmt> ::= ID <assign_op> <expression> ";"
<print_stmt>  ::= "print" <expression> ";"
<assign_op>   ::= "=" | "+=" | "-=" | "*=" | "/="
<expression>  ::= <term> | <expression> "+" <term> | <expression> "-" <term>
<term>        ::= <unary> | <term> "*" <unary> | <term> "/" <unary>
<unary>       ::= "-" <unary> | <primary>
<primary>     ::= NUMBER | ID | "(" <expression> ")"
```

## Precedence (highest to lowest)

| Level | Operators | Associativity |
|-------|-----------|---------------|
| 1 | `( )` grouping | - |
| 2 | unary `-` | right |
| 3 | `*` `/` | left |
| 4 | `+` `-` | left |

## Not yet parsed

`if`, `else`, `while`, `func`, `return`, `true`/`false`, comparison
operators, `{ }` blocks and `,` are valid lexer tokens but are not part of
this assignment's grammar. Using `if`, `else`, `while`, `func` or `return`
as a statement gives the error "'...' statements are not supported by the
parser yet".
