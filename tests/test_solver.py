import json

from src.loaders.resource_loader import (
    load_level,
    load_plants,
    load_unlock_conditions,
)
from src.output.solution_writer import write_solution
from src.solver.strategy import build_level_two_strategy


def test_level_two_strategy_is_deterministic():
    world = load_level("2.json")
    plants = load_plants()
    unlocks = load_unlock_conditions()

    first = build_level_two_strategy(
        world,
        plants,
        unlocks,
    )

    second = build_level_two_strategy(
        world,
        plants,
        unlocks,
    )

    assert first == second


def test_level_two_strategy_has_no_duplicate_positions():
    actions = build_level_two_strategy(
        load_level("2.json"),
        load_plants(),
        load_unlock_conditions(),
    )

    positions = [
        (action.x, action.y)
        for action in actions
    ]

    assert len(positions) == len(set(positions))


def test_solution_writer_creates_json_object(tmp_path):
    actions = build_level_two_strategy(
        load_level("2.json"),
        load_plants(),
        load_unlock_conditions(),
    )

    output = tmp_path / "solution.json"

    write_solution(
        actions,
        output
    )

    data = json.loads(
        output.read_text(
            encoding="utf-8"
        )
    )

    assert isinstance(data, dict)

    assert "actions" in data

    assert isinstance(
        data["actions"],
        list
    )

    assert len(
        data["actions"]
    ) == len(actions)

    if data["actions"]:
        assert {
            "tick",
            "plant",
            "x",
            "y",
        }.issubset(
            data["actions"][0]
        )