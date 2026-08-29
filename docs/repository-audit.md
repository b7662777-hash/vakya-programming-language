# Vākya Repository Audit & File Inventory

This audit documents every directory and file category within the **Vākya Programming Language** codebase, establishing retention, gitignore, and packaging decisions for the open-source GitHub release.

---

## 1. Directory & File Inventory

| Path / Pattern | Category | Purpose | Decision | Rationale |
| :--- | :--- | :--- | :--- | :--- |
| `src/vakya/` | Core Source | Lexer, Parser, AST, Type Checker, Swamitva Borrow Checker, Bytecode Compiler, VM, AST Interpreter, C-Emitter, CLI, GUI Launcher, and Error Diagnostics | **KEEP** | Core production compiler and runtime codebase. |
| `std/` | Standard Library | Built-in standard library modules (`math.vakya`, `string.vakya`, `io.vakya`, `time.vakya`, etc.) | **KEEP** | Essential standard library files bundled with distributions. |
| `runtime/` | Native Runtime | Minimal standalone C headers and runtime primitives (`vakya_runtime.h`, `vakya_runtime.c`) for compiled native binaries | **KEEP** | Required for `vakya build` C-emitter compilation. |
| `resources/` | Application Assets | High-resolution application icons (`vakya.ico`, `vakya.png`) | **KEEP** | Required for desktop GUI and Windows installer metadata. |
| `examples/` | Conformance Examples | 14 canonical Vākya code examples (`01_hello.vakya` through `14_project.vakya`) | **KEEP** | Reference language examples and integration test fixtures. |
| `showcase/` | Showcase Projects | Real-world applications built with Vākya (CLI tool, Calculator, Browser host) | **KEEP** | End-to-end applications demonstrating real-world language utility. |
| `tests/` | Test Suite | Unit, conformance, regression, borrow checker, differential, fuzzing, and CLI tests (448 tests) | **KEEP** | Complete verification and CI regression testing suite. |
| `benchmarks/` | Benchmarking | Baseline performance measurement scripts and profilers | **KEEP** | Empirical validation of compiler and VM speed. |
| `scripts/` | Tooling & Automation | Build scripts, packaging automation, icon generation, and standalone smoke tests | **KEEP** | Maintainer and CI build tooling. |
| `installer/` | Distribution Tooling | Windows installer scripts (`install.ps1`, `uninstall.ps1`, `vakya_installer.iss`) | **KEEP** | Source scripts for generating Windows installers. |
| `docs/` | Documentation | Architecture, language specification, keywords, type system, memory safety, CLI, and guides | **KEEP** | Authoritative developer and contributor documentation. |
| `.github/` | GitHub Workflows & Templates | CI, Windows build, release workflows, issue templates, PR template, dependabot | **KEEP** | Standard GitHub repository governance and automation. |
| `pyproject.toml` | Build Configuration | Python package metadata, entry points, dependencies, and build settings | **KEEP** | Standard Python packaging configuration. |
| `LICENSE` | Legal | MIT License definition | **KEEP** | Authoritative open-source license. |
| `README.md` | Repository Overview | Project homepage, quickstart, examples, architecture, and guides | **KEEP** | Public entry point for GitHub visitors. |
| `CONTRIBUTING.md` | Contributor Guide | Development setup, coding guidelines, testing instructions, and PR workflow | **KEEP** | Standard open-source contribution guide. |
| `CODE_OF_CONDUCT.md` | Community Governance | Contributor Covenant Code of Conduct v2.1 | **KEEP** | Standard community conduct guidelines. |
| `SECURITY.md` | Security Policy | Vulnerability disclosure policy and supported versions | **KEEP** | Standard security reporting instructions. |
| `CHANGELOG.md` | Release History | Semantic version changelog | **KEEP** | Official release notes. |
| `ROADMAP.md` | Future Plans | Project development milestones and future compiler backends | **KEEP** | Community and engineering roadmap. |
| `AUTHORS.md` | Attribution | Core team and contributor credits | **KEEP** | Contributor attribution. |
| `.gitignore` | Git Configuration | Ignore patterns for binaries, caches, and build outputs | **KEEP** | Prevents binary pollution of Git history. |
| `.gitattributes` | Git Configuration | Line ending normalization and binary flag declarations | **KEEP** | Ensures consistent line endings across platforms. |
| `.editorconfig` | Editor Configuration | Formatting rules (indentation, charset, trim whitespace) | **KEEP** | Ensures cross-editor code consistency. |
| `vakya.spec` | PyInstaller Spec | PyInstaller packaging specification | **KEEP** | Used by CI and release workflows to build standalone executables. |
| `dist/` | Build Artifacts | Compiled standalone binaries (`vakya.exe`, release `.zip`) | **GITIGNORE** | Binaries belong in GitHub Releases, not Git source trees. |
| `build/` | Build Artifacts | Intermediate compilation and PyInstaller caches | **GITIGNORE** | Transient build directories. |
| `__pycache__/`, `*.pyc` | Python Caches | Bytecode compilation caches | **GITIGNORE** | Machine-generated transient files. |
| `.pytest_cache/` | Test Caches | Pytest metadata and cache files | **GITIGNORE** | Transient test artifacts. |
| `*.egg-info/` | Packaging Caches | Setuptools build metadata | **GITIGNORE** | Generated during package installation. |

---

## 2. Hardcoded Path & Secret Audit Results

- **Secrets & Credentials**: 0 leaks found (scanned for `ghp_`, `github_pat_`, `sk-`, `AKIA`, credentials).
- **Machine Paths**: All absolute local paths (`file:///r:/...`, `C:\Users\...`) have been sanitized and converted to repository-relative Markdown links.
- **Git History**: Clean 1-commit baseline; no binaries or secrets exist in repository history.
