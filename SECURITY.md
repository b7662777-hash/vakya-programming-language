# Security Policy

## Supported Versions

| Version | Supported          |
| :---    | :---               |
| 0.1.x   | :white_check_mark: |
| < 0.1.0 | :x:                |

---

## Reporting a Vulnerability

The Vākya project takes security seriously. If you discover a security vulnerability in Vākya, please follow responsible disclosure guidelines:

1. **Do NOT open a public GitHub issue.**
2. Please report the vulnerability privately via **[GitHub Security Advisories](https://github.com/vakya-lang/vakya/security/advisories/new)**.
3. Include:
   - Detailed description of the vulnerability.
   - Steps or proof-of-concept code to reproduce the issue.
   - Potential impact and affected subsystems (e.g. parser, bytecode VM, memory safety borrow checker, or standard library).

The core maintainers will acknowledge receipt within 48 hours and provide updates regarding triaging and resolution.

---

## Security Model & Scope

Vākya incorporates:
- **Lexical & Parser Sandboxing**: Strict limits on source file size, identifier length, and nested AST depth.
- **VM Execution Limits**: Call stack recursion depth bounds and opcode instruction budgeting.
- **Compile-Time Memory Safety (Swamitva)**: Static verification of ownership and borrowing invariants without runtime garbage collection overhead.
