import argparse

from src.loaders.resource_loader import (
    load_animals,
    load_classifications,
    load_level,
    load_plants,
    load_unlock_conditions,
)
from src.output.solution_writer import write_solution
from src.simulation.simulator import Simulator
from src.solver.scorer import score_state
from src.solver.strategy import build_strategy


def parse_args():
    parser = argparse.ArgumentParser(
        description="Photospheria deterministic solver"
    )

    parser.add_argument(
        "level",
        nargs="?",
        type=int,
        default=3,
        choices=[1, 2, 3],
        help="Level to solve (default: 3)",
    )

    return parser.parse_args()


def main():
    args = parse_args()
    level_number = args.level

    world = load_level(
        f"{level_number}.json"
    )

    plants = load_plants()
    animals = load_animals()
    classifications = load_classifications()
    unlock_conditions = load_unlock_conditions()

    actions = build_strategy(
        level_number,
        world,
        plants,
        unlock_conditions
    )

    output_path = write_solution(
        actions
    )

    simulator = Simulator(
        world=world,
        plants=plants,
        animals=animals,
        classifications=classifications,
        unlock_conditions=unlock_conditions,
    )

    state = simulator.run(
        actions
    )

    print(
        f"Photospheria Level {level_number}"
    )

    print(
        f"World: {world.rows} x {world.cols}"
    )

    print(
        f"Ticks: {world.ticks}"
    )

    print(
        f"Animals enabled: "
        f"{world.animals_enabled}"
    )

    print(
        f"Commands: {world.commands}"
    )

    print(
        f"Generated actions: "
        f"{len(actions)}"
    )

    print(
        f"Planning-simulator plant species: "
        f"{len(state.plant_counts)}"
    )

    print(
        f"Planning-simulator active animals: "
        f"{sorted(state.active_animal_names)}"
    )

    print(
        f"Planning heuristic score: "
        f"{score_state(state):.0f}"
    )

    print(
        f"Output: {output_path}"
    )


if __name__ == "__main__":
    main()