"""Core action data structures for the Bytebot MVP executor pipeline."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Optional

try:  # pragma: no cover - exercised in integration tests
    import yaml  # type: ignore
except ModuleNotFoundError:  # pragma: no cover - optional dependency
    yaml = None
import json


class ActionStatus(str, Enum):
    """Possible execution states for an action."""

    PENDING = "pending"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"


@dataclass(slots=True)
class Action:
    """Declarative description of a single automation command."""

    name: str
    params: Dict[str, Any] = field(default_factory=dict)
    description: Optional[str] = None
    expected_outcome: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Serialize the action into a dictionary suitable for YAML/JSON."""

        payload: Dict[str, Any] = {"name": self.name, "params": dict(self.params)}
        if self.description is not None:
            payload["description"] = self.description
        if self.expected_outcome is not None:
            payload["expected_outcome"] = self.expected_outcome
        return payload

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "Action":
        """Construct an action from a dictionary."""

        if "name" not in payload:
            raise ValueError("Action payload must include a 'name' field")
        name = str(payload["name"])
        params_field = payload.get("params", {})
        if not isinstance(params_field, MutableMapping):
            raise TypeError("Action 'params' must be a mapping")
        description = payload.get("description")
        expected_outcome = payload.get("expected_outcome")
        return cls(
            name=name,
            params=dict(params_field),
            description=str(description) if description is not None else None,
            expected_outcome=str(expected_outcome) if expected_outcome is not None else None,
        )


@dataclass(slots=True)
class ActionSequence:
    """Ordered collection of actions and metadata about the requested task."""

    actions: List[Action]
    name: str
    summary: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "summary": self.summary,
            "actions": [action.to_dict() for action in self.actions],
        }

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "ActionSequence":
        if "actions" not in payload:
            raise ValueError("ActionSequence payload must include an 'actions' field")
        actions_payload = payload["actions"]
        if not isinstance(actions_payload, Iterable):
            raise TypeError("'actions' must be an iterable of action payloads")
        actions = [Action.from_dict(raw) for raw in actions_payload]
        name = str(payload.get("name", "unnamed-sequence"))
        summary = payload.get("summary")
        return cls(actions=actions, name=name, summary=str(summary) if summary else None)


def load_action_sequence(path: Path) -> ActionSequence:
    """Load an action sequence definition from a YAML file."""

    with path.open("r", encoding="utf-8") as handle:
        content = handle.read()
    if yaml is not None:
        payload = yaml.safe_load(content)
    else:
        payload = json.loads(content)
    if not isinstance(payload, Mapping):
        raise TypeError("Action sequence YAML must evaluate to a mapping at the top level")
    return ActionSequence.from_dict(payload)


__all__ = [
    "Action",
    "ActionSequence",
    "ActionStatus",
    "load_action_sequence",
]
