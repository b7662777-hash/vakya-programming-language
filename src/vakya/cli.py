"""Vākya Command-Line Interface (CLI)."""

import argparse
import json
import os
import sys
import unittest
from typing import List, Optional
from vakya import __version__
from vakya.lexer.lexer import Lexer
from vakya.parser.parser import Parser
from vakya.typechecker.checker import TypeChecker
from vakya.interpreter.interpreter import Interpreter
from vakya.bytecode.compiler import BytecodeCompiler
from vakya.vm.vm import VirtualMachine
from vakya.formatter.formatter import Formatter
from vakya.repl.repl import REPL
from vakya.native.compiler import NativeCompiler
from vakya.errors import VakyaError
from vakya.errors.codes import (
    E001_INVALID_CHAR,
    E002_UNTERMINATED_STRING,
    E003_UNTERMINATED_COMMENT,
    E004_INVALID_ESCAPE,
    E005_INVALID_NUMBER,
    E101_UNDEFINED_VARIABLE,
    E102_UNDEFINED_FUNCTION,
    E103_CONSTANT_REASSIGNMENT,
    E104_DUPLICATE_DECLARATION,
    E105_INVALID_ASSIGNMENT_TARGET,
    E201_UNEXPECTED_TOKEN,
    E202_EXPECTED_TOKEN,
    E203_EXPECTED_EXPRESSION,
    E204_INVALID_PARAM,
    E205_INVALID_LOOP_SYNTAX,
    E206_INVALID_BREAK_CONTINUE,
    E207_INVALID_RETURN,
    E301_DIVISION_BY_ZERO,
    E302_INDEX_OUT_OF_BOUNDS,
    E303_KEY_NOT_FOUND,
    E304_RECURSION_LIMIT,
    E305_NOT_CALLABLE,
    E306_RUNTIME_TYPE_ERROR,
    E307_INVALID_PROPERTY,
    E401_TYPE_MISMATCH,
    E402_ARGUMENT_TYPE_MISMATCH,
    E403_RETURN_TYPE_MISMATCH,
    E404_OPERATOR_TYPE_MISMATCH,
    E405_UNARY_TYPE_MISMATCH,
    E406_ARGUMENT_COUNT_MISMATCH,
    E407_NOT_INDEXABLE,
    E501_USE_AFTER_MOVE,
    E502_MUTABLE_BORROW_CONFLICT,
    E503_MULTIPLE_MUTABLE_BORROWS,
    E504_DANGLING_REFERENCE,
    E505_MUTATION_WHILE_BORROWED,
)


def execute_file(
    file_path: str,
    check_only: bool = False,
    engine: str = "vm",
    trace: bool = False,
    output_format: str = "text",
    optimize: bool = False,
) -> int:
    """Read, parse, typecheck, and execute a .vakya file using Bytecode VM or Interpreter."""
    if not os.path.exists(file_path):
        if output_format == "json":
            print(json.dumps({"status": "error", "error": {"code": "E000", "message": f"File not found: '{file_path}'"}}))
        else:
            sys.stderr.write(f"Error: File not found: '{file_path}'\n")
        return 1

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            source_code = f.read()
    except Exception as ex:
        if output_format == "json":
            print(json.dumps({"status": "error", "error": {"code": "E000", "message": str(ex)}}))
        else:
            sys.stderr.write(f"Error reading file '{file_path}': {ex}\n")
        return 1

    filename = os.path.basename(file_path)

    try:
        # Lexer
        lexer = Lexer(source_code, filename=filename)
        tokens = lexer.tokenize()

        # Parser
        parser = Parser(tokens, source_code=source_code, filename=filename)
        ast = parser.parse()

        # Type checker
        typechecker = TypeChecker(source_code=source_code, filename=filename)
        typechecker.check(ast)

        if check_only:
            if output_format == "json":
                print(json.dumps({"status": "ok", "file": file_path, "errors": []}))
            else:
                print(f"Check passed: No syntax or type errors found in '{file_path}'.")
            return 0

        if engine == "interpreter":
            # Reference AST Interpreter
            interpreter = Interpreter(source_code=source_code, filename=filename)
            interpreter.interpret(ast)
        else:
            # Default V2 Bytecode Virtual Machine
            compiler = BytecodeCompiler(filename=filename, source_code=source_code, optimize=optimize)
            chunk = compiler.compile(ast)
            vm = VirtualMachine(trace=trace)
            vm.run(chunk)

        return 0

    except VakyaError as err:
        if output_format == "json":
            err_dict = {
                "status": "error",
                "file": file_path,
                "error": {
                    "code": err.code,
                    "message": err.message,
                    "line": err.line,
                    "column": err.column,
                    "length": err.length,
                    "help": err.help_text,
                }
            }
            print(json.dumps(err_dict, indent=2))
        else:
            sys.stderr.write(f"\n{err.format_diagnostic(source_code)}\n\n")
        return 1
    except Exception as ex:
        if output_format == "json":
            print(json.dumps({"status": "error", "error": {"code": "E000", "message": f"Internal compiler error: {ex}"}}))
        else:
            sys.stderr.write(f"Internal compiler error: {ex}\n")
        return 1


def disassemble_file(file_path: str) -> int:
    """Read, parse, typecheck, compile, and disassemble a .vakya file."""
    if not os.path.exists(file_path):
        sys.stderr.write(f"Error: File not found: '{file_path}'\n")
        return 1

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            source_code = f.read()
    except Exception as ex:
        sys.stderr.write(f"Error reading file '{file_path}': {ex}\n")
        return 1

    filename = os.path.basename(file_path)

    try:
        lexer = Lexer(source_code, filename=filename)
        tokens = lexer.tokenize()
        parser = Parser(tokens, source_code=source_code, filename=filename)
        ast = parser.parse()
        typechecker = TypeChecker(source_code=source_code, filename=filename)
        typechecker.check(ast)

        compiler = BytecodeCompiler(filename=filename, source_code=source_code)
        chunk = compiler.compile(ast)
        print(chunk.disassemble())
        return 0
    except VakyaError as err:
        sys.stderr.write(f"\n{err.format_diagnostic(source_code)}\n\n")
        return 1
    except Exception as ex:
        sys.stderr.write(f"Disassembly error: {ex}\n")
        return 1


def format_file(file_path: str, write_in_place: bool = False, check_only: bool = False) -> int:
    """Format a .vakya source file."""
    if not os.path.exists(file_path):
        sys.stderr.write(f"Error: File not found: '{file_path}'\n")
        return 1

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            source_code = f.read()
    except Exception as ex:
        sys.stderr.write(f"Error reading file '{file_path}': {ex}\n")
        return 1

    formatter = Formatter()
    try:
        formatted = formatter.format_source(source_code, filename=os.path.basename(file_path))
    except VakyaError as err:
        sys.stderr.write(f"Formatting failed due to syntax error:\n{err.format_diagnostic(source_code)}\n")
        return 1

    if check_only:
        if source_code == formatted:
            print(f"'{file_path}' is already properly formatted.")
            return 0
        else:
            sys.stderr.write(f"'{file_path}' is not properly formatted.\n")
            return 1

    if write_in_place:
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(formatted)
            print(f"Formatted '{file_path}'")
            return 0
        except Exception as ex:
            sys.stderr.write(f"Error writing formatted file: {ex}\n")
            return 1
    else:
        sys.stdout.write(formatted)
        return 0


def build_file(file_path: str, output_path: Optional[str] = None) -> int:
    """Compile a .vakya program to C source and native executable."""
    if not os.path.exists(file_path):
        sys.stderr.write(f"Error: File not found: '{file_path}'\n")
        return 1

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            source_code = f.read()
    except Exception as ex:
        sys.stderr.write(f"Error reading file '{file_path}': {ex}\n")
        return 1

    base_name = os.path.splitext(file_path)[0]
    out_target = output_path if output_path else base_name

    compiler = NativeCompiler(filename=os.path.basename(file_path))
    success, msg = compiler.build_executable(source_code, out_target)
    if success:
        print(msg)
        return 0
    else:
        print(msg)
        return 0 if msg.startswith("C source generated") else 1


def create_new_project(project_name: str) -> int:
    """Scaffold a new standard Vākya project."""
    if os.path.exists(project_name):
        sys.stderr.write(f"Error: Directory '{project_name}' already exists.\n")
        return 1

    try:
        os.makedirs(os.path.join(project_name, "src"), exist_ok=True)
        os.makedirs(os.path.join(project_name, "tests"), exist_ok=True)

        # vakya.toml
        with open(os.path.join(project_name, "vakya.toml"), "w", encoding="utf-8") as f:
            f.write(f"""[project]
name = "{project_name}"
version = "0.1.0"
entry = "src/main.vakya"

[dependencies]
""")

        # src/main.vakya
        with open(os.path.join(project_name, "src", "main.vakya"), "w", encoding="utf-8") as f:
            f.write("""// Vākya Project Entry Point

karya main() {
    vada("Namaste Vākya Project!")
}

main()
""")

        # README.md
        with open(os.path.join(project_name, "README.md"), "w", encoding="utf-8") as f:
            f.write(f"""# {project_name}

A new Vākya project.

## Running
```bash
vakya run src/main.vakya
```
""")

        print(f"Created new Vākya project '{project_name}'.")
        return 0
    except Exception as e:
        sys.stderr.write(f"Error creating project: {e}\n")
        return 1


scaffold_project = create_new_project


def dump_errors(output_format: str = "text") -> int:
    """Display the entire catalog of Vākya error codes."""
    all_errors = [
        E001_INVALID_CHAR, E002_UNTERMINATED_STRING, E003_UNTERMINATED_COMMENT, E004_INVALID_ESCAPE, E005_INVALID_NUMBER,
        E101_UNDEFINED_VARIABLE, E102_UNDEFINED_FUNCTION, E103_CONSTANT_REASSIGNMENT, E104_DUPLICATE_DECLARATION, E105_INVALID_ASSIGNMENT_TARGET,
        E201_UNEXPECTED_TOKEN, E202_EXPECTED_TOKEN, E203_EXPECTED_EXPRESSION, E204_INVALID_PARAM, E205_INVALID_LOOP_SYNTAX,
        E206_INVALID_BREAK_CONTINUE, E207_INVALID_RETURN,
        E301_DIVISION_BY_ZERO, E302_INDEX_OUT_OF_BOUNDS, E303_KEY_NOT_FOUND, E304_RECURSION_LIMIT, E305_NOT_CALLABLE,
        E306_RUNTIME_TYPE_ERROR, E307_INVALID_PROPERTY,
        E401_TYPE_MISMATCH, E402_ARGUMENT_TYPE_MISMATCH, E403_RETURN_TYPE_MISMATCH, E404_OPERATOR_TYPE_MISMATCH,
        E405_UNARY_TYPE_MISMATCH, E406_ARGUMENT_COUNT_MISMATCH, E407_NOT_INDEXABLE,
        E501_USE_AFTER_MOVE, E502_MUTABLE_BORROW_CONFLICT, E503_MULTIPLE_MUTABLE_BORROWS,
        E504_DANGLING_REFERENCE, E505_MUTATION_WHILE_BORROWED,
    ]

    if output_format == "json":
        err_list = [{"code": e.code, "title": e.title, "help": e.default_help} for e in all_errors]
        print(json.dumps({"error_codes": err_list}, indent=2))
    else:
        print("=" * 70)
        print("VĀKYA DIAGNOSTIC ERROR CODES CATALOG")
        print("=" * 70)
        for e in all_errors:
            print(f"[{e.code}] {e.title}")
            if e.default_help:
                print(f"       Help: {e.default_help}")
    return 0


def run_tests(test_path: Optional[str] = None) -> int:
    """Run automated test suite."""
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    if hasattr(sys.stderr, "reconfigure"):
        try:
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

    start_dir = test_path if test_path and os.path.exists(test_path) else os.path.join(os.path.dirname(__file__), "..", "..", "tests")
    start_dir = os.path.abspath(start_dir)

    print(f"Running Vakya test suite in: {start_dir}")
    loader = unittest.TestLoader()
    top_level_dir = os.path.dirname(start_dir)
    suite = loader.discover(start_dir, pattern="test_*.py", top_level_dir=top_level_dir)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return 0 if result.wasSuccessful() else 1


def run_doctor() -> int:
    """Run environment and system self-diagnostics."""
    import platform
    import shutil
    from vakya.paths import get_vakya_home, get_stdlib_path, get_runtime_path

    home = get_vakya_home()
    stdlib = get_stdlib_path()
    runtime = get_runtime_path()

    print("=" * 60)
    print("VĀKYA SYSTEM DIAGNOSTIC (DOCTOR)")
    print("=" * 60)
    print(f"Vākya Version:      v{__version__}")
    print(f"Operating System:   {platform.system()} {platform.release()} ({platform.machine()})")
    print(f"Python Runtime:     {sys.version.split()[0]} ({'Bundled Standalone' if getattr(sys, 'frozen', False) else 'Host System'})")
    print(f"Vākya Installation: {home}")

    if os.path.exists(stdlib):
        mods = [f for f in os.listdir(stdlib) if f.endswith(".vakya")]
        print(f"Standard Library:   OK ({len(mods)} modules found at {stdlib})")
    else:
        print(f"Standard Library:   MISSING ({stdlib})")

    if os.path.exists(runtime):
        print(f"Native Runtime:     OK (Headers found at {runtime})")
    else:
        print(f"Native Runtime:     MISSING ({runtime})")

    print("Default Engine:     Bytecode VM (IntEnum Flat Dispatch)")
    print("Fallback Engine:    Reference AST Interpreter")

    cc = shutil.which("gcc") or shutil.which("clang") or shutil.which("cl") or shutil.which("tcc")
    if cc:
        print(f"Host C Compiler:    OK ({cc})")
    else:
        print("Host C Compiler:    Not found on PATH (C source emission active)")

    clang = shutil.which("clang")
    if clang:
        print(f"LLVM Toolchain:     OK ({clang})")
    else:
        print("LLVM Toolchain:     Not found on PATH (LLVM IR generator active)")

    print("=" * 60)
    return 0


def dump_env() -> int:
    """Display active environment and resource resolution paths."""
    from vakya.paths import get_vakya_home, get_stdlib_path, get_runtime_path

    print(f"VAKYA_VERSION={__version__}")
    print(f"VAKYA_HOME={get_vakya_home()}")
    print(f"VAKYA_STDLIB={get_stdlib_path()}")
    print(f"VAKYA_RUNTIME={get_runtime_path()}")
    print(f"VAKYA_FROZEN={'true' if getattr(sys, 'frozen', False) else 'false'}")
    return 0


def hide_console_window_if_windows():
    """Immediately hide the console window when launching GUI mode on Windows."""
    if sys.platform == "win32":
        try:
            import ctypes
            hwnd = ctypes.windll.kernel32.GetConsoleWindow()
            if hwnd:
                ctypes.windll.user32.ShowWindow(hwnd, 0)
        except Exception:
            pass


def main(argv: Optional[List[str]] = None) -> int:
    """CLI / GUI entry point."""
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    if hasattr(sys.stderr, "reconfigure"):
        try:
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

    if argv is None:
        argv = sys.argv[1:]

    # 1. Dual-Mode Dispatch: No arguments = GUI Launcher
    if not argv:
        hide_console_window_if_windows()
        from vakya.gui import launch_gui
        launch_gui()
        return 0

    # 2. Explicit GUI flag / command
    if argv[0] in ("--gui", "-g", "gui"):
        hide_console_window_if_windows()
        target_file = argv[1] if len(argv) > 1 else None
        from vakya.gui import launch_gui
        launch_gui(initial_file=target_file)
        return 0

    # Handle direct shorthand execution: vakya <file.vakya> -> vakya run <file.vakya>
    KNOWN_COMMANDS = {"new", "build", "run", "disasm", "check", "fmt", "errors", "repl", "test", "version", "doctor", "env", "help", "gui"}
    if argv and not argv[0].startswith("-") and argv[0] not in KNOWN_COMMANDS:
        if argv[0].endswith(".vakya") or os.path.exists(argv[0]):
            argv = ["run"] + argv

    parser = argparse.ArgumentParser(
        prog="vakya",
        description="Vākya — Romanized Sanskrit Programming Language CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  vakya hello.vakya                         Execute a Vākya program directly
  vakya run examples/01_hello.vakya         Execute a Vākya program
  vakya build examples/01_hello.vakya       Compile program to native C/binary
  vakya check examples/01_hello.vakya       Typecheck without executing
  vakya check app.vakya --format=json       Machine-readable diagnostic output
  vakya disasm examples/01_hello.vakya      Disassemble into bytecode
  vakya fmt examples/01_hello.vakya --write Format a source file
  vakya repl                                Start interactive REPL
  vakya doctor                              System self-diagnostic report
  vakya env                                 Display environment and resource paths
  vakya errors --format=json                Display error catalog as JSON
  vakya test                                Run test suite
  vakya version                             Show version information
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # new
    new_parser = subparsers.add_parser("new", help="Scaffold a new Vākya project")
    new_parser.add_argument("name", help="Name of project directory to create")

    # build
    build_parser = subparsers.add_parser("build", help="Compile a .vakya file into native C/binary")
    build_parser.add_argument("file", help="Path to .vakya file")
    build_parser.add_argument("-o", "--output", help="Output binary name/path")
    build_parser.add_argument("--backend", choices=["c", "llvm"], default="c", help="Native backend (default: c)")

    # run
    run_parser = subparsers.add_parser("run", help="Execute a .vakya source file")
    run_parser.add_argument("file", help="Path to .vakya file")
    run_parser.add_argument("--engine", choices=["vm", "interpreter"], default="vm", help="Execution engine (default: vm)")
    run_parser.add_argument("--trace", action="store_true", help="Trace VM bytecode instruction execution")
    run_parser.add_argument("--format", choices=["text", "json"], default="text", help="Output format (default: text)")

    # disasm
    disasm_parser = subparsers.add_parser("disasm", help="Disassemble a .vakya file into bytecode instructions")
    disasm_parser.add_argument("file", help="Path to .vakya file")

    # check
    check_parser = subparsers.add_parser("check", help="Typecheck a .vakya file without running")
    check_parser.add_argument("file", help="Path to .vakya file")
    check_parser.add_argument("--format", choices=["text", "json"], default="text", help="Output format (default: text)")

    # fmt
    fmt_parser = subparsers.add_parser("fmt", help="Format a .vakya source file")
    fmt_parser.add_argument("file", help="Path to .vakya file")
    fmt_parser.add_argument("-w", "--write", action="store_true", help="Write formatted output directly to file")
    fmt_parser.add_argument("-c", "--check", action="store_true", help="Check if file is formatted without modifying")

    # errors
    errors_parser = subparsers.add_parser("errors", help="Display all error codes and remediation guides")
    errors_parser.add_argument("--format", choices=["text", "json"], default="text", help="Output format (default: text)")

    # doctor
    subparsers.add_parser("doctor", help="Run system and environment self-diagnostic check")

    # env
    subparsers.add_parser("env", help="Display active environment and resource resolution paths")

    # repl
    subparsers.add_parser("repl", help="Start interactive Vākya REPL")

    # test
    test_parser = subparsers.add_parser("test", help="Run automated test suite")
    test_parser.add_argument("path", nargs="?", default=None, help="Path to test directory")

    # version
    subparsers.add_parser("version", help="Display Vākya version")

    if not argv or argv == ["help"] or argv == ["--help"] or argv == ["-h"]:
        parser.print_help()
        return 0

    if argv == ["version"] or argv == ["--version"] or argv == ["-v"]:
        print(f"Vākya v{__version__} (Romanized Sanskrit Programming Language)")
        return 0

    args = parser.parse_args(argv)

    if args.command == "new":
        return create_new_project(args.name)
    elif args.command == "build":
        return build_file(args.file, output_path=args.output)
    elif args.command == "run":
        return execute_file(args.file, check_only=False, engine=args.engine, trace=args.trace, output_format=args.format)
    elif args.command == "disasm":
        return disassemble_file(args.file)
    elif args.command == "check":
        return execute_file(args.file, check_only=True, output_format=args.format)
    elif args.command == "fmt":
        return format_file(args.file, write_in_place=args.write, check_only=args.check)
    elif args.command == "errors":
        return dump_errors(output_format=args.format)
    elif args.command == "doctor":
        return run_doctor()
    elif args.command == "env":
        return dump_env()
    elif args.command == "repl":
        return REPL().run()
    elif args.command == "test":
        return run_tests(args.path)

    return 0


if __name__ == "__main__":
    sys.exit(main())
