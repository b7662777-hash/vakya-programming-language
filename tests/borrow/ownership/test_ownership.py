"""Exhaustive ownership tests for the Vākya Borrow Checker."""

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


class TestOwnershipBasics(unittest.TestCase):
    def test_primitive_integer_copy(self):
        check("chara a = 10\nchara b = a\nvada(a + b)")

    def test_primitive_float_copy(self):
        check("chara a = 3.14\nchara b = a\nvada(a * b)")

    def test_primitive_bool_copy(self):
        check("chara a = satya\nchara b = a\nchara c = a evam b")

    def test_primitive_null_copy(self):
        check("chara a = shunya\nchara b = a")

    def test_list_ownership_transfer(self):
        with self.assertRaises(BorrowError):
            check("chara a = [1, 2]\nchara b = a\nvada(a)")

    def test_map_ownership_transfer(self):
        with self.assertRaises(BorrowError):
            check('chara a = {"x": 1}\nchara b = a\nvada(a["x"])')

    def test_string_ownership_transfer(self):
        with self.assertRaises(BorrowError):
            check('chara a = "hello"\nchara b = a\nvada(a)')

    def test_nested_block_variable_scope(self):
        check("chara a = 10\n{\nchara b = a\nvada(b)\n}\nvada(a)")

    def test_variable_reassignment_resets_moved_state(self):
        check("chara a = [1, 2]\nchara b = a\na = [3, 4]\nvada(a[0])")

    def test_multiple_consecutive_reassignments(self):
        check("chara a = [1]\na = [2]\na = [3]\nvada(a[0])")

    def test_constant_ownership(self):
        check("dhruva a = 100\nchara b = a\nvada(a + b)")

    def test_independent_bindings_in_same_scope(self):
        check("chara a = [1, 2]\nchara b = [3, 4]\nchara c = b\nvada(a[0])")

    def test_multiple_shadowed_scopes(self):
        check("chara x = [1]\n{\nchara x = [2]\nvada(x[0])\n}\nvada(x[0])")

    def test_arithmetic_does_not_move_primitives(self):
        check("chara a = 5\nchara b = 10\nchara c = a + b + a * b\nvada(a)\nvada(b)")

    def test_list_literal_in_expression_statement(self):
        check("[1, 2, 3]\nchara x = 10\nvada(x)")


if __name__ == "__main__":
    unittest.main()
