# Vākya Security & Capability Model

Vākya's design philosophy is **secure by default**.

---

## 1. Principles of Security

1. **No Ambient Authority**: Programs cannot access arbitrary files, network sockets, or subprocesses unless explicitly granted permission.
2. **Safe Memory Boundaries**: The runtime prevents buffer overflows, dangling pointers, and type confusion.
3. **No Arbitrary Code Execution**: Vākya explicitly forbids `eval`, `exec`, or dynamic runtime code injection.

---

## 2. Future Capability System (`anumati`)

In future Vākya versions, programs must declare or be granted explicit capabilities to access sensitive OS resources:

```vakya
// PROPOSED FUTURE VĀKYA PERMISSION DECLARATION
anumati filesystem.read("/var/log")
anumati network.connect("api.example.com")
```

### CLI Capability Flags
```bash
vakya run app.vakya --allow-net --allow-read=/data
```
Any attempt to perform unauthorized I/O without the required permission raises a security violation.
