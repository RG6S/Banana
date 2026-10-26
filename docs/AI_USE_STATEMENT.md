# AI USE STATEMENT

## AI Tool(s) Used

ChatGPT (OpenAI).

## How did your group use AI for this project milestone?

AI was used as a supporting development and review tool. It helped organize the lexer implementation, explain lexical-analysis concepts, suggest token names and test cases, and review the relationship between the Part 1 Banana grammar and the Part 2 lexer requirements.

For Parts 4 and 5, AI also helped explain interpreter implementation concepts, AST traversal, expression evaluation, and runtime error handling. For Part 5, it provided guidance on function definitions, parameters, function calls, return values, recursion, local and global scope, and the implementation of for loops. AI also assisted with developing test cases and updating the grammar, README, and other project documentation.

The group remained responsible for reviewing, testing, and making the final implementation decisions.

## Which project components received AI assistance?

AI assistance was used for:

- Lexer structure and implementation ideas.
- Token naming and organization.
- Error-handling structure and suggestions for lexer test cases.
- Review of the Part 1 grammar for lexer compatibility.
- Interpreter implementation ideas and AST evaluation.
- Environment or symbol table concepts for storing and retrieving variable values.
- Arithmetic operations, comparisons, assignments, `if/else` statements, and `while` loops.
- Runtime error handling for undefined variables and division by zero.
- Test-case development, README updates, and project documentation.
- Function definitions, parameters, function calls, and return values.
- Local and global variable scope and recursion.
- The `for` loop extension feature.
- Part 5 automated tests, including function errors and recursive calls.
- Part 5 grammar, README, and AI Use Statement updates.

## Describe at least one AI-generated suggestion, explanation, or code segment that your group modified, corrected, rejected, or improved.

One AI-generated suggestion was to support decimal numbers because the Part 2 assignment listed integer and decimal numbers as possible lexer requirements. The group compared that suggestion with the actual Banana Part 1 grammar, which defines `<number>` as one or more digits. Because the existing grammar specifies integers, the implementation was kept integer-only rather than silently changing the language specification. The README documents this decision so the grammar and lexer remain consistent.

Another implementation decision was to add line and column information to tokens and lexical errors. This makes invalid input such as `@` easier to locate and provides a more meaningful error message.

For Parts 4 and 5, AI assistance also helped explain how an interpreter evaluates AST nodes and uses an environment to store variable names and values. These concepts were applied to the interpreter's handling of expressions, assignments, comparisons, conditional statements, loops, and runtime errors. The implementation was checked using automated tests and sample Banana programs.

During Part 5, AI suggested extending the parser to recognize function definitions and calls and adding a for loop as the extension feature. The group reviewed the implementation, updated an existing parser test that had expected function definitions to be unsupported, and tested the new behavior using automated tests and sample programs. The test results were used to verify the implementation rather than relying only on AI-generated suggestions.

## How did your group test or independently verify AI-assisted work?

The lexer was checked against the Banana Part 1 keyword list, operators, assignment operators, delimiters, and grammar. Automated tests cover variable declarations, arithmetic expressions, print statements, invalid input, control structures, and other supported language features.

For Part 5, the interpreter and lexer test suite was run using `python -m unittest discover -s tests -v`, and all 23 tests passed. The parser test suite was run using `python -m unittest discover -s part3 -v`, and all 22 tests passed, for a total of 45 passing automated tests. Additional sample programs demonstrated function parameters, return values, local and global scope, nested function calls, recursion, and for loops.

## What did your group learn from using AI during this milestone?

The group learned that AI suggestions must be checked against the project's actual language specification. A general assignment requirement can differ from the specific features chosen in the group's Part 1 language, so implementation decisions must remain consistent with the grammar.

The group also learned how an interpreter uses an AST to evaluate expressions and execute statements, how an environment stores and retrieves variable values, and why testing is important for identifying errors. AI was used as a supporting assistant and review resource, not as a replacement for the group's implementation, testing, or final technical decisions.