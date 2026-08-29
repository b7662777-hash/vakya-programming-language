# Vākya Parser Architecture & AST Construction

## 1. Overview

The Vākya parser (`src/vakya/parser/parser.py`) is a handwritten **recursive-descent predictive parser** operating on a token stream produced by the Lexer.

---

## 2. Parsing Pipeline

1. **Token Ingestion**: Takes `List[Token]` with exact source positions (`line`, `column`, `length`).
2. **Top-Level Hoisting**: Function declarations (`FunctionDecl`) and variable declarations (`VarDecl`) are parsed into an Abstract Syntax Tree (`Program`).
3. **Expression Precedence (Pratt / Precedence Climbing)**:
   - Level 8: Postfix (Calls, Indexing, Member Access)
   - Level 7: Unary (`-`, `na`)
   - Level 6: Power (`**`, right-associative)
   - Level 5: Multiplicative (`*`, `/`, `%`)
   - Level 4: Additive (`+`, `-`)
   - Level 3: Relational (`<`, `<=`, `>`, `>=`)
   - Level 2: Equality (`==`, `!=`)
   - Level 1: Logical (`evam`, `va`)
4. **Panic Mode Error Recovery**: Resynchronizes to statement boundaries (`chara`, `dhruva`, `karya`, `yadi`, `yavat`, `pratyekam`, `virama`, `agaccha`, `pratyavartaya`) on syntax errors.
