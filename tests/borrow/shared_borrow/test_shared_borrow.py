"""Exhaustive shared borrow tests for the Vākya Borrow Checker."""

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


class TestSharedBorrow(unittest.TestCase):
    def test_single_shared_read(self):
        check("chara a = [1, 2]\nchara x = a[0]\nchara y = a[1]\nvada(x + y)")

    def test_multiple_readers_same_variable(self):
        check("chara a = [10, 20]\nchara r1 = a[0]\nchara r2 = a[0]\nchara r3 = a[1]")

    def test_read_in_expression(self):
        check("chara a = [5]\nchara b = [10]\nchara sum = a[0] + b[0]\nvada(sum)")

    def test_read_in_loop(self):
        code = """
        chara nums = [1, 2, 3]
        chara i = 0
        yavat i < 3 {
            vada(nums[0])
            i += 1
        }
        """
        check(code)

    def test_read_in_function_call(self):
        code = """
        karya inspect(val: sankhya) {}
        chara a = [100]
        inspect(a[0])
        inspect(a[0])
        """
        check(code)

    def test_shared_borrow_of_map(self):
        code = """
        chara m = {"alpha": 1, "beta": 2}
        chara a = m["alpha"]
        chara b = m["beta"]
        vada(a + b)
        """
        check(code)

    def test_shared_borrow_across_nested_blocks(self):
        code = """
        chara data = [1, 2, 3]
        {
            chara v1 = data[0]
            {
                chara v2 = data[1]
                vada(v1 + v2)
            }
        }
        vada(data[0])
        """
        check(code)

    def test_shared_read_in_if_condition(self):
        code = """
        chara data = [10]
        yadi data[0] > 5 {
            vada(data[0])
        }
        """
        check(code)

    def test_shared_read_in_else_branch(self):
        code = """
        chara data = [3]
        yadi data[0] > 5 {
            vada(1)
        } anyatha {
            vada(data[0])
        }
        """
        check(code)

    def test_multiple_reads_in_nested_function(self):
        code = """
        chara global_list = [10, 20]
        karya read_first() -> sankhya {
            pratyavartaya global_list[0]
        }
        vada(read_first())
        """
        check(code)

    def test_shared_borrow_with_string_length(self):
        code = """
        chara s = "Namaste"
        chara l = s.length
        vada(l)
        """
        check(code)

    def test_shared_borrow_with_list_length(self):
        code = """
        chara l = [10, 20, 30]
        chara n = l.length
        vada(n)
        """
        check(code)

    def test_shared_borrow_after_inner_scope(self):
        code = """
        chara data = [1]
        {
            chara x = data[0]
        }
        chara y = data[0]
        vada(y)
        """
        check(code)

    def test_shared_borrow_passed_as_primitive(self):
        code = """
        karya double_val(x: sankhya) -> sankhya {
            pratyavartaya x * 2
        }
        chara list_a = [5]
        vada(double_val(list_a[0]))
        """
        check(code)

    def test_shared_borrow_in_for_each(self):
        code = """
        chara list_a = [1, 2, 3]
        pratyekam x madhye list_a {
            vada(x)
        }
        vada(list_a[0])
        """
        check(code)


if __name__ == "__main__":
    unittest.main()
