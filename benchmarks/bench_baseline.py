"""Performance baseline benchmark suite for Vākya V1."""

import sys
import time
import io

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from vakya.lexer.lexer import Lexer
from vakya.parser.parser import Parser
from vakya.typechecker.checker import TypeChecker
from vakya.interpreter.interpreter import Interpreter


def benchmark_lexer(iterations: int = 1000) -> float:
    sample_code = """
    dhruva pi = 3.14159
    chara message = "Namaste"
    karya add(a: sankhya, b: sankhya) -> sankhya {
        yadi a > b {
            pratyavartaya a + b * 2
        } anyatha {
            pratyavartaya b - a
        }
    }
    """
    start = time.perf_counter()
    total_tokens = 0
    for _ in range(iterations):
        lexer = Lexer(sample_code)
        tokens = lexer.tokenize()
        total_tokens += len(tokens)
    elapsed = time.perf_counter() - start
    rate = total_tokens / elapsed
    print(f"[BENCHMARK] Lexer throughput: {rate:,.0f} tokens/sec ({total_tokens} tokens in {elapsed:.3f}s)")
    return rate


def benchmark_parser(iterations: int = 500) -> float:
    sample_code = """
    karya compute(n: sankhya) -> sankhya {
        chara total = 0
        chara i = 0
        yavat i < n {
            total += i * 2 + 1
            i += 1
        }
        pratyavartaya total
    }
    """
    lexer = Lexer(sample_code)
    tokens = lexer.tokenize()
    start = time.perf_counter()
    for _ in range(iterations):
        parser = Parser(tokens, source_code=sample_code)
        ast = parser.parse()
    elapsed = time.perf_counter() - start
    rate = iterations / elapsed
    print(f"[BENCHMARK] Parser throughput: {rate:,.0f} parses/sec ({iterations} parses in {elapsed:.3f}s)")
    return rate


def benchmark_loops_and_arithmetic(iterations: int = 10000) -> float:
    code = f"""
    chara total = 0
    chara i = 0
    yavat i < {iterations} {{
        total += i
        i += 1
    }}
    """
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens, source_code=code)
    ast = parser.parse()
    checker = TypeChecker(source_code=code)
    checker.check(ast)

    start = time.perf_counter()
    interpreter = Interpreter(source_code=code)
    interpreter.interpret(ast)
    elapsed = time.perf_counter() - start
    rate = iterations / elapsed
    print(f"[BENCHMARK] While loop & math: {rate:,.0f} iters/sec ({iterations} iterations in {elapsed:.3f}s)")
    return rate


def benchmark_function_calls(calls: int = 5000) -> float:
    code = f"""
    karya add_one(x) {{
        pratyavartaya x + 1
    }}

    chara res = 0
    chara i = 0
    yavat i < {calls} {{
        res = add_one(res)
        i += 1
    }}
    """
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens, source_code=code)
    ast = parser.parse()
    checker = TypeChecker(source_code=code)
    checker.check(ast)

    start = time.perf_counter()
    interpreter = Interpreter(source_code=code)
    interpreter.interpret(ast)
    elapsed = time.perf_counter() - start
    rate = calls / elapsed
    print(f"[BENCHMARK] Function call throughput: {rate:,.0f} calls/sec ({calls} calls in {elapsed:.3f}s)")
    return rate


def benchmark_recursive_fibonacci(n: int = 18) -> float:
    code = f"""
    karya fib(n: sankhya) -> sankhya {{
        yadi n <= 0 {{ pratyavartaya 0 }}
        yadi n == 1 {{ pratyavartaya 1 }}
        pratyavartaya fib(n - 1) + fib(n - 2)
    }}
    chara ans = fib({n})
    """
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens, source_code=code)
    ast = parser.parse()
    checker = TypeChecker(source_code=code)
    checker.check(ast)

    start = time.perf_counter()
    interpreter = Interpreter(source_code=code)
    interpreter.interpret(ast)
    elapsed = time.perf_counter() - start
    print(f"[BENCHMARK] Recursive Fibonacci({n}): {elapsed:.4f}s")
    return elapsed


def benchmark_arrays_and_maps(ops: int = 2000) -> float:
    code = f"""
    chara l = []
    chara m = {{}}
    chara i = 0
    yavat i < {ops} {{
        suchi_jodo(l, i)
        m[i] = i * 2
        i += 1
    }}
    """
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens, source_code=code)
    ast = parser.parse()
    checker = TypeChecker(source_code=code)
    checker.check(ast)

    start = time.perf_counter()
    interpreter = Interpreter(source_code=code)
    interpreter.interpret(ast)
    elapsed = time.perf_counter() - start
    rate = ops / elapsed
    print(f"[BENCHMARK] Array/Map collections: {rate:,.0f} ops/sec ({ops} elements in {elapsed:.3f}s)")
    return rate


def main():
    print("=" * 60)
    print("VĀKYA V1 — PERFORMANCE BASELINE BENCHMARKS")
    print("=" * 60)
    benchmark_lexer()
    benchmark_parser()
    benchmark_loops_and_arithmetic()
    benchmark_function_calls()
    benchmark_recursive_fibonacci()
    benchmark_arrays_and_maps()
    print("=" * 60)
    print("Benchmark suite completed successfully.")
    print("=" * 60)


if __name__ == "__main__":
    main()
