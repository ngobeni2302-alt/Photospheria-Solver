from src.models.planting_action import PlantingAction


def get_starting_plants(plants, unlock_conditions):
    """
    Find plants that do not have an unlock condition.

    These plants are treated as available at the
    beginning of Level 1.
    """

    locked_plant_names = {
        rule["plant"]
        for rule in unlock_conditions
    }

    starting_plants = []

    for plant in plants:
        if plant.name not in locked_plant_names:
            starting_plants.append(plant)

    # Always keep the order deterministic
    starting_plants.sort(key=lambda plant: plant.index)

    return starting_plants


def get_valid_cells(world, plant):
    """
    Find cells where a plant may initially be placed.

    A cell must:
    - be plantable terrain
    - have soil preferred by the plant
    """

    valid_cells = []

    for cell in world.get_plantable_cells():

        if cell.soil in plant.preferred_soil:
            valid_cells.append(cell)

    # Always sort to keep the solver deterministic
    valid_cells.sort(
        key=lambda cell: (
            cell.row,
            cell.col
        )
    )

    return valid_cells


def build_level_one_strategy(
    world,
    plants,
    unlock_conditions
):
    """
    Creates our first deterministic Level 1 planting strategy.

    For the baseline:
    - use plants available from the start
    - plant one of each species
    - spread their starting positions around the greenhouse
    - plant them at tick 0

    Later this strategy will be improved using simulation
    and optimisation.
    """

    starting_plants = get_starting_plants(
        plants,
        unlock_conditions
    )

    actions = []

    used_positions = set()

    number_of_plants = len(starting_plants)

    for plant_number, plant in enumerate(starting_plants):

        valid_cells = get_valid_cells(
            world,
            plant
        )

        # Remove positions already used
        available_cells = []

        for cell in valid_cells:

            position = (
                cell.row,
                cell.col
            )

            if position not in used_positions:
                available_cells.append(cell)

        if not available_cells:
            continue

        # Spread our plants through the available area
        fraction = (
            plant_number + 1
        ) / (
            number_of_plants + 1
        )

        cell_index = int(
            fraction
            * (len(available_cells) - 1)
        )

        chosen_cell = available_cells[cell_index]

        used_positions.add(
            (
                chosen_cell.row,
                chosen_cell.col
            )
        )

        action = PlantingAction(
            tick=0,
            plant_index=plant.index,

            # Column acts as X
            x=chosen_cell.col,

            # Row acts as Y
            y=chosen_cell.row
        )

        actions.append(action)

    return actions