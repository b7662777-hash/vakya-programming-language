"""Run all showcase project tests."""

import os
import sys
import unittest

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

def run_all_showcase_tests():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    showcase_dir = os.path.dirname(os.path.abspath(__file__))
    test_files = [
        os.path.join(showcase_dir, "01_name_program", "tests", "test_name.py"),
        os.path.join(showcase_dir, "02_calculator", "tests", "test_calculator.py"),
        os.path.join(showcase_dir, "03_browser", "tests", "test_browser.py"),
    ]

    for test_file in test_files:
        if os.path.exists(test_file):
            suite.addTests(loader.discover(os.path.dirname(test_file), pattern=os.path.basename(test_file)))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(run_all_showcase_tests())
