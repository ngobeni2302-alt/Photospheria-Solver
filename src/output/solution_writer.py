import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SOLUTION_FILE = PROJECT_ROOT / "solution.json"


def build_solution_payload(actions):
    sorted_actions = sorted(
        actions,
        key=lambda action: (
            action.tick,
            action.plant_index,
            action.x,
            action.y,
        ),
    )

    return {
        "actions": [
            action.to_dict()
            for action in sorted_actions
        ]
    }


def write_solution(actions, output_path=SOLUTION_FILE):
    solution_data = build_solution_payload(actions)

    output_path = Path(output_path)

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

        file.write("\n")

    return output_path