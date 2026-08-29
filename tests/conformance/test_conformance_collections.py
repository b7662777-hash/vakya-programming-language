"""Conformance tests for collections (arrays / suchi, maps / naksha) in Vākya."""

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


class TestConformanceCollections(unittest.TestCase):
    def test_empty_list(self):
        code = "chara l = []\nvada(l)\nvada(l.length)"
        self.assertEqual(run_code(code), "[]\n0")

    def test_single_element_list(self):
        code = "chara l = [42]\nvada(l[0])\nvada(l.length)"
        self.assertEqual(run_code(code), "42\n1")

    def test_multi_element_list(self):
        code = "chara l = [10, 20, 30]\nvada(l)\nvada(l[1])"
        self.assertEqual(run_code(code), "[10, 20, 30]\n20")

    def test_list_trailing_comma(self):
        code = "chara l = [10, 20,]\nvada(l.length)"
        self.assertEqual(run_code(code), "2")

    def test_nested_list(self):
        code = """
        chara matrix = [[1, 2], [3, 4]]
        vada(matrix[0][1])
        vada(matrix[1][0])
        """
        self.assertEqual(run_code(code), "2\n3")

    def test_list_mutation(self):
        code = """
        chara l = [1, 2, 3]
        l[1] = 99
        vada(l)
        """
        self.assertEqual(run_code(code), "[1, 99, 3]")

    def test_suchi_jodo_and_hatao(self):
        code = """
        chara l = [10]
        suchi_jodo(l, 20)
        suchi_jodo(l, 30)
        vada(l)
        chara popped = suchi_hatao(l, 1)
        vada(popped)
        vada(l)
        """
        self.assertEqual(run_code(code), "[10, 20, 30]\n20\n[10, 30]")

    def test_empty_map(self):
        code = "chara m = {}\nvada(m)\nvada(m.length)"
        self.assertEqual(run_code(code), "{}\n0")

    def test_map_access_and_mutation(self):
        code = """
        chara user = {"name": "Goku", "age": 16}
        vada(user["name"])
        vada(user["age"])
        user["age"] = 17
        user["power"] = 9001
        vada(user["age"])
        vada(user["power"])
        """
        self.assertEqual(run_code(code), "Goku\n16\n17\n9001")

    def test_map_trailing_comma(self):
        code = """
        chara m = {
            "a": 1,
            "b": 2,
        }
        vada(m.length)
        """
        self.assertEqual(run_code(code), "2")

    def test_map_nested_in_list(self):
        code = """
        chara users = [{"name": "A"}, {"name": "B"}]
        vada(users[0]["name"])
        vada(users[1]["name"])
        """
        self.assertEqual(run_code(code), "A\nB")

    def test_lamba_builtin_on_collections(self):
        code = """
        chara l = [1, 2, 3, 4]
        chara m = {"x": 10, "y": 20}
        vada(lamba(l))
        vada(lamba(m))
        """
        self.assertEqual(run_code(code), "4\n2")


if __name__ == "__main__":
    unittest.main()
