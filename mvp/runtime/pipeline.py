"""Sequential task runner for the Bytebot MVP."""
from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Dict, List, Optional

from ..agent.actions import Action, ActionSequence, ActionStatus
from ..agent.executor import ActionExecutor, ActionResult, TaskContext


def configure_task_logger(task_id: str, log_dir: Path) -> logging.Logger:
    log_dir.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger(f"bytebot.mvp.task.{task_id}")
    logger.setLevel(logging.INFO)
    # Avoid duplicate handlers when running tests repeatedly.
    if not logger.handlers:
        file_handler = logging.FileHandler(log_dir / f"{task_id}.log", encoding="utf-8")
        formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    return logger


@dataclass(slots=True)
class ExecutionStep:
    action: Action
    status: ActionStatus
    started_at: datetime
    finished_at: datetime
    detail: Optional[str] = None
    screenshot_path: Optional[Path] = None
    metadata: Dict[str, any] = field(default_factory=dict)


@dataclass(slots=True)
class ExecutionReport:
    task_id: str
    sequence_name: str
    status: ActionStatus
    started_at: datetime
    finished_at: datetime
    steps: List[ExecutionStep]

    def to_dict(self) -> Dict[str, any]:
        return {
            "task_id": self.task_id,
            "sequence_name": self.sequence_name,
            "status": self.status.value,
            "started_at": self.started_at.isoformat(),
            "finished_at": self.finished_at.isoformat(),
            "steps": [
                {
                    "action": step.action.to_dict(),
                    "status": step.status.value,
                    "started_at": step.started_at.isoformat(),
                    "finished_at": step.finished_at.isoformat(),
                    "detail": step.detail,
                    "screenshot_path": str(step.screenshot_path) if step.screenshot_path else None,
                    "metadata": step.metadata,
                }
                for step in self.steps
            ],
        }

    def dumps(self) -> str:
        return json.dumps(self.to_dict(), indent=2)


class TaskRunner:
    """Execute action sequences using a provided executor."""

    def __init__(self, *, log_dir: Path, work_dir: Path, screenshot_dir: Path | None = None) -> None:
        self.log_dir = log_dir
        self.work_dir = work_dir
        self.screenshot_dir = screenshot_dir
        self.work_dir.mkdir(parents=True, exist_ok=True)
        if self.screenshot_dir:
            self.screenshot_dir.mkdir(parents=True, exist_ok=True)

    def run(
        self,
        task_id: str,
        sequence: ActionSequence,
        executor: ActionExecutor,
        *,
        metadata: Optional[Dict[str, any]] = None,
    ) -> ExecutionReport:
        logger = configure_task_logger(task_id, self.log_dir)
        context = TaskContext(task_id=task_id, workdir=self.work_dir, log=logger, metadata=metadata or {})
        steps: List[ExecutionStep] = []
        started = datetime.now(UTC)
        status = ActionStatus.SUCCEEDED

        for action in sequence.actions:
            step_started = datetime.now(UTC)
            logger.info("Executing %s", action.name)
            result: ActionResult = executor.execute(action, context)
            step_finished = datetime.now(UTC)
            steps.append(
                ExecutionStep(
                    action=action,
                    status=result.status,
                    started_at=step_started,
                    finished_at=step_finished,
                    detail=result.detail,
                    screenshot_path=result.screenshot_path,
                    metadata=result.metadata or {},
                )
            )
            if result.status is not ActionStatus.SUCCEEDED:
                status = ActionStatus.FAILED
                logger.error("Action %s failed: %s", action.name, result.detail)
                break

        finished = datetime.now(UTC)
        report = ExecutionReport(
            task_id=task_id,
            sequence_name=sequence.name,
            status=status,
            started_at=started,
            finished_at=finished,
            steps=steps,
        )
        logger.info("Task %s finished with status %s", task_id, status.value)
        return report


__all__ = ["ExecutionReport", "ExecutionStep", "TaskRunner", "configure_task_logger"]
