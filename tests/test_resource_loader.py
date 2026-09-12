from src.loaders.resource_loader import (
    load_animals,
    load_classifications,
    load_level,
    load_plants,
    load_unlock_conditions,
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
    unlocks = load_unlock_conditions()

    assert len(unlocks) == 26
    assert unlocks[0]["plant"] == "Blue Moss"


def test_load_level_two():
    world = load_level(
        "2.json"
    )

    assert world.rows == 70
    assert world.cols == 100
    assert world.ticks == 500
    assert world.animals_enabled is True


def test_level_two_rain_event():
    world = load_level(
        "2.json"
    )

    assert (
        "Rain"
        in world.get_events_up_to_tick(
            250
        )
    )

    assert (
        "Rain"
        not in world.get_events_up_to_tick(
            249
        )
    )


def test_level_two_seasons():
    world = load_level(
        "2.json"
    )

    assert (
        world.get_season_for_tick(100)
        == "Summer"
    )

    assert (
        world.get_season_for_tick(200)
        == "Autumn"
    )

    assert (
        world.get_season_for_tick(300)
        == "Winter"
    )

    assert (
        world.get_season_for_tick(400)
        == "Spring"
    )