from src.loaders.resource_loader import (
    load_animals,
    load_classifications
)

from src.rules.animal_rules import (
    is_animal_active
)


def animal_named(name):

    return next(
        animal
        for animal
        in load_animals()
        if animal.name == name
    )


def test_nectaris_from_lavender_coverage():

    state = {
        "coverage": {
            "Lavender": 0.02
        },

        "plant_counts": {}
    }

    assert is_animal_active(
        animal_named("Nectaris"),
        state,
        load_classifications()
    )


def test_loamcrawlers_require_grass_and_rose_count():

    state = {
        "coverage": {
            "Grass": 0.04
        },

        "plant_counts": {
            "Rose Bush": 10
        },
    }

    assert is_animal_active(
        animal_named(
            "Loamcrawlers"
        ),
        state,
        load_classifications()
    )


def test_barkskips_from_eight_oaks():

    state = {
        "coverage": {},

        "plant_counts": {
            "Oak Tree": 8
        }
    }

    assert is_animal_active(
        animal_named(
            "Barkskips"
        ),
        state,
        load_classifications()
    )


def test_rhizorends_classification_name_compatibility():

    state = {
        "coverage": {},

        "plant_counts": {
            "Rose Bush": 15,
            "Lavender": 10
        },
    }

    assert is_animal_active(
        animal_named(
            "Rhizorends"
        ),
        state,
        load_classifications()
    )