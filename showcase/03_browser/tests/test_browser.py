"""Unit tests for Showcase Project 03 (Vākya Mini Browser)."""

import io
import os
import unittest
from vakya.lexer.lexer import Lexer
from vakya.parser.parser import Parser
from vakya.typechecker.checker import TypeChecker
from vakya.bytecode.compiler import BytecodeCompiler
from vakya.vm.vm import VirtualMachine
import sys

# Add showcase/03_browser to sys.path for direct module import
browser_pkg_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if browser_pkg_dir not in sys.path:
    sys.path.insert(0, browser_pkg_dir)

from browser.http_client import fetch_url
from browser.engine import HTMLParser, MiniBrowserEngine, DOMNode


class TestVakyaBrowserCore(unittest.TestCase):
    def setUp(self):
        self.script_path = os.path.join(os.path.dirname(__file__), "..", "vakya", "browser.vakya")
        with open(self.script_path, "r", encoding="utf-8") as f:
            self.source_code = f.read()

    def run_vakya_code(self, code: str) -> str:
        tokens = Lexer(code, filename="browser_test.vakya").tokenize()
        ast = Parser(tokens, source_code=code, filename="browser_test.vakya").parse()
        TypeChecker(source_code=code, filename="browser_test.vakya").check(ast)

        stdout_stream = io.StringIO()
        chunk = BytecodeCompiler(source_code=code, filename="browser_test.vakya").compile(ast)
        vm = VirtualMachine(stdout=stdout_stream)
        vm.run(chunk)
        return stdout_stream.getvalue().strip()

    def test_vakya_url_parser(self):
        code = self.source_code + '\nchara u1 = parse_url("https://example.com/docs/intro.html")\nvada("P1:", u1["protocol"])\nvada("H1:", u1["host"])\nvada("Path1:", u1["path"])'
        out = self.run_vakya_code(code)
        self.assertIn("P1: https", out)
        self.assertIn("H1: example.com", out)
        self.assertIn("Path1: /docs/intro.html", out)

    def test_vakya_history_stack(self):
        code = self.source_code + '\nchara h = itihaasa_naya()\nitihaasa_push(h, "p1")\nitihaasa_push(h, "p2")\nitihaasa_push(h, "p3")\nvada("Back1:", itihaasa_pichhe(h))\nvada("Back2:", itihaasa_pichhe(h))\nvada("Forward1:", itihaasa_aage(h))\nitihaasa_push(h, "p4")\nvada("ForwardAfterNew:", itihaasa_aage(h))\nvada("Total:", lamba(h["entries"]))'
        out = self.run_vakya_code(code)
        self.assertIn("Back1: p2", out)
        self.assertIn("Back2: p1", out)
        self.assertIn("Forward1: p2", out)
        self.assertIn("ForwardAfterNew: shunya", out)
        self.assertIn("Total: 3", out)


class TestHostBrowserEngine(unittest.TestCase):
    def setUp(self):
        self.examples_dir = os.path.join(os.path.dirname(__file__), "..", "examples")

    def test_html_parser_sample_page(self):
        sample_path = os.path.join(self.examples_dir, "sample.html")
        with open(sample_path, "r", encoding="utf-8") as f:
            html = f.read()

        dom = HTMLParser.parse(html)
        self.assertIsInstance(dom, DOMNode)
        self.assertEqual(dom.tag, "html")
        self.assertGreater(dom.count_nodes(), 5)

    def test_html_parser_malformed_page_resilience(self):
        malformed_path = os.path.join(self.examples_dir, "malformed.html")
        with open(malformed_path, "r", encoding="utf-8") as f:
            html = f.read()

        dom = HTMLParser.parse(html)
        self.assertIsInstance(dom, DOMNode)
        self.assertEqual(dom.tag, "html")
        self.assertGreater(dom.count_nodes(), 5)

    def test_browser_engine_navigation_and_history(self):
        engine = MiniBrowserEngine()
        sample_file_url = "file://" + os.path.abspath(os.path.join(self.examples_dir, "sample.html")).replace("\\", "/")
        malformed_file_url = "file://" + os.path.abspath(os.path.join(self.examples_dir, "malformed.html")).replace("\\", "/")

        # 1. Navigate to first page
        dom1 = engine.navigate(sample_file_url)
        self.assertEqual(engine.current_status, 200)
        self.assertFalse(engine.can_go_back())
        self.assertFalse(engine.can_go_forward())

        # 2. Navigate to second page
        dom2 = engine.navigate(malformed_file_url)
        self.assertEqual(engine.current_status, 200)
        self.assertTrue(engine.can_go_back())
        self.assertFalse(engine.can_go_forward())

        # 3. Go back
        back_dom = engine.back()
        self.assertIsNotNone(back_dom)
        self.assertEqual(engine.current_url, sample_file_url)
        self.assertTrue(engine.can_go_forward())

        # 4. Go forward
        fwd_dom = engine.forward()
        self.assertIsNotNone(fwd_dom)
        self.assertEqual(engine.current_url, malformed_file_url)

        # 5. Reload
        reload_dom = engine.reload()
        self.assertIsNotNone(reload_dom)
        self.assertEqual(engine.current_status, 200)

    def test_fetch_url_local_file_not_found(self):
        status, body, headers = fetch_url("file:///nonexistent_path_12345.html")
        self.assertEqual(status, 404)
        self.assertIn("404 Not Found", body)

    def test_fetch_url_empty(self):
        status, body, headers = fetch_url("")
        self.assertEqual(status, 400)


if __name__ == "__main__":
    unittest.main()
