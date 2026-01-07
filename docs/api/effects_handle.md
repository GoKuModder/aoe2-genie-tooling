# Effect Handle & Commands

The `EffectHandle` allows you to manage the commands inside an effect holder. The `CommandHandle` represents a single command (action) within that list.

## Mental Model

*   **Command List**: An `EffectHandle` wraps a list of commands. You can append, insert, remove, or modify commands.
*   **Cryptic Parameters**: Raw effect commands use generic parameters `A`, `B`, `C`, `D` whose meaning changes based on the `Command Type`.
    *   Example: For "Attribute Modifier", `A` is the Unit ID, `B` is the Amount.
    *   Example: For "Research Tech", `A` is the Tech ID.
*   **Typed Builders**: `Actual_Tools_GDP` provides `add_command` (a builder) to hide these cryptic parameters behind named arguments.

## Public API

### EffectHandle (`Actual_Tools_GDP.Effects.effect_handle`)

*   `commands`: List of `CommandHandle` objects.
*   `add_command`: Access to the `EffectCommandBuilder` (fluent API).
*   `new_command(type, a, b, c, d)`: Low-level method to add a raw command.
*   `remove_command(index)`: Removes a command.
*   `clear_commands()`: Removes all commands.

### CommandHandle (`Actual_Tools_GDP.Effects.command_handle`)

Wraps an individual command.

*   `type` (int): Command type ID.
*   `a`, `b`, `c` (int): Integer parameters.
*   `d` (float): Float parameter.
*   `unit_id`, `resource_id`, `attribute_id` (properties): Semantic aliases for `a`, `b`, etc., depending on the command type (if implemented).

## Workflows

### Adding Commands via Builder

This is the recommended way. See [Effect Builder](effects_builder.md) for details.

```python
effect.add_command.attribute_modifier_multiply(
    a=4, # Archer Class
    b=-1, # Attribute: HP (Legacy mapping, use Enums!)
    c=9, # Multiply mode
    d=1.2 # +20% HP
)
```

### Inspecting Commands

```python
for cmd in effect.commands:
    print(f"Type: {cmd.type}, A: {cmd.a}, B: {cmd.b}")
```

### Modifying Commands

```python
# Change the amount of the first command
cmd = effect.commands[0]
cmd.d = 50.0 # Set float value
```

## Gotchas & Invariants

*   **Parameter Types**: `A`, `B`, `C` are strictly integers (16-bit or 32-bit depending on version). `D` is strictly a float.
*   **Legacy Data**: The Genie Engine has evolved. Some command types are deprecated or behave differently in DE. The library blindly passes values to the engine; it doesn't enforce game-logic rules (like "you can't modify attribute 50").
*   **Order**: Command execution order usually doesn't matter, but for some complex modding scenarios (like stacked triggers), it might.

## Cross-Links

*   [Effects Manager](effects_manager.md)
*   [Effect Builder](effects_builder.md)
