from dataclasses import dataclass, field
from typing import Any


@dataclass
class Growth:
    time_to_maturity: int
    spread_rate: float
    spread_mechanism: str
    spread_type: str
    spread_range: int
    root_type: str
    invasiveness_rank: int
    conditional_modifiers: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class PlantRules:
    weaknesses: list[dict[str, Any]] = field(default_factory=list)
    special: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class Plant:
    name: str
    index: int
    growth: Growth
    preferred_soil: list[int]
    rules: PlantRules
    role: str