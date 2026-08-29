"""Application state and persistent settings manager for Vākya GUI."""

import json
import os
from typing import Any, Dict, List, Optional


class AppState:
    """Manages user preferences, recent files, and engine settings."""

    SETTINGS_DIR = os.path.join(os.environ.get("APPDATA", os.path.expanduser("~")), "Vakya")
    SETTINGS_FILE = os.path.join(SETTINGS_DIR, "gui_settings.json")

    def __init__(self):
        self.engine: str = "vm"          # "vm" or "interpreter"
        self.theme_mode: str = "dark"     # "dark" or "light"
        self.default_workspace: str = os.path.expanduser("~")
        self.max_recursion: int = 200
        self.recent_files: List[str] = []
        self.load()

    def load(self):
        """Load settings from JSON file if available."""
        if not os.path.exists(self.SETTINGS_FILE):
            return
        try:
            with open(self.SETTINGS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.engine = data.get("engine", "vm")
            self.theme_mode = data.get("theme_mode", "dark")
            self.default_workspace = data.get("default_workspace", os.path.expanduser("~"))
            self.max_recursion = data.get("max_recursion", 200)
            self.recent_files = [f for f in data.get("recent_files", []) if os.path.exists(f)]
        except Exception:
            pass

    def save(self):
        """Persist settings to JSON file."""
        try:
            os.makedirs(self.SETTINGS_DIR, exist_ok=True)
            data = {
                "engine": self.engine,
                "theme_mode": self.theme_mode,
                "default_workspace": self.default_workspace,
                "max_recursion": self.max_recursion,
                "recent_files": self.recent_files[:10],
            }
            with open(self.SETTINGS_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
        except Exception:
            pass

    def add_recent_file(self, file_path: str):
        """Add a file path to the recent files list."""
        abs_path = os.path.abspath(file_path)
        if abs_path in self.recent_files:
            self.recent_files.remove(abs_path)
        self.recent_files.insert(0, abs_path)
        self.recent_files = self.recent_files[:10]
        self.save()
