from dataclasses import dataclass


@dataclass(frozen=True)
class PlantingAction:
    tick: int
    plant_index: int
    x: int
    y: int

    def to_dict(self):
        return {
            "tick": self.tick,
            "plant": self.plant_index,
            "x": self.x,
            "y": self.y
        }