# aoe2-genie-tooling

High-level Python toolkit for editing Age of Empires II Definitive Edition DAT files.

## Features

- **Object-Oriented API** – Proper handle objects for Units, Graphics, Sounds
- **Multi-Civ Propagation** – Changes apply to all civilizations automatically
- **Attribute Flattening** – Access nested properties directly
- **Type-Safe Datasets** – IntEnum constants for resources, tasks, attack classes

## Quick Example

```python
from Actual_Tools import GenieWorkspace

workspace = GenieWorkspace.load("empires2_x2_p1.dat")

# Get managers
um = workspace.genie_unit_manager()
gm = workspace.graphic_manager()
sm = workspace.sound_manager()

# Create a custom unit
unit = um.create("Elite Guard", base_unit_id=4)
unit.hit_points = 120
unit.max_range = 6.0

# Create and assign graphics
attack_gfx = gm.add_graphic("guard_attack.slp", frame_count=15)
unit.combat.attack_graphic = attack_gfx.id

workspace.save("output.dat")
```

## Installation

```bash
pip install aoe2-genie-tooling
```

## Documentation

- [Getting Started](getting-started/quickstart.md) – Installation and first steps
- [Units API](api/units/overview.md) – Complete unit manipulation guide
- [Graphics API](api/graphics/overview.md) – Graphics and deltas
- [Examples](examples/units.md) – Real-world usage examples
