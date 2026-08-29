# Debugging and Disassembly in Vākya

Vākya provides built-in tools for inspecting bytecode execution, analyzing stack states, and debugging compiler outputs.

---

## 1. Bytecode Disassembly (`vakya disasm`)

To inspect compiled bytecode instructions, constants, upvalues, and source offsets:

```bash
vakya disasm examples/01_hello.vakya
```

Output:
```text
=== Bytecode Disassembly: <main> (params=0, locals=0, upvalues=0) ===
Constants:
  [00] 'Namaste, World!'
Instructions:
    2: CONSTANT           0
       STORE_GLOBAL       message
    3: LOAD_GLOBAL        message
       CALL_BUILTIN       vada 1
       POP
       NULL
       HALT
```

---

## 2. Instruction Trace Mode (`--trace`)

To trace VM execution step-by-step with the exact instruction pointer and stack contents:

```bash
vakya run examples/01_hello.vakya --trace
```

Output:
```text
[TRACE] IP=0000 OP=CONSTANT             STACK=[]
[TRACE] IP=0001 OP=STORE_GLOBAL         STACK=['Namaste, World!']
[TRACE] IP=0002 OP=LOAD_GLOBAL          STACK=[]
[TRACE] IP=0003 OP=CALL_BUILTIN         STACK=['Namaste, World!']
Namaste, World!
[TRACE] IP=0004 OP=POP                  STACK=['shunya']
[TRACE] IP=0005 OP=NULL                 STACK=[]
[TRACE] IP=0006 OP=HALT                 STACK=['shunya']
```
