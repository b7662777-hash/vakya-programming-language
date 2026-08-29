# Vākya Release Process & Engineering

This document describes the release engineering procedure, artifact definitions, and automated publishing pipeline for the **Vākya Programming Language**.

---

## 1. Source Repository vs Binary Releases

- **GitHub Source Repository**: Contains clean source code, standard library modules, native runtime headers, tests, documentation, examples, and build automation. **No pre-compiled binaries (`.exe`, `.zip`) are stored in Git history.**
- **GitHub Releases**: Attached compiled binary artifacts (`vakya.exe`, `Vakya-v0.1.0-Windows-x64.zip`) and cryptographic SHA-256 checksum manifests built automatically by GitHub Actions.

---

## 2. Release Artifacts

For each stable release tag `vX.Y.Z`:

| Artifact | Format | Description |
| :--- | :--- | :--- |
| `vakya.exe` | Single-File Executable | Standalone portable executable with CLI, VM, Interpreter, stdlib, docs, and Desktop GUI |
| `Vakya-vX.Y.Z-Windows-x64.zip` | Compressed Archive | Complete distribution with `bin/vakya.exe`, `std/`, `runtime/`, `docs/`, `examples/`, `install.ps1`, `uninstall.ps1` |
| `release-manifest.json` | JSON Manifest | Cryptographic SHA-256 checksums and build metadata |

---

## 3. Release Automation Pipeline

When a version tag (e.g. `git tag v0.1.0 && git push origin v0.1.0`) is pushed to GitHub:

1. **`.github/workflows/release.yml`** triggers on the `windows-latest` runner.
2. Checks out the repository and installs build dependencies (`pyinstaller`, `pillow`).
3. Runs the complete 448-test test suite and CLI smoke tests.
4. Executes `scripts/build_windows.ps1` to compile the standalone binary.
5. Runs isolated acceptance tests in a clean temporary directory.
6. Computes SHA-256 hashes.
7. Publishes a new GitHub Release with attached assets and release notes.

---

## 4. Release Checklist

- [ ] Version updated consistently in `pyproject.toml`, `src/vakya/__init__.py`, `LANGUAGE_SPEC.md`, `CHANGELOG.md`.
- [ ] All 448 automated unit tests pass cleanly (`python -m unittest discover -s tests`).
- [ ] All showcase application tests pass cleanly (`python -m unittest discover -s showcase`).
- [ ] Standalone smoke tests pass (`scripts/test_gui_windows.ps1`).
- [ ] Changelog updated with new features and fixes under `[X.Y.Z]`.
- [ ] Git tag pushed: `git tag vX.Y.Z && git push origin vX.Y.Z`.
