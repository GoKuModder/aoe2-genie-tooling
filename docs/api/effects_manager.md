# Effects Manager

The `EffectManager` controls the creation, deletion, and searching of Tech Effects (Effect Holders). Note that in Genie terminology, a "Tech Effect" is a container that holds a list of "Effect Commands" (the actual actions).

## Mental Model

*   **Effect Holder**: A container with a name and an ID. It doesn't do anything by itself; it just holds commands.
*   **Effect Commands**: The individual instructions inside a holder (e.g., "Add 10 HP to Archers", "Research Chemistry").
*   **Techs use Effects**: Technologies (like "Loom") don't directly modify unit stats. Instead, they point to an Effect ID. When the tech is researched, the engine executes all commands in that Effect Holder.

## Public API

### EffectManager (`Actual_Tools_GDP.Effects.effect_manager`)

Access via `workspace.effect_manager`.

*   `add_new(name: str) -> EffectHandle`: Creates a new, empty effect holder.
*   `get(effect_id: int) -> EffectHandle`: Gets a handle for an existing effect.
*   `copy(source_id: int, target_id: int = None) -> EffectHandle`: Duplicates an effect holder and all its commands.
*   `copy_to_clipboard(effect_id: int)`: Copies an effect to an internal clipboard.
*   `paste(target_id: int = None) -> EffectHandle`: Pastes the clipboard effect to a new or specific ID.
*   `find_by_name(name: str) -> EffectHandle | None`: Searches for an effect by name.
*   `count() -> int`: Returns total number of effect slots.

## Workflows

### Creating a New Effect

```python
# Create a new effect container
effect = workspace.effect_manager.add_new("Super Archer Upgrade")

# Now add commands to it (see EffectHandle)
effect.add_command.attribute_modifier_add(
    a=4, # Unit Class: Archer
    b=10 # Amount: +10 HP
)
```

### Copying an Effect

Useful if you want to create a variation of an existing upgrade.

```python
# Copy existing Fletching effect
fletching = workspace.effect_manager.find_by_name("Fletching")
new_fletching = workspace.effect_manager.copy(fletching.id)
new_fletching.name = "Super Fletching"
```

### Clipboard Operations

Useful for moving effects between unrelated IDs or across files (conceptually, though workspace isolation applies).

```python
workspace.effect_manager.copy_to_clipboard(100)
# ... later ...
workspace.effect_manager.paste() # Pastes to end of list
```

## Gotchas & Invariants

*   **Holders vs Commands**: Don't confuse the *Effect Holder* (managed here) with the *Effect Commands* (managed by `EffectHandle` / `CommandHandle`). The manager deals with the containers.
*   **Tech Links**: Creating an effect does nothing in-game unless a Technology points to it (via `tech.effect_id = effect.id`) or it's triggered by a specific game mechanic (like Civ Bonuses).
*   **ID Stability**: Effect IDs are referenced by Techs. If you move an effect (which isn't directly supported via `move` but can be done via copy/delete), you must update all Techs that point to the old ID.

## Cross-Links

*   [Effect Handle](effects_handle.md)
*   [Techs](../techs.md)
