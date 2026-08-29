"""Code Editor and File Execution View for Vākya Launcher."""

import io
import os
import sys
import time
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, Optional

from vakya.gui.theme import Theme, Colors
from vakya.gui.state import AppState
from vakya.lexer.lexer import Lexer
from vakya.parser.parser import Parser
from vakya.typechecker.checker import TypeChecker
from vakya.typechecker.borrow_checker import BorrowChecker
from vakya.bytecode.compiler import BytecodeCompiler
from vakya.vm.vm import VirtualMachine
from vakya.interpreter.interpreter import Interpreter
from vakya.errors import VakyaError


class EditorView(tk.Frame):
    """View for viewing, editing, typechecking, and running a .vakya file."""

    def __init__(
        self,
        parent: tk.Widget,
        theme: Theme,
        state: AppState,
        file_path: str,
        on_back: Callable[[], None],
    ):
        super().__init__(parent, bg=theme.bg)
        self.theme = theme
        self.state = state
        self.file_path = file_path
        self.on_back = on_back

        self._build_ui()
        self._load_file()

    def _build_ui(self):
        # 1. Top Toolbar
        toolbar = tk.Frame(self, bg=self.theme.surface, height=45)
        toolbar.pack(fill="x", side="top")

        # Back button
        back_btn = tk.Button(
            toolbar,
            text="← Dashboard",
            font=("Segoe UI", 9, "bold"),
            bg=self.theme.card,
            fg=self.theme.text,
            activebackground=self.theme.card_hover,
            activeforeground=self.theme.accent,
            relief="flat",
            padx=10,
            pady=4,
            command=self.on_back,
        )
        back_btn.pack(side="left", padx=(15, 10), pady=6)

        # File title
        self.title_lbl = tk.Label(
            toolbar,
            text=os.path.basename(self.file_path),
            font=("Segoe UI", 10, "bold"),
            bg=self.theme.surface,
            fg=self.theme.accent,
        )
        self.title_lbl.pack(side="left", padx=5)

        # Actions on right
        run_btn = tk.Button(
            toolbar,
            text="▷ Run Program",
            font=("Segoe UI", 9, "bold"),
            bg=self.theme.accent,
            fg="#11111B" if self.theme.mode == "dark" else "#FFFFFF",
            activebackground=self.theme.accent_hover,
            relief="flat",
            padx=12,
            pady=4,
            command=self.run_code,
        )
        run_btn.pack(side="right", padx=(5, 15), pady=6)

        check_btn = tk.Button(
            toolbar,
            text="🔍 Type Check",
            font=("Segoe UI", 9),
            bg=self.theme.card,
            fg=self.theme.text,
            activebackground=self.theme.card_hover,
            relief="flat",
            padx=10,
            pady=4,
            command=self.check_code,
        )
        check_btn.pack(side="right", padx=5, pady=6)

        fmt_btn = tk.Button(
            toolbar,
            text="🪄 Format",
            font=("Segoe UI", 9),
            bg=self.theme.card,
            fg=self.theme.text,
            activebackground=self.theme.card_hover,
            relief="flat",
            padx=10,
            pady=4,
            command=self.format_code,
        )
        fmt_btn.pack(side="right", padx=5, pady=6)

        disasm_btn = tk.Button(
            toolbar,
            text="🔬 Disasm",
            font=("Segoe UI", 9),
            bg=self.theme.card,
            fg=self.theme.text,
            activebackground=self.theme.card_hover,
            relief="flat",
            padx=10,
            pady=4,
            command=self.disasm_code,
        )
        disasm_btn.pack(side="right", padx=5, pady=6)

        save_btn = tk.Button(
            toolbar,
            text="💾 Save",
            font=("Segoe UI", 9),
            bg=self.theme.card,
            fg=self.theme.text,
            activebackground=self.theme.card_hover,
            relief="flat",
            padx=10,
            pady=4,
            command=self.save_file,
        )
        save_btn.pack(side="right", padx=5, pady=6)

        # 2. Main Content Split: Code Editor (top) & Console Output (bottom)
        paned = tk.PanedWindow(self, orient=tk.VERTICAL, bg=self.theme.border, bd=0, sashwidth=4)
        paned.pack(fill="both", expand=True, padx=10, pady=10)

        # Editor Frame
        editor_frame = tk.Frame(paned, bg=self.theme.code_bg)
        paned.add(editor_frame, height=360)

        editor_lbl = tk.Label(
            editor_frame,
            text="SOURCE CODE",
            font=("Segoe UI", 8, "bold"),
            bg=self.theme.card,
            fg=self.theme.text_dim,
            padx=8,
            pady=2,
        )
        editor_lbl.pack(anchor="w")

        self.editor = tk.Text(
            editor_frame,
            font=("Consolas", 11),
            bg=self.theme.code_bg,
            fg=self.theme.text,
            insertbackground=self.theme.accent,
            selectbackground=self.theme.border,
            relief="flat",
            undo=True,
            padx=10,
            pady=8,
        )
        self.editor.pack(fill="both", expand=True)

        # Output / Console Frame
        output_frame = tk.Frame(paned, bg=self.theme.code_bg)
        paned.add(output_frame, height=220)

        self.output_header = tk.Label(
            output_frame,
            text="OUTPUT & DIAGNOSTICS",
            font=("Segoe UI", 8, "bold"),
            bg=self.theme.card,
            fg=self.theme.text_dim,
            padx=8,
            pady=2,
        )
        self.output_header.pack(anchor="w")

        self.console = tk.Text(
            output_frame,
            font=("Consolas", 10),
            bg=self.theme.card,
            fg=self.theme.text,
            relief="flat",
            padx=10,
            pady=8,
            state="disabled",
        )
        self.console.pack(fill="both", expand=True)

    def _load_file(self):
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                self.editor.delete("1.0", tk.END)
                self.editor.insert("1.0", content)
            except Exception as ex:
                messagebox.showerror("Error Opening File", f"Could not read {self.file_path}:\n{ex}")

    def save_file(self):
        try:
            content = self.editor.get("1.0", tk.END)
            with open(self.file_path, "w", encoding="utf-8") as f:
                f.write(content)
            self._write_console("File saved successfully.\n", is_success=True)
        except Exception as ex:
            messagebox.showerror("Error Saving File", f"Could not save {self.file_path}:\n{ex}")

    def _write_console(self, text: str, is_success: bool = False, is_error: bool = False):
        self.console.config(state="normal")
        self.console.delete("1.0", tk.END)
        self.console.insert("1.0", text)
        self.console.config(state="disabled")

    def run_code(self):
        source = self.editor.get("1.0", tk.END)
        filename = os.path.basename(self.file_path)
        out_buf = io.StringIO()
        start_t = time.perf_counter()

        try:
            tokens = Lexer(source, filename=filename).tokenize()
            ast = Parser(tokens, source_code=source, filename=filename).parse()
            TypeChecker(source_code=source, filename=filename).check(ast)
            BorrowChecker(source_code=source, filename=filename).check(ast)

            if self.state.engine == "interpreter":
                interp = Interpreter(source_code=source, filename=filename, stdout=out_buf)
                interp.interpret(ast)
            else:
                compiler = BytecodeCompiler(filename=filename, source_code=source)
                chunk = compiler.compile(ast)
                vm = VirtualMachine(stdout=out_buf)
                vm.run(chunk)

            elapsed = (time.perf_counter() - start_t) * 1000
            output_text = out_buf.getvalue()
            engine_name = "Bytecode VM" if self.state.engine == "vm" else "AST Interpreter"
            summary = f"=== Execution Succeeded ({engine_name} • {elapsed:.2f}ms) ===\n{output_text}"
            self._write_console(summary, is_success=True)

        except VakyaError as ve:
            self._write_console(f"=== Execution Error ===\n\n{ve.format_diagnostic()}", is_error=True)
        except Exception as ex:
            self._write_console(f"=== Execution Error ===\n\nError: {ex}", is_error=True)

    def check_code(self):
        source = self.editor.get("1.0", tk.END)
        filename = os.path.basename(self.file_path)
        try:
            tokens = Lexer(source, filename=filename).tokenize()
            ast = Parser(tokens, source_code=source, filename=filename).parse()
            TypeChecker(source_code=source, filename=filename).check(ast)
            BorrowChecker(source_code=source, filename=filename).check(ast)
            self._write_console(f"✓ Check passed: No syntax, type, or memory borrow errors in '{filename}'.\n", is_success=True)
        except VakyaError as ve:
            self._write_console(f"=== Check Diagnostic ===\n\n{ve.format_diagnostic()}", is_error=True)
        except Exception as ex:
            self._write_console(f"=== Check Error ===\n\nError: {ex}", is_error=True)

    def format_code(self):
        from vakya.formatter.formatter import format_code
        source = self.editor.get("1.0", tk.END)
        try:
            formatted = format_code(source)
            self.editor.delete("1.0", tk.END)
            self.editor.insert("1.0", formatted)
            self._write_console("✓ Code formatted successfully.\n", is_success=True)
        except Exception as ex:
            self._write_console(f"=== Format Error ===\n\n{ex}", is_error=True)

    def disasm_code(self):
        source = self.editor.get("1.0", tk.END)
        filename = os.path.basename(self.file_path)
        try:
            tokens = Lexer(source, filename=filename).tokenize()
            ast = Parser(tokens, source_code=source, filename=filename).parse()
            compiler = BytecodeCompiler(filename=filename, source_code=source)
            chunk = compiler.compile(ast)
            self._write_console(f"=== Bytecode Disassembly for {filename} ===\n\n{chunk.disassemble()}", is_success=True)
        except VakyaError as ve:
            self._write_console(f"=== Disassembly Error ===\n\n{ve.format_diagnostic()}", is_error=True)
        except Exception as ex:
            self._write_console(f"=== Disassembly Error ===\n\nError: {ex}", is_error=True)
