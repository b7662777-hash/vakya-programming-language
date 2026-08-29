# Vākya Module System

The **Vākya Module System** provides structured code reuse, encapsulation, and standard library integration using the `aayat` (आयात — *Import*) statement.

---

## 1. Syntax & Semantics

Modules are imported at the top of a file:

```vakya
aayat math
aayat utils
```

This compiles to a module load instruction (`OP_IMPORT_MODULE`), resolving the requested module and binding its exported table to a global variable matching the module name.

---

## 2. Module Resolution Priority

When an `aayat <name>` statement is encountered, the module loader searches paths in the following priority:

1. **Relative Directory**: The directory containing the importing `.vakya` file (e.g. `./utils.vakya`).
2. **Bundled Library**: PyInstaller runtime environment (`sys._MEIPASS/std/<name>.vakya`).
3. **Environment Home**: `$env:VAKYA_HOME/std/<name>.vakya`.
4. **Repository Standard Library**: Local development `std/<name>.vakya`.
5. **System Installation**: `%LOCALAPPDATA%\Programs\Vakya\std\<name>.vakya` (Windows) or `/usr/local/share/vakya/std/<name>.vakya` (Linux/macOS).

If the file cannot be located across all search paths, compiler diagnostic `E307: Module Not Found` is reported.

---

## 3. Creating a Custom Module

Create a file named `geometry.vakya`:

```vakya
// geometry.vakya
aayat math

dhruva PI = 3.141592653589793

karya circle_area(radius: sankhya) -> dashamika {
    pratyavartaya PI * math.varga(radius)
}

karya rectangle_area(w: sankhya, h: sankhya) -> sankhya {
    pratyavartaya w * h
}
```

Now import and use it in `main.vakya`:

```vakya
// main.vakya
aayat geometry

chara r = 10
vada("Circle Area:", geometry.circle_area(r))
vada("Rectangle Area:", geometry.rectangle_area(4, 5))
```

---

## 4. Circular Dependency Prevention

The module loader maintains an active loading stack. If module `A` imports module `B`, and module `B` attempts to directly or indirectly import `A`, the loader detects the cycle and reports error `E307: Circular module dependency detected`.
