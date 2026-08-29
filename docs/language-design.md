# Vākya Language Design Rationale & Philosophy

## 1. Why Vākya?

Programming languages shape how developers conceptualize algorithms. Vākya (**वाक्य**, meaning *sentence* or *statement*) was conceived to marry the structured conceptual clarity of Sanskrit philosophy with modern software engineering ergonomics.

---

## 2. Key Design Tenets

### A. Romanized Sanskrit (Universal Keyboard Accessibility)
While Sanskrit is traditionally written in Devanagari script, Vākya adopts Roman/Latin script as its primary canonical source representation. This ensures that any standard developer keyboard worldwide can author Vākya programs without special IME configurations or input layers.

### B. Not a Toy Keyword-Replacement
Vākya is engineered from the ground up as a standalone programming language with:
- Formal EBNF grammar
- Custom lexer, parser, AST, and type checker
- Independent stack-based Bytecode Virtual Machine
- Explicit runtime value models and lexical closure cells
- Strict operator precedence and typing rules

### C. Developer Ergonomics First
- Deterministic formatting (`vakya fmt`)
- Caret-based formatted diagnostic error reports with helpful remediation tips
- Interactive REPL and bytecode disassembler
- Fast startup and cross-platform consistency
