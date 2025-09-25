from __future__ import annotations

from pathlib import Path

import pytest

from mvp.agent.actions import Action, ActionSequence, ActionStatus
from mvp.agent.executor import ActionExecutor, ActionResult, TaskContext
from mvp.runtime.pipeline import ExecutionReport, TaskRunner


class DummyExecutor(ActionExecutor):
    def __init__(self, fail_on: set[str] | None = None):
        self.fail_on = fail_on or set()
        self.recorded: list[str] = []

    def execute(self, action: Action, context: TaskContext) -> ActionResult:  # type: ignore[override]
        self.recorded.append(action.name)
        if action.name in self.fail_on:
            return ActionResult(status=ActionStatus.FAILED, detail="forced failure")
        return ActionResult(status=ActionStatus.SUCCEEDED, metadata={"echo": action.params})


@pytest.fixture()
def runner(tmp_path: Path) -> TaskRunner:
    return TaskRunner(log_dir=tmp_path / "logs", work_dir=tmp_path / "work", screenshot_dir=tmp_path / "shots")


def test_task_runner_success(tmp_path: Path, runner: TaskRunner):
    sequence = ActionSequence(actions=[Action(name="step", params={})], name="demo")
    executor = DummyExecutor()
    report = runner.run("task-1", sequence, executor)
    assert isinstance(report, ExecutionReport)
    assert report.status is ActionStatus.SUCCEEDED
    assert executor.recorded == ["step"]

    log_path = tmp_path / "logs" / "task-1.log"
    assert log_path.exists()
    assert "Executing step" in log_path.read_text(encoding="utf-8")


def test_task_runner_failure(runner: TaskRunner):
    sequence = ActionSequence(actions=[Action(name="first"), Action(name="second")], name="demo")
    executor = DummyExecutor(fail_on={"second"})
    report = runner.run("task-2", sequence, executor)
    assert report.status is ActionStatus.FAILED
    assert [step.status for step in report.steps][-1] is ActionStatus.FAILED
    assert executor.recorded == ["first", "second"]
