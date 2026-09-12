# Photospheria Solver

## Overview

Photospheria Solver is a Python optimisation project built for the Entelect Hackathon.

The challenge takes place on the fictional planet **Photospheria**, where plant species interact with each other and with their environment.

The purpose of the solver is to analyse the supplied world, select suitable plants and planting locations, and generate a deterministic planting strategy.

This repository is currently focused on:

# Level 1 — Greenhouse Study

The overall challenge goal is to create a diverse biological sample and keep as many species alive for as long as possible.

---

## Level 1 Environment

The supplied Level 1 input is stored in:

```text
data/1.json
```

Level 1 contains:

```text
World size:       50 x 50
Ticks:            500
Animals enabled:  False
Seasons:          Enabled
```

The Level 1 file also contains the available cells and their:

```text
row
column
terrain
soil
```

The solver reads these values directly instead of manually creating a world.

---

## Level 1 Seasons

The Level 1 input contains season commands.

The supplied season changes are:

| Tick | Season |
|------|--------|
| 100 | Summer |
| 200 | Autumn |
| 300 | Winter |
| 400 | Spring |

The solver reads these commands directly from `1.json`.

This means the season schedule is not hard-coded into the main solver.

---

## Goal of the Solver

The solver must decide:

```text
Which plant should be planted?
Where should it be planted?
When should it be planted?
```

A planting action contains:

```text
tick
plant index
x coordinate
y coordinate
```

The project will gradually improve its strategy to consider:

- Plant diversity
- Suitable soil
- Terrain restrictions
- Plant maturity
- Plant spreading
- Plant weaknesses
- Plant special rules
- Unlock conditions
- Seasons
- Long-term survival
- Final ecosystem diversity

---

# Project Flow

The project currently follows this flow:

```text
                    INPUT
                      │
                      ▼
                 data/1.json
                      │
                      ▼
              Resource Loader
                      │
          ┌───────────┴───────────┐
          ▼                       ▼
      World Data               Plant Data
          │                       │
          └───────────┬───────────┘
                      ▼
                 Strategy
                      │
                      ▼
              Planting Actions
                      │
                      ▼
              Solution Writer
                      │
                      ▼
               solution.json
```

Running:

```bash
python main.py
```

will eventually perform the complete Level 1 pipeline.

The current implementation already loads Level 1 and can generate a baseline set of planting actions.

---

# Project Structure

```text
Photospheria-Solver/
│
├── main.py
├── README.md
├── solution.json
├── requirements.txt
│
├── data/
│   ├── 1.json
│   ├── plant_dataset.json
│   ├── plant_unlock_conditions.json
│   ├── animals.json
│   └── classifications.json
│
├── src/
│   │
│   ├── __init__.py
│   ├── level_config.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── plant.py
│   │   ├── animal.py
│   │   ├── cell.py
│   │   ├── world.py
│   │   └── planting_action.py
│   │
│   ├── loaders/
│   │   ├── __init__.py
│   │   └── resource_loader.py
│   │
│   ├── rules/
│   │   ├── __init__.py
│   │   ├── unlock_rules.py
│   │   ├── plant_rules.py
│   │   ├── animal_rules.py
│   │   └── spread_rules.py
│   │
│   ├── simulation/
│   │   ├── __init__.py
│   │   ├── simulator.py
│   │   └── world_state.py
│   │
│   ├── solver/
│   │   ├── __init__.py
│   │   ├── strategy.py
│   │   ├── optimizer.py
│   │   └── scorer.py
│   │
│   └── output/
│       ├── __init__.py
│       └── solution_writer.py
│
└── tests/
    ├── test_resource_loader.py
    ├── test_unlock_rules.py
    ├── test_plant_rules.py
    ├── test_animal_rules.py
    ├── test_simulator.py
    └── test_solver.py
```

---

# Input Files

## `1.json`

This is the Level 1 world supplied by the hackathon.

It contains:

```text
animals_enabled
rows
cols
ticks
cells
commands
```

Example cell:

```json
{
  "row": 0,
  "col": 21,
  "terrain": 0,
  "soil": 1
}
```

The solver uses the supplied cell information instead of assuming every coordinate is plantable.

---

## `plant_dataset.json`

Contains the Photospherian plant catalogue.

Each plant contains information such as:

```text
plant name
plant index
growth properties
preferred soil
rules
role
```

Growth information includes properties such as:

```text
time to maturity
spread rate
spread mechanism
spread type
spread range
root type
invasiveness rank
```

---

## `plant_unlock_conditions.json`

Contains the conditions required to unlock certain plant species.

The current unlock engine supports conditions such as:

```text
AND
OR
species_present
species_absent
coverage
count
event
feature_count
```

If a plant does not have an unlock condition, the current strategy treats it as available at the beginning.

---

## `animals.json`

Contains animal information.

Although the common resource data contains animals, Level 1 has:

```text
animals_enabled = false
```

Animal simulation is therefore not currently used for Level 1.

The files remain in the project because later levels may enable animals.

---

## `classifications.json`

Contains plant classification information used by the Photospheria ecosystem.

This data is loaded and kept available for later strategy and scoring logic.

---

# Models

## Plant

`src/models/plant.py`

Represents one Photospherian plant.

The plant model stores the data loaded from the plant catalogue.

---

## Animal

`src/models/animal.py`

Represents an animal and its:

```text
id
name
requirements
effects
```

Animals are not currently active in Level 1.

---

## Cell

`src/models/cell.py`

Represents one supplied world cell.

A cell stores:

```text
row
column
terrain
soil
```

The cell model also determines whether the terrain may be considered plantable.

---

## World

`src/models/world.py`

Represents the loaded Photospheria level.

It stores:

```text
rows
columns
ticks
animals_enabled
cells
commands
```

It also provides helper methods such as:

```python
world.get_cell(row, col)

world.has_cell(row, col)

world.get_plantable_cells()

world.get_season_for_tick(tick)
```

---

## PlantingAction

`src/models/planting_action.py`

Represents one decision made by the solver.

A planting action currently stores:

```python
tick
plant_index
x
y
```

The action can be converted into JSON-ready data using:

```python
action.to_dict()
```

---

# Resource Loader

`src/loaders/resource_loader.py`

The resource loader is responsible for reading the supplied JSON files and converting them into Python objects.

It currently supports:

```python
load_plants()

load_animals()

load_classifications()

load_unlock_conditions()

load_level()
```

For Level 1:

```python
world = load_level("1.json")
```

creates the Level 1 `World` object.

---

# Unlock Rules

`src/rules/unlock_rules.py`

The unlock engine determines whether a plant is currently available.

The engine supports nested:

```text
AND
OR
```

conditions and several individual condition types.

Plants without an unlock definition are currently treated as starting plants.

---

# Current Level 1 Strategy

`src/solver/strategy.py`

The current Level 1 strategy is a **baseline deterministic strategy**.

It currently:

1. Loads all plants.
2. Reads the plant unlock conditions.
3. Finds plants without unlock requirements.
4. Finds suitable Level 1 cells.
5. Checks each plant's preferred soil.
6. Avoids reusing the same starting coordinate.
7. Spreads starting positions across available cells.
8. Creates planting actions at tick `0`.
9. Returns the actions to the output writer.

This is not the final optimisation strategy.

Its purpose is to establish a complete working pipeline:

```text
Level input
    ↓
strategy
    ↓
actions
    ↓
solution.json
```

The strategy will later be improved using actual plant growth and ecosystem simulation.

---

# solution.json

`solution.json` is the output produced by the solver.

It is **not an explanation of how the challenge was solved**.

The source code represents how the problem was solved.

`solution.json` represents the actual planting decisions made by the program.

Conceptually:

```text
code.zip
    =
HOW the problem was solved

solution.json
    =
WHAT planting decisions the solver produced
```

Each planting action contains:

```text
tick
plant index
x
y
```

The current writer produces a JSON representation of the generated actions.

The final JSON structure must match the official Photospheria submission specification.

---

# Solution Writer

`src/output/solution_writer.py`

The solution writer takes the planting actions produced by the strategy and writes them to:

```text
solution.json
```

Before writing, actions are sorted using:

```text
tick
plant index
x
y
```

This helps ensure deterministic output.

---

# Running the Solver

First activate the virtual environment:

```bash
source .venv/bin/activate
```

Then run:

```bash
python main.py
```

The current process is:

```text
Loading Photospheria Level 1
            ↓
Loading plants
            ↓
Loading unlock rules
            ↓
Finding starting plants
            ↓
Finding suitable cells
            ↓
Creating planting actions
            ↓
Writing solution.json
```

The terminal should display information about the Level 1 world and the actions selected by the current strategy.

---

# Deterministic Output

The challenge requires deterministic behaviour.

That means:

```text
Same input
      ↓
Same source code
      ↓
Same strategy
      ↓
Same planting actions
      ↓
Same solution.json
```

The solver therefore sorts cells, plants and output actions instead of relying on unpredictable ordering.

Random behaviour is currently avoided.

---

# Running the Tests

The project uses `pytest`.

Activate the environment:

```bash
source .venv/bin/activate
```

Run all tests:

```bash
python -m pytest -v
```

The project has already verified:

```text
Plant loading
Animal loading
Classification loading
Unlock-condition loading
Level 1 loading
Level dimensions
Level cells
Season commands
Basic unlock behaviour
```

Additional solver/output tests are being added as the Level 1 strategy develops.

---

# Next Development Steps

The next major goal is to move from a simple baseline planting strategy to an actual ecosystem simulation.

The planned flow is:

```text
Plant placement validation
          ↓
Plant maturity
          ↓
Plant spreading
          ↓
Season effects
          ↓
Plant interactions
          ↓
Unlock new species
          ↓
Score ecosystem
          ↓
Try alternative strategies
          ↓
Choose better strategy
          ↓
solution.json
```

The solver will continue to produce `solution.json`, but the quality of the generated planting plan will improve as more Photospheria mechanics are implemented.

---

# Technology

The project currently uses:

```text
Python
JSON
pytest
Python dataclasses
```

Python was selected because the Photospheria challenge involves:

```text
Data processing
Simulation
Rule evaluation
Search
Optimisation
JSON generation
```

---

# Level 1 Status

The project can currently:

```text
Read the actual Level 1 input          
Understand the supplied world cells   
Read plant information                
Read unlock information               
Read season changes                   
Find starting plants                  
Find suitable starting cells         
Create planting actions               
Generate solution.json               
```

The next objective is not simply to make the output file exist.

The next objective is to make the generated **Level 1 strategy smarter and more competitive**.