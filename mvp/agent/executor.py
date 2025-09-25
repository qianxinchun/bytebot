"""Execution interfaces for Bytebot MVP actions."""
from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Dict, Optional, Protocol

from .actions import Action, ActionStatus


@dataclass(slots=True)
class ActionResult:
    """Outcome of running a single action."""

    status: ActionStatus
    detail: Optional[str] = None
    screenshot_path: Optional[Path] = None
    metadata: Dict[str, Any] | None = None


class ActionExecutor(Protocol):
    """Minimal protocol any executor must follow."""

    def execute(self, action: Action, context: "TaskContext") -> ActionResult:  # pragma: no cover - structural typing
        ...


@dataclass(slots=True)
class TaskContext:
    """Shared context passed to each action during execution."""

    task_id: str
    workdir: Path
    log: logging.Logger
    metadata: Dict[str, Any]


class LoggingActionExecutor(ActionExecutor, ABC):
    """Base class that provides logging helpers for concrete executors."""

    def __init__(self, screenshot_dir: Path | None = None) -> None:
        self.screenshot_dir = screenshot_dir
        if self.screenshot_dir:
            self.screenshot_dir.mkdir(parents=True, exist_ok=True)

    @abstractmethod
    def perform(self, action: Action, context: TaskContext) -> ActionResult:
        """Execute a single action."""

    def execute(self, action: Action, context: TaskContext) -> ActionResult:
        context.log.info("Starting action %s", action.name, extra={"params": action.params})
        started = datetime.now(UTC)
        try:
            result = self.perform(action, context)
        except Exception as exc:  # pragma: no cover - defensive branch
            context.log.exception("Action %s failed", action.name)
            result = ActionResult(status=ActionStatus.FAILED, detail=str(exc))
        duration_ms = (datetime.now(UTC) - started).total_seconds() * 1000
        context.log.info(
            "Finished action %s", action.name, extra={"status": result.status.value, "duration_ms": duration_ms}
        )
        return result


__all__ = ["ActionExecutor", "ActionResult", "TaskContext", "LoggingActionExecutor"]
