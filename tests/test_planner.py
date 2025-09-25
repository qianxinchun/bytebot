import pytest

from mvp.planner.rule_based import PlannerConfig, RuleBasedPlanner


def test_basic_notepad_plan():
    planner = RuleBasedPlanner()
    sequence = planner.plan("Open notepad and type 'hello' then save to desktop")
    names = [action.name for action in sequence.actions]
    assert names[:2] == ["launch_app", "type_text"]
    assert names[-1] == "capture_screenshot"


def test_requires_matching_rule():
    planner = RuleBasedPlanner()
    with pytest.raises(ValueError):
        planner.plan("do something impossible")


def test_filename_extraction():
    planner = RuleBasedPlanner(PlannerConfig(default_save_directory="Desktop"))
    sequence = planner.plan("Open Notepad, type 'hello', save bytebot.txt")
    save_action = next(action for action in sequence.actions if action.name == "save_file")
    assert save_action.params["filename"] == "bytebot.txt"
