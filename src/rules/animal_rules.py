import re

from src.rules.unlock_rules import compare


def _normalise_group_name(
    value: str
) -> str:

    return re.sub(
        r"[^a-z0-9]",
        "",
        value.lower()
    )


def resolve_group(
    group_name: str,
    classifications: dict[str, list[str]]
) -> list[str]:

    if group_name in classifications:
        return classifications[
            group_name
        ]

    wanted = _normalise_group_name(
        group_name
    )

    for name, members in classifications.items():

        if (
            _normalise_group_name(name)
            == wanted
        ):
            return members

    return []


def _state_value(
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


def _species_names(
    value
) -> list[str]:

    if isinstance(
        value,
        list
    ):
        return value

    if value is None:
        return []

    return [value]


def evaluate_animal_requirement(
    requirement: dict,
    world_state,
    classifications: dict[str, list[str]]
) -> bool:

    requirement_type = requirement.get(
        "type"
    )

    if requirement_type in {
        "AND",
        "OR"
    }:

        results = [
            evaluate_animal_requirement(
                item,
                world_state,
                classifications
            )
            for item in requirement.get(
                "conditions",
                []
            )
        ]

        if requirement_type == "AND":
            return all(results)

        return any(results)

    coverage = _state_value(
        world_state,
        "coverage",
        {}
    )

    counts = _state_value(
        world_state,
        "plant_counts",
        {}
    )

    if requirement_type == "coverage":

        names = _species_names(
            requirement.get(
                "species"
            )
        )

        actual = sum(
            coverage.get(
                name,
                0.0
            )
            for name in names
        )

        return compare(
            actual,
            requirement.get(
                "operator",
                ">="
            ),
            requirement.get(
                "threshold",
                0
            )
        )

    if requirement_type == "group_coverage":

        raw_group = requirement.get(
            "species_group",
            []
        )

        if isinstance(
            raw_group,
            str
        ):

            names = resolve_group(
                raw_group,
                classifications
            )

        else:

            names = raw_group

        actual = sum(
            coverage.get(
                name,
                0.0
            )
            for name in names
        )

        return compare(
            actual,
            requirement.get(
                "operator",
                ">="
            ),
            requirement.get(
                "threshold",
                0
            )
        )

    if requirement_type == "count":

        if "species" in requirement:

            names = _species_names(
                requirement.get(
                    "species"
                )
            )

        else:

            raw_group = requirement.get(
                "species_group",
                []
            )

            if isinstance(
                raw_group,
                str
            ):

                names = resolve_group(
                    raw_group,
                    classifications
                )

            elif (
                len(raw_group) == 1
                and raw_group[0]
                not in counts
            ):

                names = (
                    resolve_group(
                        raw_group[0],
                        classifications
                    )
                    or raw_group
                )

            else:

                expanded = []

                for item in raw_group:

                    expanded.extend(
                        resolve_group(
                            item,
                            classifications
                        )
                        or [item]
                    )

                names = expanded

        actual = sum(
            counts.get(
                name,
                0
            )
            for name in names
        )

        return compare(
            actual,
            requirement.get(
                "operator",
                ">="
            ),
            requirement.get(
                "threshold",
                0
            )
        )

    if requirement_type == "dominance":

        total = sum(
            counts.values()
        )

        if total == 0:
            return False

        largest = (
            max(
                counts.values(),
                default=0
            )
            / total
        )

        return largest >= requirement.get(
            "threshold",
            0
        )

    return False


def is_animal_active(
    animal,
    world_state,
    classifications: dict[str, list[str]]
) -> bool:

    return evaluate_animal_requirement(
        animal.requirements,
        world_state,
        classifications
    )


def active_animals(
    animals,
    world_state,
    classifications: dict[str, list[str]]
) -> list:

    return [
        animal
        for animal in animals
        if is_animal_active(
            animal,
            world_state,
            classifications
        )
    ]


def collect_animal_effects(
    animals,
    world_state,
    classifications: dict[str, list[str]]
) -> list[dict]:

    effects = []

    for animal in active_animals(
        animals,
        world_state,
        classifications
    ):

        for effect in animal.effects:

            effects.append(
                {
                    "animal": animal.name,
                    **effect
                }
            )

    return effects