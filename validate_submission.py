import argparse
import json
from pathlib import Path


PROJECT_ROOT = Path(
    __file__
).resolve().parent

SOLUTION_FILE = (
    PROJECT_ROOT
    / "solution.json"
)


def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "Validate Photospheria "
            "solution.json"
        )
    )

    parser.add_argument(
        "level",
        nargs="?",
        type=int,
        default=3,
        choices=[1, 2, 3],
        help=(
            "Level whose world bounds "
            "should be used (default: 3)"
        ),
    )

    return parser.parse_args()


def validate_submission(
    level_number
):

    level_file = (
        PROJECT_ROOT
        / "data"
        / f"{level_number}.json"
    )

    with open(
        level_file,
        "r",
        encoding="utf-8"
    ) as file:

        level = json.load(
            file
        )

    with open(
        SOLUTION_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        solution = json.load(
            file
        )

    if not isinstance(
        solution,
        dict
    ):

        raise ValueError(
            "solution.json root "
            "must be a JSON object"
        )

    if "actions" not in solution:

        raise ValueError(
            "solution.json must contain "
            "an 'actions' list"
        )

    actions = solution[
        "actions"
    ]

    if not isinstance(
        actions,
        list
    ):

        raise ValueError(
            "'actions' must be a list"
        )

    valid_plant_indexes = set(
        range(
            1,
            32
        )
    )

    seen_positions = set()

    for index, action in enumerate(
        actions
    ):

        if not isinstance(
            action,
            dict
        ):

            raise ValueError(
                f"Action {index} "
                f"must be an object"
            )

        required = {
            "tick",
            "plant",
            "x",
            "y"
        }

        missing = (
            required
            - set(action)
        )

        if missing:

            raise ValueError(
                f"Action {index} "
                f"is missing "
                f"{sorted(missing)}"
            )

        tick = action["tick"]

        plant = action["plant"]

        x = action["x"]

        y = action["y"]

        values = (
            tick,
            plant,
            x,
            y
        )

        if not all(
            isinstance(
                value,
                int
            )
            for value in values
        ):

            raise ValueError(
                f"Action {index} "
                f"values must be integers"
            )

        if not (
            0
            <= tick
            < level["ticks"]
        ):

            raise ValueError(
                f"Action {index} "
                f"has invalid tick {tick}"
            )

        if (
            plant
            not in valid_plant_indexes
        ):

            raise ValueError(
                f"Action {index} "
                f"has invalid plant "
                f"index {plant}"
            )

        if not (
            0
            <= x
            < level["cols"]
        ):

            raise ValueError(
                f"Action {index} "
                f"has invalid x {x}"
            )

        if not (
            0
            <= y
            < level["rows"]
        ):

            raise ValueError(
                f"Action {index} "
                f"has invalid y {y}"
            )

        position = (
            x,
            y
        )

        if position in seen_positions:

            raise ValueError(
                f"Duplicate starting "
                f"position: {position}"
            )

        seen_positions.add(
            position
        )

    print(
        "Submission validation passed"
    )

    print(
        f"Level: {level_number}"
    )

    print(
        "Root type: object"
    )

    print(
        f"Actions: {len(actions)}"
    )


if __name__ == "__main__":

    args = parse_args()

    validate_submission(
        args.level
    )