from dataclasses import dataclass, field


@dataclass
class WorldState:
    current_tick: int = 0

    plant_counts: dict[
        str,
        int
    ] = field(
        default_factory=dict
    )

    coverage: dict[
        str,
        float
    ] = field(
        default_factory=dict
    )

    species: set[str] = field(
        default_factory=set
    )

    events: set[str] = field(
        default_factory=set
    )

    features: dict[
        str,
        float
    ] = field(
        default_factory=dict
    )

    plant_positions: dict[
        tuple[int, int],
        str
    ] = field(
        default_factory=dict
    )

    active_animal_names: set[str] = field(
        default_factory=set
    )

    def recalculate(
        self,
        plantable_cell_count: int
    ) -> None:

        counts = {}

        for plant_name in (
            self.plant_positions.values()
        ):

            counts[plant_name] = (
                counts.get(
                    plant_name,
                    0
                )
                + 1
            )

        self.plant_counts = counts

        denominator = max(
            plantable_cell_count,
            1
        )

        self.coverage = {
            name: count / denominator
            for name, count
            in self.plant_counts.items()
        }

        self.species = (
            set(self.plant_counts)
            |
            set(
                self.active_animal_names
            )
        )