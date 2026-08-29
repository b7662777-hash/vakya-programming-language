"""Exhaustive lifetime and scope duration tests for the Vākya Borrow Checker."""

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


class TestLifetimes(unittest.TestCase):
    def test_local_variable_lifetime_ends_at_block(self):
        code = """
        {
            chara local_val = [1, 2]
            vada(local_val[0])
        }
        chara new_val = [3, 4]
        vada(new_val[0])
        """
        check(code)

    def test_local_variables_in_multiple_sequential_blocks(self):
        code = """
        {
            chara x = [1]
            vada(x[0])
        }
        {
            chara x = [2]
            vada(x[0])
        }
        {
            chara x = [3]
            vada(x[0])
        }
        """
        check(code)

    def test_outer_variable_outlives_inner_scope(self):
        code = """
        chara outer = [10, 20]
        {
            chara inner = outer[0]
            vada(inner)
        }
        vada(outer[0])
        """
        check(code)

    def test_loop_iteration_variable_lifetime(self):
        code = """
        chara items = [1, 2, 3]
        pratyekam it madhye items {
            chara temp = it * 2
            vada(temp)
        }
        """
        check(code)

    def test_while_loop_scoped_locals(self):
        code = """
        chara i = 0
        yavat i < 3 {
            chara local_buf = [i]
            vada(local_buf[0])
            i += 1
        }
        """
        check(code)

    def test_function_stack_frame_lifetime(self):
        code = """
        karya run_task() {
            chara buf = [1, 2, 3]
            vada(buf[0])
        }
        run_task()
        run_task()
        """
        check(code)

    def test_returned_owned_value_extends_lifetime(self):
        code = """
        karya generate() -> suchi {
            chara data = [10, 20]
            pratyavartaya data
        }
        chara owned = generate()
        vada(owned[0])
        """
        check(code)

    def test_primitive_return_by_value(self):
        code = """
        karya get_num() -> sankhya {
            chara x = 42
            pratyavartaya x
        }
        chara val = get_num()
        vada(val)
        """
        check(code)

    def test_nested_function_lifetimes(self):
        code = """
        karya outer_fn() -> sankhya {
            karya inner_fn() -> sankhya {
                pratyavartaya 99
            }
            pratyavartaya inner_fn()
        }
        vada(outer_fn())
        """
        check(code)

    def test_deeply_nested_block_lifetimes(self):
        code = """
        {
            {
                {
                    chara deeply_nested = [1]
                    vada(deeply_nested[0])
                }
            }
        }
        """
        check(code)

    def test_if_branch_local_lifetime(self):
        code = """
        yadi 10 > 5 {
            chara branch_var = [1, 2]
            vada(branch_var[0])
        }
        """
        check(code)

    def test_else_branch_local_lifetime(self):
        code = """
        yadi 10 < 5 {
            chara a = [1]
        } anyatha {
            chara b = [2]
            vada(b[0])
        }
        """
        check(code)

    def test_multiple_parameters_lifetime(self):
        code = """
        karya combine(a: suchi, b: suchi) -> suchi {
            pratyavartaya a
        }
        chara l1 = [1]
        chara l2 = [2]
        chara res = combine(l1, l2)
        """
        check(code)

    def test_scope_exit_with_break(self):
        code = """
        yavat satya {
            chara loop_data = [10]
            virama
        }
        """
        check(code)

    def test_scope_exit_with_continue(self):
        code = """
        chara i = 0
        yavat i < 2 {
            i += 1
            chara loop_data = [i]
            agaccha
        }
        """
        check(code)


if __name__ == "__main__":
    unittest.main()
