"""Tests for scoping, variable shadowing, environments, and closures in Vākya."""

import io
import unittest
from vakya.lexer.lexer import Lexer
from vakya.parser.parser import Parser
from vakya.typechecker.checker import TypeChecker
from vakya.interpreter.interpreter import Interpreter


def run_code(code: str) -> str:
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens, source_code=code)
    ast = parser.parse()
    checker = TypeChecker(source_code=code)
    checker.check(ast)
    out = io.StringIO()
    interpreter = Interpreter(source_code=code, stdout=out)
    interpreter.interpret(ast)
    return out.getvalue().strip()


class TestScopingAndClosures(unittest.TestCase):
    def test_spec_section_7_scoping_challenge(self):
        code = """
        chara x = 10

        karya test() {
            chara x = 20

            yadi satya {
                chara x = 30
                vada(x)
            }

            vada(x)
        }

        test()
        vada(x)
        """
        self.assertEqual(run_code(code), "30\n20\n10")

    def test_nested_functions_scope_chain(self):
        code = """
        chara a = "global_a"

        karya outer() {
            chara b = "outer_b"

            karya middle() {
                chara c = "middle_c"

                karya inner() {
                    vada(a)
                    vada(b)
                    vada(c)
                }
                inner()
            }
            middle()
        }
        outer()
        """
        self.assertEqual(run_code(code), "global_a\nouter_b\nmiddle_c")

    def test_independent_closure_instances(self):
        code = """
        karya create_accumulator(initial) {
            chara total = initial
            karya add_val(delta) {
                total += delta
                pratyavartaya total
            }
            pratyavartaya add_val
        }

        chara acc1 = create_accumulator(100)
        chara acc2 = create_accumulator(0)

        vada(acc1(10))
        vada(acc2(5))
        vada(acc1(20))
        vada(acc2(5))
        """
        self.assertEqual(run_code(code), "110\n5\n130\n10")

    def test_mutation_of_outer_variable_in_block(self):
        code = """
        chara x = 10
        yadi satya {
            x = 50
        }
        vada(x)
        """
        self.assertEqual(run_code(code), "50")

    def test_loop_scope_isolation(self):
        code = """
        chara x = 999
        chara nums = [1, 2]
        pratyekam x madhye nums {
            vada("Loop:", x)
        }
        vada("Outer:", x)
        """
        self.assertEqual(run_code(code), "Loop: 1\nLoop: 2\nOuter: 999")


if __name__ == "__main__":
    unittest.main()
