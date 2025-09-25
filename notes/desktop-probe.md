# Desktop Automation Probe Notes

These notes capture the investigative work carried out while experimenting
with Windows automation libraries. They follow the Phase 1 guidance from the
Bytebot MVP plan and will be expanded as new findings emerge.

## Environment Checklist
- Windows 11 Pro (build 22631)
- Python 3.11 installed via `pyenv`
- Created virtual environment with `pywinauto`, `uiautomation`, `pyautogui`, and
  `Pillow`
- Enabled "Enable access to the clipboard" in Windows privacy settings to
  prevent focus issues during automation

## Initial Findings
1. **Window Focus Latency** — `pywinauto` requires a short wait after launching
   Notepad before the edit control accepts keystrokes. A `wait("visible")`
   check plus a 0.2 second sleep eliminated early keystroke loss.
2. **DPI Scaling** — Machines using display scaling above 125% caused inaccurate
   click coordinates when using `pyautogui`. Switching to UI Automation APIs or
   temporarily disabling scaling resolved the issue.
3. **File Dialog Paths** — Saving to the Desktop works reliably when providing
   an absolute path instead of relying on the default directory in the dialog.
4. **Stability Strategy** — Adding retries for locating controls (max three
   attempts) dramatically reduced flaky runs.

## Open Questions
- Evaluate whether `uiautomation` offers more robust control discovery than
  `pywinauto` for complex applications.
- Investigate using image-based fallbacks (OpenCV template matching) for UI
  elements without accessible names.
- Explore running the automation inside a dedicated Windows VM snapshot for
  deterministic testing.

## Next Steps
- Script the above experiments into reproducible Python functions to collect
  timing metrics.
- Start capturing before/after screenshots to better diagnose focus problems.
- Integrate these learnings into the structured executor implementation.
