"""Vākya installation and resource path resolution."""

import os
import sys
from typing import Optional, List


def get_vakya_home() -> str:
    """Get the root directory of the Vākya installation or repository."""
    # 1. Explicit VAKYA_HOME environment variable
    env_home = os.environ.get("VAKYA_HOME")
    if env_home and os.path.exists(env_home):
        return os.path.abspath(env_home)

    # 2. PyInstaller bundled temporary directory
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return os.path.abspath(sys._MEIPASS)

    # 3. Installed binary location (e.g. <InstallDir>/bin/vakya.exe -> <InstallDir>)
    if getattr(sys, "frozen", False):
        exe_dir = os.path.dirname(os.path.abspath(sys.executable))
        if os.path.basename(exe_dir).lower() == "bin":
            parent = os.path.dirname(exe_dir)
            if os.path.exists(os.path.join(parent, "std")):
                return parent
        if os.path.exists(os.path.join(exe_dir, "std")):
            return exe_dir

    # 4. Development mode: repository root
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    return repo_root


def get_stdlib_path() -> str:
    """Locate the Vākya standard library directory."""
    home = get_vakya_home()
    candidate = os.path.join(home, "std")
    if os.path.exists(candidate):
        return candidate

    # Check next to executable
    if getattr(sys, "frozen", False):
        exe_dir = os.path.dirname(os.path.abspath(sys.executable))
        candidate = os.path.join(exe_dir, "std")
        if os.path.exists(candidate):
            return candidate

    # Current working directory fallback
    cwd_std = os.path.abspath("std")
    if os.path.exists(cwd_std):
        return cwd_std

    return candidate


def get_runtime_path() -> str:
    """Locate the Vākya native runtime directory."""
    home = get_vakya_home()
    candidate = os.path.join(home, "runtime")
    if os.path.exists(candidate):
        return candidate

    # Check next to executable
    if getattr(sys, "frozen", False):
        exe_dir = os.path.dirname(os.path.abspath(sys.executable))
        candidate = os.path.join(exe_dir, "runtime")
        if os.path.exists(candidate):
            return candidate

    return candidate


def get_resources_path() -> str:
    """Locate the Vākya resources directory (icons, assets)."""
    home = get_vakya_home()
    candidate = os.path.join(home, "resources")
    if os.path.exists(candidate):
        return candidate
    if getattr(sys, "frozen", False):
        exe_dir = os.path.dirname(os.path.abspath(sys.executable))
        candidate = os.path.join(exe_dir, "resources")
        if os.path.exists(candidate):
            return candidate
    return candidate


def get_icon_path() -> Optional[str]:
    """Locate the Vākya .ico or .png icon."""
    res_dir = get_resources_path()
    ico = os.path.join(res_dir, "vakya.ico")
    if os.path.exists(ico):
        return ico
    png = os.path.join(res_dir, "vakya.png")
    if os.path.exists(png):
        return png
    return None


def get_docs_path() -> str:
    """Locate the Vākya documentation directory."""
    home = get_vakya_home()
    candidate = os.path.join(home, "docs")
    if os.path.exists(candidate):
        return candidate
    if getattr(sys, "frozen", False):
        exe_dir = os.path.dirname(os.path.abspath(sys.executable))
        candidate = os.path.join(exe_dir, "docs")
        if os.path.exists(candidate):
            return candidate
    return candidate


def get_examples_path() -> str:
    """Locate the Vākya canonical examples directory."""
    home = get_vakya_home()
    candidate = os.path.join(home, "examples")
    if os.path.exists(candidate):
        return candidate
    if getattr(sys, "frozen", False):
        exe_dir = os.path.dirname(os.path.abspath(sys.executable))
        candidate = os.path.join(exe_dir, "examples")
        if os.path.exists(candidate):
            return candidate
    return candidate


def get_default_search_paths() -> List[str]:
    """Return all default search paths for module resolution."""
    paths = []
    std = get_stdlib_path()
    if os.path.exists(std) and std not in paths:
        paths.append(std)

    home = get_vakya_home()
    if os.path.exists(home) and home not in paths:
        paths.append(home)

    return paths
