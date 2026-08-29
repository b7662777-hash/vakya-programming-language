"""End-to-End Integration tests for Vākya."""

import os
import unittest
from vakya.cli import execute_file, format_file, main


class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.examples_dir = os.path.join(os.path.dirname(__file__), "..", "..", "examples")

    def test_run_hello(self):
        file_path = os.path.join(self.examples_dir, "hello.vakya")
        code = execute_file(file_path, check_only=False)
        self.assertEqual(code, 0)

    def test_run_calculator(self):
        file_path = os.path.join(self.examples_dir, "calculator.vakya")
        code = execute_file(file_path, check_only=False)
        self.assertEqual(code, 0)

    def test_run_fibonacci(self):
        file_path = os.path.join(self.examples_dir, "fibonacci.vakya")
        code = execute_file(file_path, check_only=False)
        self.assertEqual(code, 0)

    def test_run_factorial(self):
        file_path = os.path.join(self.examples_dir, "factorial.vakya")
        code = execute_file(file_path, check_only=False)
        self.assertEqual(code, 0)

    def test_run_loops(self):
        file_path = os.path.join(self.examples_dir, "loops.vakya")
        code = execute_file(file_path, check_only=False)
        self.assertEqual(code, 0)

    def test_run_arrays(self):
        file_path = os.path.join(self.examples_dir, "arrays.vakya")
        code = execute_file(file_path, check_only=False)
        self.assertEqual(code, 0)

    def test_run_maps(self):
        file_path = os.path.join(self.examples_dir, "maps.vakya")
        code = execute_file(file_path, check_only=False)
        self.assertEqual(code, 0)

    def test_run_functions(self):
        file_path = os.path.join(self.examples_dir, "functions.vakya")
        code = execute_file(file_path, check_only=False)
        self.assertEqual(code, 0)

    def test_cli_check_all_examples(self):
        for fname in os.listdir(self.examples_dir):
            if fname.endswith(".vakya"):
                path = os.path.join(self.examples_dir, fname)
                status = execute_file(path, check_only=True)
                self.assertEqual(status, 0, f"Check failed for {fname}")

    def test_cli_version(self):
        res = main(["version"])
        self.assertEqual(res, 0)


if __name__ == "__main__":
    unittest.main()
