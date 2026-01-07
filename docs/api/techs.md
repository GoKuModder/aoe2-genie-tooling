# Techs Manager

The `TechManager` handles the creation, deletion, and searching of Technologies.

## Mental Model

*   **Technology**: A "Tech" is an item that can be researched at a building. It has a cost, a research time, and most importantly, it links to an **Effect**.
*   **Separation of Concerns**: The Tech itself defines *how* it is researched (cost, time, location). The Effect defines *what happens* when it is researched.
*   **Unique Techs**: Civilizations often have unique techs. These are just normal techs that are only available in that civ's tech tree (or enabled via effects).

## Public API

### TechManager (`Actual_Tools_GDP.Techs.tech_manager`)

Access via `workspace.tech_manager`.

*   `add_new(name: str) -> TechHandle`: Creates a new tech.
*   `get(tech_id: int) -> TechHandle`: Gets a handle.
*   `find_by_name(name: str) -> TechHandle | None`: Searches by name.
*   `copy(source_id: int, target_id: int = None) -> TechHandle`: Copies a tech.

### TechHandle (`Actual_Tools_GDP.Techs.tech_handle`)

*   `id`: Tech ID.
*   `name`: Internal name.
*   `research_time`: Time in seconds.
*   `effect_id`: ID of the Effect to trigger upon completion.
*   `research_location`: ID of the Unit (building) where this is researched (DE mostly uses the Building's `tech_id` list instead).
*   `resource_costs`: List of `TechCost` objects (Type, Amount, Flag).

## Workflows

### Creating a New Tech

```python
# 1. Create the Tech
tech = workspace.tech_manager.add_new("Super Loom")
tech.research_time = 30.0

# 2. Set Cost (50 Food)
from Actual_Tools_GDP.Datasets import Resource, TechCostType
tech.resource_costs[0].type = Resource.FOOD
tech.resource_costs[0].amount = 50
tech.resource_costs[0].flag = TechCostType.PAY_COST

# 3. Link to Effect
effect = workspace.effect_manager.add_new("Super Loom Effect")
tech.effect_id = effect.id
```

## Gotchas & Invariants

*   **Costs**: Techs usually support up to 3 cost types. The list is fixed-size in older versions but dynamic in DE. The handles abstract this.
*   **Research Location**: In older engine versions, the Tech defined where it was researched. In DE, the Building (Unit) usually defines which techs it contains. You might need to add the Tech ID to the Building's interface list, not just set `tech.research_location`.

## Cross-Links

*   [Effects Manager](../effects/effects_manager.md)
*   [Civilizations](../civilizations/civs.md)
