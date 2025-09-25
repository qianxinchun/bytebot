"""Utilities for summarising execution reports."""
from __future__ import annotations

from pathlib import Path
from typing import Iterable

from .pipeline import ExecutionReport


def write_human_readable_summary(report: ExecutionReport, output_path: Path) -> None:
    """Persist a text summary for quick inspection."""

    lines = [
        f"Task: {report.task_id}",
        f"Sequence: {report.sequence_name}",
        f"Status: {report.status.value}",
        f"Started: {report.started_at.isoformat()}",
        f"Finished: {report.finished_at.isoformat()}",
        "Steps:",
    ]
    for idx, step in enumerate(report.steps, start=1):
        lines.append(
            f"  {idx}. {step.action.name} -> {step.status.value}"
            + (f" ({step.detail})" if step.detail else "")
        )
        if step.screenshot_path:
            lines.append(f"     Screenshot: {step.screenshot_path}")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines), encoding="utf-8")


def summarize_reports(reports: Iterable[ExecutionReport]) -> dict:
    """Aggregate high-level metrics across multiple reports."""

    reports = list(reports)
    total = len(reports)
    successes = sum(1 for report in reports if report.status.value == "succeeded")
    return {
        "total_tasks": total,
        "successful_tasks": successes,
        "success_rate": successes / total if total else 0.0,
    }


__all__ = ["write_human_readable_summary", "summarize_reports"]
