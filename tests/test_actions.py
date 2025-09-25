from pathlib import Path

import pytest

from mvp.agent.actions import Action, ActionSequence, load_action_sequence


def test_action_serialization_round_trip():
    action = Action(name="type_text", params={"text": "hi"}, description="Type")
    payload = action.to_dict()
    restored = Action.from_dict(payload)
    assert restored == action


def test_sequence_from_yaml(tmp_path: Path):
    yaml_content = """
{
  "name": "sample",
  "summary": "demo",
  "actions": [
    {"name": "click", "params": {"x": 10, "y": 20}}
  ]
}
"""
    yaml_path = tmp_path / "sample.yaml"
    yaml_path.write_text(yaml_content, encoding="utf-8")
    sequence = load_action_sequence(yaml_path)
    assert sequence.name == "sample"
    assert sequence.summary == "demo"
    assert len(sequence.actions) == 1
    assert sequence.actions[0].params == {"x": 10, "y": 20}


def test_sequence_validation():
    with pytest.raises(ValueError):
        ActionSequence.from_dict({"name": "broken"})

    with pytest.raises(TypeError):
        Action.from_dict({"name": "bad", "params": 123})
