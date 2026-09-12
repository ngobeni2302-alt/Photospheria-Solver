from dataclasses import dataclass, field
from typing import Any


@dataclass
class Animal:
    id: str
    name: str
    requirements: dict[str, Any]

    effects: list[dict[str, Any]] = field(
        default_factory=list
    )