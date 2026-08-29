# Vākya Mini Browser Architecture Specification

## 1. System Overview

The **Vākya Mini Browser** is an educational, multi-tiered mini-browser demonstrating the path from language primitives to high-level networking, document parsing, DOM tree modeling, and visual rendering.

```
┌────────────────────────────────────────────────────────────────────────┐
│                        USER INTERFACE LAYER                            │
│  [UI] Window Shell, Address Bar, Back/Forward/Reload Controls, Tabs    │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
┌───────────────────────────────────▼────────────────────────────────────┐
│                    VĀKYA CORE ALGORITHMS & MODELS                      │
│  [Vākya] URL Parser (url_vibhaga / parse_url)                          │
│  [Vākya] History Stack (itihaasa_naya, itihaasa_push, pichhe, aage)     │
│  [Vākya] DOM Node Data Structures (dom_node, tag, attrs, children)     │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
┌───────────────────────────────────▼────────────────────────────────────┐
│                      HOST RUNTIME & ENGINE LAYER                       │
│  [Host Runtime] Socket Transport & HTTP Client (http_client.py)        │
│  [Browser Engine] HTML Tokenizer & Resilient Tree Builder (engine.py)  │
│  [Browser Engine] Text-mode Layout & Visual DOM Pipeline               │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Component Responsibility Matrix

| Component Layer | Responsibility | Language / Implementation |
| :--- | :--- | :--- |
| **`[Vākya]` URL Parser** | Parsing protocol schemes (`http`, `https`, `file`), hostname, path | `showcase/03_browser/vakya/browser.vakya` |
| **`[Vākya]` History Stack** | Maintaining backward/forward navigation history with truncation | `showcase/03_browser/vakya/browser.vakya` |
| **`[Vākya]` DOM Model** | Hierarchical map/list tree data representation | `showcase/03_browser/vakya/browser.vakya` |
| **`[Host Runtime]` HTTP Client** | Network transport, headers parsing, HTTP status resolution | `showcase/03_browser/browser/http_client.py` |
| **`[Browser Engine]` Parser** | Tokenizing HTML tags, comments, attributes, auto-closing unclosed tags | `showcase/03_browser/browser/engine.py` |
| **`[UI]` Browser Shell** | Visual window rendering, live DOM tree inspector, tab switching | `showcase/03_browser/ui/` |

---

## 3. Current Language Limitations & Honest Separation

### What Works Today in Native Vākya:
1. Pure URL parsing and string extraction (`parse_url`).
2. Complete navigation history stack algorithms with forward history truncation (`itihaasa_push`, `itihaasa_pichhe`, `itihaasa_aage`).
3. Recursive tree data structures storing arbitrary DOM nodes and attributes.

### What is Delegated to the Host Layer:
1. **Network Transport**: Vākya V1/V2 does not currently expose standard networking sockets (`jalam` / `http`). The host HTTP client handles TCP/TLS transport.
2. **Platform Windowing / GUI**: Vākya does not yet ship with an embedded GUI toolkit. The UI layer provides the visual viewport shell.

---

## 4. Proposed Future Vākya Native Networking API Concept

```vakya
// PROPOSED FUTURE VĀKYA API — (ROADMAP V3 SPECIFICATION)
// NOTE: Not implemented in current V2 Alpha.

aayat jalam // Import networking module

karya fetch_page(url: shabda) -> shabda {
    chara response = jalam.get(url)
    yadi response.status == 200 {
        pratyavartaya response.body
    } anyatha {
        pratyavartaya "Error: HTTP " + response.status
    }
}
```
