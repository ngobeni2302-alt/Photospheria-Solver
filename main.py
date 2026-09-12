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


def main():

    print("Loading Photospheria Level 1...")

    world = load_level("1.json")

    plants = load_plants()

    unlock_conditions = load_unlock_conditions()

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

    print("Building Level 1 strategy...")

    actions = build_level_one_strategy(
        world,
        plants,
        unlock_conditions
    )

    output_path = write_solution(
        actions
    )

    print()
    print(
        f"Created {len(actions)} "
        f"planting actions."
    )

    print(
        f"Solution written to: "
        f"{output_path}"
    )

    print()

    for action in actions:

        print(
            f"Tick {action.tick}: "
            f"Plant {action.plant_index} "
            f"at ({action.x}, {action.y})"
        )


if __name__ == "__main__":
    main()