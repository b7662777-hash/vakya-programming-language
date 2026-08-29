# Getting Started with Vākya

Welcome to the **Vākya Programming Language** (वाक्य).

This guide will help you set up your development environment, run your first Vākya programs, and understand the workflow of the Vākya toolchain.

---

## 1. Quick Setup

Make sure you have **Python 3.12+** installed on your system.

```bash
# Clone the repository
git clone https://github.com/vakya-lang/vakya.git
cd vakya

# Install the Vākya toolchain in editable mode
pip install -e .
```

Verify your installation:

```bash
vakya version
```

Output:
```text
Vākya v0.1.0 (Romanized Sanskrit Programming Language)
```

---

## 2. Running Your First Program

Create a file named `hello.vakya`:

```vakya
// hello.vakya
dhruva message = "Namaste, World!"
vada(message)
```

Execute it using the Vākya CLI:

```bash
vakya run hello.vakya
```

Output:
```text
Namaste, World!
```

---

## 3. Interactive REPL

Start the interactive Read-Eval-Print Loop:

```bash
vakya repl
```

```text
Vākya REPL v0.1.0 — Romanized Sanskrit Programming Language
Type '.help' for commands, '.exit' or Ctrl+D / Ctrl+C to exit.

>>> chara x = 10
>>> chara y = 20
>>> vada("Sum:", x + y)
Sum: 30
>>> .exit
Namaste!
```

---

## 4. Next Steps

- Explore [Language Basics](variables.md)
- Learn about [Types and Inference](types.md)
- Read the [Authoritative Language Specification](../LANGUAGE_SPEC.md)
