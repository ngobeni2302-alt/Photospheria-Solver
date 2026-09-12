from src.rules.animal_rules import active_animals
from src.rules.plant_rules import can_plant
from src.rules.unlock_rules import is_plant_unlocked
from src.simulation.world_state import WorldState


class Simulator:

    def __init__(
        self,
        world,
        plants,
        animals,
        classifications,
        unlock_conditions
    ):

        self.world = world

        self.plants = plants

        self.animals = animals

        self.classifications = (
            classifications
        )

        self.unlock_conditions = (
            unlock_conditions
        )

        self.plants_by_index = {
            plant.index: plant
            for plant in plants
        }

    def run(
        self,
        actions
    ) -> WorldState:

        state = WorldState()

        plantable_count = len(
            self.world.get_plantable_cells()
        )

        sorted_actions = sorted(
            actions,
            key=lambda action: (
                action.tick,
                action.plant_index,
                action.x,
                action.y
            )
        )

        for action in sorted_actions:

            state.current_tick = (
                action.tick
            )

            state.events.update(
                self.world
                .get_events_up_to_tick(
                    action.tick
                )
            )

            plant = self.plants_by_index.get(
                action.plant_index
            )

            if plant is None:
                continue

            cell = self.world.get_cell(
                action.y,
                action.x
            )

            occupied = set(
                state.plant_positions
            )

            if not can_plant(
                plant,
                cell,
                action.tick,
                self.world,
                occupied
            ):
                continue

            if not is_plant_unlocked(
                plant.name,
                self.unlock_conditions,
                state
            ):
                continue

            state.plant_positions[
                (
                    cell.row,
                    cell.col
                )
            ] = plant.name

            state.recalculate(
                plantable_count
            )

            if self.world.animals_enabled:

                animals_now = active_animals(
                    self.animals,
                    state,
                    self.classifications
                )

                state.active_animal_names = {
                    animal.name
                    for animal
                    in animals_now
                }

                state.recalculate(
                    plantable_count
                )

        state.events.update(
            self.world
            .get_events_up_to_tick(
                self.world.ticks - 1
            )
        )

        state.current_tick = (
            self.world.ticks - 1
        )

        return state