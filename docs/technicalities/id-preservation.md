# ID Preservation (Registry)

The Registry system tracks created objects with persistent UUIDs, enabling cross-session identification and integration with external tools.

## Overview

When you create objects (units, graphics, sounds, techs, effects), the Registry:

1. Assigns a unique UUID to each created object
2. Maps UIDs to current integer IDs
3. Enables export to JSON for external tools
4. Tracks dependencies between objects

---

## Why UUIDs?

Integer IDs can change:
- If you add objects, existing IDs might shift
- Different DAT versions have different ID ranges
- Sharing mods requires ID awareness

UUIDs provide stable identity:
- Always unique
- Persist across sessions
- Can be used to find objects even if IDs change

---

## Accessing the Registry

```python
workspace = GenieWorkspace.load("input.dat")
registry = workspace.registry
```

---

## Registering Objects

Objects are automatically registered when created through managers:

```python
# Automatically registered
unit = workspace.unit_manager.create("Hero")
print(f"UUID: {registry.get_uuid_for_unit(unit.id)}")

graphic = workspace.graphic_manager.add_graphic("hero.slp")
print(f"UUID: {registry.get_uuid_for_graphic(graphic.id)}")
```

### Manual Registration

You can also manually register existing objects:

```python
# Register an existing unit for tracking
registry.register_unit("MyArcher", id=4)
```

---

## Looking Up by UUID

```python
# Get ID from UUID
unit_id = registry.get_id_by_uuid("units", "abc-123-uuid")

# Use in operations
if unit_id:
    unit = workspace.unit_manager.get(unit_id)
```

---

## JSON Export

Export registry data for external tools (like AoE2ScenarioParser):

```python
# Export to JSON file
registry.export_json("registry.json")
```

The JSON contains:
```json
{
  "units": [
    {"uuid": "abc-123", "id": 500, "name": "Hero"},
    {"uuid": "def-456", "id": 501, "name": "Elite Hero"}
  ],
  "graphics": [
    {"uuid": "ghi-789", "id": 6000, "name": "hero_attack.slp"}
  ],
  "sounds": [...],
  "techs": [...],
  "effects": [...]
}
```

External tools can read this to understand what was created and at what IDs.

---

## Bulk Registration

Register all existing objects in the DAT file:

```python
# Register all existing objects (marks them as "existing" vs "created")
registry.register_existing_objects(workspace)
```

This is useful for:
- Full validation of all references
- Building a complete object map
- Migration/comparison tools

---

## Integration with AoE2ScenarioParser

The Registry was designed to work with AoE2ScenarioParser for scenario editing:

```python
# In your mod script
workspace = GenieWorkspace.load("input.dat")

# Create custom units
hero = workspace.unit_manager.create("Hero", unit_id=1000)
hero.hit_points = 200

# Export registry
workspace.registry.export_json("my_mod_registry.json")
workspace.save("my_mod.dat")

# In scenario parser script, you can read the registry
# to know which IDs correspond to your custom units
```

---

## Dependency Tracking

The Registry can track dependencies between objects:

```python
# When you assign a graphic to a unit, that's a dependency
unit.standing_graphic_1 = graphic.id

# The registry knows unit depends on graphic
# This helps with:
# - Ensuring referenced objects exist
# - Export ordering
# - Deletion safety checks
```

---

## Session vs Existing Objects

The Registry distinguishes between:

- **Session-created**: Objects you created in this session
- **Existing**: Objects that were already in the DAT file

This enables selective validation:

```python
# Validate only session-created objects (faster)
issues = workspace.validator.validate_all_references(
    workspace, 
    validate_existing=False  # Only check new stuff
)

# Validate everything (slower but thorough)
issues = workspace.validator.validate_all_references(
    workspace,
    validate_existing=True
)
```

---

## Best Practices

### Export Registry for Complex Mods

```python
# At the end of your mod script
workspace.registry.export_json("my_mod_registry.json")
```

### Use Meaningful Names

```python
# Names are stored in registry and help identify objects
unit = workspace.unit_manager.create("EliteLongbowman")  # Clear name
# vs
unit = workspace.unit_manager.create("u1")  # Unhelpful
```

### Check UUID Collisions

If importing from multiple sources:

```python
# UUIDs should never collide, but if using custom UUIDs:
existing_uuid = registry.get_uuid_for_unit(some_id)
if existing_uuid:
    print(f"ID {some_id} already tracked as {existing_uuid}")
```
