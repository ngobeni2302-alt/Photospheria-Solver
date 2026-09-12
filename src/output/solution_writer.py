import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

SOLUTION_FILE = PROJECT_ROOT / "solution.json"


def write_solution(
    actions,
    output_path=SOLUTION_FILE
):
    """
    Write planting actions to solution.json.

    The actions are sorted before writing so that
    the output is always deterministic.
    """

    sorted_actions = sorted(
        actions,
        key=lambda action: (
            action.tick,
            action.plant_index,
            action.x,
            action.y
        )
    )

    solution_data = [
        action.to_dict()
        for action in sorted_actions
    ]

    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            solution_data,
            file,
            indent=2
        )

    return output_path