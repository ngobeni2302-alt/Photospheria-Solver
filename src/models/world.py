from dataclasses import dataclass, field

from src.models.cell import Cell


@dataclass
class World:
    rows: int
    cols: int
    ticks: int
    animals_enabled: bool

    cells: dict[tuple[int, int], Cell] = field(default_factory=dict)
    commands: list[dict] = field(default_factory=list)

    def get_cell(self, row, col):
        return self.cells.get((row, col))

    def has_cell(self, row, col):
        return (row, col) in self.cells

    def get_plantable_cells(self):
        return [
            cell
            for cell in self.cells.values()
            if cell.is_plantable()
        ]

    def get_season_for_tick(self, tick):
        current_season = None

        for command in self.commands:
            if command["type"] != "season":
                continue

            if command["tick"] <= tick:
                current_season = command["season"]

        return current_season