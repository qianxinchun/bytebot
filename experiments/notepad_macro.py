"""Manual Notepad automation probe script.

This script is not executed within the CI environment. It documents the
discovery work recommended in Phase 1 of the MVP plan. When run on Windows,
it demonstrates how to launch Notepad, type text, and save a file using
`pywinauto` primitives. The goal is to keep knowledge in code, even if it
remains exploratory.
"""
from __future__ import annotations

import time
from pathlib import Path

try:  # pragma: no cover - optional dependency on Windows
    from pywinauto.application import Application
except Exception:  # pragma: no cover - we only need this on Windows
    Application = None  # type: ignore[assignment]


def run_notepad_macro(text: str, *, save_path: Path) -> None:
    if Application is None:
        raise RuntimeError("pywinauto is required to run this script on Windows")

    app = Application().start("notepad.exe")
    window = app.UntitledNotepad
    window.wait("visible", timeout=10)
    edit = window.Edit
    edit.type_keys(text, with_spaces=True, pause=0.05)

    window.menu_select("File->Save As")
    save_dialog = app.window(title_re="Save As")
    save_dialog.wait("visible", timeout=10)
    save_dialog["File name:"].type_keys(str(save_path), with_spaces=True)
    save_dialog.Save.click()
    time.sleep(0.5)


if __name__ == "__main__":  # pragma: no cover - manual experiment
    destination = Path.home() / "Desktop" / "bytebot-macro.txt"
    run_notepad_macro("Hello from the Bytebot MVP probe!", save_path=destination)
