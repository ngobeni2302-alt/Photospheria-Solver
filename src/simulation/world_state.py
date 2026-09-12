from dataclasses import dataclass, field

from src.level_config import (
    WORLD_WIDTH,
    WORLD_HEIGHT,
    MAX_TICKS,
    SEASONS_ENABLED,
    ANIMALS_ENABLED,
    WEATHER_ENABLED
)


@dataclass
class WorldState:
    width: int = WORLD_WIDTH
    height: int = WORLD_HEIGHT

    current_tick: int = 0
    max_ticks: int = MAX_TICKS

    seasons_enabled: bool = SEASONS_ENABLED
    animals_enabled: bool = ANIMALS_ENABLED
    weather_enabled: bool = WEATHER_ENABLED

    plant_counts: dict = field(default_factory=dict)
    coverage: dict = field(default_factory=dict)
    species: set = field(default_factory=set)
    events: set = field(default_factory=set)
    features: dict = field(default_factory=dict)