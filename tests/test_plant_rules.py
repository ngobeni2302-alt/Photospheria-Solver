from src.loaders.resource_loader import (
    load_level,
    load_plants
)

from src.rules.plant_rules import can_plant


def test_grass_can_be_planted_on_matching_level_two_soil_cell():

    world = load_level(
        "2.json"
    )

    grass = next(
        plant
        for plant in load_plants()
        if plant.name == "Grass"
    )

    cell = next(
        cell
        for cell
        in world.get_plantable_cells()
        if cell.soil
        in grass.preferred_soil
    )

    assert can_plant(
        grass,
        cell,
        0,
        world,
        set()
    ) is True


def test_out_of_range_tick_is_invalid():

    world = load_level(
        "2.json"
    )

    grass = next(
        plant
        for plant in load_plants()
        if plant.name == "Grass"
    )

    cell = next(
        cell
        for cell
        in world.get_plantable_cells()
        if cell.soil
        in grass.preferred_soil
    )

    assert can_plant(
        grass,
        cell,
        500,
        world,
        set()
    ) is False