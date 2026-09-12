def compare(
    actual_value,
    operator,
    required_value
) -> bool:

    operations = {
        ">": actual_value > required_value,
        ">=": actual_value >= required_value,
        "<": actual_value < required_value,
        "<=": actual_value <= required_value,
        "==": actual_value == required_value,
        "!=": actual_value != required_value,
    }

    return operations.get(
        operator,
        False
    )


def _get_value(
    world_state,
    name,
    default
):

    if isinstance(
        world_state,
        dict
    ):
        return world_state.get(
            name,
            default
        )

    return getattr(
        world_state,
        name,
        default
    )


def evaluate_condition(
    condition: dict,
    world_state
) -> bool:

    if "op" in condition:

        operation = condition["op"]

        children = condition.get(
            "children",
            []
        )

        if operation == "AND":

            return all(
                evaluate_condition(
                    child,
                    world_state
                )
                for child in children
            )

        if operation == "OR":

            return any(
                evaluate_condition(
                    child,
                    world_state
                )
                for child in children
            )

        return False

    condition_type = condition.get(
        "type"
    )

    species = _get_value(
        world_state,
        "species",
        set()
    )

    coverage = _get_value(
        world_state,
        "coverage",
        {}
    )

    plant_counts = _get_value(
        world_state,
        "plant_counts",
        {}
    )

    events = _get_value(
        world_state,
        "events",
        set()
    )

    features = _get_value(
        world_state,
        "features",
        {}
    )

    if condition_type == "species_present":

        return (
            condition.get("species")
            in species
        )

    if condition_type == "species_absent":

        return (
            condition.get("species")
            not in species
        )

    if condition_type == "coverage":

        actual = coverage.get(
            condition.get("plant"),
            0.0
        )

        return compare(
            actual,
            condition.get("operator"),
            condition.get("value")
        )

    if condition_type == "count":

        actual = plant_counts.get(
            condition.get("plant"),
            0
        )

        return compare(
            actual,
            condition.get("operator"),
            condition.get("value")
        )

    if condition_type == "event":

        return (
            condition.get("event")
            in events
        )

    if condition_type == "feature_count":

        actual = features.get(
            condition.get("feature"),
            0
        )

        return compare(
            actual,
            condition.get("operator"),
            condition.get("value")
        )

    return False


def is_plant_unlocked(
    plant_name: str,
    unlock_conditions: list[dict],
    world_state
) -> bool:

    for rule in unlock_conditions:

        if rule.get(
            "plant"
        ) == plant_name:

            return evaluate_condition(
                rule["unlock"],
                world_state
            )

    return True