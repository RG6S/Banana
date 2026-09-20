# AI USE STATEMENT

## AI Tool(s) Used
ChatGPT (OpenAI).

## How did your group use AI for this project milestone?
AI was used as a supporting development and review tool. It helped organize the lexer implementation, explain lexical-analysis concepts, suggest token names and test cases, and review the relationship between the Part 1 Banana grammar and the Part 2 lexer requirements.

## Which project components received AI assistance?
AI assistance was used for:
- Lexer structure and implementation ideas.
- Token naming and organization.
- Error-handling structure.
- Suggestions for lexer test cases.
- README/documentation organization.
- Review of the Part 1 grammar for lexer compatibility.

The group remained responsible for reviewing, testing, and making the final implementation decisions.

## Describe at least one AI-generated suggestion, explanation, or code segment that your group modified, corrected, rejected, or improved.
One AI-generated suggestion was to support decimal numbers because the Part 2 assignment lists integer/decimal numbers as a possible lexer requirement. The group compared that suggestion with the actual Banana Part 1 grammar, which defines `<number>` as one or more digits. Because the existing grammar specifies integers, the implementation was kept integer-only rather than silently changing the language specification. The README documents this decision so the grammar and lexer remain consistent.

Another implementation decision was to add line/column information to tokens and lexical errors. This makes invalid input such as `@` easier to locate and gives a more meaningful error than an unexplained Python exception.

## How did your group test or independently verify AI-assisted work?
The lexer was independently checked against the Banana Part 1 keyword list, operators, assignment operators, delimiters, and grammar. Automated unit tests cover variable declarations, arithmetic expressions, print statements, if/else, invalid input, while loops with compound assignment, and functions with return values. The invalid-input test verifies that `@` raises `LexerError` with a readable message.

## What did your group learn from using AI during this milestone?
The group learned that AI suggestions must be checked against the project's actual language specification. In particular, a general assignment requirement can differ from the specific features chosen in the group's Part 1 language. Comparing the suggestion with the Banana grammar helped us avoid introducing an undocumented language feature.

AI was used as an assistant and review resource, not as a replacement for the group's implementation, testing, or final technical decisions.
