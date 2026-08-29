"""Tests for Vākya Formatter."""

import unittest
from vakya.formatter.formatter import Formatter


class TestFormatter(unittest.TestCase):
    def setUp(self):
        self.formatter = Formatter()

    def test_format_function(self):
        source = "karya add(a,b){pratyavartaya a+b}"
        formatted = self.formatter.format_source(source)
        expected = "karya add(a, b) {\n    pratyavartaya a + b\n}\n"
        self.assertEqual(formatted, expected)

    def test_format_if_else(self):
        source = "yadi x>10{vada(1)}anyatha{vada(0)}"
        formatted = self.formatter.format_source(source)
        expected = "yadi x > 10 {\n    vada(1)\n} anyatha {\n    vada(0)\n}\n"
        self.assertEqual(formatted, expected)

    def test_formatter_idempotency(self):
        source = """
karya factorial(n: sankhya) -> sankhya {
    yadi n <= 1 {
        pratyavartaya 1
    }
    pratyavartaya n * factorial(n - 1)
}

chara result = factorial(5)
vada(result)
"""
        pass1 = self.formatter.format_source(source)
        pass2 = self.formatter.format_source(pass1)
        self.assertEqual(pass1, pass2)


if __name__ == "__main__":
    unittest.main()
