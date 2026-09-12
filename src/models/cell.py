from dataclasses import dataclass


@dataclass
class Cell:
    row: int
    col: int
    terrain: int
    soil: int

    def is_plantable(self):
        return self.terrain == 0