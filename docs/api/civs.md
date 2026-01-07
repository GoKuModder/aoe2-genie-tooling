# Civilizations API

Manage civilization data using `CivManager` and `CivHandle`.

## Mental Model

1.  **Civilization**: Defines the starting resources, tech tree, and unique units for a faction.
2.  **Tech Tree**: The `tech_tree_id` points to the layout of the tech tree UI.
3.  **Global Resources**: Resources (Food, Wood, Gold, etc.) are defined globally. Every civ has a table of resource stockpiles. `Actual_Tools_GDP` manages adding/removing resources globally to ensure all civs stay in sync.

## Common Workflows

### Modifying Starting Resources
```python
britons = workspace.civ_manager.get(1)

# Set starting Food (Resource ID 0)
britons.resources[0] = 500
```

### Adding a New Global Resource
```python
# Adds a new resource column to ALL civilizations
new_res_id = workspace.civ_manager.add_resource(default_value=0.0)
print(f"New resource ID: {new_res_id}")
```

## Gotchas & Invariants

*   **Global Sync**: You cannot add a resource to just one civilization. The engine requires all civs to have the exact same number of resource slots. The `CivManager` enforces this.
*   **Team Bonus**: The `team_bonus_id` is just a pointer to a Tech/Effect that applies to allies.

## CivManager

Access via `workspace.civ_manager`.

### Methods

#### `get(civ_id: int) -> CivHandle`
Get a handle for a civilization.

#### `add_resource(default_value: float) -> int`
Adds a new resource to ALL civilizations.

## CivHandle

Wrapper for civilization data.

### Attributes
- `name` (str)
- `tech_tree_id` (int)
- `team_bonus_id` (int)
- `resources` (ResourceAccessor) - Access resources like `civ.resources.food` or by index `civ.resources[0]`.
