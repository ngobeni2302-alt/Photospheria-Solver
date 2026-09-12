from src.loaders.resource_loader import load_unlock_conditions
from src.rules.unlock_rules import is_plant_unlocked


def create_world_state():
    return {
        "species": set(),
        "coverage": {},
        "plant_counts": {},
        "events": set(),
        "features": {}
    }


def test_starting_plant_is_available():
    unlock_conditions = load_unlock_conditions()

    world_state = create_world_state()

    result = is_plant_unlocked(
        "Grass",
        unlock_conditions,
        world_state
    )

    assert result is True