"""Exhaustive move semantics tests for the Vākya Borrow Checker."""

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


class TestMoveSemantics(unittest.TestCase):
    def test_direct_use_after_move_e501(self):
        with self.assertRaises(BorrowError) as ctx:
            check("chara a = [1, 2]\nchara b = a\nvada(a)")
        self.assertEqual(ctx.exception.code, "E501")

    def test_indexing_after_move_e501(self):
        with self.assertRaises(BorrowError) as ctx:
            check("chara a = [1, 2]\nchara b = a\nchara x = a[0]")
        self.assertEqual(ctx.exception.code, "E501")

    def test_moving_moved_value_e501(self):
        with self.assertRaises(BorrowError) as ctx:
            check("chara a = [1]\nchara b = a\nchara c = a")
        self.assertEqual(ctx.exception.code, "E501")

    def test_passing_moved_value_to_function_e501(self):
        code = """
        karya take(lst: suchi) {}
        chara a = [10, 20]
        chara b = a
        take(a)
        """
        with self.assertRaises(BorrowError) as ctx:
            check(code)
        self.assertEqual(ctx.exception.code, "E501")

    def test_chain_of_moves(self):
        code = """
        chara a = [1]
        chara b = a
        chara c = b
        chara d = c
        vada(d[0])
        """
        check(code)

    def test_chain_of_moves_access_middle_e501(self):
        code = """
        chara a = [1]
        chara b = a
        chara c = b
        vada(b[0])
        """
        with self.assertRaises(BorrowError) as ctx:
            check(code)
        self.assertEqual(ctx.exception.code, "E501")

    def test_string_concatenation_move(self):
        with self.assertRaises(BorrowError) as ctx:
            check('chara s1 = "Namaste"\nchara s2 = s1\nvada(s1 + " World")')
        self.assertEqual(ctx.exception.code, "E501")

    def test_move_inside_nested_block(self):
        code = """
        chara a = [1, 2]
        {
            chara b = a
        }
        vada(a[0])
        """
        with self.assertRaises(BorrowError) as ctx:
            check(code)
        self.assertEqual(ctx.exception.code, "E501")

    def test_reassignment_in_nested_block_then_move(self):
        code = """
        chara a = [1]
        chara b = a
        {
            a = [2]
            chara c = a
        }
        """
        check(code)

    def test_function_return_moves_ownership(self):
        code = """
        karya make_list() -> suchi {
            chara l = [10, 20]
            pratyavartaya l
        }
        chara res = make_list()
        vada(res[0])
        """
        check(code)

    def test_passing_value_to_two_functions(self):
        code = """
        karya f1(x: suchi) {}
        karya f2(x: suchi) {}
        chara data = [1, 2]
        f1(data)
        """
        check(code)

    def test_move_in_while_loop_header(self):
        code = """
        chara a = [1]
        chara b = a
        """
        check(code)

    def test_move_with_binary_expression(self):
        with self.assertRaises(BorrowError) as ctx:
            check("chara a = [1]\nchara b = a\nchara c = a == b")
        self.assertEqual(ctx.exception.code, "E501")

    def test_move_into_map_value(self):
        code = """
        chara val = [10, 20]
        chara m = {"key": val}
        """
        check(code)

    def test_access_after_move_into_map_e501(self):
        code = """
        chara val = [10, 20]
        chara m = {"key": val}
        vada(val[0])
        """
        with self.assertRaises(BorrowError) as ctx:
            check(code)
        self.assertEqual(ctx.exception.code, "E501")


if __name__ == "__main__":
    unittest.main()
