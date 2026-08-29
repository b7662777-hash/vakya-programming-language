"""Tests for Vākya CLI commands and process return codes."""

import os
import tempfile
import unittest
from vakya.cli import main, execute_file, format_file


class TestCLI(unittest.TestCase):
    def setUp(self):
        self.examples_dir = os.path.join(os.path.dirname(__file__), "..", "..", "examples")

    def test_cli_version(self):
        self.assertEqual(main(["version"]), 0)
        self.assertEqual(main(["--version"]), 0)

    def test_cli_help(self):
        self.assertEqual(main(["help"]), 0)
        self.assertEqual(main(["--help"]), 0)
        self.assertEqual(main([]), 0)

    def test_cli_run_valid_file(self):
        file_path = os.path.join(self.examples_dir, "hello.vakya")
        self.assertEqual(main(["run", file_path]), 0)

    def test_cli_run_nonexistent_file(self):
        self.assertEqual(main(["run", "missing_file_xyz.vakya"]), 1)

    def test_cli_check_valid_file(self):
        file_path = os.path.join(self.examples_dir, "factorial.vakya")
        self.assertEqual(main(["check", file_path]), 0)

    def test_cli_check_invalid_file(self):
        with tempfile.NamedTemporaryFile("w", suffix=".vakya", delete=False) as f:
            f.write('chara x: sankhya = "type error"')
            temp_path = f.name
        try:
            self.assertEqual(main(["check", temp_path]), 1)
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    def test_cli_fmt_check_and_write(self):
        with tempfile.NamedTemporaryFile("w", suffix=".vakya", delete=False) as f:
            f.write("karya add(a,b){pratyavartaya a+b}")
            temp_path = f.name
        try:
            # Unformatted file should fail --check
            self.assertEqual(main(["fmt", temp_path, "--check"]), 1)
            # Format in place
            self.assertEqual(main(["fmt", temp_path, "--write"]), 0)
            # Now should pass --check
            self.assertEqual(main(["fmt", temp_path, "--check"]), 0)
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)


if __name__ == "__main__":
    unittest.main()
