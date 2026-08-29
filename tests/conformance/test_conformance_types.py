"""Conformance tests for type system and prakaar builtin in Vākya."""

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


class TestConformanceTypes(unittest.TestCase):
    def test_prakaar_builtin_all_types(self):
        code = """
        karya dummy() {}
        vada(prakaar(42))
        vada(prakaar(3.14))
        vada(prakaar("text"))
        vada(prakaar(satya))
        vada(prakaar([1, 2]))
        vada(prakaar({"a": 1}))
        vada(prakaar(shunya))
        vada(prakaar(dummy))
        """
        expected = "\n".join([
            "sankhya",
            "dashamika",
            "shabda",
            "boolean",
            "suchi",
            "naksha",
            "shunya",
            "karya",
        ])
        self.assertEqual(run_code(code), expected)

    def test_type_promotion_int_to_float(self):
        code = """
        chara x: dashamika = 10
        vada(x)
        """
        # sankhya assigned to dashamika variable
        self.assertEqual(run_code(code), "10.0")

    def test_arithmetic_type_promotion(self):
        code = """
        chara a = 10
        chara b = 2.5
        chara c = a + b
        vada(c)
        vada(prakaar(c))
        """
        self.assertEqual(run_code(code), "12.5\ndashamika")


if __name__ == "__main__":
    unittest.main()
