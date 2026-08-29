# Vākya CLI Reference Manual

The `vakya` command-line interface provides tools for running, compiling, formatting, typechecking, and debugging Vākya programs.

---

## 1. Quick Reference

```text
vakya [COMMAND] [OPTIONS] [ARGUMENTS]
```

| Command | Description | Example |
| :--- | :--- | :--- |
| `vakya <file>` | Execute a Vākya file directly | `vakya hello.vakya` |
| `vakya run` | Execute with engine selection and options | `vakya run app.vakya --engine=vm` |
| `vakya check` | Typecheck & borrowcheck without running | `vakya check app.vakya` |
| `vakya build` | Compile program to standalone native binary | `vakya build app.vakya -o app` |
| `vakya fmt` | Format Vākya source code in place | `vakya fmt app.vakya --write` |
| `vakya disasm`| Disassemble bytecode instructions | `vakya disasm app.vakya` |
| `vakya repl` | Start interactive REPL | `vakya repl` |
| `vakya new` | Scaffold a new standard project structure | `vakya new my_app` |
| `vakya doctor`| System & environment self-diagnostic report | `vakya doctor` |
| `vakya env` | Display active environment resolution paths | `vakya env` |
| `vakya errors`| Display error catalog and remediation rules | `vakya errors --format=json` |
| `vakya test` | Run automated test suite | `vakya test` |
| `vakya version`| Display version information | `vakya version` |
| `vakya --gui` | Launch graphical desktop application | `vakya --gui` |

---

## 2. Command Details

### `vakya run`
Executes a `.vakya` source file.
```bash
vakya run <file.vakya> [OPTIONS]
```
**Options**:
- `--engine={vm|interpreter}`: Select execution engine (`vm` is default, `interpreter` uses AST tree-walker).
- `--trace`: Trace VM bytecode execution step-by-step with stack dumps.
- `--format={text|json}`: Output diagnostic format.

---

### `vakya check`
Runs static type checking and the Swamitva borrow checker without executing code.
```bash
vakya check <file.vakya> [--format=text|json]
```

---

### `vakya build`
Compiles a Vākya program into native C and invokes the system compiler (GCC, Clang, or MSVC) to produce a standalone executable binary.
```bash
vakya build <file.vakya> [-o output_name]
```

---

### `vakya fmt`
Formats Vākya source code according to the official style specification.
```bash
vakya fmt <file.vakya> [--write] [--check]
```
**Options**:
- `-w, --write`: Overwrites the file in place with formatted code.
- `-c, --check`: Checks whether the file is formatted without modifying it (returns exit code 1 if unformatted; ideal for CI).

---

### `vakya repl`
Launches the interactive read-eval-print loop with multi-line input and command history.
```bash
vakya repl
```

---

### `vakya disasm`
Compiles the program to bytecode and displays the disassembly table, constant pools, and instruction offsets.
```bash
vakya disasm <file.vakya>
```

---

### `vakya doctor`
Inspects the environment, standard library paths, backend compilers, and subsystem health.
```bash
vakya doctor
```

---

### `vakya new`
Scaffolds a new Vākya project with `src/main.vakya`, `vakya.toml`, and `README.md`.
```bash
vakya new my_project
```
