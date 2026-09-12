from dataclasses import dataclass, field

from src.models.cell import Cell


@dataclass
class World:
    rows: int
    cols: int
    ticks: int
    animals_enabled: bool

    cells: dict[tuple[int, int], Cell] = field(
        default_factory=dict
    )

    commands: list[dict] = field(
        default_factory=list
    )

    def get_cell(self, row: int, col: int):
        return self.cells.get(
            (row, col)
        )

    def has_cell(self, row: int, col: int) -> bool:
        return (row, col) in self.cells

    def get_plantable_cells(self) -> list[Cell]:
        return [
            cell
            for cell in self.cells.values()
            if cell.is_plantable()
        ]

    def get_season_for_tick(self, tick: int):
        current_season = None

        commands = sorted(
            self.commands,
            key=lambda item: item.get("tick", -1)
        )

        for command in commands:

            if command.get("type") != "season":
                continue

            if command.get("tick", 0) <= tick:
                current_season = command.get("season")

        return current_season

    def get_events_up_to_tick(
        self,
        tick: int
    ) -> set[str]:

        return {
            command["event"]
            for command in self.commands
            if (
                command.get("type") == "event"
                and command.get("tick", 0) <= tick
            )
        }

    def get_commands_at_tick(
        self,
        tick: int
    ) -> list[dict]:

        return [
            command
            for command in self.commands
            if command.get("tick") == tick
        ]