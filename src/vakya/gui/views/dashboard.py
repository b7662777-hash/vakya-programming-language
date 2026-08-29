"""Main Dashboard and Action Hub for Vākya Launcher."""

import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from typing import Callable, Optional

from vakya.gui.theme import Theme, Colors
from vakya.gui.state import AppState


class DashboardView(tk.Frame):
    """Primary hub for Vākya Launcher with quick actions, recent files, and engine info."""

    def __init__(
        self,
        parent: tk.Widget,
        theme: Theme,
        state: AppState,
        on_open_file: Callable[[str], None],
        on_new_project: Callable[[], None],
        on_open_repl: Callable[[], None],
        on_open_examples: Callable[[], None],
        on_open_docs: Callable[[], None],
        on_open_doctor: Callable[[], None],
        on_open_settings: Callable[[], None],
    ):
        super().__init__(parent, bg=theme.bg)
        self.theme = theme
        self.state = state
        self.on_open_file = on_open_file
        self.on_new_project = on_new_project
        self.on_open_repl = on_open_repl
        self.on_open_examples = on_open_examples
        self.on_open_docs = on_open_docs
        self.on_open_doctor = on_open_doctor
        self.on_open_settings = on_open_settings

        self._build_ui()

    def _build_ui(self):
        # Top Header Section
        header = tk.Frame(self, bg=self.theme.bg)
        header.pack(fill="x", padx=40, pady=(30, 20))

        title_box = tk.Frame(header, bg=self.theme.bg)
        title_box.pack(side="left")

        title = tk.Label(
            title_box,
            text="VĀKYA",
            font=("Segoe UI", 24, "bold"),
            bg=self.theme.bg,
            fg=self.theme.accent,
        )
        title.pack(anchor="w")

        subtitle = tk.Label(
            title_box,
            text="Romanized Sanskrit Programming Language  •  v0.1.0",
            font=("Segoe UI", 10),
            bg=self.theme.bg,
            fg=self.theme.text_muted,
        )
        subtitle.pack(anchor="w", pady=(2, 0))

        # Status badge on top right
        engine_label = "Bytecode VM" if self.state.engine == "vm" else "AST Interpreter"
        badge_frame = tk.Frame(header, bg=self.theme.card, bd=1, relief="solid")
        badge_frame.pack(side="right", pady=5)
        badge = tk.Label(
            badge_frame,
            text=f" Engine: {engine_label}  |  Ready ",
            font=("Segoe UI", 9, "bold"),
            bg=self.theme.card,
            fg=self.theme.success,
            padx=8,
            pady=4,
        )
        badge.pack()

        # Scrollable container for main body
        container = tk.Frame(self, bg=self.theme.bg)
        container.pack(fill="both", expand=True, padx=40, pady=(0, 20))

        # 1. Primary Action Hero Card (Open File / Dropzone)
        hero_card = tk.Frame(container, bg=self.theme.card, cursor="hand2")
        hero_card.pack(fill="x", pady=(0, 15))
        hero_card.bind("<Button-1>", lambda e: self._browse_file())

        hero_inner = tk.Frame(hero_card, bg=self.theme.card)
        hero_inner.pack(fill="x", padx=25, pady=20)
        hero_inner.bind("<Button-1>", lambda e: self._browse_file())

        hero_title = tk.Label(
            hero_inner,
            text="📁  Open Vākya File",
            font=("Segoe UI", 14, "bold"),
            bg=self.theme.card,
            fg=self.theme.text,
        )
        hero_title.pack(anchor="w")
        hero_title.bind("<Button-1>", lambda e: self._browse_file())

        hero_desc = tk.Label(
            hero_inner,
            text="Select or drop a .vakya source file to run, check syntax, or format",
            font=("Segoe UI", 9),
            bg=self.theme.card,
            fg=self.theme.text_muted,
        )
        hero_desc.pack(anchor="w", pady=(4, 0))
        hero_desc.bind("<Button-1>", lambda e: self._browse_file())

        # 2. Grid Cards Section
        grid_frame = tk.Frame(container, bg=self.theme.bg)
        grid_frame.pack(fill="x", pady=(0, 15))
        grid_frame.columnconfigure(0, weight=1)
        grid_frame.columnconfigure(1, weight=1)

        cards = [
            ("🚀  New Project", "Scaffold a new Vākya project directory", self.on_new_project, 0, 0),
            ("⚡  Vākya REPL", "Launch interactive evaluation console", self.on_open_repl, 0, 1),
            ("💡  Canonical Examples", "Browse & run official language examples", self.on_open_examples, 1, 0),
            ("📚  Documentation", "Read offline guides & language specifications", self.on_open_docs, 1, 1),
            ("🩺  System Doctor", "Run runtime & diagnostic health checks", self.on_open_doctor, 2, 0),
            ("⚙️  Settings", "Configure engine and environment preferences", self.on_open_settings, 2, 1),
        ]

        for title_text, desc_text, callback, row, col in cards:
            c = tk.Frame(grid_frame, bg=self.theme.card, cursor="hand2")
            c.grid(row=row, column=col, sticky="nsew", padx=6, pady=6)
            c.bind("<Button-1>", lambda e, cb=callback: cb())

            inner = tk.Frame(c, bg=self.theme.card)
            inner.pack(fill="both", expand=True, padx=16, pady=14)
            inner.bind("<Button-1>", lambda e, cb=callback: cb())

            t_lbl = tk.Label(
                inner,
                text=title_text,
                font=("Segoe UI", 11, "bold"),
                bg=self.theme.card,
                fg=self.theme.text,
            )
            t_lbl.pack(anchor="w")
            t_lbl.bind("<Button-1>", lambda e, cb=callback: cb())

            d_lbl = tk.Label(
                inner,
                text=desc_text,
                font=("Segoe UI", 9),
                bg=self.theme.card,
                fg=self.theme.text_muted,
            )
            d_lbl.pack(anchor="w", pady=(3, 0))
            d_lbl.bind("<Button-1>", lambda e, cb=callback: cb())

        # 3. Recent Files Section
        if self.state.recent_files:
            recent_frame = tk.Frame(container, bg=self.theme.bg)
            recent_frame.pack(fill="x", pady=(10, 0))

            recent_lbl = tk.Label(
                recent_frame,
                text="Recent Files",
                font=("Segoe UI", 11, "bold"),
                bg=self.theme.bg,
                fg=self.theme.text,
            )
            recent_lbl.pack(anchor="w", pady=(0, 6))

            for fpath in self.state.recent_files[:4]:
                rf = tk.Frame(recent_frame, bg=self.theme.card, cursor="hand2")
                rf.pack(fill="x", pady=2)
                rf.bind("<Button-1>", lambda e, p=fpath: self.on_open_file(p))

                rf_name = tk.Label(
                    rf,
                    text=f"📄  {os.path.basename(fpath)}",
                    font=("Segoe UI", 9, "bold"),
                    bg=self.theme.card,
                    fg=self.theme.text,
                )
                rf_name.pack(side="left", padx=12, pady=6)
                rf_name.bind("<Button-1>", lambda e, p=fpath: self.on_open_file(p))

                rf_path = tk.Label(
                    rf,
                    text=fpath,
                    font=("Segoe UI", 8),
                    bg=self.theme.card,
                    fg=self.theme.text_dim,
                )
                rf_path.pack(side="right", padx=12, pady=6)
                rf_path.bind("<Button-1>", lambda e, p=fpath: self.on_open_file(p))

    def _browse_file(self):
        fpath = filedialog.askopenfilename(
            title="Open Vākya Source File",
            filetypes=[("Vākya Files", "*.vakya"), ("All Files", "*.*")],
            initialdir=self.state.default_workspace,
        )
        if fpath:
            self.state.add_recent_file(fpath)
            self.on_open_file(fpath)
