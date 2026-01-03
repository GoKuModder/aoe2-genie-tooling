# Actual_Tools

Production-quality tools layer for editing Age of Empires II DAT files.

An AoE2ScenarioParser-style API with GUI-like tabs for intuitive DAT file editing.

## Quickstart

```python
from Actual_Tools import GenieWorkspace

# Load a DAT file
workspace = GenieWorkspace.load("empires2_x2_p1.dat")

# Create a new unit based on Archer (ID 4)
handle = workspace.units.create("My Unit", base_unit_id=4)

# Edit via GUI-like tabs (changes apply to all civs)
handle.stats.hit_points = 150
handle.cost.food = 50
handle.cost.gold = 30

# Per-civ overrides
handle.for_civ(1).stats.hit_points = 200

# Save
workspace.save("output.dat")
```

## Public API

### GenieWorkspace

Root entry point. Owns the DatFile and exposes managers.

| Attribute | Description |
|-----------|-------------|
| `workspace.units` | GenieUnitManager |
| `workspace.graphics` | GraphicManager |
| `workspace.sounds` | SoundManager |
| `workspace.techs` | TechManager |
| `workspace.civs` | CivilizationsManager |
| `workspace.dat` | Raw DatFile object |

**Methods:**
- `GenieWorkspace.load(path)` - Load a DAT file
- `workspace.save(path)` - Save to a DAT file
- `workspace.validate()` - Run integrity checks (returns list of issues)
- `workspace.is_valid()` - Quick validity check (returns bool)

### Unit Operations

```python
# Create new unit
handle = workspace.units.create(
    name="My Unit",
    base_unit_id=4,           # Clone from (optional, defaults to first valid)
    unit_id=None,             # Target ID (optional, appends if None)
    enable_for_civs=None,     # Civ IDs (optional, all if None)
    on_conflict="error",      # "error" | "overwrite"
    fill_gaps="placeholder",  # "error" | "placeholder"
)

# Clone to specific ID
handle = workspace.units.clone_into(
    dest_unit_id=1500,
    base_unit_id=4,
    name="Clone",             # Optional, keeps original if None
    on_conflict="overwrite",
)

# Move unit
workspace.units.move(src_id, dst_id, on_conflict="swap")

# Get existing unit
handle = workspace.units.get(unit_id)
```

### UnitHandle Tabs

The handle provides tab-style access matching the in-game editor:

| Tab | Properties |
|-----|------------|
| `handle.stats` | `hit_points`, `speed`, `line_of_sight`, `attack.melee`, `armor.pierce` |
| `handle.cost` | `food`, `wood`, `gold`, `stone` |
| `handle.train` | `time_seconds`, `location_id`, `button_id` |
| `handle.graphics` | `standing`, `dying`, `attack`, `copy_from_unit(id)` |
| `handle.sounds` | `selection`, `dying`, `train`, `copy_from_unit(id)` |

**Direct attribute access:** Any Unit attribute can be accessed directly:
```python
handle.icon_id = 123
handle.class_ = 6
```

### Other Managers

```python
# Graphics
graphic = workspace.graphics.add_graphic("filename.slp", template_id=0)
graphic = workspace.graphics.get(graphic_id)

# Sounds
sound = workspace.sounds.add_sound("filename.wav", probability=100)
sound = workspace.sounds.get(sound_id)

# Techs
tech = workspace.techs.add_tech("My Tech", template_id=None)
tech = workspace.techs.get(tech_id)

# Civs (read-only)
civ = workspace.civs.get(civ_id)
civ = workspace.civs.get_by_name("Britons")
all_civs = workspace.civs.all()
```

## Invariants

### No Gaps Policy

Unit tables use index-based IDs (`id == index`). This library enforces **no None gaps**:

- Creating beyond max ID fills intermediate slots with **placeholder units**
- Placeholders: `enabled=0`, `name=""`, `hit_points=1` (valid for serialization)
- Use `fill_gaps="error"` to prevent automatic extension

### Conflict Handling

| Mode | Behavior |
|------|----------|
| `"error"` | Raise exception if target ID exists |
| `"overwrite"` | Replace existing unit |
| `"swap"` | Exchange source and destination (move only) |

## Exceptions

| Exception | When Raised |
|-----------|-------------|
| `UnitIdConflictError` | Target ID exists with `on_conflict="error"` |
| `GapNotAllowedError` | Extension needed with `fill_gaps="error"` |
| `InvalidIdError` | Negative ID or ID doesn't exist |
| `TemplateNotFoundError` | No template for cloning |
| `ValidationError` | Validation check failed |

## Running Tests

### Demo Script (Round-Trip Test)
```bash
cd Actual_Tools
python test_main.py
```

### Pytest (if installed)
```bash
cd Actual_Tools
python -m pytest tests/ -v
```

## Directory Structure

```
Actual_Tools/
├── __init__.py         # Public API exports
├── exceptions.py       # All exceptions
├── Base/               # GenieWorkspace
├── Units/              # GenieUnitManager, UnitHandle
├── Graphics/           # GraphicManager
├── Sounds/             # SoundManager
├── Techs/              # TechManager
├── Civilizations/      # CivilizationsManager
├── Shared/             # ToolBase utilities
├── tests/              # Pytest tests
├── test_main.py        # Round-trip demo
├── CHANGELOG.md        # Version history
└── README.md           # This file
```
