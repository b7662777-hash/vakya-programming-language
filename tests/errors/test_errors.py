"""Tests for Vākya Diagnostic and Error Formatting."""

import unittest
from vakya.errors import VakyaError, E101_UNDEFINED_VARIABLE


class TestErrorFormatting(unittest.TestCase):
    def test_diagnostic_snippet_formatting(self):
        source = "chara a = 10\nvada(naam)\nchara b = 20"
        err = VakyaError.from_info(
            E101_UNDEFINED_VARIABLE,
            "Undefined variable 'naam'",
            filename="test.vakya",
            line=2,
            column=6,
            length=4,
            source_code=source,
            help_text="Declare 'naam' before using it.",
        )
        diagnostic = err.format_diagnostic()
        self.assertIn("Error [E101]: Undefined variable", diagnostic)
        self.assertIn("--> test.vakya:2:6", diagnostic)
        self.assertIn("2 | vada(naam)", diagnostic)
        self.assertIn("^^^^", diagnostic)
        self.assertIn("Help: Declare 'naam' before using it.", diagnostic)


if __name__ == "__main__":
    unittest.main()
