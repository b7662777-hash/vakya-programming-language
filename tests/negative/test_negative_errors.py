"""Negative tests ensuring all invalid Vākya programs fail cleanly with structured error diagnostics."""

import unittest
from vakya.lexer.lexer import Lexer
from vakya.parser.parser import Parser
from vakya.typechecker.checker import TypeChecker
from vakya.interpreter.interpreter import Interpreter
from vakya.errors import (
    VakyaError,
    LexerError,
    ParseError,
    TypeError,
    RuntimeError,
    NameError,
    ArgumentError,
    IndexError,
    ConstantError,
)


def run_code(code: str):
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens, source_code=code)
    ast = parser.parse()
    checker = TypeChecker(source_code=code)
    checker.check(ast)
    interpreter = Interpreter(source_code=code)
    return interpreter.interpret(ast)


class TestNegativeErrors(unittest.TestCase):
    def test_e101_undefined_variable(self):
        with self.assertRaises(NameError) as ctx:
            run_code("vada(missing_var)")
        self.assertEqual(ctx.exception.code, "E101")

    def test_e102_undefined_function(self):
        with self.assertRaises(NameError) as ctx:
            run_code("unknown_fn()")
        self.assertEqual(ctx.exception.code, "E102")

    def test_e103_constant_reassignment(self):
        code = "dhruva pi = 3.14\npi = 3.14159"
        with self.assertRaises(ConstantError) as ctx:
            run_code(code)
        self.assertEqual(ctx.exception.code, "E103")

    def test_e105_invalid_assignment_target(self):
        code = "10 = 20"
        with self.assertRaises(ParseError) as ctx:
            run_code(code)
        self.assertEqual(ctx.exception.code, "E105")

    def test_e202_missing_closing_brace(self):
        code = "yadi satya { vada(1)"
        with self.assertRaises(ParseError) as ctx:
            run_code(code)
        self.assertEqual(ctx.exception.code, "E202")

    def test_e202_missing_closing_paren(self):
        code = "vada(10 + 20"
        with self.assertRaises(ParseError) as ctx:
            run_code(code)
        self.assertEqual(ctx.exception.code, "E202")

    def test_e202_missing_colon_in_map(self):
        code = 'chara m = {"key" 10}'
        with self.assertRaises(ParseError) as ctx:
            run_code(code)
        self.assertEqual(ctx.exception.code, "E202")

    def test_e203_expected_expression(self):
        code = "chara x = +"
        with self.assertRaises(ParseError) as ctx:
            run_code(code)
        self.assertEqual(ctx.exception.code, "E203")

    def test_e205_invalid_for_each_syntax(self):
        code = "pratyekam item in items {}"
        with self.assertRaises(ParseError) as ctx:
            run_code(code)
        self.assertEqual(ctx.exception.code, "E205")

    def test_e206_break_outside_loop(self):
        code = "virama"
        with self.assertRaises(ParseError) as ctx:
            run_code(code)
        self.assertEqual(ctx.exception.code, "E206")

    def test_e206_continue_outside_loop(self):
        code = "agaccha"
        with self.assertRaises(ParseError) as ctx:
            run_code(code)
        self.assertEqual(ctx.exception.code, "E206")

    def test_e207_return_outside_function(self):
        code = "pratyavartaya 42"
        with self.assertRaises(ParseError) as ctx:
            run_code(code)
        self.assertEqual(ctx.exception.code, "E207")

    def test_e301_division_by_zero(self):
        code = "chara x = 10 / 0"
        with self.assertRaises(RuntimeError) as ctx:
            run_code(code)
        self.assertEqual(ctx.exception.code, "E301")

    def test_e301_modulo_by_zero(self):
        code = "chara x = 10 % 0"
        with self.assertRaises(RuntimeError) as ctx:
            run_code(code)
        self.assertEqual(ctx.exception.code, "E301")

    def test_e302_list_index_out_of_bounds_positive(self):
        code = "chara l = [1, 2]\nchara val = l[5]"
        with self.assertRaises(IndexError) as ctx:
            run_code(code)
        self.assertEqual(ctx.exception.code, "E302")

    def test_e302_list_index_out_of_bounds_negative(self):
        code = "chara l = [1, 2]\nchara val = l[-1]"
        with self.assertRaises(IndexError) as ctx:
            run_code(code)
        self.assertEqual(ctx.exception.code, "E302")

    def test_e302_string_index_out_of_bounds(self):
        code = 'chara s = "hi"\nchara ch = s[10]'
        with self.assertRaises(IndexError) as ctx:
            run_code(code)
        self.assertEqual(ctx.exception.code, "E302")

    def test_e303_map_key_not_found(self):
        code = 'chara m = {"a": 1}\nchara val = m["nonexistent"]'
        with self.assertRaises(RuntimeError) as ctx:
            run_code(code)
        self.assertEqual(ctx.exception.code, "E303")

    def test_e304_recursion_limit(self):
        code = """
        karya inf() {
            pratyavartaya inf()
        }
        inf()
        """
        with self.assertRaises(RuntimeError) as ctx:
            run_code(code)
        self.assertEqual(ctx.exception.code, "E304")

    def test_e305_calling_non_function(self):
        code = "chara x = 42\nx()"
        with self.assertRaises(RuntimeError) as ctx:
            run_code(code)
        self.assertEqual(ctx.exception.code, "E305")

    def test_e307_invalid_property(self):
        code = "chara x = 42\nchara p = x.length"
        with self.assertRaises(RuntimeError) as ctx:
            run_code(code)
        self.assertEqual(ctx.exception.code, "E307")

    def test_e401_type_mismatch_assignment(self):
        code = 'chara x: sankhya = 10\nx = "string"'
        with self.assertRaises(TypeError) as ctx:
            run_code(code)
        self.assertEqual(ctx.exception.code, "E401")

    def test_e402_argument_type_mismatch(self):
        code = """
        karya add(a: sankhya, b: sankhya) -> sankhya { pratyavartaya a + b }
        add(10, "string")
        """
        with self.assertRaises(TypeError) as ctx:
            run_code(code)
        self.assertEqual(ctx.exception.code, "E402")

    def test_e403_return_type_mismatch(self):
        code = """
        karya get_num() -> sankhya {
            pratyavartaya "not a number"
        }
        """
        with self.assertRaises(TypeError) as ctx:
            run_code(code)
        self.assertEqual(ctx.exception.code, "E403")

    def test_e404_operator_type_mismatch_bool_arithmetic(self):
        code = "chara x = satya + 5"
        with self.assertRaises(TypeError) as ctx:
            run_code(code)
        self.assertEqual(ctx.exception.code, "E404")

    def test_e405_unary_type_mismatch(self):
        code = 'chara x = -"string"'
        with self.assertRaises(TypeError) as ctx:
            run_code(code)
        self.assertEqual(ctx.exception.code, "E405")

    def test_e406_argument_count_mismatch_too_few(self):
        code = """
        karya add(a: sankhya, b: sankhya) -> sankhya { pratyavartaya a + b }
        add(10)
        """
        with self.assertRaises(ArgumentError) as ctx:
            run_code(code)
        self.assertEqual(ctx.exception.code, "E406")

    def test_e406_argument_count_mismatch_too_many(self):
        code = """
        karya add(a: sankhya, b: sankhya) -> sankhya { pratyavartaya a + b }
        add(10, 20, 30)
        """
        with self.assertRaises(ArgumentError) as ctx:
            run_code(code)
        self.assertEqual(ctx.exception.code, "E406")

    def test_e407_type_not_indexable(self):
        code = "chara x = 42\nchara val = x[0]"
        with self.assertRaises(TypeError) as ctx:
            run_code(code)
        self.assertEqual(ctx.exception.code, "E407")


if __name__ == "__main__":
    unittest.main()
