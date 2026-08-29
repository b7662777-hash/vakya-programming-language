"""Conformance tests for control flow (if/else, while, for-each, break, continue) in Vākya."""

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


class TestConformanceControlFlow(unittest.TestCase):
    def test_if_true_branch(self):
        code = """
        chara x = 10
        yadi x > 5 {
            vada("Greater")
        }
        """
        self.assertEqual(run_code(code), "Greater")

    def test_if_false_no_else(self):
        code = """
        chara x = 2
        yadi x > 5 {
            vada("Greater")
        }
        vada("Done")
        """
        self.assertEqual(run_code(code), "Done")

    def test_if_else(self):
        code = """
        chara age = 15
        yadi age >= 18 {
            vada("Adult")
        } anyatha {
            vada("Minor")
        }
        """
        self.assertEqual(run_code(code), "Minor")

    def test_if_else_if_cascade(self):
        code = """
        chara score = 85
        yadi score >= 90 {
            vada("A")
        } anyatha yadi score >= 80 {
            vada("B")
        } anyatha yadi score >= 70 {
            vada("C")
        } anyatha {
            vada("D")
        }
        """
        self.assertEqual(run_code(code), "B")

    def test_if_with_tarhi_keyword(self):
        code = """
        chara x = 10
        yadi x == 10 tarhi {
            vada("Matched with tarhi")
        }
        """
        self.assertEqual(run_code(code), "Matched with tarhi")

    def test_nested_if(self):
        code = """
        chara a = 10
        chara b = 20
        yadi a > 5 {
            yadi b > 15 {
                vada("Both true")
            }
        }
        """
        self.assertEqual(run_code(code), "Both true")

    def test_while_loop_basic(self):
        code = """
        chara i = 0
        yavat i < 3 {
            vada(i)
            i += 1
        }
        """
        self.assertEqual(run_code(code), "0\n1\n2")

    def test_while_loop_break(self):
        code = """
        chara i = 0
        yavat satya {
            yadi i >= 3 {
                virama
            }
            vada(i)
            i += 1
        }
        """
        self.assertEqual(run_code(code), "0\n1\n2")

    def test_while_loop_continue(self):
        code = """
        chara i = 0
        yavat i < 4 {
            i += 1
            yadi i == 2 {
                agaccha
            }
            vada(i)
        }
        """
        self.assertEqual(run_code(code), "1\n3\n4")

    def test_for_each_list(self):
        code = """
        chara items = ["apple", "banana"]
        pratyekam item madhye items {
            vada(item)
        }
        """
        self.assertEqual(run_code(code), "apple\nbanana")

    def test_for_each_map(self):
        code = """
        chara user = {"name": "Goku"}
        pratyekam key madhye user {
            vada(key + ":" + user[key])
        }
        """
        self.assertEqual(run_code(code), "name:Goku")

    def test_for_each_string(self):
        code = """
        chara word = "Hi"
        pratyekam ch madhye word {
            vada(ch)
        }
        """
        self.assertEqual(run_code(code), "H\ni")

    def test_for_each_break_and_continue(self):
        code = """
        chara nums = [1, 2, 3, 4, 5]
        pratyekam n madhye nums {
            yadi n == 2 {
                agaccha
            }
            yadi n == 4 {
                virama
            }
            vada(n)
        }
        """
        self.assertEqual(run_code(code), "1\n3")


if __name__ == "__main__":
    unittest.main()
