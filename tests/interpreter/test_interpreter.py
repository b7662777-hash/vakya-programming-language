"""Tests for Vākya Tree-Walking Interpreter."""

import io
import unittest
from vakya.lexer.lexer import Lexer
from vakya.parser.parser import Parser
from vakya.typechecker.checker import TypeChecker
from vakya.interpreter.interpreter import Interpreter
from vakya.errors import RuntimeError, IndexError


def run_vakya(code: str) -> str:
    """Helper to run code and capture stdout output."""
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens, source_code=code)
    ast = parser.parse()
    checker = TypeChecker(source_code=code)
    checker.check(ast)

    out_stream = io.StringIO()
    interpreter = Interpreter(source_code=code, stdout=out_stream)
    interpreter.interpret(ast)
    return out_stream.getvalue()


class TestInterpreter(unittest.TestCase):
    def test_milestone_1_basic_math_and_print(self):
        code = """
        chara x = 10
        chara y = 20
        vada(x + y)
        """
        output = run_vakya(code)
        self.assertEqual(output.strip(), "30")

    def test_milestone_2_function_and_call(self):
        code = """
        karya yog(a, b) {
            pratyavartaya a + b
        }
        vada(yog(10, 20))
        """
        output = run_vakya(code)
        self.assertEqual(output.strip(), "30")

    def test_recursion_factorial(self):
        code = """
        karya factorial(n) {
            yadi n <= 1 {
                pratyavartaya 1
            }
            pratyavartaya n * factorial(n - 1)
        }
        vada(factorial(5))
        """
        output = run_vakya(code)
        self.assertEqual(output.strip(), "120")

    def test_if_else_logic(self):
        code = """
        chara score = 85
        yadi score >= 90 {
            vada("A")
        } anyatha yadi score >= 80 {
            vada("B")
        } anyatha {
            vada("C")
        }
        """
        output = run_vakya(code)
        self.assertEqual(output.strip(), "B")

    def test_loops_while_and_break(self):
        code = """
        chara x = 0
        yavat satya {
            x += 1
            yadi x == 3 {
                virama
            }
        }
        vada(x)
        """
        output = run_vakya(code)
        self.assertEqual(output.strip(), "3")

    def test_loops_for_each(self):
        code = """
        chara names = ["Goku", "Vegeta"]
        pratyekam n madhye names {
            vada(n)
        }
        """
        output = run_vakya(code)
        self.assertEqual(output.strip(), "Goku\nVegeta")

    def test_arrays_and_maps(self):
        code = """
        chara lst = [10, 20]
        lst[0] = 100
        suchi_jodo(lst, 30)
        vada(lst)
        vada(lst.length)

        chara map = {"name": "Goku"}
        map["age"] = 16
        vada(map["name"])
        vada(map["age"])
        """
        output = run_vakya(code)
        lines = [line.strip() for line in output.strip().splitlines()]
        self.assertEqual(lines[0], "[100, 20, 30]")
        self.assertEqual(lines[1], "3")
        self.assertEqual(lines[2], "Goku")
        self.assertEqual(lines[3], "16")

    def test_string_builtins(self):
        code = """
        chara text = "  Namaste World  "
        vada(shabda_bada(shabda_trim(text)))
        vada(shabda_chhota("HELLO"))
        vada(lamba("Goku"))
        vada(prakaar(42))
        """
        output = run_vakya(code)
        lines = [line.strip() for line in output.strip().splitlines()]
        self.assertEqual(lines[0], "NAMASTE WORLD")
        self.assertEqual(lines[1], "hello")
        self.assertEqual(lines[2], "4")
        self.assertEqual(lines[3], "sankhya")

    def test_closures(self):
        code = """
        karya make_adder(x) {
            karya adder(y) {
                pratyavartaya x + y
            }
            pratyavartaya adder
        }
        chara add10 = make_adder(10)
        vada(add10(5))
        """
        output = run_vakya(code)
        self.assertEqual(output.strip(), "15")

    def test_error_division_by_zero(self):
        code = "chara x = 10 / 0"
        with self.assertRaises(RuntimeError) as ctx:
            run_vakya(code)
        self.assertEqual(ctx.exception.code, "E301")

    def test_error_index_out_of_bounds(self):
        code = """
        chara list = [1, 2]
        chara val = list[5]
        """
        with self.assertRaises(IndexError) as ctx:
            run_vakya(code)
        self.assertEqual(ctx.exception.code, "E302")

    def test_error_map_key_not_found(self):
        code = """
        chara map = {"a": 1}
        chara val = map["b"]
        """
        with self.assertRaises(RuntimeError) as ctx:
            run_vakya(code)
        self.assertEqual(ctx.exception.code, "E303")

    def test_error_recursion_limit(self):
        code = """
        karya infinite_loop() {
            pratyavartaya infinite_loop()
        }
        infinite_loop()
        """
        with self.assertRaises(RuntimeError) as ctx:
            run_vakya(code)
        self.assertEqual(ctx.exception.code, "E304")


if __name__ == "__main__":
    unittest.main()
