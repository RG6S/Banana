# Banana Grammar (Part 5)

This document describes the syntax supported by the Banana Part 5 parser
and interpreter.

## EBNF Grammar

Notation: `{ x }` means zero or more repetitions, `[ x ]` means optional,
and `|` means a choice. Quoted text represents literal tokens.

program          = { statement } , EOF ;

statement        = let_stmt
                 | assign_stmt
                 | print_stmt
                 | if_stmt
                 | while_stmt
                 | function_def
                 | return_stmt
                 | for_stmt
                 | function_call , ";" ;

let_stmt         = "let" , ID , "=" , expression , ";" ;
assign_stmt      = ID , assign_op , expression , ";" ;
print_stmt       = "print" , expression , ";" ;
assign_op        = "=" | "+=" | "-=" | "*=" | "/=" ;

function_def     = ("function" | "func") , ID , "(" ,
                   [ parameter_list ] , ")" , block ;
parameter_list   = ID , { "," , ID } ;

return_stmt      = "return" , expression , ";" ;

function_call    = ID , "(" , [ argument_list ] , ")" ;
argument_list    = expression , { "," , expression } ;

if_stmt          = "if" , expression , block ,
                   [ "else" , block ] ;
while_stmt       = "while" , expression , block ;

for_stmt         = "for" , "(" , for_initializer , ";" ,
                   expression , ";" , assign_core , ")" , block ;
for_initializer  = let_core | assign_core ;
let_core         = "let" , ID , "=" , expression ;
assign_core      = ID , assign_op , expression ;

block            = "{" , { statement } , "}" ;

expression       = comparison ;
comparison       = additive , [ comp_op , additive ] ;
comp_op          = "==" | "!=" | "<" | ">" | "<=" | ">=" ;

additive         = term , { ("+" | "-") , term } ;
term             = unary , { ("*" | "/") , unary } ;
unary            = "-" , unary | primary ;
primary          = NUMBER
                 | ID
                 | function_call
                 | "(" , expression , ")" ;

## Operator Precedence

From highest to lowest:

1. Parentheses
2. Unary minus
3. Multiplication and division
4. Addition and subtraction
5. Comparison operators

Multiplication, division, addition, and subtraction are left-associative.
Chained comparisons are not supported.

## Functions and Scope

Function definitions use `function` or the existing alias `func`.
Parameters are separated by commas. Calls provide matching arguments,
and `return` returns an expression value.

Each function call receives a local environment for its parameters and
local declarations. Variable lookup searches the current local environment
first, then outer environments, including the global environment. Assignment
updates the nearest environment containing the assigned variable.

Function definitions are stored by name. Functions must be defined before
they are called during program execution. Recursion is supported.

## Extension Feature: for Loops

A `for` loop has an initializer, condition, increment assignment, and body.
The initializer supports a `let` declaration or an assignment. The increment
supports assignment or compound assignment.

Example:

```text
for (let i = 1; i <= 5; i += 1) {
    print i;
}

