"""Extremely small rule-based planner for the MVP."""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import List, Optional

from ..agent.actions import Action, ActionSequence


@dataclass(slots=True)
class PlannerConfig:
    default_application: str = "notepad"
    default_save_directory: str = "Desktop"


class RuleBasedPlanner:
    """Map simple natural language tasks to pre-defined action templates."""

    def __init__(self, config: PlannerConfig | None = None) -> None:
        self.config = config or PlannerConfig()

    def plan(self, instruction: str, *, task_name: Optional[str] = None) -> ActionSequence:
        normalized = instruction.lower()
        actions: List[Action] = []

        if "open" in normalized and "notepad" in normalized:
            actions.append(
                Action(
                    name="launch_app",
                    params={"application": "notepad"},
                    description="Launch Windows Notepad",
                    expected_outcome="Notepad window is focused",
                )
            )
        if any(keyword in normalized for keyword in ("type", "write", "input")):
            text = self._extract_quoted_text(instruction) or "Hello, world!"
            actions.append(
                Action(
                    name="type_text",
                    params={"text": text},
                    description="Type the provided text into the focused window",
                )
            )
        if "save" in normalized:
            filename = self._extract_filename(normalized) or "bytebot-notes.txt"
            actions.append(
                Action(
                    name="save_file",
                    params={"directory": self.config.default_save_directory, "filename": filename},
                    description="Save the current document",
                )
            )
        if not actions:
            raise ValueError(f"Could not derive plan from instruction: {instruction}")
        actions.append(
            Action(
                name="capture_screenshot",
                params={},
                description="Capture final screenshot for auditing",
            )
        )
        return ActionSequence(actions=actions, name=task_name or "rule-plan")

    @staticmethod
    def _extract_quoted_text(text: str) -> Optional[str]:
        match = re.search(r"['\"]([^'\"]+)['\"]", text)
        return match.group(1) if match else None

    @staticmethod
    def _extract_filename(text: str) -> Optional[str]:
        match = re.search(r"save (?:to )?(?:the )?(\w+\.\w+)", text)
        return match.group(1) if match else None


__all__ = ["RuleBasedPlanner", "PlannerConfig"]
