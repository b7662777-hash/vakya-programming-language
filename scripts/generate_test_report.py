"""Generate machine-readable test report across all test suites and examples."""

import glob
import io
import json
import os
import sys
import time
import unittest

# Ensure UTF-8 output
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from vakya.lexer.lexer import Lexer
from vakya.parser.parser import Parser
from vakya.typechecker.checker import TypeChecker
from vakya.bytecode.compiler import BytecodeCompiler
from vakya.vm.vm import VirtualMachine
from vakya.interpreter.interpreter import Interpreter


def run_all_tests():
    start_time = time.perf_counter()
    report = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "suites": {},
        "examples": {},
        "summary": {}
    }

    # 1. Discover and run unittest suites
    loader = unittest.TestLoader()
    suite = loader.discover("tests", pattern="test_*.py")
    runner = unittest.TextTestRunner(stream=io.StringIO(), verbosity=2)
    result = runner.run(suite)

    report["suites"]["core_tests"] = {
        "ran": result.testsRun,
        "failures": len(result.failures),
        "errors": len(result.errors),
        "passed": result.testsRun - len(result.failures) - len(result.errors),
        "was_successful": result.wasSuccessful(),
    }

    # 2. Discover and run showcase test suite
    showcase_suite = unittest.TestSuite()
    for tf in glob.glob("showcase/*/tests/test_*.py"):
        showcase_suite.addTests(loader.discover(os.path.dirname(tf), pattern=os.path.basename(tf)))
    showcase_result = runner.run(showcase_suite)

    report["suites"]["showcase_tests"] = {
        "ran": showcase_result.testsRun,
        "failures": len(showcase_result.failures),
        "errors": len(showcase_result.errors),
        "passed": showcase_result.testsRun - len(showcase_result.failures) - len(showcase_result.errors),
        "was_successful": showcase_result.wasSuccessful(),
    }

    # 3. Canonical example verification (VM vs Interpreter)
    example_files = sorted(glob.glob("examples/*.vakya"))
    all_examples_passed = True

    for ex_path in example_files:
        ex_name = os.path.basename(ex_path)
        with open(ex_path, "r", encoding="utf-8") as f:
            src = f.read()

        try:
            tokens = Lexer(src, filename=ex_name).tokenize()
            ast = Parser(tokens, filename=ex_name, source_code=src).parse()
            TypeChecker(filename=ex_name, source_code=src).check(ast)
            chunk = BytecodeCompiler(filename=ex_name, source_code=src).compile(ast)

            # Interpreter
            out_interp = io.StringIO()
            interp = Interpreter(filename=ex_name, source_code=src, stdout=out_interp)
            interp.interpret(ast)
            res_interp = out_interp.getvalue().strip()

            # VM
            out_vm = io.StringIO()
            vm = VirtualMachine(stdout=out_vm)
            vm.run(chunk)
            res_vm = out_vm.getvalue().strip()

            matched = (res_interp == res_vm)
            if not matched:
                all_examples_passed = False

            report["examples"][ex_name] = {
                "interpreter_status": "ok",
                "vm_status": "ok",
                "differential_parity": matched,
                "output_length": len(res_vm)
            }
        except Exception as e:
            all_examples_passed = False
            report["examples"][ex_name] = {
                "interpreter_status": "error",
                "vm_status": "error",
                "error": str(e),
                "differential_parity": False
            }

    total_time = time.perf_counter() - start_time
    total_tests = report["suites"]["core_tests"]["ran"] + report["suites"]["showcase_tests"]["ran"]
    total_passed = report["suites"]["core_tests"]["passed"] + report["suites"]["showcase_tests"]["passed"]

    report["summary"] = {
        "total_tests": total_tests,
        "total_passed": total_passed,
        "total_failed": total_tests - total_passed,
        "all_examples_verified": all_examples_passed,
        "total_duration_sec": round(total_time, 4),
        "overall_success": (total_tests == total_passed) and all_examples_passed
    }

    with open("test_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print(json.dumps(report["summary"], indent=2))
    return 0 if report["summary"]["overall_success"] else 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
