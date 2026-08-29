"""Conformance tests for operators and expressions in Vākya."""

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


class TestConformanceExpressions(unittest.TestCase):
    def test_arithmetic_addition(self):
        self.assertEqual(run_code("vada(10 + 20)"), "30")

    def test_arithmetic_subtraction(self):
        self.assertEqual(run_code("vada(50 - 15)"), "35")

    def test_arithmetic_multiplication(self):
        self.assertEqual(run_code("vada(6 * 7)"), "42")

    def test_arithmetic_division_exact(self):
        self.assertEqual(run_code("vada(100 / 4)"), "25")

    def test_arithmetic_division_float(self):
        self.assertEqual(run_code("vada(7 / 2)"), "3.5")

    def test_arithmetic_modulo(self):
        self.assertEqual(run_code("vada(17 % 5)"), "2")

    def test_arithmetic_power(self):
        self.assertEqual(run_code("vada(2 ** 5)"), "32")

    def test_right_associative_power(self):
        # 2 ** 3 ** 2 is 2 ** (3 ** 2) = 2 ** 9 = 512
        self.assertEqual(run_code("vada(2 ** 3 ** 2)"), "512")

    def test_precedence_mult_over_add(self):
        # 1 + 2 * 3 = 7
        self.assertEqual(run_code("vada(1 + 2 * 3)"), "7")

    def test_precedence_power_over_mult(self):
        # 2 ** 3 * 4 = 8 * 4 = 32
        self.assertEqual(run_code("vada(2 ** 3 * 4)"), "32")

    def test_precedence_parentheses(self):
        # (1 + 2) * 3 = 9
        self.assertEqual(run_code("vada((1 + 2) * 3)"), "9")

    def test_relational_lt_gt(self):
        self.assertEqual(run_code("vada(5 < 10)"), "satya")
        self.assertEqual(run_code("vada(10 < 5)"), "asatya")
        self.assertEqual(run_code("vada(10 > 5)"), "satya")

    def test_relational_lte_gte(self):
        self.assertEqual(run_code("vada(5 <= 5)"), "satya")
        self.assertEqual(run_code("vada(6 <= 5)"), "asatya")
        self.assertEqual(run_code("vada(5 >= 5)"), "satya")

    def test_equality_numbers(self):
        self.assertEqual(run_code("vada(42 == 42)"), "satya")
        self.assertEqual(run_code("vada(42 != 42)"), "asatya")
        self.assertEqual(run_code("vada(42 != 100)"), "satya")

    def test_equality_booleans(self):
        self.assertEqual(run_code("vada(satya == satya)"), "satya")
        self.assertEqual(run_code("vada(asatya == asatya)"), "satya")
        self.assertEqual(run_code("vada(satya != asatya)"), "satya")

    def test_equality_boolean_vs_integer(self):
        # satya is not 1, asatya is not 0 in Vakya
        self.assertEqual(run_code("vada(satya == 1)"), "asatya")
        self.assertEqual(run_code("vada(asatya == 0)"), "asatya")
        self.assertEqual(run_code("vada(satya != 1)"), "satya")

    def test_equality_null(self):
        self.assertEqual(run_code("vada(shunya == shunya)"), "satya")
        self.assertEqual(run_code("vada(shunya != 0)"), "satya")

    def test_logical_and_evam(self):
        self.assertEqual(run_code("vada(satya evam satya)"), "satya")
        self.assertEqual(run_code("vada(satya evam asatya)"), "asatya")
        self.assertEqual(run_code("vada(asatya evam satya)"), "asatya")

    def test_logical_or_va(self):
        self.assertEqual(run_code("vada(satya va asatya)"), "satya")
        self.assertEqual(run_code("vada(asatya va asatya)"), "asatya")

    def test_logical_not_na(self):
        self.assertEqual(run_code("vada(na satya)"), "asatya")
        self.assertEqual(run_code("vada(na asatya)"), "satya")

    def test_logical_not_precedence(self):
        # na 1 + 2 == 3 parses as na ((1 + 2) == 3) -> na (3 == 3) -> na satya -> asatya
        self.assertEqual(run_code("vada(na 1 + 2 == 3)"), "asatya")

    def test_chained_comparisons_and_logicals(self):
        # a == b evam c == d
        code = "chara a = 5\nchara b = 5\nchara c = 10\nchara d = 10\nvada(a == b evam c == d)"
        self.assertEqual(run_code(code), "satya")

    def test_unary_minus_and_plus(self):
        self.assertEqual(run_code("vada(-42)"), "-42")
        self.assertEqual(run_code("vada(+42)"), "42")
        self.assertEqual(run_code("vada(-(-42))"), "42")


if __name__ == "__main__":
    unittest.main()
