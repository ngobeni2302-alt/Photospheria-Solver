from src.loaders.resource_loader import (
    load_plants,
    load_animals,
    load_classifications,
    load_unlock_conditions,
    load_level
)


def test_load_plants():
    plants = load_plants()

    assert len(plants) == 31
    assert plants[0].name == "Grass"
    assert plants[0].index == 1


def test_load_animals():
    animals = load_animals()

    assert len(animals) == 10
    assert animals[0].name == "Nectaris"


def test_load_classifications():
    classifications = load_classifications()

    assert len(classifications) == 15
    assert "Ground Cover" in classifications


def test_load_unlock_conditions():
    unlock_conditions = load_unlock_conditions()

    assert len(unlock_conditions) == 26
    assert unlock_conditions[0]["plant"] == "Blue Moss"


def test_load_level():
    world = load_level()

    assert world.rows == 50
    assert world.cols == 50
    assert world.ticks == 500
    assert world.animals_enabled is False


def test_level_contains_cells():
    world = load_level()

    cell = world.get_cell(0, 10)

    assert cell is not None
    assert cell.row == 0
    assert cell.col == 10
    assert cell.terrain == 2
    assert cell.soil == 0


def test_level_seasons():
    world = load_level()

    assert world.get_season_for_tick(99) is None
    assert world.get_season_for_tick(100) == "Summer"
    assert world.get_season_for_tick(200) == "Autumn"
    assert world.get_season_for_tick(300) == "Winter"
    assert world.get_season_for_tick(400) == "Spring"