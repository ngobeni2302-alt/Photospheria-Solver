# Photospheria Solver

## Overview

Photospheria Solver is a Python optimisation project built for the Entelect Hackathon.

The challenge takes place on the fictional planet **Photospheria**, where different plant species interact with each other and with the environment.

The goal of the solver is to create a planting strategy that produces a diverse and sustainable ecosystem.

This repository is currently focused on **Level 1: Greenhouse Study**.

---

## Level 1

Level 1 takes place inside a greenhouse.

The supplied Level 1 world contains:

- World size: **50 x 50**
- Simulation length: **500 ticks**
- Animals: **Disabled**
- Seasons: **Enabled**

The season changes are:

| Tick | Season |
|------|--------|
| 0 - 99 | Initial season |
| 100 | Summer |
| 200 | Autumn |
| 300 | Winter |
| 400 | Spring |

The level information is stored in:

```text
data/1.json
```

The level file also contains the terrain and soil information for the available cells.

---

## Goal

The goal of the solver is to decide:

- Which plant should be planted
- Where the plant should be planted
- When the plant should be planted

A planting action is based on:

```text
tick
plant
x coordinate
y coordinate
```

The strategy should try to:

- Increase plant diversity
- Keep plants alive for as long as possible
- Use suitable soil for each plant
- Respect terrain restrictions
- Make use of plant spreading
- Consider seasonal changes
- Respect plant unlock conditions
- Produce deterministic results

---

## Project Structure

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

## How the Solver Works

The project is designed around the following flow:

```text
Level 1 JSON
     ↓
Resource Loader
     ↓
World + Plant Data
     ↓
Plant Rules
     ↓
Simulation
     ↓
Strategy / Optimiser
     ↓
Planting Actions
     ↓
solution.json
```

### 1. Load the resources

`resource_loader.py` reads the supplied JSON files.

These include:

- Level information
- Plant information
- Plant unlock conditions
- Plant classifications
- Animal information

Although animals are included in the common resources, animals are disabled in Level 1.

---

## Plant Model

Each plant is converted from JSON into a Python object.

Plant information includes properties such as:

- Plant name
- Plant index
- Time to maturity
- Spread rate
- Spread type
- Spread range
- Root type
- Invasiveness
- Preferred soil
- Weaknesses
- Special rules

This allows the solver to work with plant information using Python objects instead of raw JSON dictionaries.

---

## World Model

The Level 1 world is loaded from:

```text
data/1.json
```

Each supplied cell contains:

```text
row
column
terrain
soil
```

The solver stores these cells using their coordinates.

Example:

```python
world.get_cell(0, 10)
```

The world model also stores:

- Number of rows
- Number of columns
- Number of ticks
- Whether animals are enabled
- Season commands

---

## Seasons

Level 1 includes season changes.

The solver reads these directly from `1.json` instead of hard-coding them into the simulation.

The Level 1 season events are:

```text
Tick 100 -> Summer
Tick 200 -> Autumn
Tick 300 -> Winter
Tick 400 -> Spring
```

Season effects will later be applied during simulation when the appropriate plant rules are implemented.

---

## Unlock Conditions

Some plants are not immediately available.

The unlock engine reads:

```text
data/plant_unlock_conditions.json
```

The current rule engine supports condition types including:

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

Plants without an unlock rule are treated as available from the beginning.

---

## Level 1 Strategy

The Level 1 strategy will be developed in stages.

The solver will:

1. Find valid plantable cells.
2. Match plants with suitable soil.
3. Place starting plants.
4. Allow plants to mature.
5. Simulate plant spreading.
6. Track season changes.
7. Evaluate plant interactions.
8. Increase ecosystem diversity.
9. Preserve useful species until the final tick.
10. Generate the final planting plan.

The strategy can later be improved using an optimisation algorithm.

---

## Deterministic Output

The hackathon requires the solution to be deterministic.

This means:

```text
Same input
    ↓
Same program
    ↓
Same decisions
    ↓
Same solution.json
```

Random behaviour should therefore either be avoided or use a fixed seed.

The final source code must reproduce the submitted `solution.json`.

---

## solution.json

`solution.json` represents the planting decisions produced by the solver.

The source code is responsible for generating this file.

Conceptually, each decision contains:

```text
tick
plant index
x coordinate
y coordinate
```

The exact submission structure should follow the official Photospheria output specification.

---

## Running the Project

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Run the tests:

```bash
python -m pytest -v
```

Run the solver:

```bash
python main.py
```

Once the solver is complete, running `main.py` will generate:

```text
solution.json
```

---

## Testing

The project uses `pytest`.

Current tests check that:

- Plants can be loaded
- Animals can be loaded
- Plant classifications can be loaded
- Unlock conditions can be loaded
- Level 1 can be loaded
- The Level 1 dimensions are correct
- Level 1 cell information can be accessed
- Level 1 season changes are recognised
- Basic plant unlock logic works

Current test status:

```text
8 tests passed
```

Run all tests using:

```bash
python -m pytest -v
```

---

## Current Progress

```text
Project structure        
Plant model              
Animal model            
Resource loader          
Plant data loading      
Level 1 loading          
World model              
Cell model              
Season loading           
Basic unlock rules       
Automated tests          

Plant placement rules    
Growth simulation        
Spread simulation        
Season effects           
Scoring                   
Optimisation strategy    
solution.json generator  
```

---

## Future Levels

The project structure is designed so that later Photospheria levels can reuse the same engine.

Future levels may introduce additional mechanics such as:

- Animals
- More terrain restrictions
- Weather
- More plant species
- More environmental interactions

Instead of creating a new solver for every level, the goal is to reuse the same simulation engine with different level input files.

---

## Technology

The project currently uses:

- **Python**
- **JSON**
- **pytest**
- **Python dataclasses**

Python was selected because the challenge involves data processing, simulation, searching possible strategies and producing JSON output.

---
