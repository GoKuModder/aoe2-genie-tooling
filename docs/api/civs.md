# Civilizations Manager

The `CivManager` handles the management of Civilizations and their global resources.

## Mental Model

*   **Civilization**: A container for Units and a list of starting Resources.
*   **Units are Per-Civ**: As explained in the Unit Manager, each Civ has its own table of Units. The `CivManager` manages the containers themselves.
*   **Global Resources**: The list of available resources (Food, Wood, Gold, etc.) is global. Every civilization has the same *number* of resource slots, but different *values*.

## Public API

### CivManager (`Actual_Tools_GDP.Civilizations.civ_manager`)

Access via `workspace.civ_manager`.

*   `get(civ_id: int) -> CivHandle`: Gets a civ handle (e.g., 1=Britons).
*   `add_resource(default_value=0.0) -> int`: Adds a new resource type to **ALL** civilizations. Returns the new Resource ID.
*   `remove_resource(index)`: Removes a resource type from **ALL** civilizations.

### CivHandle (`Actual_Tools_GDP.Civilizations.civ_handle`)

*   `name`: Civ name.
*   `tech_tree_effect_id`: ID of the effect that disables units/techs for this civ.
*   `resource`: Accessor for this civ's resource stockpiles.

### ResourceAccessor

*   `get(index) -> float`
*   `set(index, value)`

## Workflows

### Modifying Starting Resources

```python
from Actual_Tools_GDP.Datasets import Resource

# Give Britons (ID 1) 500 extra gold
britons = workspace.civ_manager.get(1)
current_gold = britons.resource.get(Resource.GOLD)
britons.resource.set(Resource.GOLD, current_gold + 500)
```

### Adding a New Resource Type

If you are making a total conversion mod and want a new resource (e.g., "Mana").

```python
# Add "Mana" slot to all civs, initialized to 0
mana_id = workspace.civ_manager.add_resource(default_value=0.0)
print(f"Mana is Resource ID {mana_id}")
```

## Gotchas & Invariants

*   **Civ Order**: The order of civilizations is fixed by the game engine (0=Gaia, 1=Britons, etc.). Adding/Removing civs is complex and usually requires modifying other files (string tables, UI). The manager supports `add_civ` (if implemented), but be careful.
*   **Gaia (Civ 0)**: This is the "Nature" civilization. Units here (Trees, Wolves) are neutral.

## Cross-Links

*   [Units Manager](../units/units_manager.md)
*   [Datasets](../datasets.md)
