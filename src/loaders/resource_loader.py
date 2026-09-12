import json
from pathlib import Path

from src.models.animal import Animal
from src.models.cell import Cell
from src.models.plant import (
    Growth,
    Plant,
    PlantRules
)
from src.models.world import World


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_FOLDER = PROJECT_ROOT / "data"


def load_json(filename: str):
    file_path = DATA_FOLDER / filename

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def load_plants() -> list[Plant]:
    plants = []

    for item in load_json(
        "plant_dataset.json"
    ):

        growth_data = dict(
            item["growth"]
        )

        growth_data.setdefault(
            "conditional_modifiers",
            []
        )

        growth = Growth(
            **growth_data
        )

        rules = PlantRules(
            weaknesses=(
                item
                .get("rules", {})
                .get("weaknesses", [])
            ),
            special=(
                item
                .get("rules", {})
                .get("special", [])
            ),
        )

        plant = Plant(
            name=item["plant"],
            index=item["index"],
            growth=growth,
            preferred_soil=item.get(
                "preferred_soil",
                []
            ),
            rules=rules,
            role=item.get(
                "role",
                ""
            ),
        )

        plants.append(
            plant
        )

    return plants


def load_animals() -> list[Animal]:

    animals = []

    for item in load_json(
        "animals.json"
    ):

        animal = Animal(
            id=item["id"],
            name=item["name"],
            requirements=item[
                "requirements"
            ],
            effects=item.get(
                "effects",
                []
            ),
        )

        animals.append(
            animal
        )

    return animals


def load_classifications() -> dict[str, list[str]]:
    return load_json(
        "classifications.json"
    )


def load_unlock_conditions() -> list[dict]:
    return load_json(
        "plant_unlock_conditions.json"
    )


def load_level(
    filename: str = "2.json"
) -> World:

    level_data = load_json(
        filename
    )

    cells = {}

    for item in level_data["cells"]:

        cell = Cell(
            row=item["row"],
            col=item["col"],
            terrain=item["terrain"],
            soil=item["soil"],
        )

        cells[
            (cell.row, cell.col)
        ] = cell

    return World(
        rows=level_data["rows"],
        cols=level_data["cols"],
        ticks=level_data["ticks"],

        animals_enabled=(
            level_data[
                "animals_enabled"
            ]
        ),

        cells=cells,

        commands=level_data.get(
            "commands",
            []
        ),
    )