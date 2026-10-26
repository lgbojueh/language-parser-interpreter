# Language Parser & Interpreter

A small interpreted programming language built from scratch in Python.

This project demonstrates the full language-processing pipeline:

```text
Source code
   ↓
Lexer / Tokenizer
   ↓
Recursive-Descent Parser
   ↓
Abstract Syntax Tree
   ↓
Interpreter
   ↓
Program Output
```

## Why I Built It

The goal is to demonstrate core computer-science concepts that sit underneath compilers and interpreters rather than relying on a parser generator or framework.

The implementation includes lexical analysis, grammar design, recursive-descent parsing, AST construction, expression evaluation, variable storage, control flow, runtime validation, and automated tests.

## Language Features

- variable declarations with `let`
- variable reassignment
- integer and decimal numbers
- strings and booleans
- arithmetic: `+ - * /`
- comparisons: `< <= > >=`
- equality: `== !=`
- unary operators: `- !`
- `print` statements
- `if / else`
- `while` loops
- block statements
- comments beginning with `//`
- syntax errors with line/column information
- runtime errors for undefined variables, invalid operations, and division by zero

## Example

```text
let x = 5;
let total = 0;

while (x > 0) {
    total = total + x;
    x = x - 1;
}

if (total == 15) {
    print "sum is";
    print total;
} else {
    print "unexpected result";
}
```

Output:

```text
sum is
15
```

## Grammar

```text
program        -> statement* EOF ;

statement      -> "let" IDENT "=" expression ";"
                | IDENT "=" expression ";"
                | "print" expression ";"
                | "if" "(" expression ")" block ("else" block)?
                | "while" "(" expression ")" block
                | block ;

block          -> "{" statement* "}" ;

expression     -> equality ;
equality       -> comparison ( ("==" | "!=") comparison )* ;
comparison     -> term ( (">" | ">=" | "<" | "<=") term )* ;
term           -> factor ( ("+" | "-") factor )* ;
factor         -> unary ( ("*" | "/") unary )* ;
unary          -> ("!" | "-") unary | primary ;
primary        -> NUMBER
                | STRING
                | "true"
                | "false"
                | IDENT
                | "(" expression ")" ;
```

## Project Structure

```text
language-parser-interpreter/
├── src/minilang/
│   ├── ast_nodes.py
│   ├── cli.py
│   ├── errors.py
│   ├── interpreter.py
│   ├── lexer.py
│   ├── parser.py
│   └── tokens.py
├── examples/
│   └── demo.mini
├── tests/
├── .github/workflows/ci.yml
├── pyproject.toml
└── README.md
```

## Run It

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
minilang examples/demo.mini
```

You can also run:

```bash
PYTHONPATH=src python3 -m minilang.cli examples/demo.mini
```

Inspect lexer output:

```bash
minilang examples/demo.mini --tokens
```

Inspect the AST:

```bash
minilang examples/demo.mini --ast
```

Parse without running:

```bash
minilang examples/demo.mini --no-run
```

## Tests

```bash
pip install -r requirements-dev.txt
python -m pytest -q
```

## Technical Decisions

### Hand-written lexer
The lexer scans source text character by character, making token boundaries, keywords, literals, comments, and source locations explicit.

### Recursive-descent parser
Each grammar level maps directly to a parser method. Operator precedence is encoded by the parser call hierarchy.

### Explicit AST
The parser produces dataclass-based AST nodes before execution, keeping syntax recognition separate from runtime behavior.

### Runtime safeguards
The interpreter detects undefined variables, duplicate declarations, invalid arithmetic, division by zero, and runaway loops.

## Possible Extensions

- functions and return statements
- lexical scopes
- arrays
- REPL mode
- AST visualization
- static type checking
- bytecode compilation

## Portfolio Summary

Built a small interpreted language in Python using a hand-written lexer, recursive-descent parser, AST, and execution engine supporting variables, expressions, conditionals, loops, and structured error handling.
