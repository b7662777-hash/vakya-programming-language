"""Tests for Vākya Parser."""

import unittest
from vakya.lexer.lexer import Lexer
from vakya.parser.parser import Parser
from vakya.ast.nodes import (
    VarDecl,
    FunctionDecl,
    IfStatement,
    WhileStatement,
    ForEachStatement,
    BinaryExpr,
    UnaryExpr,
    Literal,
    Identifier,
    ListLiteral,
    MapLiteral,
    CallExpr,
    IndexExpr,
    MemberExpr,
    ReturnStatement,
)
from vakya.errors import ParseError


def parse_code(code: str):
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens, source_code=code)
    return parser.parse()


class TestParser(unittest.TestCase):
    def test_var_and_const_decls(self):
        ast = parse_code("chara x = 10\ndhruva pi: dashamika = 3.14\nchara name: shabda")
        self.assertEqual(len(ast.statements), 3)

        s1 = ast.statements[0]
        self.assertIsInstance(s1, VarDecl)
        self.assertEqual(s1.name, "x")
        self.assertFalse(s1.is_constant)
        self.assertEqual(s1.initializer.value, 10)

        s2 = ast.statements[1]
        self.assertIsInstance(s2, VarDecl)
        self.assertEqual(s2.name, "pi")
        self.assertTrue(s2.is_constant)
        self.assertEqual(s2.type_annotation, "dashamika")

        s3 = ast.statements[2]
        self.assertIsInstance(s3, VarDecl)
        self.assertEqual(s3.name, "name")
        self.assertIsNone(s3.initializer)

    def test_function_decl(self):
        code = "karya yog(a: sankhya, b: sankhya) -> sankhya { pratyavartaya a + b }"
        ast = parse_code(code)
        fn = ast.statements[0]
        self.assertIsInstance(fn, FunctionDecl)
        self.assertEqual(fn.name, "yog")
        self.assertEqual(len(fn.params), 2)
        self.assertEqual(fn.params[0].name, "a")
        self.assertEqual(fn.params[0].type_annotation, "sankhya")
        self.assertEqual(fn.return_type, "sankhya")
        self.assertIsInstance(fn.body.statements[0], ReturnStatement)

    def test_if_else(self):
        code = """
        yadi x > 10 {
            vada("Big")
        } anyatha yadi x == 10 {
            vada("Equal")
        } anyatha {
            vada("Small")
        }
        """
        ast = parse_code(code)
        stmt = ast.statements[0]
        self.assertIsInstance(stmt, IfStatement)
        self.assertEqual(len(stmt.else_if_branches), 1)
        self.assertIsNotNone(stmt.else_block)

    def test_while_and_for_each(self):
        code = """
        yavat x < 10 {
            x += 1
        }
        pratyekam naam madhye names {
            vada(naam)
        }
        """
        ast = parse_code(code)
        self.assertIsInstance(ast.statements[0], WhileStatement)
        self.assertIsInstance(ast.statements[1], ForEachStatement)
        self.assertEqual(ast.statements[1].variable, "naam")

    def test_operator_precedence(self):
        ast = parse_code("chara x = 2 + 3 * 4 ** 2")
        decl = ast.statements[0]
        bin_add = decl.initializer
        self.assertIsInstance(bin_add, BinaryExpr)
        self.assertEqual(bin_add.operator, "+")
        self.assertEqual(bin_add.left.value, 2)
        bin_mul = bin_add.right
        self.assertEqual(bin_mul.operator, "*")
        self.assertEqual(bin_mul.left.value, 3)
        bin_pow = bin_mul.right
        self.assertEqual(bin_pow.operator, "**")

    def test_collections_and_properties(self):
        code = """
        chara list = [1, 2, 3]
        chara map = {"key": 100}
        chara val = map["key"]
        chara len = list.length
        """
        ast = parse_code(code)
        self.assertIsInstance(ast.statements[0].initializer, ListLiteral)
        self.assertIsInstance(ast.statements[1].initializer, MapLiteral)
        self.assertIsInstance(ast.statements[2].initializer, IndexExpr)
        self.assertIsInstance(ast.statements[3].initializer, MemberExpr)

    def test_parse_error_missing_brace(self):
        code = "yadi x > 10 { vada(x)"
        with self.assertRaises(ParseError) as ctx:
            parse_code(code)
        self.assertEqual(ctx.exception.code, "E202")

    def test_parse_error_uninitialized_constant(self):
        code = "dhruva pi: dashamika"
        with self.assertRaises(ParseError) as ctx:
            parse_code(code)
        self.assertEqual(ctx.exception.code, "E202")


if __name__ == "__main__":
    unittest.main()
