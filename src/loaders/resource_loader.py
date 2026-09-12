import json
from pathlib import Path

from src.models.plant import Plant, Growth, PlantRules
from src.models.animal import Animal
from src.models.cell import Cell
from src.models.world import World


# Root folder of the project
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# data/ folder
DATA_FOLDER = PROJECT_ROOT / "data"


def load_json(filename):
    """
    Opens a JSON file from the data folder
    and returns the Python data.
    """

    file_path = DATA_FOLDER / filename

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def load_plants():
    """
    Loads all Photospheria plants
    from plant_dataset.json.
    """

    plant_data = load_json("plant_dataset.json")

    plants = []

    for item in plant_data:

        growth = Growth(
            **item["growth"]
        )

        rules = PlantRules(
            weaknesses=item["rules"]["weaknesses"],
            special=item["rules"]["special"]
        )

        plant = Plant(
            name=item["plant"],
            index=item["index"],
            growth=growth,
            preferred_soil=item["preferred_soil"],
            rules=rules,
            role=item["role"]
        )

        plants.append(plant)

    return plants


def load_animals():
    """
    Loads all animals from animals.json.
    """

    animal_data = load_json("animals.json")

    animals = []

    for item in animal_data:

        animal = Animal(
            id=item["id"],
            name=item["name"],
            requirements=item["requirements"],
            effects=item["effects"]
        )

        animals.append(animal)

    return animals


def load_classifications():
    """
    Loads the plant classifications.
    """

    return load_json("classifications.json")


def load_unlock_conditions():
    """
    Loads all plant unlock conditions.
    """

    return load_json("plant_unlock_conditions.json")


def load_level(filename="1.json"):
    """
    Loads a Photospheria level file.

    For now the default is Level 1.
    """

    level_data = load_json(filename)

    cells = {}

    for item in level_data["cells"]:

        cell = Cell(
            row=item["row"],
            col=item["col"],
            terrain=item["terrain"],
            soil=item["soil"]
        )

        # Store each cell using its coordinates
        cells[(cell.row, cell.col)] = cell

    world = World(
        rows=level_data["rows"],
        cols=level_data["cols"],
        ticks=level_data["ticks"],
        animals_enabled=level_data["animals_enabled"],
        cells=cells,
        commands=level_data.get("commands", [])
    )

    return world