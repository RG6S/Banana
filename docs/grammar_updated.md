# Banana Grammar Notes – Part 2

The lexer was implemented to match the Part 1 grammar.

## Token-related grammar

```text
<identifier> ::= <letter> { <letter> | <digit> | "_" } ;
<number> ::= <digit> { <digit> } ;

<assign-op> ::= "=" | "+=" | "-=" | "*=" | "/=" ;

<relop> ::= "==" | "!=" | "<" | ">" | "<=" | ">=" ;
```

The Part 1 grammar lists these keywords:

```text
let print if else while func return true false
```

No grammar changes were required for the lexer implementation.

### Lexer-specific clarification
The Part 1 grammar defines `<number>` as an integer sequence of digits. Decimal literals are therefore not recognized in this Part 2 implementation. If decimal numbers become part of the language, the grammar should first be updated and then the lexer should be changed to recognize that form.
