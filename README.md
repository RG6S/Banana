# Banana Programming Language

Banana is a simple C-style programming language that our group is designing and developing for our programming languages course project. The goal of Banana is to create a small and easy-to-understand programming language that supports common programming concepts while remaining simple enough to implement within the project timeline.

## Features

- Variable declaration using let
- Numeric values
- Arithmetic operations: +, -, *, /
- Comparison operators: ==, !=, <, >, <=, >=
- Parentheses and operator precedence
- print statements
- if / else statements
- while loops
- Compound assignments: +=, -=, *=, /=
- Error handling for undefined variables and division by zero

## Example

let x = 10;
let y = 20;

if x < y {
    print x + y;
} else {
    print 0;
}

## Group Members

1. Nabin Shrestha
2. Rajiv Gautam
3. Nishan Thapa

## Project Structure

1. src/ - Lexer source files
2. part3/ - Parser and parser tests
3. tests/ - Automated tests
4. outputs/ - Sample programs and test files
5. ast_nodes.py - Abstract syntax tree definitions
6. interpreter.py - Runs Banana programs
7. GRAMMAR.md - Banana language grammar
8. Language-Design.md - Language design documentation
9. docs/ - Project documentation

## How to Run

Run a Banana program from the project folder:

python .\interpreter.py .\outputs\test1.banana

## How to Run Tests

Run the lexer and interpreter tests:

python -m unittest discover -s tests -v

Run the parser tests:

python -m unittest discover -s part3 -v

All 14 lexer and interpreter tests and 22 parser tests passed during development.

## Language Design

For more information about the language, grammar, and design, see [Language-Design.md](Language-Design.md).