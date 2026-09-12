def score_state(
    state
) -> float:

    plant_species = len(
        state.plant_counts
    )

    animal_species = len(
        state.active_animal_names
    )

    total_plants = sum(
        state.plant_counts.values()
    )

    return (
        plant_species * 1000
        + animal_species * 250
        + total_plants
    )