"""Tests for Vākya Lexer."""

import unittest
from vakya.lexer.lexer import Lexer
from vakya.lexer.tokens import TokenType
from vakya.errors import LexerError


class TestLexer(unittest.TestCase):
    def test_keywords(self):
        source = "chara dhruva karya pratyavartaya yadi anyatha tarhi yavat pratyekam madhye virama agaccha satya asatya shunya aayat antah sarvajan evam va na"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        expected_types = [
            TokenType.CHARA,
            TokenType.DHRUVA,
            TokenType.KARYA,
            TokenType.PRATYAVARTAYA,
            TokenType.YADI,
            TokenType.ANYATHA,
            TokenType.TARHI,
            TokenType.YAVAT,
            TokenType.PRATYEKAM,
            TokenType.MADHYE,
            TokenType.VIRAMA,
            TokenType.AGACCHA,
            TokenType.SATYA,
            TokenType.ASATYA,
            TokenType.SHUNYA,
            TokenType.AAYAT,
            TokenType.ANTAH,
            TokenType.SARVAJAN,
            TokenType.EVAM,
            TokenType.VA,
            TokenType.NA,
            TokenType.EOF,
        ]
        self.assertEqual([t.type for t in tokens], expected_types)

    def test_numbers(self):
        source = "10 0 1000000 3.14 0.5 12.75"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        self.assertEqual(tokens[0].type, TokenType.INTEGER)
        self.assertEqual(tokens[0].value, 10)
        self.assertEqual(tokens[3].type, TokenType.FLOAT)
        self.assertAlmostEqual(tokens[3].value, 3.14)

    def test_strings_and_escapes(self):
        source = r'"Goku" "Namaste\nWorld" "Tab\tSeparated\"Quote\""'
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        self.assertEqual(tokens[0].type, TokenType.STRING)
        self.assertEqual(tokens[0].value, "Goku")
        self.assertEqual(tokens[1].value, "Namaste\nWorld")
        self.assertEqual(tokens[2].value, 'Tab\tSeparated"Quote"')

    def test_operators(self):
        source = "+ - * / % ** = += -= *= /= == != < > <= >= ->"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        expected = [
            TokenType.PLUS,
            TokenType.MINUS,
            TokenType.STAR,
            TokenType.SLASH,
            TokenType.PERCENT,
            TokenType.POWER,
            TokenType.EQ,
            TokenType.PLUS_EQ,
            TokenType.MINUS_EQ,
            TokenType.STAR_EQ,
            TokenType.SLASH_EQ,
            TokenType.EQ_EQ,
            TokenType.NOT_EQ,
            TokenType.LT,
            TokenType.GT,
            TokenType.LT_EQ,
            TokenType.GT_EQ,
            TokenType.ARROW,
            TokenType.EOF,
        ]
        self.assertEqual([t.type for t in tokens], expected)

    def test_comments(self):
        source = """
        // Single-line comment
        chara x = 10 /* multi-line
        comment */
        vada(x)
        """
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        token_types = [t.type for t in tokens]
        self.assertIn(TokenType.CHARA, token_types)
        self.assertIn(TokenType.INTEGER, token_types)
        self.assertIn(TokenType.IDENTIFIER, token_types)

    def test_error_unterminated_string(self):
        source = 'chara naam = "Goku'
        lexer = Lexer(source)
        with self.assertRaises(LexerError) as ctx:
            lexer.tokenize()
        self.assertEqual(ctx.exception.code, "E002")

    def test_error_unterminated_comment(self):
        source = '/* Unclosed comment'
        lexer = Lexer(source)
        with self.assertRaises(LexerError) as ctx:
            lexer.tokenize()
        self.assertEqual(ctx.exception.code, "E003")

    def test_error_invalid_char(self):
        source = 'chara x = @10'
        lexer = Lexer(source)
        with self.assertRaises(LexerError) as ctx:
            lexer.tokenize()
        self.assertEqual(ctx.exception.code, "E001")


if __name__ == "__main__":
    unittest.main()
