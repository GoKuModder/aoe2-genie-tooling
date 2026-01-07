# Graphics API

Manage graphics (sprites, deltas) using `GraphicManager` and `GraphicHandle`.

## Mental Model

Graphics (Sprites) define the visual appearance.
1.  **SLP Reference**: A Graphic points to an SLP file ID (from the DRS archives or local files).
2.  **Animation**: It defines frames, angles, and duration.
3.  **Deltas**: Graphics can have "Deltas" attached to them. These are other graphics that are drawn relative to the parent (e.g., a rider on a horse, or a flame on a torch).

## Common Workflows

### Creating a New Graphic
```python
# Add a new graphic pointing to file 5000.slp
gfx = workspace.graphic_manager.add_graphic(
    file_name="5000.slp",
    name="New Unit Gfx",
    frame_count=10,
    angle_count=8
)
```

### Adding a Delta (Composite Graphic)
```python
horse = workspace.graphic_manager.get(100)
rider = workspace.graphic_manager.get(101)

# Attach rider to horse
horse.add_delta(
    delta_graphic_id=rider.id,
    offset_x=0,
    offset_y=-10
)
```

## Gotchas & Invariants

*   **Missing SLPs**: The DAT file only stores the *ID* of the SLP. If the actual SLP file is missing from your game folders, the unit will be invisible or crash the game. `Actual_Tools_GDP` cannot validate file existence on disk, only the data references.
*   **Delta Loops**: Do not create circular deltas (A has delta B, B has delta A). This will crash the game.

## GraphicManager

Access via `workspace.graphic_manager`.

### Methods

#### `get(graphic_id: int) -> GraphicHandle`
Get a handle for an existing graphic.

#### `add_graphic(...) -> GraphicHandle`
Create a new graphic.

#### `copy(source_id: int, ...) -> GraphicHandle`
Copy an existing graphic.

## GraphicHandle

Wrapper for graphic data.

### Attributes
- `name` (str)
- `slp_id` (int)
- `layer` (int)
- `deltas` (list)

### Methods

#### `add_delta(...)`
Adds a delta (variant) to the graphic.
