"""Conformance tests for functions, recursion, returns, and closures in Vākya."""

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


class TestConformanceFunctions(unittest.TestCase):
    def test_function_no_params_no_return(self):
        code = """
        karya say_hello() {
            vada("Hello")
        }
        say_hello()
        """
        self.assertEqual(run_code(code), "Hello")

    def test_function_with_params(self):
        code = """
        karya greet(name) {
            vada("Namaste " + name)
        }
        greet("Goku")
        """
        self.assertEqual(run_code(code), "Namaste Goku")

    def test_function_with_return_value(self):
        code = """
        karya add(a, b) {
            pratyavartaya a + b
        }
        vada(add(10, 20))
        """
        self.assertEqual(run_code(code), "30")

    def test_function_type_annotated_signature(self):
        code = """
        karya multiply(a: sankhya, b: sankhya) -> sankhya {
            pratyavartaya a * b
        }
        vada(multiply(6, 7))
        """
        self.assertEqual(run_code(code), "42")

    def test_function_default_return_shunya(self):
        code = """
        karya noop() {}
        chara res = noop()
        vada(res)
        """
        self.assertEqual(run_code(code), "shunya")

    def test_function_early_return(self):
        code = """
        karya check_positive(x) {
            yadi x > 0 {
                pratyavartaya "positive"
            }
            pratyavartaya "non-positive"
        }
        vada(check_positive(5))
        vada(check_positive(-5))
        """
        self.assertEqual(run_code(code), "positive\nnon-positive")

    def test_return_without_expression(self):
        code = """
        karya stop_early(x) {
            yadi x == 0 {
                pratyavartaya
            }
            vada("Valid:", x)
        }
        stop_early(0)
        stop_early(10)
        """
        self.assertEqual(run_code(code), "Valid: 10")

    def test_recursive_factorial(self):
        code = """
        karya fact(n: sankhya) -> sankhya {
            yadi n <= 1 {
                pratyavartaya 1
            }
            pratyavartaya n * fact(n - 1)
        }
        vada(fact(6))
        """
        self.assertEqual(run_code(code), "720")

    def test_recursive_fibonacci(self):
        code = """
        karya fib(n: sankhya) -> sankhya {
            yadi n <= 0 { pratyavartaya 0 }
            yadi n == 1 { pratyavartaya 1 }
            pratyavartaya fib(n - 1) + fib(n - 2)
        }
        vada(fib(8))
        """
        self.assertEqual(run_code(code), "21")

    def test_mutual_recursion_hoisting(self):
        code = """
        karya is_even(n: sankhya) -> boolean {
            yadi n == 0 {
                pratyavartaya satya
            }
            pratyavartaya is_odd(n - 1)
        }

        karya is_odd(n: sankhya) -> boolean {
            yadi n == 0 {
                pratyavartaya asatya
            }
            pratyavartaya is_even(n - 1)
        }

        vada(is_even(4))
        vada(is_odd(4))
        vada(is_even(5))
        vada(is_odd(5))
        """
        self.assertEqual(run_code(code), "satya\nasatya\nasatya\nsatya")

    def test_higher_order_functions(self):
        code = """
        karya apply_op(fn, x: sankhya, y: sankhya) -> sankhya {
            pratyavartaya fn(x, y)
        }

        karya add(a: sankhya, b: sankhya) -> sankhya {
            pratyavartaya a + b
        }

        karya sub(a: sankhya, b: sankhya) -> sankhya {
            pratyavartaya a - b
        }

        vada(apply_op(add, 20, 10))
        vada(apply_op(sub, 20, 10))
        """
        self.assertEqual(run_code(code), "30\n10")

    def test_lexical_closure_counter(self):
        code = """
        karya make_counter() {
            chara count = 0
            karya increment() -> sankhya {
                count += 1
                pratyavartaya count
            }
            pratyavartaya increment
        }

        chara c1 = make_counter()
        chara c2 = make_counter()

        vada(c1())
        vada(c1())
        vada(c2())
        vada(c1())
        """
        self.assertEqual(run_code(code), "1\n2\n1\n3")


if __name__ == "__main__":
    unittest.main()
