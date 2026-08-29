"""Unit tests for the Vākya Compile-Time Borrow Checker & Swamitva Ownership Model."""

import unittest
from vakya.lexer.lexer import Lexer
from vakya.parser.parser import Parser
from vakya.typechecker.checker import TypeChecker
from vakya.typechecker.borrow_checker import BorrowChecker
from vakya.errors import BorrowError


def check_borrow(code: str):
    tokens = Lexer(code).tokenize()
    ast = Parser(tokens, source_code=code).parse()
    TypeChecker(source_code=code).check(ast)
    BorrowChecker(source_code=code).check(ast)


class TestBorrowChecker(unittest.TestCase):
    def test_primitive_copy_semantics(self):
        # Primitives are Copy types; copying them leaves the source active
        code = """
        chara a = 42
        chara b = a
        chara c = a + b
        vada(c)
        """
        check_borrow(code)  # Should pass without error

    def test_use_after_move_e501(self):
        # Assigning a heap list transfers ownership; using it afterwards is an error
        code = """
        chara a = [1, 2, 3]
        chara b = a
        chara first = a[0]
        """
        with self.assertRaises(BorrowError) as ctx:
            check_borrow(code)
        self.assertEqual(ctx.exception.code, "E501")
        self.assertIn("Use of moved value 'a'", str(ctx.exception))

    def test_reassigned_after_move_is_valid(self):
        # Once reassigned, a variable is re-initialized and active again
        code = """
        chara a = [1, 2, 3]
        chara b = a
        a = [4, 5, 6]
        chara first = a[0]
        """
        check_borrow(code)  # Should pass without error

    def test_string_move_semantics(self):
        code = """
        chara s1 = "Namaste"
        chara s2 = s1
        vada(s1)
        """
        with self.assertRaises(BorrowError) as ctx:
            check_borrow(code)
        self.assertEqual(ctx.exception.code, "E501")

    def test_nested_block_drop(self):
        code = """
        chara outer = [10, 20]
        {
            chara inner = outer
            vada(inner[0])
        }
        """
        check_borrow(code)  # Moves into inner scope cleanly

    def test_function_scope_isolation(self):
        code = """
        karya process(items: suchi) -> sankhya {
            pratyavartaya items[0]
        }

        chara data = [1, 2, 3]
        chara r = process(data)
        """
        check_borrow(code)


if __name__ == "__main__":
    unittest.main()
