"""Theme, color schemes, and High-DPI styling for Vākya GUI."""

import ctypes
import sys
import tkinter as tk
from tkinter import ttk


def enable_high_dpi():
    """Enable Per-Monitor High-DPI awareness on Windows."""
    if sys.platform == "win32":
        try:
            # SetProcessDpiAwarenessContext(-4) -> DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE_V2
            ctypes.windll.user32.SetProcessDpiAwarenessContext(-4)
        except Exception:
            try:
                # Fallback: SetProcessDpiAwareness(1)
                ctypes.windll.shcore.SetProcessDpiAwareness(1)
            except Exception:
                pass


class Colors:
    """Modern dark and light color palettes."""
    # Dark Theme (Default)
    DARK_BG = "#11111B"           # Crust / Deep Dark
    DARK_SURFACE = "#181825"      # Mantle
    DARK_CARD = "#1E1E2E"         # Base
    DARK_CARD_HOVER = "#28283D"   # Lighter Base
    DARK_BORDER = "#313244"       # Surface0
    DARK_TEXT = "#CDD6F4"         # Text
    DARK_TEXT_MUTED = "#A6ADC8"   # Subtext0
    DARK_TEXT_DIM = "#6C7086"     # Overlay0
    DARK_ACCENT = "#F59E0B"       # Amber Gold
    DARK_ACCENT_HOVER = "#D97706" # Darker Amber
    DARK_PRIMARY = "#89B4FA"      # Blue
    DARK_SUCCESS = "#A6E3A1"      # Green
    DARK_WARNING = "#FAB387"      # Peach
    DARK_ERROR = "#F38BA8"        # Red
    DARK_CODE_BG = "#14141E"      # Code background

    # Light Theme
    LIGHT_BG = "#F8FAFC"
    LIGHT_SURFACE = "#FFFFFF"
    LIGHT_CARD = "#F1F5F9"
    LIGHT_CARD_HOVER = "#E2E8F0"
    LIGHT_BORDER = "#CBD5E1"
    LIGHT_TEXT = "#0F172A"
    LIGHT_TEXT_MUTED = "#475569"
    LIGHT_TEXT_DIM = "#94A3B8"
    LIGHT_ACCENT = "#D97706"
    LIGHT_ACCENT_HOVER = "#B45309"
    LIGHT_PRIMARY = "#2563EB"
    LIGHT_SUCCESS = "#16A34A"
    LIGHT_WARNING = "#EA580C"
    LIGHT_ERROR = "#DC2626"
    LIGHT_CODE_BG = "#F8FAFC"


class Theme:
    """Manages active theme palette and widget configurations."""
    def __init__(self, mode: str = "dark"):
        self.mode = mode.lower()
        self._apply_palette()

    def _apply_palette(self):
        if self.mode == "light":
            self.bg = Colors.LIGHT_BG
            self.surface = Colors.LIGHT_SURFACE
            self.card = Colors.LIGHT_CARD
            self.card_hover = Colors.LIGHT_CARD_HOVER
            self.border = Colors.LIGHT_BORDER
            self.text = Colors.LIGHT_TEXT
            self.text_muted = Colors.LIGHT_TEXT_MUTED
            self.text_dim = Colors.LIGHT_TEXT_DIM
            self.accent = Colors.LIGHT_ACCENT
            self.accent_hover = Colors.LIGHT_ACCENT_HOVER
            self.primary = Colors.LIGHT_PRIMARY
            self.success = Colors.LIGHT_SUCCESS
            self.warning = Colors.LIGHT_WARNING
            self.error = Colors.LIGHT_ERROR
            self.code_bg = Colors.LIGHT_CODE_BG
        else:
            self.bg = Colors.DARK_BG
            self.surface = Colors.DARK_SURFACE
            self.card = Colors.DARK_CARD
            self.card_hover = Colors.DARK_CARD_HOVER
            self.border = Colors.DARK_BORDER
            self.text = Colors.DARK_TEXT
            self.text_muted = Colors.DARK_TEXT_MUTED
            self.text_dim = Colors.DARK_TEXT_DIM
            self.accent = Colors.DARK_ACCENT
            self.accent_hover = Colors.DARK_ACCENT_HOVER
            self.primary = Colors.DARK_PRIMARY
            self.success = Colors.DARK_SUCCESS
            self.warning = Colors.DARK_WARNING
            self.error = Colors.DARK_ERROR
            self.code_bg = Colors.DARK_CODE_BG

    def apply_to_ttk(self, style: ttk.Style):
        """Apply modern flat styles to ttk widgets."""
        style.theme_use("clam")

        # Global fonts
        font_family = "Segoe UI" if sys.platform == "win32" else "Helvetica"
        code_family = "Consolas" if sys.platform == "win32" else "Courier"

        style.configure(".",
            background=self.bg,
            foreground=self.text,
            font=(font_family, 10),
        )

        # Frames
        style.configure("TFrame", background=self.bg)
        style.configure("Surface.TFrame", background=self.surface)
        style.configure("Card.TFrame", background=self.card, relief="flat")

        # Labels
        style.configure("TLabel", background=self.bg, foreground=self.text)
        style.configure("Muted.TLabel", foreground=self.text_muted)
        style.configure("Dim.TLabel", foreground=self.text_dim)
        style.configure("Card.TLabel", background=self.card, foreground=self.text)
        style.configure("CardMuted.TLabel", background=self.card, foreground=self.text_muted)
        style.configure("Title.TLabel", font=(font_family, 18, "bold"), foreground=self.accent)
        style.configure("Subtitle.TLabel", font=(font_family, 11), foreground=self.text_muted)
        style.configure("Section.TLabel", font=(font_family, 12, "bold"), foreground=self.text)

        # Buttons
        style.configure("TButton",
            background=self.card,
            foreground=self.text,
            borderwidth=1,
            relief="flat",
            padding=(12, 6),
            font=(font_family, 10),
        )
        style.map("TButton",
            background=[("active", self.card_hover), ("pressed", self.border)],
            foreground=[("active", self.accent)],
        )

        # Accent Action Button
        style.configure("Accent.TButton",
            background=self.accent,
            foreground="#11111B" if self.mode == "dark" else "#FFFFFF",
            font=(font_family, 10, "bold"),
            padding=(14, 7),
            borderwidth=0,
        )
        style.map("Accent.TButton",
            background=[("active", self.accent_hover), ("pressed", self.accent_hover)],
        )

        # Primary Button
        style.configure("Primary.TButton",
            background=self.primary,
            foreground="#11111B" if self.mode == "dark" else "#FFFFFF",
            font=(font_family, 10, "bold"),
            padding=(12, 6),
        )

        # Progressbar
        style.configure("Horizontal.TProgressbar",
            troughcolor=self.card,
            background=self.accent,
            borderwidth=0,
        )

        # Notebook (Tabs)
        style.configure("TNotebook", background=self.bg, borderwidth=0)
        style.configure("TNotebook.Tab",
            background=self.surface,
            foreground=self.text_muted,
            padding=(14, 8),
            font=(font_family, 10),
            borderwidth=0,
        )
        style.map("TNotebook.Tab",
            background=[("selected", self.card), ("active", self.card_hover)],
            foreground=[("selected", self.accent), ("active", self.text)],
        )
