"""Exhaustive closure environment capture and ownership tests for the Vākya Borrow Checker."""

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


class TestClosureOwnership(unittest.TestCase):
    def test_closure_captures_primitive_by_value(self):
        code = """
        chara factor = 3
        karya make_mul() {
            karya mul(x: sankhya) -> sankhya {
                pratyavartaya x * factor
            }
            pratyavartaya mul
        }
        chara fn = make_mul()
        vada(fn(10))
        """
        check(code)

    def test_closure_with_multiple_upvalues(self):
        code = """
        chara a = 10
        chara b = 20
        karya make_adder() {
            karya adder() -> sankhya {
                pratyavartaya a + b
            }
            pratyavartaya adder
        }
        chara add_fn = make_adder()
        vada(add_fn())
        """
        check(code)

    def test_independent_closure_instances(self):
        code = """
        karya create_counter() {
            chara count = 0
            karya inc() -> sankhya {
                count += 1
                pratyavartaya count
            }
            pratyavartaya inc
        }
        chara c1 = create_counter()
        chara c2 = create_counter()
        vada(c1())
        vada(c2())
        """
        check(code)

    def test_closure_returned_and_invoked_immediately(self):
        code = """
        karya get_multiplier(f: sankhya) {
            karya mult(x: sankhya) -> sankhya {
                pratyavartaya x * f
            }
            pratyavartaya mult
        }
        vada(get_multiplier(5)(10))
        """
        check(code)

    def test_closure_passed_to_another_function(self):
        code = """
        karya apply_fn(f: any, val: sankhya) -> sankhya {
            pratyavartaya f(val)
        }
        chara offset = 100
        karya add_offset(n: sankhya) -> sankhya {
            pratyavartaya n + offset
        }
        vada(apply_fn(add_offset, 25))
        """
        check(code)

    def test_deeply_nested_closure_chain(self):
        code = """
        karya f1(a: sankhya) {
            karya f2(b: sankhya) {
                karya f3(c: sankhya) -> sankhya {
                    pratyavartaya a + b + c
                }
                pratyavartaya f3
            }
            pratyavartaya f2
        }
        vada(f1(1)(2)(3))
        """
        check(code)

    def test_closure_mutating_outer_local(self):
        code = """
        chara accumulator = 0
        karya add_to_acc(val: sankhya) {
            accumulator += val
        }
        add_to_acc(10)
        add_to_acc(20)
        vada(accumulator)
        """
        check(code)

    def test_closure_inside_loop(self):
        code = """
        chara i = 0
        yavat i < 2 {
            karya greet() {
                vada("Hi")
            }
            greet()
            i += 1
        }
        """
        check(code)

    def test_closure_capturing_string_literal(self):
        code = """
        karya make_greeter(prefix: shabda) {
            karya greeter(name: shabda) -> shabda {
                pratyavartaya prefix + " " + name
            }
            pratyavartaya greeter
        }
        chara g = make_greeter("Namaste")
        vada(g("Arjuna"))
        """
        check(code)

    def test_closure_returning_boolean(self):
        code = """
        chara threshold = 50
        karya is_above_threshold(val: sankhya) -> boolean {
            pratyavartaya val > threshold
        }
        vada(is_above_threshold(75))
        """
        check(code)


if __name__ == "__main__":
    unittest.main()
