# Techs API

The Techs API provides control over technology entries in AoE2 DAT files.

Unlike Sounds and Effects, Techs are **single-tier objects** - they don't have a nested list of sub-items. Each tech has properties like `name`, `effect_id`, `costs`, etc.

## Quick Example

```python
tm = workspace.tech_manager

# Create a new tech
tech = tm.add_new(name="Elite Archer Upgrade", effect_id=100)

# Configure costs using named properties
tech.cost_1.resource_id = 0  # Food
tech.cost_1.quantity = 500
tech.cost_2.resource_id = 3  # Gold
tech.cost_2.quantity = 300

# Set research time and icon
tech.research_time = 60
tech.icon_id = 50

# Link to the tech tree
tech.required_tech_ids[0] = 22  # Archery Range tech
```

## TechManager Methods

| Method | Description |
|--------|-------------|
| `add_new(name, effect_id, ...)` | Create a new tech |
| `get(tech_id)` | Get tech by ID |
| `exists(tech_id)` | Check if tech exists |
| `count()` | Total tech slots |
| `find_by_name(name)` | Find tech by name |
| `copy(source_id, target_id)` | Copy tech to new ID |
| `copy_to_clipboard(id)` | Copy tech to clipboard |
| `paste(target_id)` | Paste from clipboard |
| `delete(tech_id)` | Reset slot to blank |

## TechHandle Properties

| Property | Type | Description |
|----------|------|-------------|
| `id` | `int` | Tech ID |
| `name` | `str` | Tech name |
| `effect_id` | `int` | Linked effect ID |
| `research_time` | `int` | Time to research |
| `costs` | `list` | 3 TechCost objects |
| `required_tech_ids` | `list` | Required tech IDs |
| `icon_id` | `int` | Icon ID |

## TechCost Properties

Each tech has 3 cost slots. Access via `tech.costs[0]`, `tech.costs[1]`, `tech.costs[2]`.

| Property | Type | Description |
|----------|------|-------------|
| `resource_id` | `int` | Resource type (0=Food, 1=Wood, 2=Stone, 3=Gold) |
| `quantity` | `int` | Amount required |
| `deduct_flag` | `bool` | Whether to deduct resource |
