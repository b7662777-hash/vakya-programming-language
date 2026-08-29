"""Exhaustive mutable borrow and mutation tests for the Vākya Borrow Checker."""

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


class TestMutableBorrow(unittest.TestCase):
    def test_mutate_unborrowed_list_element(self):
        code = """
        chara nums = [1, 2, 3]
        nums[0] = 100
        vada(nums[0])
        """
        check(code)

    def test_mutate_unborrowed_map_entry(self):
        code = """
        chara m = {"k": 1}
        m["k"] = 99
        vada(m["k"])
        """
        check(code)

    def test_mutate_list_in_loop(self):
        code = """
        chara nums = [0, 0, 0]
        chara i = 0
        yavat i < 3 {
            nums[i] = i * 10
            i += 1
        }
        """
        check(code)

    def test_mutate_map_in_loop(self):
        code = """
        chara m = {"a": 0}
        chara i = 0
        yavat i < 3 {
            m["a"] = i
            i += 1
        }
        """
        check(code)

    def test_mutate_list_in_function(self):
        code = """
        karya update(lst: suchi) {
            lst[0] = 42
        }
        chara data = [1, 2]
        update(data)
        """
        check(code)

    def test_mutate_after_reassignment(self):
        code = """
        chara nums = [1, 2]
        chara b = nums
        nums = [10, 20]
        nums[0] = 99
        vada(nums[0])
        """
        check(code)

    def test_mutate_inside_nested_scope(self):
        code = """
        chara nums = [1, 2]
        {
            nums[0] = 5
        }
        vada(nums[0])
        """
        check(code)

    def test_mutate_in_if_branch(self):
        code = """
        chara nums = [1, 2]
        yadi 10 > 5 {
            nums[0] = 100
        }
        vada(nums[0])
        """
        check(code)

    def test_mutate_in_else_branch(self):
        code = """
        chara nums = [1, 2]
        yadi 10 < 5 {
            nums[0] = 0
        } anyatha {
            nums[0] = 999
        }
        vada(nums[0])
        """
        check(code)

    def test_mutate_multiple_indices(self):
        code = """
        chara nums = [1, 2, 3]
        nums[0] = 10
        nums[1] = 20
        nums[2] = 30
        vada(nums[0] + nums[1] + nums[2])
        """
        check(code)

    def test_mutate_primitive_variable_valid(self):
        code = """
        chara x = 10
        x += 5
        x = x * 2
        vada(x)
        """
        check(code)

    def test_mutate_primitive_in_while_loop(self):
        code = """
        chara count = 0
        yavat count < 10 {
            count += 1
        }
        vada(count)
        """
        check(code)

    def test_mutate_multiple_nested_scopes(self):
        code = """
        chara a = 1
        {
            a += 1
            {
                a += 1
            }
        }
        vada(a)
        """
        check(code)

    def test_mutate_map_with_new_key(self):
        code = """
        chara m = {"a": 1}
        m["b"] = 2
        vada(m["b"])
        """
        check(code)

    def test_mutate_array_element_with_expression(self):
        code = """
        chara nums = [1, 2, 3]
        nums[1] = nums[0] + nums[2]
        vada(nums[1])
        """
        check(code)


if __name__ == "__main__":
    unittest.main()
