"""Permanent regression test suite for Vākya bug fixes and edge cases."""

import io
import unittest
from vakya.lexer.lexer import Lexer
from vakya.parser.parser import Parser
from vakya.typechecker.checker import TypeChecker
from vakya.interpreter.interpreter import Interpreter
from vakya.formatter.formatter import Formatter
from vakya.errors import LexerError, TypeError, IndexError


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


class TestRegressions(unittest.TestCase):
    def test_bug_boolean_integer_equality(self):
        """Prevent Python boolean-int subclass equality leak (satya == 1 must be asatya)."""
        self.assertEqual(run_code("vada(satya == 1)"), "asatya")
        self.assertEqual(run_code("vada(asatya == 0)"), "asatya")
        self.assertEqual(run_code("vada(satya != 1)"), "satya")
        self.assertEqual(run_code("vada(asatya != 0)"), "satya")

    def test_bug_boolean_arithmetic_leak(self):
        """Prevent Python boolean numeric coercion in arithmetic."""
        with self.assertRaises(TypeError):
            run_code("chara x = satya + 1")
        with self.assertRaises(TypeError):
            run_code("chara x = asatya * 5")

    def test_bug_number_identifier_token(self):
        """Identifiers cannot directly begin with digits (e.g. 123abc)."""
        with self.assertRaises(LexerError) as ctx:
            lexer = Lexer("chara 123abc = 10")
            lexer.tokenize()
        self.assertEqual(ctx.exception.code, "E005")

    def test_bug_na_operator_precedence(self):
        """Logical NOT (na) must have lower precedence than == and + (na 1 + 2 == 3 is na ((1 + 2) == 3))."""
        self.assertEqual(run_code("vada(na 1 + 2 == 3)"), "asatya")
        self.assertEqual(run_code("vada(na 1 + 2 == 4)"), "satya")

    def test_bug_mutual_recursion_hoisting(self):
        """Top-level functions must be hoisted so mutual recursion works without forward declaration errors."""
        code = """
        karya is_even(n: sankhya) -> boolean {
            yadi n == 0 { pratyavartaya satya }
            pratyavartaya is_odd(n - 1)
        }
        karya is_odd(n: sankhya) -> boolean {
            yadi n == 0 { pratyavartaya asatya }
            pratyavartaya is_even(n - 1)
        }
        vada(is_even(6))
        vada(is_odd(6))
        """
        self.assertEqual(run_code(code), "satya\nasatya")

    def test_bug_trailing_comma_lists_maps(self):
        """Trailing commas in array literals and map literals must parse cleanly."""
        code = """
        chara l = [10, 20, 30,]
        chara m = {
            "a": 1,
            "b": 2,
        }
        vada(l.length)
        vada(m.length)
        """
        self.assertEqual(run_code(code), "3\n2")

    def test_bug_trailing_comma_params_calls(self):
        """Trailing commas in function parameters and call arguments must parse cleanly."""
        code = """
        karya add(
            a: sankhya,
            b: sankhya,
        ) -> sankhya {
            pratyavartaya a + b
        }
        vada(add(10, 20,))
        """
        self.assertEqual(run_code(code), "30")

    def test_bug_formatter_idempotency_multiline(self):
        """Formatter must produce deterministic, idempotent output."""
        source = """
karya test(a: sankhya, b: sankhya) -> sankhya {
    yadi a > b {
        pratyavartaya a
    } anyatha {
        pratyavartaya b
    }
}
"""
        fmt = Formatter()
        pass1 = fmt.format_source(source)
        pass2 = fmt.format_source(pass1)
        self.assertEqual(pass1, pass2)

    def test_bug_negative_index_rejection(self):
        """Negative indexes must be strictly rejected rather than wrapping around."""
        code = "chara l = [1, 2, 3]\nchara val = l[-1]"
        with self.assertRaises(IndexError) as ctx:
            run_code(code)
        self.assertEqual(ctx.exception.code, "E302")

    def test_bug_power_right_associativity(self):
        """Exponentiation (**) must be right-associative: 2 ** 3 ** 2 = 2 ** 9 = 512."""
        self.assertEqual(run_code("vada(2 ** 3 ** 2)"), "512")

    def test_bug_string_multiplication(self):
        """String repetition with sankhya must be typechecked and execute properly."""
        code = 'chara s = "ha" * 3\nvada(s)'
        self.assertEqual(run_code(code), "hahaha")


if __name__ == "__main__":
    unittest.main()
