# Quick Start

Get up and running with aoe2-genie-tooling in 5 minutes.

## Loading a DAT File

```python
from Actual_Tools import GenieWorkspace

# Load the DAT file
workspace = GenieWorkspace.load("empires2_x2_p1.dat")

# Get managers
um = workspace.genie_unit_manager()
gm = workspace.graphic_manager()
sm = workspace.sound_manager()
```

## Creating a Unit

```python
# Create a new unit (clones from Archer)
hero = um.create("My Hero", base_unit_id=4)

# Modify properties
hero.hit_points = 150
hero.speed = 1.4
hero.max_range = 6.0

# Set costs
hero.cost.food = 50
hero.cost.gold = 75
```

## Adding Attacks and Armor

```python
from genieutils.unit import AttackOrArmor

# Add attacks
hero.add_attack(class_=3, amount=8)   # Pierce
hero.add_attack(class_=11, amount=3)  # Bonus vs Buildings

# Add armor
hero.add_armour(class_=3, amount=2)   # Pierce armor
hero.add_armour(class_=4, amount=1)   # Melee armor

# Or replace all attacks
hero.attacks = [
    AttackOrArmor(class_=3, amount=10),
    AttackOrArmor(class_=4, amount=5),
]
```

## Creating Graphics

```python
# Create a new graphic
attack_gfx = gm.add_graphic(
    file_name="hero_attack.slp",
    frame_count=15,
    angle_count=8,
)

# Assign to unit
hero.combat.attack_graphic = attack_gfx.id
```

## Creating Sounds

```python
# Create a new sound
attack_snd = sm.add_sound("hero_attack.wav")

# Assign to unit
hero.bird.attack_sound = attack_snd.id
```

## Saving

```python
# Save the modified DAT file
workspace.save("output.dat")

# Export registry for AoE2ScenarioParser integration
workspace.save_registry("genie_edits.json")
```

## Complete Example

```python
from Actual_Tools import GenieWorkspace
from genieutils.unit import AttackOrArmor

# Load
workspace = GenieWorkspace.load("empires2_x2_p1.dat")
um = workspace.genie_unit_manager()
gm = workspace.graphic_manager()

# Create unit
hero = um.create("Champion", base_unit_id=38)  # Knight clone
hero.hit_points = 200
hero.speed = 1.5

# Combat stats
hero.combat.max_range = 0
hero.combat.reload_time = 1.8

# Attacks
hero.attacks = [
    AttackOrArmor(class_=4, amount=15),   # Melee
    AttackOrArmor(class_=8, amount=8),    # Bonus vs Cavalry
]

# Cost
hero.cost.food = 80
hero.cost.gold = 100

# Save
workspace.save("output.dat")
print(f"Created {hero.name} at ID {hero.id}")
```

## Next Steps

- [Units API](../api/units/overview.md) – Complete unit manipulation guide
- [Graphics API](../api/graphics/overview.md) – Graphics and deltas
- [Unit Examples](../examples/units.md) – Real-world examples
