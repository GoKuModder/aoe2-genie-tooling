# Graphics API Overview

The Graphics API provides control over graphic entries in AoE2 DE DAT files.

## Architecture

```
GenieWorkspace
    └── graphic_manager() → GraphicManager
                               └── add_graphic() / get() → GraphicHandle
                                                              └── .deltas → DeltaHandle[]
```

## Key Differences from Units

- **No civ-specific versions** – Each graphic exists once in `dat_file.graphics`
- **Simpler structure** – No nested wrappers, direct property access
- **Deltas** – Graphics can have sub-graphics (shadows, attachments)

---

## Quick Reference

| Class | Purpose |
|-------|---------|
| [GraphicManager](graphic-manager.md) | Create, copy, delete graphics |
| [GraphicHandle](graphic-handle.md) | Access and modify graphic properties |
| [Deltas](deltas.md) | Sub-graphics (shadows, attachments) |

---

## Basic Usage

```python
from Actual_Tools import GenieWorkspace

workspace = GenieWorkspace.load("empires2_x2_p1.dat")
gm = workspace.graphic_manager()

# Create a new graphic
attack_gfx = gm.add_graphic(
    file_name="hero_attack.slp",
    frame_count=15,
    angle_count=8,
)
print(f"Created graphic ID: {attack_gfx.id}")

# Copy existing graphic
copied = gm.copy(source_id=100, target_id=5000)

# Modify properties
copied.frame_duration = 0.08
copied.sound_id = 50

# Add shadow delta
copied.add_delta(graphic_id=200, offset_y=5)

workspace.save("output.dat")
```
