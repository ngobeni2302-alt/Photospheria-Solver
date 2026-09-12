from dataclasses import dataclass


@dataclass(frozen=True)
class Cell:
    row: int
    col: int
    terrain: int
    soil: int

    def is_plantable(self) -> bool:
        return self.terrain == 0