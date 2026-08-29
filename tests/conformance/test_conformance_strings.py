"""Conformance tests for strings in Vākya."""

import io
import unittest
from vakya.lexer.lexer import Lexer
from vakya.parser.parser import Parser
from vakya.typechecker.checker import TypeChecker
from vakya.interpreter.interpreter import Interpreter


def run_code(code: str) -> str:
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens, source_code=code)
    ast = parser.parse()
    checker = TypeChecker(source_code=code)
    checker.check(ast)
    out = io.StringIO()
    interpreter = Interpreter(source_code=code, stdout=out)
    interpreter.interpret(ast)
    return out.getvalue().strip()


class TestConformanceStrings(unittest.TestCase):
    def test_empty_string(self):
        code = 'chara s = ""\nvada(s)\nvada(s.length)'
        self.assertEqual(run_code(code), "0")

    def test_string_escapes_newline(self):
        code = 'chara s = "Hello\\nWorld"\nvada(s)'
        self.assertEqual(run_code(code), "Hello\nWorld")

    def test_string_escapes_tab(self):
        code = 'chara s = "A\\tB"\nvada(s)'
        self.assertEqual(run_code(code), "A\tB")

    def test_string_escapes_backslash(self):
        code = 'chara s = "A\\\\B"\nvada(s)'
        self.assertEqual(run_code(code), "A\\B")

    def test_string_escapes_quotes(self):
        code = 'chara s = "He said \\"Namaste\\""\nvada(s)'
        self.assertEqual(run_code(code), 'He said "Namaste"')

    def test_string_concatenation_both_strings(self):
        code = 'chara a = "Hello "\nchara b = "World"\nvada(a + b)'
        self.assertEqual(run_code(code), "Hello World")

    def test_string_concatenation_with_number(self):
        code = 'chara s = "Score: " + 99\nvada(s)'
        self.assertEqual(run_code(code), "Score: 99")

    def test_string_concatenation_number_first(self):
        code = 'chara s = 100 + " points"\nvada(s)'
        self.assertEqual(run_code(code), "100 points")

    def test_string_concatenation_with_boolean(self):
        code = 'chara s = "Active: " + satya\nvada(s)'
        self.assertEqual(run_code(code), "Active: satya")

    def test_string_indexing(self):
        code = 'chara name = "Goku"\nvada(name[0])\nvada(name[3])'
        self.assertEqual(run_code(code), "G\nu")

    def test_string_length(self):
        code = 'chara s = "Namaste"\nvada(s.length)\nvada(lamba(s))'
        self.assertEqual(run_code(code), "7\n7")

    def test_string_builtins_case_and_trim(self):
        code = """
        chara s = "  hello world  "
        vada(shabda_bada(s))
        vada(shabda_chhota("GOKU"))
        vada(shabda_trim(s))
        """
        lines = [l.strip() for l in run_code(code).splitlines()]
        self.assertEqual(lines[0], "HELLO WORLD")
        self.assertEqual(lines[1], "goku")
        self.assertEqual(lines[2], "hello world")

    def test_string_repetition(self):
        code = 'chara s = "ab" * 3\nvada(s)'
        self.assertEqual(run_code(code), "ababab")

    def test_string_repetition_reversed(self):
        code = 'chara s = 3 * "xy"\nvada(s)'
        self.assertEqual(run_code(code), "xyxyxy")


if __name__ == "__main__":
    unittest.main()
