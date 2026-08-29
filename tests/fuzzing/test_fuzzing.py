"""Fuzzing tests for Vākya Lexer and Parser resilience."""

import unittest
from vakya.lexer.lexer import Lexer
from vakya.parser.parser import Parser
from vakya.errors import VakyaError, LexerError, ParseError


class TestFuzzing(unittest.TestCase):
    def test_lexer_fuzz_random_symbols(self):
        fuzz_chars = ["@", "#", "$", "?", "~", "^", "\\", "`", ";", "&", "|", "§", "€", "🚀"]
        for ch in fuzz_chars:
            source = f"chara x = {ch} 10"
            lexer = Lexer(source)
            with self.assertRaises(LexerError, msg=f"Failed to cleanly reject '{ch}'") as ctx:
                lexer.tokenize()
            self.assertEqual(ctx.exception.code, "E001")

    def test_lexer_fuzz_unterminated_strings(self):
        malformed_strings = [
            '"',
            '""',  # valid empty
            '"hello',
            '"hello\\',
            '"hello\nworld"',
            '"""',
        ]
        for s in malformed_strings:
            if s == '""':
                lexer = Lexer(s)
                tokens = lexer.tokenize()
                self.assertEqual(len(tokens), 2)
            else:
                lexer = Lexer(s)
                with self.assertRaises(LexerError, msg=f"Failed for malformed string {s!r}") as ctx:
                    lexer.tokenize()
                self.assertIn(ctx.exception.code, ("E002", "E004"))

    def test_lexer_fuzz_unterminated_comments(self):
        malformed_comments = [
            "/*",
            "/* hello",
            "/* * /",
            "/* /* */",  # first closed, but if open again...
        ]
        for c in malformed_comments[:3]:
            lexer = Lexer(c)
            with self.assertRaises(LexerError, msg=f"Failed for comment {c!r}") as ctx:
                lexer.tokenize()
            self.assertEqual(ctx.exception.code, "E003")

    def test_parser_fuzz_deeply_nested_parens(self):
        depth = 30
        source = "(" * depth + "42" + ")" * depth
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens, source_code=source)
        ast = parser.parse()
        self.assertEqual(len(ast.statements), 1)

    def test_parser_fuzz_deeply_nested_unary(self):
        # 20 unary minus
        source = "-" * 20 + "42"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens, source_code=source)
        ast = parser.parse()
        self.assertEqual(len(ast.statements), 1)

    def test_parser_fuzz_deeply_nested_logical_not(self):
        # 10 logical not
        source = "na " * 10 + "satya"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens, source_code=source)
        ast = parser.parse()
        self.assertEqual(len(ast.statements), 1)

    def test_parser_fuzz_malformed_syntax_snippets(self):
        malformed_snippets = [
            "(((((((",
            "}}}}}}}",
            "]]]]]]]",
            "karya ()",
            "karya 123()",
            "yadi { vada(1) }",
            "yavat { vada(1) }",
            "pratyekam madhye items {}",
            "pratyekam x items {}",
            "pratyekam x madhye {}",
            "chara",
            "dhruva",
            "chara x:",
            "chara x: =",
            "karya fn(a: ) {}",
            "karya fn(a) -> {}",
            "[1, , 2]",
            "{ : 1 }",
            "{ 1 : }",
            "+ + +",
            "* * *",
            "-> ->",
        ]
        for snippet in malformed_snippets:
            try:
                lexer = Lexer(snippet)
                tokens = lexer.tokenize()
                parser = Parser(tokens, source_code=snippet)
                parser.parse()
                # Should not reach here without exception
                self.fail(f"Expected ParseError for malformed snippet: {snippet!r}")
            except VakyaError:
                # Successfully caught and converted into VakyaError!
                pass


if __name__ == "__main__":
    unittest.main()
