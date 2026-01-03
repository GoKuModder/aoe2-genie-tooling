# Graphics Examples

Real-world examples for graphics and delta manipulation.

## Create Unit Graphics Set

```python
from Actual_Tools import GenieWorkspace

workspace = GenieWorkspace.load("empires2_x2_p1.dat")
gm = workspace.graphic_manager()
um = workspace.genie_unit_manager()

# Create graphics for a hero unit
idle = gm.add_graphic("hero_idle.slp", frame_count=10, angle_count=8)
walk = gm.add_graphic("hero_walk.slp", frame_count=15, angle_count=8)
attack = gm.add_graphic("hero_attack.slp", frame_count=12, angle_count=8)
death = gm.add_graphic("hero_death.slp", frame_count=20, angle_count=8)

# Configure animation speeds
idle.frame_duration = 0.1
walk.frame_duration = 0.07
attack.frame_duration = 0.06  # Fast attack
death.frame_duration = 0.08

# Assign to unit
hero = um.create("Hero", base_unit_id=38)
hero.standing_graphic = idle.id
hero.dead_fish.walking_graphic = walk.id
hero.combat.attack_graphic = attack.id
hero.dying_graphic = death.id

workspace.save("output.dat")
```

## Add Shadows to Graphics

```python
# Find shadow graphic
shadow = gm.find_by_name("SHADOW_CAVALRY")
if not shadow:
    shadow = gm.find_by_file_name("shadow.slp")

# Add shadow to multiple graphics
graphics_to_shadow = [idle, walk, attack, death]

for gfx in graphics_to_shadow:
    if shadow:
        gfx.add_delta(
            graphic_id=shadow.id,
            offset_x=0,
            offset_y=4,
        )
        print(f"Added shadow to graphic {gfx.id}")
```

## Create Weapon Effects

```python
# Weapon flash effect (only on front angles)
flash = gm.find_by_name("WEAPON_FLASH")

if flash:
    # Add to attack graphic for front-facing angles
    attack.add_delta(
        graphic_id=flash.id,
        offset_x=8,
        offset_y=-5,
        display_angle=0,  # Front
    )
    attack.add_delta(
        graphic_id=flash.id,
        offset_x=6,
        offset_y=-5,
        display_angle=1,  # Front-right
    )
    attack.add_delta(
        graphic_id=flash.id,
        offset_x=-6,
        offset_y=-5,
        display_angle=7,  # Front-left
    )
```

## Copy and Modify Graphics

```python
# Find original graphic
original = gm.find_by_name("KNIGHT_ATTACK")

if original:
    # Copy it
    modified = gm.copy(source_id=original.id)
    modified.name = "HERO_KNIGHT_ATTACK"
    
    # Speed up animation
    modified.speed_multiplier = 1.3
    modified.frame_duration = 0.05
    
    # Add sound
    modified.sound_id = 50
    
    print(f"Created modified graphic at ID {modified.id}")
```

## Damage State Graphics

```python
# Create damage graphics for building
barracks = um.get(12)

# At 50% damage
barracks.add_damage_graphic(graphic_id=450, damage_percent=50)

# At 25% damage (more visible damage)
barracks.add_damage_graphic(graphic_id=451, damage_percent=25)

# Near destruction
barracks.add_damage_graphic(graphic_id=452, damage_percent=10)
```

## Managing Deltas

### List All Deltas

```python
gfx = gm.get(100)

print(f"Graphic {gfx.id} has {len(gfx.deltas)} deltas:")
for i, d in enumerate(gfx.deltas):
    print(f"  [{i}] graphic={d.graphic_id}, offset=({d.offset_x}, {d.offset_y}), angle={d.display_angle}")
```

### Remove Specific Delta

```python
# Remove shadow (graphic ID 200)
removed = gfx.remove_delta_by_graphic(graphic_id=200)
if removed:
    print("Shadow removed")
```

### Replace Delta Graphic

```python
# Replace old shadow with new one
for delta in gfx.deltas:
    if delta.graphic_id == 200:  # Old shadow
        delta.graphic_id = 201   # New shadow
```

### Adjust Delta Positions

```python
# Move all deltas down by 2 pixels
for delta in gfx.deltas:
    delta.offset_y += 2
```

## Clipboard Operations

```python
# Copy a nice graphic to clipboard
gm.copy_to_clipboard(100)

# Create variations
for i in range(5):
    pasted = gm.paste()
    pasted.name = f"VARIATION_{i}"
    pasted.speed_multiplier = 1.0 + (i * 0.1)
    print(f"Created variation at ID {pasted.id}")

gm.clear_clipboard()
```

## Complete Example: Hero with Full Graphics

```python
from Actual_Tools import GenieWorkspace

workspace = GenieWorkspace.load("empires2_x2_p1.dat")
gm = workspace.graphic_manager()
um = workspace.genie_unit_manager()

# Find existing components
shadow = gm.find_by_name("SHADOW_CAVALRY")
flame = gm.find_by_name("FLAME_SMALL")

# Create graphics
idle = gm.add_graphic("hero_idle.slp", frame_count=10, angle_count=8)
walk = gm.add_graphic("hero_walk.slp", frame_count=15, angle_count=8)
attack = gm.add_graphic("hero_attack.slp", frame_count=12, angle_count=8)

# Configure timing
for gfx in [idle, walk, attack]:
    gfx.frame_duration = 0.07
    
    # Add shadow
    if shadow:
        gfx.add_delta(graphic_id=shadow.id, offset_y=3)

# Add flame effect to attack
if flame:
    attack.add_delta(
        graphic_id=flame.id,
        offset_x=0,
        offset_y=-12,
        display_angle=-1,  # All angles
    )

# Create unit
hero = um.create("Flame Knight", base_unit_id=38)
hero.standing_graphic = idle.id
hero.dead_fish.walking_graphic = walk.id
hero.combat.attack_graphic = attack.id
hero.hit_points = 200

workspace.save("output.dat")

# Summary
print(f"\nCreated Flame Knight (ID {hero.id})")
print(f"  Idle graphic: {idle.id} ({len(idle.deltas)} deltas)")
print(f"  Walk graphic: {walk.id} ({len(walk.deltas)} deltas)")
print(f"  Attack graphic: {attack.id} ({len(attack.deltas)} deltas)")
```
