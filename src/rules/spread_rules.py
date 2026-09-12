def spread_offsets(
    spread_type: str,
    spread_range: int
) -> list[tuple[int, int]]:

    offsets = []

    for distance in range(
        1,
        spread_range + 1
    ):

        if spread_type == "VonNeumann":

            offsets.extend(
                [
                    (distance, 0),
                    (-distance, 0),
                    (0, distance),
                    (0, -distance),
                ]
            )

        elif spread_type == "Moore":

            for dr in range(
                -distance,
                distance + 1
            ):

                for dc in range(
                    -distance,
                    distance + 1
                ):

                    if (
                        (dr, dc) != (0, 0)
                        and max(
                            abs(dr),
                            abs(dc)
                        ) == distance
                    ):

                        offsets.append(
                            (dr, dc)
                        )

        elif spread_type == "Row":

            offsets.extend(
                [
                    (0, distance),
                    (0, -distance),
                ]
            )

        elif spread_type == "Column":

            offsets.extend(
                [
                    (distance, 0),
                    (-distance, 0),
                ]
            )

        elif spread_type == "CrossHatch":

            offsets.extend(
                [
                    (
                        distance,
                        distance
                    ),
                    (
                        distance,
                        -distance
                    ),
                    (
                        -distance,
                        distance
                    ),
                    (
                        -distance,
                        -distance
                    ),
                ]
            )

    return sorted(
        set(offsets)
    )