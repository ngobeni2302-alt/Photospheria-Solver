import json

from src.loaders.resource_loader import (
    load_level,
    load_plants,
    load_unlock_conditions
)

from src.solver.strategy import (
    build_level_one_strategy
)

from src.output.solution_writer import (
    write_solution
)


def test_level_one_strategy():
    world = load_level("1.json")
    plants = load_plants()
    unlock_conditions = load_unlock_conditions()

    actions = build_level_one_strategy(
        world,
        plants,
        unlock_conditions
    )

    # There are five plants without unlock conditions
    assert len(actions) == 5

    # Baseline plants are planted at the beginning
    for action in actions:
        assert action.tick == 0

    # No two plants should start on the same cell
    positions = {
        (action.x, action.y)
        for action in actions
    }

    assert len(positions) == len(actions)


def test_solution_writer(tmp_path):
    world = load_level("1.json")
    plants = load_plants()
    unlock_conditions = load_unlock_conditions()

    actions = build_level_one_strategy(
        world,
        plants,
        unlock_conditions
    )

    output_file = (
        tmp_path / "solution.json"
    )

    write_solution(
        actions,
        output_file
    )

    assert output_file.exists()

    with open(
        output_file,
        "r",
        encoding="utf-8"
    ) as file:

        solution = json.load(file)

    assert len(solution) == 5

    assert "tick" in solution[0]
    assert "plant" in solution[0]
    assert "x" in solution[0]
    assert "y" in solution[0]