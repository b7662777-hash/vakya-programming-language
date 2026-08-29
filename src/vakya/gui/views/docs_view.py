"""Offline Documentation Reader View for Vākya Launcher."""

import os
import tkinter as tk
from tkinter import ttk
from typing import Callable, List

from vakya.gui.theme import Theme, Colors
from vakya.gui.state import AppState
from vakya.paths import get_docs_path


class DocsView(tk.Frame):
    """Offline reader for all Vākya language documentation and guides."""

    def __init__(self, parent: tk.Widget, theme: Theme, state: AppState, on_back: Callable[[], None]):
        super().__init__(parent, bg=theme.bg)
        self.theme = theme
        self.state = state
        self.on_back = on_back

        self.docs_dir = get_docs_path()
        self.doc_files: List[str] = []

        self._build_ui()
        self._load_docs_list()

    def _build_ui(self):
        # Toolbar
        toolbar = tk.Frame(self, bg=self.theme.surface, height=45)
        toolbar.pack(fill="x", side="top")

        back_btn = tk.Button(
            toolbar,
            text="← Dashboard",
            font=("Segoe UI", 9, "bold"),
            bg=self.theme.card,
            fg=self.theme.text,
            activebackground=self.theme.card_hover,
            relief="flat",
            padx=10,
            pady=4,
            command=self.on_back,
        )
        back_btn.pack(side="left", padx=(15, 10), pady=6)

        title = tk.Label(
            toolbar,
            text="📚  Vākya Offline Documentation & Language Guides",
            font=("Segoe UI", 11, "bold"),
            bg=self.theme.surface,
            fg=self.theme.accent,
        )
        title.pack(side="left", padx=5)

        # Main Split: Table of Contents (Left) & Reader (Right)
        paned = tk.PanedWindow(self, orient=tk.HORIZONTAL, bg=self.theme.border, bd=0, sashwidth=4)
        paned.pack(fill="both", expand=True, padx=10, pady=10)

        # Left Sidebar (Table of contents)
        toc_frame = tk.Frame(paned, bg=self.theme.card, width=220)
        paned.add(toc_frame, width=220)

        toc_title = tk.Label(
            toc_frame,
            text="TABLE OF CONTENTS",
            font=("Segoe UI", 8, "bold"),
            bg=self.theme.surface,
            fg=self.theme.text_dim,
            padx=10,
            pady=6,
        )
        toc_title.pack(fill="x")

        self.listbox = tk.Listbox(
            toc_frame,
            font=("Segoe UI", 9),
            bg=self.theme.card,
            fg=self.theme.text,
            selectbackground=self.theme.accent,
            selectforeground="#11111B" if self.theme.mode == "dark" else "#FFFFFF",
            relief="flat",
            bd=0,
            highlightthickness=0,
        )
        self.listbox.pack(fill="both", expand=True, padx=4, pady=4)
        self.listbox.bind("<<ListboxSelect>>", self._on_select_doc)

        # Right Reader
        reader_frame = tk.Frame(paned, bg=self.theme.code_bg)
        paned.add(reader_frame, width=680)

        self.reader = tk.Text(
            reader_frame,
            font=("Segoe UI", 10),
            bg=self.theme.code_bg,
            fg=self.theme.text,
            relief="flat",
            padx=20,
            pady=16,
            wrap="word",
            state="disabled",
        )
        self.reader.pack(fill="both", expand=True)

    def _load_docs_list(self):
        if not os.path.exists(self.docs_dir):
            return
        files = sorted([f for f in os.listdir(self.docs_dir) if f.endswith(".md") or f.endswith(".ebnf")])
        self.doc_files = [os.path.join(self.docs_dir, f) for f in files]

        self.listbox.delete(0, tk.END)
        for f in files:
            clean_name = f.replace(".md", "").replace(".ebnf", " (Grammar)").replace("-", " ").replace("_", " ").title()
            self.listbox.insert(tk.END, f"  {clean_name}")

        if self.doc_files:
            self.listbox.selection_set(0)
            self._display_doc(self.doc_files[0])

    def _on_select_doc(self, event):
        sel = self.listbox.curselection()
        if sel and sel[0] < len(self.doc_files):
            self._display_doc(self.doc_files[sel[0]])

    def _display_doc(self, file_path: str):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.reader.config(state="normal")
            self.reader.delete("1.0", tk.END)
            self.reader.insert("1.0", content)
            self.reader.config(state="disabled")
        except Exception as ex:
            self.reader.config(state="normal")
            self.reader.delete("1.0", tk.END)
            self.reader.insert("1.0", f"Error reading guide:\n{ex}")
            self.reader.config(state="disabled")
