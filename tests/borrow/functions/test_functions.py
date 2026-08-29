"""Exhaustive function ownership and parameter passing tests for the Vākya Borrow Checker."""

import unittest
from vakya.lexer.lexer import Lexer
from vakya.parser.parser import Parser
from vakya.typechecker.checker import TypeChecker
from vakya.typechecker.borrow_checker import BorrowChecker
from vakya.errors import BorrowError


def check(code: str):
    tokens = Lexer(code).tokenize()
    ast = Parser(tokens, source_code=code).parse()
    TypeChecker(source_code=code).check(ast)
    BorrowChecker(source_code=code).check(ast)


class TestFunctionOwnership(unittest.TestCase):
    def test_pass_primitive_to_function(self):
        code = """
        karya square(n: sankhya) -> sankhya {
            pratyavartaya n * n
        }
        chara x = 5
        vada(square(x))
        vada(x) // x remains valid
        """
        check(code)

    def test_pass_multiple_primitives_to_function(self):
        code = """
        karya add(a: sankhya, b: sankhya) -> sankhya {
            pratyavartaya a + b
        }
        chara x = 10
        chara y = 20
        vada(add(x, y))
        vada(x + y)
        """
        check(code)

    def test_function_internal_allocations(self):
        code = """
        karya make_vector() -> suchi {
            chara v = [1, 2, 3]
            pratyavartaya v
        }
        chara vec = make_vector()
        vada(vec[0])
        """
        check(code)

    def test_recursive_function_ownership(self):
        code = """
        karya factorial(n: sankhya) -> sankhya {
            yadi n <= 1 { pratyavartaya 1 }
            pratyavartaya n * factorial(n - 1)
        }
        vada(factorial(5))
        """
        check(code)

    def test_fibonacci_function_ownership(self):
        code = """
        karya fib(n: sankhya) -> sankhya {
            yadi n <= 1 { pratyavartaya n }
            pratyavartaya fib(n - 1) + fib(n - 2)
        }
        vada(fib(7))
        """
        check(code)

    def test_mutual_recursion_ownership(self):
        code = """
        karya is_even(n: sankhya) -> boolean {
            yadi n == 0 { pratyavartaya satya }
            pratyavartaya is_odd(n - 1)
        }
        karya is_odd(n: sankhya) -> boolean {
            yadi n == 0 { pratyavartaya asatya }
            pratyavartaya is_even(n - 1)
        }
        vada(is_even(10))
        """
        check(code)

    def test_function_modifying_local_copy(self):
        code = """
        karya modify_param(n: sankhya) {
            n += 100
        }
        chara val = 10
        modify_param(val)
        vada(val)
        """
        check(code)

    def test_function_with_multiple_return_branches(self):
        code = """
        karya classify(n: sankhya) -> shabda {
            yadi n > 0 { pratyavartaya "positive" }
            anyatha yadi n < 0 { pratyavartaya "negative" }
            anyatha { pratyavartaya "zero" }
        }
        vada(classify(5))
        """
        check(code)

    def test_function_returning_nested_expression(self):
        code = """
        karya compute(a: sankhya, b: sankhya) -> sankhya {
            pratyavartaya (a + b) * (a - b)
        }
        vada(compute(10, 5))
        """
        check(code)

    def test_function_with_local_loop(self):
        code = """
        karya sum_up_to(n: sankhya) -> sankhya {
            chara s = 0
            chara i = 1
            yavat i <= n {
                s += i
                i += 1
            }
            pratyavartaya s
        }
        vada(sum_up_to(10))
        """
        check(code)

    def test_function_returning_map(self):
        code = """
        karya build_point(x: sankhya, y: sankhya) -> naksha {
            pratyavartaya {"x": x, "y": y}
        }
        chara pt = build_point(10, 20)
        vada(pt["x"])
        """
        check(code)

    def test_nested_functions_independent_params(self):
        code = """
        karya outer_calc(x: sankhya) -> sankhya {
            karya inner_calc(y: sankhya) -> sankhya {
                pratyavartaya y * 2
            }
            pratyavartaya inner_calc(x) + 1
        }
        vada(outer_calc(5))
        """
        check(code)

    def test_function_calling_another_with_expressions(self):
        code = """
        karya add_one(x: sankhya) -> sankhya { pratyavartaya x + 1 }
        karya double(x: sankhya) -> sankhya { pratyavartaya x * 2 }
        vada(add_one(double(5)))
        """
        check(code)

    def test_function_void_return_implicit(self):
        code = """
        karya log_msg(msg: shabda) {
            vada(msg)
        }
        log_msg("Hello")
        """
        check(code)

    def test_pass_primitive_returned_from_function(self):
        code = """
        karya get_val() -> sankhya { pratyavartaya 42 }
        karya print_val(x: sankhya) { vada(x) }
        print_val(get_val())
        """
        check(code)


if __name__ == "__main__":
    unittest.main()
