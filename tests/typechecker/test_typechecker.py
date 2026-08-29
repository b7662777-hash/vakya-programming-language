"""Tests for Vākya Type Checker."""

import unittest
from vakya.lexer.lexer import Lexer
from vakya.parser.parser import Parser
from vakya.typechecker.checker import TypeChecker
from vakya.errors import TypeError, NameError, ConstantError, ArgumentError


def check_code(code: str):
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens, source_code=code)
    ast = parser.parse()
    checker = TypeChecker(source_code=code)
    checker.check(ast)
    return checker


class TestTypeChecker(unittest.TestCase):
    def test_valid_declarations_and_inference(self):
        code = """
        chara a: sankhya = 10
        chara b: dashamika = 3.14
        chara c: shabda = "Goku"
        chara d: boolean = satya
        chara e = 42
        chara f = "inference"
        """
        # Should not raise any error
        check_code(code)

    def test_error_type_mismatch_declaration(self):
        code = 'chara x: sankhya = "hello"'
        with self.assertRaises(TypeError) as ctx:
            check_code(code)
        self.assertEqual(ctx.exception.code, "E401")

    def test_error_type_mismatch_assignment(self):
        code = """
        chara x: sankhya = 10
        x = "hello"
        """
        with self.assertRaises(TypeError) as ctx:
            check_code(code)
        self.assertEqual(ctx.exception.code, "E401")

    def test_error_constant_reassignment(self):
        code = """
        dhruva pi = 3.14
        pi = 3.14159
        """
        with self.assertRaises(ConstantError) as ctx:
            check_code(code)
        self.assertEqual(ctx.exception.code, "E103")

    def test_error_undefined_variable(self):
        code = "vada(unknown_var)"
        with self.assertRaises(NameError) as ctx:
            check_code(code)
        self.assertEqual(ctx.exception.code, "E101")

    def test_error_function_argument_type_mismatch(self):
        code = """
        karya add(a: sankhya, b: sankhya) -> sankhya {
            pratyavartaya a + b
        }
        add(10, "not_a_number")
        """
        with self.assertRaises(TypeError) as ctx:
            check_code(code)
        self.assertEqual(ctx.exception.code, "E402")

    def test_error_function_return_type_mismatch(self):
        code = """
        karya get_number() -> sankhya {
            pratyavartaya "not_a_number"
        }
        """
        with self.assertRaises(TypeError) as ctx:
            check_code(code)
        self.assertEqual(ctx.exception.code, "E403")

    def test_error_argument_count_mismatch(self):
        code = """
        karya add(a: sankhya, b: sankhya) -> sankhya {
            pratyavartaya a + b
        }
        add(10)
        """
        with self.assertRaises(ArgumentError) as ctx:
            check_code(code)
        self.assertEqual(ctx.exception.code, "E406")


if __name__ == "__main__":
    unittest.main()
