# Banana Grammar (Part 4)

## EBNF

Notation: { x } means zero or more, [ x ] means optional, and | means choice. Quoted text represents literal tokens.

program        = { statement } , EOF ;

statement      = let_stmt
               | assign_stmt
               | print_stmt
               | if_stmt
               | while_stmt ;

let_stmt      = "let" , ID , "=" , expression , ";" ;
assign_stmt   = ID , assign_op , expression , ";" ;
print_stmt    = "print" , expression , ";" ;

assign_op     = "=" | "+=" | "-=" | "*=" | "/=" ;

if_stmt       = "if" , expression , block , [ "else" , block ] ;
while_stmt    = "while" , expression , block ;
block         = "{" , { statement } , "}" ;

expression    = comparison ;
comparison    = additive , [ comp_op , additive ] ;
comp_op       = "==" | "!=" | "<" | ">" | "<=" | ">=" ;

additive      = term , { ( "+" | "-" ) , term } ;
term          = unary , { ( "*" | "/" ) , unary } ;
unary         = "-" , unary | primary ;
primary       = NUMBER
              | ID
              | "(" , expression , ")" ;

## Operator Precedence (Highest to Lowest)

| Level | Operators | Associativity |
|---|---|---|
| 1 | Parentheses ( ) | Grouping |
| 2 | Unary - | Right |
| 3 | *, / | Left |
| 4 | +, - | Left |
| 5 | ==, !=, <, >, <=, >= | Follow parser implementation |

## Supported Features

- Variable declaration using let
- Variable reassignment and compound assignment
- Numeric expressions and arithmetic operations
- Parentheses and operator precedence
- Print statements
- Comparison operators
- if / else conditional statements
- while loops
- Runtime errors for undefined variables and division by zero

## Not Yet Implemented

Function declarations and return statements are recognized by the lexer but are not implemented as executable statements in the current interpreter.