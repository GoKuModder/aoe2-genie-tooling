# Techs API

Manage technologies using `TechManager` and `TechHandle`.

## Mental Model

Technologies (Techs) are the triggers in the game.
1.  **Research**: When a player clicks a button in a building, they are researching a Tech.
2.  **Cost & Time**: The Tech defines how much it costs and how long it takes.
3.  **Effect Link**: The Tech points to an `Effect ID`. When research completes, that Effect is applied.
4.  **Requirements**: Techs can require other Techs (e.g., "Heavy Plow" requires "Plow").

## Common Workflows

### Modifying a Tech
```python
loom = workspace.tech_manager.get(22)
loom.research_time = 25  # Make it faster
loom.cost_1.amount = 50  # Make it cheaper
```

### Linking to an Effect
```python
# Create effect first
bonus = workspace.effect_manager.create("Super Loom")

# Link tech to it
loom.effect_id = bonus.id
```

## Gotchas & Invariants

*   **Circular Dependencies**: The engine does not prevent circular tech requirements, but they will logic-lock the game.
*   **Effect ID Validity**: If you set `tech.effect_id = -1`, the tech will do nothing upon completion.
*   **Civ Availability**: Techs can be hidden from specific civilizations using the `civilization_id` field (usually set to -1 for all, or specific ID for unique techs).

## TechManager

Access via `workspace.tech_manager`.

### Methods

#### `get(tech_id: int) -> TechHandle`
Get a handle for an existing technology.

#### `add(name: str, ...) -> TechHandle`
Create a new technology.

## TechHandle

Wrapper for technology data.

### Attributes
- `name` (str)
- `research_time` (int)
- `effect_id` (int)
- `cost_1`, `cost_2`, `cost_3` (TechCost objects)
- `required_techs` (list)
