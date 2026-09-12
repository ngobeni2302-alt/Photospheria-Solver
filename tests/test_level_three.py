from src.loaders.resource_loader import (
    load_animals,
    load_classifications,
    load_level,
    load_plants,
    load_unlock_conditions,
)

from src.simulation.simulator import (
    Simulator
)

from src.solver.strategy import (
    build_level_three_strategy
)


def test_level_three_metadata():

    world = load_level(
        "3.json"
    )

    assert world.rows == 150

    assert world.cols == 150

    assert world.ticks == 800

    assert (
        world.animals_enabled
        is True
    )


def test_level_three_events():

    world = load_level(
        "3.json"
    )

    assert (
        "Drought"
        in world.get_events_up_to_tick(
            10
        )
    )

    assert (
        "Rain"
        not in world.get_events_up_to_tick(
            149
        )
    )

    assert (
        "Rain"
        in world.get_events_up_to_tick(
            150
        )
    )

    assert (
        "Ash Eclipse"
        not in world.get_events_up_to_tick(
            299
        )
    )

    assert (
        "Ash Eclipse"
        in world.get_events_up_to_tick(
            300
        )
    )


def test_level_three_seasons():

    world = load_level(
        "3.json"
    )

    assert (
        world.get_season_for_tick(100)
        == "Summer"
    )

    assert (
        world.get_season_for_tick(200)
        == "Autumn"
    )

    assert (
        world.get_season_for_tick(300)
        == "Winter"
    )

    assert (
        world.get_season_for_tick(400)
        == "Spring"
    )

    assert (
        world.get_season_for_tick(500)
        == "Summer"
    )

    assert (
        world.get_season_for_tick(600)
        == "Autumn"
    )

    assert (
        world.get_season_for_tick(700)
        == "Winter"
    )


def test_level_three_strategy_is_deterministic():

    world = load_level(
        "3.json"
    )

    plants = load_plants()

    unlocks = (
        load_unlock_conditions()
    )

    first = (
        build_level_three_strategy(
            world,
            plants,
            unlocks
        )
    )

    second = (
        build_level_three_strategy(
            world,
            plants,
            unlocks
        )
    )

    assert first == second


def test_level_three_strategy_has_no_duplicate_positions():

    actions = (
        build_level_three_strategy(
            load_level(
                "3.json"
            ),
            load_plants(),
            load_unlock_conditions(),
        )
    )

    positions = [
        (
            action.x,
            action.y
        )
        for action in actions
    ]

    assert (
        len(positions)
        == len(set(positions))
    )


def test_level_three_actions_are_inside_world():

    world = load_level(
        "3.json"
    )

    actions = (
        build_level_three_strategy(
            world,
            load_plants(),
            load_unlock_conditions(),
        )
    )

    for action in actions:

        assert (
            0
            <= action.tick
            < world.ticks
        )

        assert (
            0
            <= action.x
            < world.cols
        )

        assert (
            0
            <= action.y
            < world.rows
        )


def test_level_three_planning_simulator_runs():

    world = load_level(
        "3.json"
    )

    plants = load_plants()

    unlocks = (
        load_unlock_conditions()
    )

    actions = (
        build_level_three_strategy(
            world,
            plants,
            unlocks
        )
    )

    simulator = Simulator(
        world,
        plants,
        load_animals(),
        load_classifications(),
        unlocks,
    )

    state = simulator.run(
        actions
    )

    assert (
        state.current_tick
        == 799
    )

    assert (
        "Drought"
        in state.events
    )

    assert (
        "Rain"
        in state.events
    )

    assert (
        "Ash Eclipse"
        in state.events
    )

    assert (
        len(
            state.plant_counts
        )
        >= 15
    )