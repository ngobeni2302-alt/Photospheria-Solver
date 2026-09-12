from src.loaders.resource_loader import (
    load_animals,
    load_classifications,
    load_level,
    load_plants,
    load_unlock_conditions,
)

from src.simulation.simulator import Simulator

from src.solver.strategy import (
    build_level_two_strategy
)


def test_level_two_planning_simulator_runs():

    world = load_level(
        "2.json"
    )

    plants = load_plants()

    unlocks = (
        load_unlock_conditions()
    )

    actions = (
        build_level_two_strategy(
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
        == 499
    )

    assert (
        "Rain"
        in state.events
    )

    assert (
        sum(
            state.plant_counts.values()
        )
        > 0
    )