from src.models.planting_action import PlantingAction
from src.rules.plant_rules import can_plant


LEVEL_TWO_STARTING_COUNTS = {
    "Grass": 24,
    "Rose Bush": 18,
    "Lavender": 18,
    "Dwarf Sunflower": 14,
    "Oak Tree": 8,
}


LEVEL_TWO_SECOND_WAVE = {
    "Blue Moss": 24,
    "Orange Blossom": 10,
    "Crimson Vine": 18,
    "Stone Reed": 4,
    "Razorgrass": 4,
}


LEVEL_TWO_THIRD_WAVE = {
    "Silver Fern": 12,
    "Purple Canopy Tree": 4,
    "Moonpetal Lily": 8,
    "Ironthorn Shrub": 8,
}


LEVEL_TWO_AFTER_RAIN = {
    "Mire Bloom": 8,
}


LEVEL_THREE_STARTING_COUNTS = {
    "Grass": 70,
    "Rose Bush": 55,
    "Lavender": 55,
    "Dwarf Sunflower": 40,
    "Oak Tree": 10,
}


LEVEL_THREE_AFTER_DROUGHT = {
    "Crystal Cactus": 20,
}


LEVEL_THREE_SECOND_WAVE = {
    "Blue Moss": 70,
    "Orange Blossom": 30,
    "Crimson Vine": 70,
    "Stone Reed": 10,
    "Razorgrass": 10,
}


LEVEL_THREE_THIRD_WAVE = {
    "Silver Fern": 80,
    "Purple Canopy Tree": 8,
    "Moonpetal Lily": 55,
    "Ironthorn Shrub": 65,
}


LEVEL_THREE_ADVANCED_WAVE = {
    "Skyvine": 10,
    "Amber Fern": 10,
    "Thornheart Bramble": 10,
    "Living Topiary": 10,
    "Bloodbloom": 10,
    "Sunshard Bloom": 10,
}


LEVEL_THREE_AFTER_RAIN = {
    "Mire Bloom": 20,
}


def get_starting_plants(
    plants,
    unlock_conditions
):
    locked_names = {
        rule["plant"]
        for rule in unlock_conditions
    }

    return sorted(
        [
            plant
            for plant in plants
            if plant.name not in locked_names
        ],
        key=lambda plant: plant.index,
    )


def _candidate_cells(
    world,
    plant
):
    return sorted(
        [
            cell
            for cell
            in world.get_plantable_cells()
            if cell.soil
            in plant.preferred_soil
        ],
        key=lambda cell: (
            cell.row,
            cell.col
        ),
    )


def _spread_choice(
    candidates,
    amount
):
    if amount <= 0:
        return []

    if not candidates:
        return []

    if amount >= len(candidates):
        return candidates[:]

    chosen = []

    for i in range(amount):
        index = round(
            i
            * (len(candidates) - 1)
            / max(
                amount - 1,
                1
            )
        )

        chosen.append(
            candidates[index]
        )

    unique = []
    seen = set()

    for cell in chosen:
        key = (
            cell.row,
            cell.col
        )

        if key not in seen:
            seen.add(
                key
            )

            unique.append(
                cell
            )

    if len(unique) < amount:
        for cell in candidates:
            key = (
                cell.row,
                cell.col
            )

            if key not in seen:
                seen.add(
                    key
                )

                unique.append(
                    cell
                )

                if len(unique) == amount:
                    break

    return unique


def _add_wave(
    actions,
    world,
    plants_by_name,
    counts,
    tick,
    used_positions
):

    for plant_name, amount in counts.items():

        plant = plants_by_name.get(
            plant_name
        )

        if plant is None:
            continue

        candidates = [
            cell
            for cell
            in _candidate_cells(
                world,
                plant
            )
            if (
                cell.row,
                cell.col
            )
            not in used_positions
        ]

        selected_cells = _spread_choice(
            candidates,
            amount
        )

        for cell in selected_cells:

            if not can_plant(
                plant,
                cell,
                tick,
                world,
                used_positions
            ):
                continue

            used_positions.add(
                (
                    cell.row,
                    cell.col
                )
            )

            action = PlantingAction(
                tick=tick,
                plant_index=plant.index,
                x=cell.col,
                y=cell.row,
            )

            actions.append(
                action
            )


def _event_tick(
    world,
    event_name
):
    ticks = [
        command["tick"]
        for command
        in world.commands
        if (
            command.get("type")
            == "event"
            and command.get("event")
            == event_name
        )
    ]

    if not ticks:
        return None

    return min(
        ticks
    )


def _sort_actions(
    actions
):
    return sorted(
        actions,
        key=lambda action: (
            action.tick,
            action.plant_index,
            action.x,
            action.y,
        ),
    )


def build_level_one_strategy(
    world,
    plants,
    unlock_conditions
):

    actions = []
    used_positions = set()

    starting_plants = get_starting_plants(
        plants,
        unlock_conditions
    )

    for plant in starting_plants:

        candidates = [
            cell
            for cell
            in _candidate_cells(
                world,
                plant
            )
            if (
                cell.row,
                cell.col
            )
            not in used_positions
        ]

        if not candidates:
            continue

        cell = candidates[
            len(candidates) // 2
        ]

        used_positions.add(
            (
                cell.row,
                cell.col
            )
        )

        actions.append(
            PlantingAction(
                tick=0,
                plant_index=plant.index,
                x=cell.col,
                y=cell.row,
            )
        )

    return _sort_actions(
        actions
    )


def build_level_two_strategy(
    world,
    plants,
    unlock_conditions
):

    actions = []
    used_positions = set()

    plants_by_name = {
        plant.name: plant
        for plant in plants
    }

    _add_wave(
        actions,
        world,
        plants_by_name,
        LEVEL_TWO_STARTING_COUNTS,
        tick=0,
        used_positions=used_positions,
    )

    _add_wave(
        actions,
        world,
        plants_by_name,
        LEVEL_TWO_SECOND_WAVE,
        tick=25,
        used_positions=used_positions,
    )

    _add_wave(
        actions,
        world,
        plants_by_name,
        LEVEL_TWO_THIRD_WAVE,
        tick=80,
        used_positions=used_positions,
    )

    rain_tick = _event_tick(
        world,
        "Rain"
    )

    if rain_tick is not None:

        _add_wave(
            actions,
            world,
            plants_by_name,
            LEVEL_TWO_AFTER_RAIN,
            tick=rain_tick + 1,
            used_positions=used_positions,
        )

    return _sort_actions(
        actions
    )


def build_level_three_strategy(
    world,
    plants,
    unlock_conditions
):

    actions = []

    used_positions = set()

    plants_by_name = {
        plant.name: plant
        for plant in plants
    }

    # Starting species
    _add_wave(
        actions,
        world,
        plants_by_name,
        LEVEL_THREE_STARTING_COUNTS,
        tick=0,
        used_positions=used_positions,
    )

    # Drought occurs at tick 10.
    drought_tick = _event_tick(
        world,
        "Drought"
    )

    if drought_tick is not None:

        _add_wave(
            actions,
            world,
            plants_by_name,
            LEVEL_THREE_AFTER_DROUGHT,
            tick=drought_tick + 1,
            used_positions=used_positions,
        )

    # Animal/unlock-driven species
    _add_wave(
        actions,
        world,
        plants_by_name,
        LEVEL_THREE_SECOND_WAVE,
        tick=25,
        used_positions=used_positions,
    )

    _add_wave(
        actions,
        world,
        plants_by_name,
        LEVEL_THREE_THIRD_WAVE,
        tick=60,
        used_positions=used_positions,
    )

    _add_wave(
        actions,
        world,
        plants_by_name,
        LEVEL_THREE_ADVANCED_WAVE,
        tick=100,
        used_positions=used_positions,
    )

    # Rain occurs at tick 150.
    rain_tick = _event_tick(
        world,
        "Rain"
    )

    if rain_tick is not None:

        _add_wave(
            actions,
            world,
            plants_by_name,
            LEVEL_THREE_AFTER_RAIN,
            tick=rain_tick + 1,
            used_positions=used_positions,
        )

    return _sort_actions(
        actions
    )


def build_strategy(
    level_number,
    world,
    plants,
    unlock_conditions
):

    if level_number == 1:

        return build_level_one_strategy(
            world,
            plants,
            unlock_conditions
        )

    if level_number == 2:

        return build_level_two_strategy(
            world,
            plants,
            unlock_conditions
        )

    if level_number == 3:

        return build_level_three_strategy(
            world,
            plants,
            unlock_conditions
        )

    raise ValueError(
        f"Unsupported level: "
        f"{level_number}"
    )