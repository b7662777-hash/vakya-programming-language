"""Settings view for configuring Vākya runtime and GUI preferences."""

import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from typing import Callable

from vakya.gui.theme import Theme, Colors
from vakya.gui.state import AppState


class SettingsView(tk.Frame):
    """Settings configuration view."""

    def __init__(
        self,
        parent: tk.Widget,
        theme: Theme,
        state: AppState,
        on_back: Callable[[], None],
        on_settings_saved: Callable[[], None],
    ):
        super().__init__(parent, bg=theme.bg)
        self.theme = theme
        self.state = state
        self.on_back = on_back
        self.on_settings_saved = on_settings_saved

        self._build_ui()

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
            text="⚙️  Vākya Launcher Settings",
            font=("Segoe UI", 11, "bold"),
            bg=self.theme.surface,
            fg=self.theme.accent,
        )
        title.pack(side="left", padx=5)

        # Form content
        container = tk.Frame(self, bg=self.theme.bg)
        container.pack(fill="both", expand=True, padx=40, pady=30)

        # 1. Execution Engine
        sec1 = tk.Label(
            container,
            text="Execution Runtime Engine",
            font=("Segoe UI", 11, "bold"),
            bg=self.theme.bg,
            fg=self.theme.text,
        )
        sec1.pack(anchor="w", pady=(0, 8))

        self.engine_var = tk.StringVar(value=self.state.engine)

        r1 = tk.Radiobutton(
            container,
            text="Bytecode Virtual Machine (Recommended • High Performance)",
            variable=self.engine_var,
            value="vm",
            font=("Segoe UI", 9),
            bg=self.theme.bg,
            fg=self.theme.text,
            selectcolor=self.theme.card,
            activebackground=self.theme.bg,
            activeforeground=self.theme.accent,
        )
        r1.pack(anchor="w", padx=10, pady=2)

        r2 = tk.Radiobutton(
            container,
            text="Tree-Walking AST Interpreter (Reference Specification Engine)",
            variable=self.engine_var,
            value="interpreter",
            font=("Segoe UI", 9),
            bg=self.theme.bg,
            fg=self.theme.text,
            selectcolor=self.theme.card,
            activebackground=self.theme.bg,
            activeforeground=self.theme.accent,
        )
        r2.pack(anchor="w", padx=10, pady=2)

        # 2. Theme Mode
        sec2 = tk.Label(
            container,
            text="Visual Appearance",
            font=("Segoe UI", 11, "bold"),
            bg=self.theme.bg,
            fg=self.theme.text,
        )
        sec2.pack(anchor="w", pady=(20, 8))

        self.theme_var = tk.StringVar(value=self.state.theme_mode)

        t1 = tk.Radiobutton(
            container,
            text="Dark Theme (Obsidian & Amber Gold)",
            variable=self.theme_var,
            value="dark",
            font=("Segoe UI", 9),
            bg=self.theme.bg,
            fg=self.theme.text,
            selectcolor=self.theme.card,
            activebackground=self.theme.bg,
            activeforeground=self.theme.accent,
        )
        t1.pack(anchor="w", padx=10, pady=2)

        t2 = tk.Radiobutton(
            container,
            text="Light Theme",
            variable=self.theme_var,
            value="light",
            font=("Segoe UI", 9),
            bg=self.theme.bg,
            fg=self.theme.text,
            selectcolor=self.theme.card,
            activebackground=self.theme.bg,
            activeforeground=self.theme.accent,
        )
        t2.pack(anchor="w", padx=10, pady=2)

        # 3. Default Workspace
        sec3 = tk.Label(
            container,
            text="Default Workspace Location",
            font=("Segoe UI", 11, "bold"),
            bg=self.theme.bg,
            fg=self.theme.text,
        )
        sec3.pack(anchor="w", pady=(20, 8))

        ws_frame = tk.Frame(container, bg=self.theme.bg)
        ws_frame.pack(fill="x", padx=10, pady=2)

        self.ws_entry = tk.Entry(
            ws_frame,
            font=("Segoe UI", 9),
            bg=self.theme.card,
            fg=self.theme.text,
            insertbackground=self.theme.accent,
            relief="flat",
        )
        self.ws_entry.pack(side="left", fill="x", expand=True, padx=(0, 8), pady=4)
        self.ws_entry.insert(0, self.state.default_workspace)

        ws_btn = tk.Button(
            ws_frame,
            text="Browse...",
            font=("Segoe UI", 8),
            bg=self.theme.card,
            fg=self.theme.text,
            activebackground=self.theme.card_hover,
            relief="flat",
            padx=8,
            command=self._browse_ws,
        )
        ws_btn.pack(side="right")

        # Save Button
        save_btn = tk.Button(
            container,
            text="Save Preferences",
            font=("Segoe UI", 10, "bold"),
            bg=self.theme.accent,
            fg="#11111B" if self.theme.mode == "dark" else "#FFFFFF",
            activebackground=self.theme.accent_hover,
            relief="flat",
            padx=18,
            pady=6,
            command=self._save,
        )
        save_btn.pack(anchor="w", padx=10, pady=(30, 0))

    def _browse_ws(self):
        d = filedialog.askdirectory(initialdir=self.ws_entry.get())
        if d:
            self.ws_entry.delete(0, tk.END)
            self.ws_entry.insert(0, d)

    def _save(self):
        self.state.engine = self.engine_var.get()
        self.state.theme_mode = self.theme_var.get()
        self.state.default_workspace = self.ws_entry.get().strip()
        self.state.save()
        messagebox.showinfo("Settings Saved", "Preferences saved successfully.")
        self.on_settings_saved()
