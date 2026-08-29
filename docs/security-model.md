# Vākya Capability-Based Security Architecture

## 1. Principles of Security vs Memory Safety

* **Memory Safety (*Swamitva*)**: Guarantees absence of undefined behavior, buffer overflows, use-after-free, and dangling references within the process memory space.
* **Security & Authorization**: Enforces strict privilege boundaries on external system resources (file system, network sockets, process execution, environment variables).

```text
┌─────────────────────────────────────────────────────────────┐
│                    VĀKYA APPLICATION CODE                   │
│                                                             │
│         pashya/chara (Compile-Time Memory Safety)           │
│                             │                               │
│                             ▼                               │
│                  CAPABILITY ENFORCEMENT                     │
│               [anumati filesystem.read = false]             │
│                             │                               │
│                   ❌ PERMISSION DENIED                      │
└─────────────────────────────┬───────────────────────────────┘
                              │
                    HOST OPERATING SYSTEM
```

---

## 2. Capability Permissions Matrix

| Capability String | Description | Default Policy |
| :--- | :--- | :--- |
| `filesystem.read` | Read files from local disk | Denied (Explicit opt-in required) |
| `filesystem.write` | Create, modify, or delete files | Denied |
| `network.connect` | Open outbound TCP/UDP connections | Denied |
| `network.listen` | Bind inbound network sockets | Denied |
| `process.spawn` | Execute host shell sub-processes | Denied |
| `env.read` | Read system environment variables | Denied |

---

## 3. CLI Permission Flags (Roadmap)

```bash
# Sandboxed by default (zero filesystem/network access)
vakya run app.vakya

# Explicitly granted read access to data directory
vakya run app.vakya --allow-read=./data/

# Explicitly granted outbound network access
vakya run server.vakya --allow-net=api.example.com
```
