# Vākya Language Design & Architecture

## Philosophy

Vākya (*statement / sentence*) is designed around the core principle:

> **Modern programming structure + Sanskrit vocabulary + extremely readable syntax.**

Vākya is not natural Sanskrit grammar translated into a programming language. Rather, it is a formal programming language that adopts meaningful Sanskrit technical terms for its keywords, operators, and data types, written in Roman script.

## Execution Pipeline

Vākya V1 follows a clean tree-walking architecture with strict separation between frontend analysis and runtime evaluation:

```
Source (.vakya)
      │
      ▼
   Lexer  ──────────► Tokens (with line, column, start/end byte offsets)
      │
      ▼
   Parser ──────────► Abstract Syntax Tree (AST with Span locations)
      │
      ▼
Type Checker ───────► Semantic Validation & Type Inference
      │
      ▼
 Interpreter ───────► Lexical Environment & Evaluation
      │
      ▼
    Output
```

## Architectural Decoupling for Future Compilation

The V1 frontend (Lexer, Parser, AST, Type Checker) is completely decoupled from the runtime execution engine. This ensures that future versions (V2 bytecode VM or V3 LLVM/Cranelift native compiler) can reuse the exact same frontend pipeline without architectural rewrites.

## Lexical Scoping

Vākya implements lexical scoping with nested block environments. Variables declared with `chara` or constants declared with `dhruva` are accessible in their enclosing block and any inner nested blocks. Functions capture their enclosing environment at definition time, creating lexical closures.
