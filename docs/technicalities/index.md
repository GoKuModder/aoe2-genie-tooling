# Technicalities

This section covers advanced topics and internal mechanisms of `Actual_Tools_GDP`.

These topics are optional reading - you don't need to understand them to use the library effectively, but they can help with edge cases and advanced usage.

## Topics

### [Error Handling](error-handling.md)

Understanding the exception types and how to handle errors gracefully.

- `InvalidIdError` - When IDs are out of range or invalid
- `ValidationError` - When data validation fails
- `TemplateNotFoundError` - When a source for cloning doesn't exist
- Best practices for try/except patterns

### [Validation](validation.md)

How the library validates data integrity.

- Attribute allow-lists (preventing typos)
- Reference validation (checking IDs exist)
- Save-time validation
- Configuring validation levels

### [ID Preservation (Registry)](id-preservation.md)

Understanding the Registry system for tracking created objects.

- UUID-based identity tracking
- JSON export for external tools (AoE2ScenarioParser)
- Cross-session ID mapping
- Dependency tracking

---

## General Best Practices

### Always Save to a New File First

```python
# Good - test your changes first
workspace.save("output_test.dat")

# Then if it works, you can overwrite
workspace.save("empires2_x2_p1.dat")
```

### Check Existence Before Modifying

```python
if workspace.unit_manager.exists(1000):
    unit = workspace.unit_manager.get(1000)
    unit.hit_points = 100
else:
    print("Unit 1000 doesn't exist")
```

### Use Handles, Not Raw Objects

```python
# Good - use handles
unit = workspace.unit_manager.get(4)
unit.hit_points = 100

# Avoid - direct access to dat structures
workspace.dat.civilizations[0].units[4].hit_points = 100  # Don't do this
```
