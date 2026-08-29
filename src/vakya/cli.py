"""Vākya Command-Line Interface (CLI)."""

import argparse
import os
import sys
import unittest
from typing import List, Optional
from . import __version__
from .lexer.lexer import Lexer
from .parser.parser import Parser
from .typechecker.checker import TypeChecker
from .interpreter.interpreter import Interpreter
from .formatter.formatter import Formatter
from .repl.repl import REPL
from .errors import VakyaError


def execute_file(file_path: str, check_only: bool = False) -> int:
    """Read, parse, typecheck, and optionally interpret a .vakya file."""
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
            print(f"Check passed: No syntax or type errors found in '{file_path}'.")
            return 0

        # Interpreter
        interpreter = Interpreter(source_code=source_code, filename=filename)
        interpreter.interpret(ast)
        return 0

    except VakyaError as err:
        sys.stderr.write(f"\n{err.format_diagnostic(source_code)}\n\n")
        return 1
    except Exception as ex:
        sys.stderr.write(f"Internal compiler error: {ex}\n")
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


def main(argv: Optional[List[str]] = None) -> int:
    """CLI entry point."""
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

    parser = argparse.ArgumentParser(
        prog="vakya",
        description="Vākya — Romanized Sanskrit Programming Language CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  vakya run examples/hello.vakya         Execute a Vākya program
  vakya check examples/factorial.vakya   Typecheck without executing
  vakya fmt examples/hello.vakya --write Format a source file
  vakya repl                             Start interactive REPL
  vakya test                             Run test suite
  vakya version                          Show version information
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # run
    run_parser = subparsers.add_parser("run", help="Execute a .vakya source file")
    run_parser.add_argument("file", help="Path to .vakya file")

    # check
    check_parser = subparsers.add_parser("check", help="Typecheck a .vakya file without running")
    check_parser.add_argument("file", help="Path to .vakya file")

    # fmt
    fmt_parser = subparsers.add_parser("fmt", help="Format a .vakya source file")
    fmt_parser.add_argument("file", help="Path to .vakya file")
    fmt_parser.add_argument("-w", "--write", action="store_true", help="Write formatted output directly to file")
    fmt_parser.add_argument("-c", "--check", action="store_true", help="Check if file is formatted without modifying")

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

    if args.command == "run":
        return execute_file(args.file, check_only=False)
    elif args.command == "check":
        return execute_file(args.file, check_only=True)
    elif args.command == "fmt":
        return format_file(args.file, write_in_place=args.write, check_only=args.check)
    elif args.command == "repl":
        repl = REPL()
        repl.start()
        return 0
    elif args.command == "test":
        return run_tests(args.path)
    elif args.command == "version":
        print(f"Vākya v{__version__} (Romanized Sanskrit Programming Language)")
        return 0
    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    sys.exit(main())
