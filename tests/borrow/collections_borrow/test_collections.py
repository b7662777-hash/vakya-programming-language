"""Exhaustive collections ownership and indexing tests for the Vākya Borrow Checker."""

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


class TestCollectionsOwnership(unittest.TestCase):
    def test_list_of_primitives_element_access(self):
        check("chara nums = [10, 20, 30]\nvada(nums[0] + nums[1] + nums[2])")

    def test_list_mutation_and_element_access(self):
        check("chara nums = [1, 2, 3]\nnums[0] = 99\nvada(nums[0])")

    def test_list_assigned_moves_ownership_e501(self):
        with self.assertRaises(BorrowError) as ctx:
            check("chara a = [1, 2]\nchara b = a\nchara x = a[0]")
        self.assertEqual(ctx.exception.code, "E501")

    def test_map_assigned_moves_ownership_e501(self):
        with self.assertRaises(BorrowError) as ctx:
            check('chara a = {"x": 1}\nchara b = a\nchara x = a["x"]')
        self.assertEqual(ctx.exception.code, "E501")

    def test_nested_list_indexing(self):
        check("chara matrix = [[1, 2], [3, 4]]\nvada(matrix[0][0])")

    def test_list_passed_to_builtin(self):
        check("chara lst = [10, 20]\nsuchi_jodo(lst, 30)\nvada(lst[0])")

    def test_for_each_iteration_over_list(self):
        code = """
        chara items = [10, 20, 30]
        pratyekam it madhye items {
            vada(it)
        }
        vada(items[0])
        """
        check(code)

    def test_map_iteration_and_read(self):
        code = """
        chara user = {"name": "Goku", "age": 16}
        vada(user["name"])
        vada(user["age"])
        """
        check(code)

    def test_list_length_property(self):
        check("chara items = [1, 2, 3, 4]\nvada(items.length)")

    def test_map_length_property(self):
        check('chara m = {"a": 1, "b": 2}\nvada(m.length)')


if __name__ == "__main__":
    unittest.main()
