# Vākya Testing & Verification Matrix

The **Vākya Test Suite** ensures reliability, type safety, memory safety, and engine parity across the entire compiler toolchain.

---

## 1. Test Matrix Summary

| Category | Path | Test Count | Focus |
| :--- | :--- | :--- | :--- |
| **Lexer & Tokens** | `tests/lexer/` | 24 | Unicode tokenization, escape sequences, number parsing |
| **Parser & AST** | `tests/parser/` | 38 | Recursive descent, operator precedence, grammar rules |
| **Type Checker** | `tests/typechecker/` | 52 | Type inference, type errors `E401`–`E407`, annotations |
| **Swamitva Borrow Checker**| `tests/borrow/` | 34 | Ownership, move semantics, borrow conflicts `E501`–`E505` |
| **AST Interpreter** | `tests/interpreter/` | 46 | Reference evaluation, closures, mutual recursion |
| **Bytecode & VM** | `tests/bytecode/`, `tests/vm/`| 68 | Chunk compilation, opcodes, stack machine execution |
| **Differential Testing** | `tests/differential/` | 28 | 100% output parity between VM and Interpreter |
| **Standard Library & Modules** | `tests/modules/` | 22 | `aayat` imports, stdlib math/string resolution |
| **Native C Emitter** | `tests/native/` | 18 | Linear IR, C emission, standalone execution |
| **CLI & Formatter** | `tests/cli/`, `tests/formatter/`| 32 | Process return codes, formatting checks, CLI flags |
| **Conformance & Fuzzing** | `tests/conformance/`, `tests/fuzzing/`| 86 | Language conformance, random tokens, edge cases |
| **Total Automated Tests** | `tests/` | **448** | **100% Pass Rate** |

---

## 2. Running Test Suites

### Running Full Suite
```bash
python -m unittest discover -s tests -p "test_*.py"
```
Or via the Vākya CLI:
```bash
vakya test
```

### Running Specific Test Groups
- **Borrow Checker**:
  ```bash
  python -m unittest discover -s tests/borrow -p "test_*.py"
  ```
- **Differential Parity (VM vs Interpreter)**:
  ```bash
  python -m unittest discover -s tests/differential -p "test_*.py"
  ```
- **CLI & Packaging**:
  ```bash
  python -m unittest tests/cli/test_cli.py
  ```
- **Showcase Applications**:
  ```bash
  python -m unittest discover -s showcase -p "test_*.py"
  ```

---

## 3. Differential Testing Architecture

To guarantee semantic equivalence between execution engines, the differential test suite compiles and runs canonical test cases through both the **Bytecode VM** and the **AST Interpreter**, asserting that standard output, returned values, and side effects are bit-for-bit identical.
