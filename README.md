# Banana Programming Language

Banana is a simple C-style programming language designed and developed by our group for our Programming Languages course project. Its goal is to support common programming concepts while remaining small enough to understand and implement.

## Features

- Variable declarations using `let`
- Numeric values
- Arithmetic operations: `+`, `-`, `*`, `/`
- Comparison operators: `==`, `!=`, `<`, `>`, `<=`, `>=`
- Parentheses and operator precedence
- Print statements
- `if` / `else` statements
- `while` loops
- `for` loops
- Compound assignments: `+=`, `-=`, `*=`, `/=`
- Function definitions, parameters, and function calls
- Return values and recursion
- Local and global variable scope
- Runtime error handling for undefined variables and division by zero
- Lexical error handling for invalid characters

## Current Limitations

- Numeric literals are integers, although division can produce decimal results.
- Boolean literals such as `true` and `false` are not supported as expressions.
- A function without an explicit return statement produces `None`.

## Example

```banana
let x = 10;
let y = 20;

if (x < y) {
    print(x + y);
} else {
    print(0);
}
```

## Group Members

1. Nabin Shrestha
2. Achyuth Kumar Kurakula
3. Nishan Thapa

## Project Structure

- `interpreter.py` - Runs Banana programs and handles interpretation.
- `ast_nodes.py` - Abstract syntax tree definitions.
- `part3/lexer.py` - Active lexer used by the parser and interpreter.
- `part3/banana_parser.py` - Banana parser.
- `part3/` - Parser tests and related files.
- `src/` - Additional lexer and token source files.
- `tests/` - Automated interpreter and lexer tests, including sample Banana programs.
- `outputs/` - Additional sample programs and output examples.
- `GRAMMAR.md` - Banana language grammar.
- `Language-Design.md` - Language design documentation.
- `docs/` - Project documentation.

## How to Run

From the project folder, run:

```powershell
python .\interpreter.py .\outputs\test1.banana
```

Replace `test1.banana` with the Banana program you want to execute.

## How to Run Tests

Run the interpreter and lexer tests:

```powershell
python -m unittest discover -s tests -v
```

Run the parser tests:

```powershell
python -m unittest discover -s part3 -v
```

## Latest Test Results

The latest unit test runs completed successfully:

- Interpreter and lexer tests: 24 passed
- Parser tests: 22 passed
- Total: 46 passed

Additionally, 12 Banana programs in `tests/cases/` were executed through the interpreter. These covered variable declarations, arithmetic, printing, conditionals, lexical errors, loops, functions, parameters, scope, nested function calls, and for loops. The invalid-input program intentionally produced a lexical error.

Additional runtime error examples are available in the `outputs/` directory.

## Language Design

For more information about the language, grammar, and design, see [Language-Design.md](Language-Design.md).
