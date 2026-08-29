"""Interactive Read-Eval-Print Loop (REPL) for Vākya."""

import sys
from typing import Optional, TextIO
from ..lexer.lexer import Lexer
from ..parser.parser import Parser
from ..typechecker.checker import TypeChecker
from ..interpreter.interpreter import Interpreter
from ..interpreter.values import vakya_str
from ..errors import VakyaError
from ..ast.nodes import ExpressionStatement, Program


def count_open_delimiters(code: str) -> int:
    """Count unbalanced open braces, brackets, and parentheses."""
    depth = 0
    in_string = False
    escape = False

    for ch in code:
        if escape:
            escape = False
            continue
        if ch == "\\":
            escape = True
            continue
        if ch == '"':
            in_string = not in_string
            continue
        if not in_string:
            if ch in "({[":
                depth += 1
            elif ch in ")}]":
                depth -= 1
    return depth


class REPL:
    """Vākya interactive shell."""

    def __init__(
        self,
        stdout: TextIO = sys.stdout,
        stdin: TextIO = sys.stdin,
        stderr: TextIO = sys.stderr,
    ):
        self.stdout = stdout
        self.stdin = stdin
        self.stderr = stderr
        self.interpreter = Interpreter(filename="<repl>", stdout=self.stdout, stdin=self.stdin)
        self.typechecker = TypeChecker(filename="<repl>")

    def start(self) -> None:
        """Run the REPL main loop."""
        self.stdout.write("Vākya REPL v0.1.0 — Romanized Sanskrit Programming Language\n")
        self.stdout.write("Type '.help' for commands, '.exit' or Ctrl+D / Ctrl+C to exit.\n\n")
        self.stdout.flush()

        buffer = []
        depth = 0

        while True:
            prompt = ">>> " if depth == 0 else "... "
            try:
                self.stdout.write(prompt)
                self.stdout.flush()
                line = self.stdin.readline()
                if not line:  # EOF
                    self.stdout.write("\nNamaste!\n")
                    break

                line_str = line.rstrip("\r\n")

                # Check top-level REPL commands when buffer is empty
                if depth == 0 and line_str.startswith("."):
                    cmd = line_str.strip()
                    if cmd in (".exit", ".quit"):
                        self.stdout.write("Namaste!\n")
                        break
                    elif cmd == ".help":
                        self._print_help()
                        continue
                    elif cmd == ".clear":
                        self.stdout.write("\033[H\033[2J")
                        self.stdout.flush()
                        continue
                    elif cmd == ".env":
                        self._print_env()
                        continue
                    else:
                        self.stdout.write(f"Unknown command: '{cmd}'. Type '.help' for commands.\n")
                        continue

                buffer.append(line_str)
                full_code = "\n".join(buffer)
                depth = max(0, count_open_delimiters(full_code))

                if depth > 0:
                    continue

                # Finished multi-line or single-line input
                code_to_eval = "\n".join(buffer).strip()
                buffer.clear()
                depth = 0

                if not code_to_eval:
                    continue

                self._eval_line(code_to_eval)

            except KeyboardInterrupt:
                buffer.clear()
                depth = 0
                self.stdout.write("\nKeyboardInterrupt\n")
            except EOFError:
                self.stdout.write("\nNamaste!\n")
                break

    def _eval_line(self, code: str) -> None:
        try:
            lexer = Lexer(code, filename="<repl>")
            tokens = lexer.tokenize()
            parser = Parser(tokens, source_code=code, filename="<repl>")
            ast = parser.parse()

            # Run typechecker on the statement
            self.typechecker.source_code = code
            self.typechecker.check(ast)

            # Update interpreter source_code for runtime diagnostics
            self.interpreter.source_code = code
            result = self.interpreter.interpret(ast)

            # If the last statement was an expression statement, display the result
            if ast.statements and isinstance(ast.statements[-1], ExpressionStatement):
                if result is not None:
                    self.stdout.write(f"{vakya_str(result)}\n")
                    self.stdout.flush()

        except VakyaError as err:
            self.stderr.write(f"{err.format_diagnostic(code)}\n")
            self.stderr.flush()
        except Exception as ex:
            self.stderr.write(f"Internal Error: {ex}\n")
            self.stderr.flush()

    def _print_help(self) -> None:
        help_text = """
Vākya REPL Commands:
  .help          Show this help message
  .env           List active variables and functions in scope
  .clear         Clear the terminal screen
  .exit          Exit the REPL session

Vākya Quick Syntax:
  chara x = 10                  Variable declaration
  dhruva pi = 3.14              Constant declaration
  karya add(a, b) { ... }       Function definition
  yadi x >= 10 { ... }          If / else condition
  yavat x < 5 { ... }           While loop
  pratyekam i madhye [1,2,3]    For-each loop
  vada("Namaste")               Print output
"""
        self.stdout.write(help_text + "\n")
        self.stdout.flush()

    def _print_env(self) -> None:
        self.stdout.write("Active Variables in Scope:\n")
        for k, v in self.interpreter.current_env.values.items():
            if not k.startswith("__"):
                self.stdout.write(f"  {k} = {vakya_str(v)}\n")
        self.stdout.flush()
