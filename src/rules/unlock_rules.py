def compare(actual_value, operator, required_value):
    if operator == ">":
        return actual_value > required_value

    if operator == ">=":
        return actual_value >= required_value

    return False


def evaluate_condition(condition, world_state):
    # Handle AND / OR groups
    if "op" in condition:
        operation = condition["op"]
        children = condition["children"]

        if operation == "AND":
            return all(
                evaluate_condition(child, world_state)
                for child in children
            )

        if operation == "OR":
            return any(
                evaluate_condition(child, world_state)
                for child in children
            )

    condition_type = condition["type"]

    if condition_type == "species_present":
        species = condition["species"]
        return species in world_state["species"]

    if condition_type == "species_absent":
        species = condition["species"]
        return species not in world_state["species"]

    if condition_type == "coverage":
        plant = condition["plant"]
        operator = condition["operator"]
        required_value = condition["value"]

        actual_value = world_state["coverage"].get(plant, 0)

        return compare(
            actual_value,
            operator,
            required_value
        )

    if condition_type == "count":
        plant = condition["plant"]
        operator = condition["operator"]
        required_value = condition["value"]

        actual_value = world_state["plant_counts"].get(plant, 0)

        return compare(
            actual_value,
            operator,
            required_value
        )

    if condition_type == "event":
        event = condition["event"]
        return event in world_state["events"]

    if condition_type == "feature_count":
        feature = condition["feature"]
        operator = condition["operator"]
        required_value = condition["value"]

        actual_value = world_state["features"].get(feature, 0)

        return compare(
            actual_value,
            operator,
            required_value
        )

    return False


def is_plant_unlocked(plant_name, unlock_conditions, world_state):
    for plant_rule in unlock_conditions:

        if plant_rule["plant"] == plant_name:
            return evaluate_condition(
                plant_rule["unlock"],
                world_state
            )

    # Plants with no unlock rule are available from the start
    return True