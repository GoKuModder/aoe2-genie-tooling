---
layout: home

hero:
  name: "GenieTooling"
  text: "Python Tools for AoE2 DE"
  tagline: High-level toolkit for editing Age of Empires II Definitive Edition DAT files
  image:
    src: /logo.svg
    alt: GenieTooling
  actions:
    - theme: brand
      text: Get Started
      link: /getting-started
    - theme: alt
      text: View on GitHub
      link: https://github.com/GoKuModder/aoe2-genie-tooling

features:
  - icon: 🎯
    title: Object-Oriented API
    details: Work with proper Handle objects for Units, Graphics, Sounds, Effects, and Techs instead of raw data structures.
  - icon: 🌍
    title: Multi-Civ Propagation
    details: Changes automatically apply to all civilizations. Easily target specific civs when needed.
  - icon: ⚡
    title: Attribute Flattening
    details: Access nested properties directly (unit.hit_points) instead of navigating complex hierarchies.
  - icon: 🔧
    title: Fluent Builders
    details: Create tasks and effect commands with readable, auto-complete friendly methods.
  - icon: 🛡️
    title: Safe Cloning
    details: Deep copy operations prevent shared reference bugs across civilizations.
  - icon: 📊
    title: Type-Safe Datasets
    details: IntEnum constants for resources, tasks, attack classes, and more.
---

## Quick Example

```python
from Actual_Tools_GDP import GenieWorkspace

# Load workspace
workspace = GenieWorkspace.load("empires2_x2_p1.dat")

# Get managers
unit_manager = workspace.unit_manager
effect_manager = workspace.effect_manager

# Modify existing unit
archer = unit_manager.get(4)  # Archer
archer.hit_points = 50
archer.max_range = 7.0
archer.add_attack(class_=4, amount=8)

# Create a new unit from template
hero = unit_manager.create("Elite Guard", base_unit_id=4)
hero.hit_points = 200
hero.add_task.combat(class_id=0)

# Save changes
workspace.save("output.dat")
```

## Installation

```bash
pip install genieutils
```

## Documentation

<div class="doc-links">

| Section | Description |
|---------|-------------|
| [Getting Started](/getting-started) | Installation and first steps |
| [Units](/units) | Managing units, tasks, attacks |
| [Effects](/effects) | Technology effects and commands |
| [Techs](/techs) | Research and upgrades |
| [Graphics](/graphics) | Sprites and animations |
| [Sounds](/sounds) | Audio management |
| [Civilizations](/civilizations) | Civ bonuses and resources |
| [Datasets](/datasets) | Enums and constants |

</div>
