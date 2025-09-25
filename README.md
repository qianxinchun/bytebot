# Bytebot MVP for Agent Mastery

This repository now contains the scaffolding for a Windows-focused Bytebot
minimum viable product that will be grown iteratively using Karpathy's
Philosophy of Mastery. The codebase is intentionally small and transparent so
that every concept—from planning rules to execution pipelines—can be understood
and modified without black boxes.

## Repository Layout

- `Bytebot-MVP.md` – expansive learning and delivery roadmap.
- `experiments/` – scratch scripts for probing Windows automation libraries.
- `mvp/` – production-bound Python package housing the agent pipeline.
  - `agent/` – declarative action schema and executor interfaces.
  - `planner/` – seed rule-based planner translating language into actions.
  - `runtime/` – task runner, logging, and reporting utilities.
- `notes/` – research journals and reflective documentation.
- `templates/` – YAML action plans for canonical tasks.
- `tests/` – pytest suite covering serialization, planning, and execution flow.

## Quick Start (Development Environment)

1. Create and activate a Python 3.11 virtual environment.
2. Install dependencies: `pip install -r requirements-dev.txt` *(or
   `pip install -e .[dev]` once packaging metadata is finalised).* The core code
   only depends on the standard library and `pyyaml`; Windows automation tools
   are optional and used in the exploratory scripts.
3. Run tests: `pytest` – ensures action schemas, planner rules, and the task
   runner behave as expected.

## Automation Lessons Learned

Notes captured in `notes/desktop-probe.md` document the first wave of Windows
automation experiments. Highlights so far:

- Launch-to-focus latency must be absorbed with explicit waits before typing.
- DPI scaling alters coordinate-based interactions; UI Automation APIs provide
  more resilient control targeting than raw screen coordinates.
- File dialogs prefer absolute paths for deterministic saves to Desktop.
- Simple retry wrappers around control discovery significantly increase
  stability during flaky VM sessions.

These insights will continue to feed the executor implementation and future
benchmark design.

## Next Milestones

- Expand the executor with concrete Windows integrations using `pywinauto`.
- Flesh out planner templates for additional office tooling tasks.
- Introduce CLI tooling for submitting tasks and inspecting reports.
- Record demos and capture artefacts for each iteration to embody the
  "executable explanations" principle.
