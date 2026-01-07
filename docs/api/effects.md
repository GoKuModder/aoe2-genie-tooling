# Effects API

Manage effects and effect commands using `EffectManager` and `EffectHandle`.

## Mental Model

Effects in Age of Empires 2 are containers for "Commands".
1.  **Effect (Container)**: Defines the name of the modification (e.g., "Fletching"). It holds a list of commands.
2.  **Command (Action)**: The actual logic (e.g., "Add +1 Range to Archers").
3.  **Tech Linking**: A Technology (Tech) points to an Effect ID. When the tech is researched, the game executes all commands in that Effect.

## Common Workflows

### Creating a New Effect
```python
# Create the container
effect = workspace.effect_manager.create("New Civ Bonus")

# It starts empty. You must add commands.
```

### Adding Commands (Fluent API)
Use `add_command` to access the `EffectCommandBuilder`. It provides typed methods so you don't have to remember "Command Type 4 is multiply".
```python
# Mode 4 = Multiply, Attribute 0 = HP
effect.add_command.attribute_modifier_multiply(
    a=9,    # Unit Class (Archers)
    b=0,    # Attribute (Hit Points)
    d=1.1   # 1.1x multiplier (10% increase)
)

# Mode 0 = Add, Attribute 9 = Attack
effect.add_command.attribute_modifier_add(
    a=4,    # Unit ID (Archer)
    b=9,    # Attribute (Attack)
    d=1.0   # +1 Attack
)
```

## Gotchas & Invariants

*   **Commands Execute in Order**: The game processes commands top-to-bottom.
*   **One-Way Linking**: Techs point to Effects. Effects do *not* know which Techs use them. If you delete an Effect, any Tech referencing it will be broken (validation will catch this).
*   **Hardcoded Types**: While the builder helps, you still need to know Unit Class IDs and Attribute IDs. Use the `Actual_Tools_GDP.Datasets` enums (e.g. `Attribute.HIT_POINTS`) to make your code readable.

## EffectManager

Access via `workspace.effect_manager`.

### Methods

#### `get(effect_id: int) -> EffectHandle`
Get a handle for an existing effect.

#### `create(name: str) -> EffectHandle`
Create a new effect (aliased as `add_new`).

## EffectHandle

Wrapper for effect data.

### Properties
- `name` (str)
- `commands` (list of CommandHandle)

### Methods

#### `add_command`
Returns an `EffectCommandBuilder` to fluently add commands.

## EffectCommandBuilder

Fluent interface for adding commands.

### Methods

#### `attribute_modifier_multiply(a, b, c, d)`
Adds a command to multiply an attribute.
- **a**: Unit/Class ID
- **b**: Attribute ID
- **c**: Mode (usually 4 for multiply class, 5 for multiply unit)
- **d**: Multiplier value (float)

#### `attribute_modifier_add(a, b, c, d)`
Adds a command to add to an attribute.
- **a**: Unit/Class ID
- **b**: Attribute ID
- **c**: Mode (usually 0 for add to unit, 4 for add to class)
- **d**: Value to add (float)

#### `modify_tech(...)`
Adds a command to modify a technology (e.g., enable/disable).
