from src.loaders.resource_loader import load_unlock_conditions
from src.rules.unlock_rules import is_plant_unlocked


def test_grass_is_starting_plant():

    state = {
        "species": set(),
        "coverage": {},
        "plant_counts": {},
        "events": set(),
        "features": {},
    }

    assert is_plant_unlocked(
        "Grass",
        load_unlock_conditions(),
        state
    ) is True


def test_blue_moss_unlock_rule():

    state = {
        "species": {
            "Loamcrawlers"
        },

        "coverage": {
            "Grass": 0.05,
            "Rose Bush": 0.02
        },

        "plant_counts": {},

        "events": set(),

        "features": {},
    }

    assert is_plant_unlocked(
        "Blue Moss",
        load_unlock_conditions(),
        state
    ) is True


def test_mire_bloom_requires_rain():

    unlocks = load_unlock_conditions()

    state = {
        "species": set(),

        "coverage": {
            "Blue Moss": 0.06
        },

        "plant_counts": {},

        "events": set(),

        "features": {},
    }

    assert is_plant_unlocked(
        "Mire Bloom",
        unlocks,
        state
    ) is False

    state["events"].add(
        "Rain"
    )

    assert is_plant_unlocked(
        "Mire Bloom",
        unlocks,
        state
    ) is True