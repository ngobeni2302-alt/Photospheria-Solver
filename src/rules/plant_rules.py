def can_plant(
    plant,
    cell,
    tick: int,
    world,
    occupied_positions: set[
        tuple[int, int]
    ] | None = None
) -> bool:

    if cell is None:
        return False

    if tick < 0:
        return False

    if tick >= world.ticks:
        return False

    if not cell.is_plantable():
        return False

    if (
        cell.soil
        not in plant.preferred_soil
    ):
        return False

    occupied_positions = (
        occupied_positions
        or set()
    )

    if (
        cell.row,
        cell.col
    ) in occupied_positions:

        return False

    return True