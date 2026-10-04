# Banana — Language Design Document

## 1. Language Design — Name & Description

**Banana** is a simple programming language our group is designing and building as part of this course project. It is a small, C-style language. Variables are declared with `let`, code blocks use curly braces `{ }`, and statements end with semicolons, similar to languages like Java or JavaScript.

We kept the list of keywords and features small on purpose, since this is our first attempt at designing a grammar and building an interpreter. A simpler language is easier to get right within six weeks.

### Example

```banana
let x = 10;
let y = 20;

if (x < y) {
    print(x + y);
}
```

## 2. Required Features Checklist

Every required feature below is demonstrated in the grammar (§8) and/or the sample programs (§7).

| Requirement | Where it appears |
|---|---|
| Variable declaration & assignment | `<assignment>`; Sample A |
| Numeric values | `<number>`; all samples |
| Arithmetic `+ - * /` | `<expression>`, `<term>`; Sample A, B |
| Parentheses & precedence | `<factor>` allows `"(" <expression> ")"`; Sample A |
| Comparison operators | `<condition>`, `<relop>`; Sample A |
| Print statements | `<print-statement>`; all samples |
| if/else | `<if-statement>`; Sample A |
| while loops | `<while-statement>`; Sample B |
| Functions with parameters & return values | `<function-definition>`, `<return-statement>`; Sample C |
| Basic variable scope | Sample D (a variable inside a function does not leak to the outer scope) |
| Additional feature | Compound assignment (`+=`, `-=`, `*=`, `/=`); §9, Sample B |

---

## 3. Keywords, Operators, Delimiters

### Keywords

```text
let
print
if
else
while
func
return
```

### Operators

**Arithmetic:**

```text
+  -  *  /
```

**Comparison:**

```text
==  !=  <  >  <=  >=
```

**Assignment:**

```text
=  +=  -=  *=  /=
```

### Delimiters

```text
(  )  {  }  ,  ;
```

---

## 4. Variable Declaration / Assignment Syntax

Banana uses `let` to declare a new variable. Once a variable has been declared, it can be reassigned using `=` or one of the compound assignment operators.

### Variable declaration

```banana
let x = 10;
```

### Re-assignment

```banana
x = x + 1;
```

### Compound assignment

```banana
x += 5;
```

Other supported compound assignments include:

```banana
x -= 2;
x *= 3;
x /= 4;
```

The `let` keyword is used only when declaring a new variable.

---

## 5. Control-Structure Syntax

### If / Else

```banana
if (x < y) {
    print(x);
} else {
    print(y);
}
```

### While Loop

```banana
while (i < 10) {
    i += 1;
}
```

---

## 6. Function Syntax

Banana supports functions with parameters and return values.

```banana
func add(a, b) {
    return a + b;
}

let sum = add(3, 4);
```

Parameters and any `let`-declared variables inside a function body are local to that function and are not visible outside it (see Sample D).

---

## 7. Sample Programs

### Sample A — Arithmetic, Precedence, Comparison, If/Else

```banana
let x = 10;
let y = 20;

if (x < y) {
    print((x + y) * 2);
} else {
    print(x - y);
}
```

### Sample B — While Loop with Compound Assignment

```banana
let i = 0;
let sum = 0;

while (i < 10) {
    sum += i;
    i += 1;
}

print(sum);
```

### Sample C — Function with Parameters & Return Value

```banana
func square(n) {
    return n * n;
}

print(square(7));
```

### Sample D — Variable Scope

```banana
let x = 100;

func shadow() {
    let x = 1;
    return x + 1;
}

print(shadow());
print(x);
```

In Sample D, the `x` declared inside `shadow()` is local to the function. It does not change or leak into the outer scope where `x` is `100`.

---

## 8. BNF/EBNF Grammar

```text
<program> ::= { <statement> };

<statement> ::= <assignment>
              | <print-statement>
              | <if-statement>
              | <while-statement>
              | <function-definition>
              | <return-statement>
              | <block>;

<block> ::= "{" { <statement> "}";

<assignment> ::= "let" <identifier> "=" <expression> ";"
               | <identifier> <assign-op> <expression> ";";

<assign-op> ::= "=" | "+=" | "-=" | "*=" | "/=";

<print-statement> ::= "print" "(" <expression> ")" ";";

<condition> ::= <expression> <relop> <expression>;

<relop> ::= "==" | "!=" | "<" | ">" | "<=" | ">=";

<if-statement> ::= "if" "(" <condition> ")" <block>
                 [ "else" <block> ];

<while-statement> ::= "while" "(" <condition> ")" <block>;

<function-definition> ::= "func" <identifier> "(" [ <param-list> ] ")" <block>;

<param-list> ::= <identifier> { "," <identifier> };

<return-statement> ::= "return" [ <expression> ] ";";

<expression> ::= <term> { ("+" | "-") <term> };

<term> ::= <factor> { ("*" | "/") <factor> };

<factor> ::= <number>
           | <identifier>
           | <identifier> "(" [ <arg-list> ] ")"
           | "(" <expression> ")";

<arg-list> ::= <expression> { "," <expression> };

<identifier> ::= <letter> { <letter> | <digit> | "_" };

<number> ::= <digit> { <digit> };

<letter> ::= "a" | "b" | "c" | ... | "z"
           | "A" | "B" | "C" | ... | "Z";

<digit> ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9";
```

### Precedence Note

`*` and `/` happen before `+` and `-`, because `<term>` sits below `<expression>` in the grammar.

Parentheses always take priority because `<factor>` allows an expression inside parentheses:

```text
"(" <expression> ")"
```

For example:

```banana
(x + y) * 2
```

evaluates the expression inside the parentheses first. This is how the arithmetic and precedence example in Sample A works correctly.

---

## 9. Proposed Extension Feature: Compound Assignment

Banana adds compound assignment operators:

```text
+=
-=
*=
/=
```

These operators provide shorthand for common assignment operations.

For example:

```banana
i += 1;
```

is equivalent to:

```banana
i = i + 1;
```

Similarly:

```banana
x -= 2;
x *= 3;
x /= 4;
```

are shorthand forms of:

```banana
x = x - 2;
x = x * 3;
x = x / 4;
```

Compound assignment can only be used with an existing variable. The `let` keyword is used for new variable declarations and must be followed by the normal `=` operator.

This feature only requires a small addition to the assignment rules and provides useful day-to-day convenience while keeping the implementation cost relatively small during the project.




