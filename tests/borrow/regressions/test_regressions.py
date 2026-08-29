"""Exhaustive regression and edge-case tests for the Vākya Borrow Checker."""

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


class TestBorrowRegressions(unittest.TestCase):
    def test_empty_program(self):
        check("")

    def test_only_comments(self):
        check("// Only a comment\n/* Multi-line */")

    def test_standalone_literal_expressions(self):
        check("42\n3.14\n\"hello\"\nsatya\nshunya")

    def test_complex_arithmetic_precedence(self):
        check("chara x = 2 + 3 * 4 ** 2 - 10 / 2\nvada(x)")

    def test_logical_short_circuit_with_borrowing(self):
        check("chara a = 10\nchara b = 20\nchara res = (a < b) va (a > b)\nvada(res)")

    def test_variable_reassigned_to_itself(self):
        check("chara a = 10\na = a\nvada(a)")

    def test_break_and_continue_inside_nested_loops(self):
        code = """
        chara i = 0
        yavat i < 5 {
            i += 1
            yadi i == 2 { agaccha }
            yadi i == 4 { virama }
            vada(i)
        }
        """
        check(code)

    def test_empty_block(self):
        check("{}")

    def test_multiple_empty_blocks(self):
        check("{}\n{}\n{}")

    def test_nested_empty_blocks(self):
        check("{{{}}}")


if __name__ == "__main__":
    unittest.main()
