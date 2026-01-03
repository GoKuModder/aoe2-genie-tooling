# Unit Examples

Real-world examples for unit manipulation.

## Create a Hero Unit

```python
from Actual_Tools import GenieWorkspace
from Datasets import UnitClass
from genieutils.unit import AttackOrArmor

workspace = GenieWorkspace.load("empires2_x2_p1.dat")
um = workspace.genie_unit_manager()
gm = workspace.graphic_manager()
sm = workspace.sound_manager()

# Create hero from Knight
hero = um.create("Champion Knight", base_unit_id=38)

# Stats
hero.hit_points = 250
hero.speed = 1.6
hero.line_of_sight = 6
hero.class_ = UnitClass.CAVALRY

# Combat
hero.combat.max_range = 0
hero.combat.reload_time = 1.8

# Attacks
hero.attacks = [
    AttackOrArmor(class_=4, amount=18),  # Melee
    AttackOrArmor(class_=8, amount=8),   # Bonus vs Cavalry
]

# Armor
hero.add_armour(class_=3, amount=4)  # Pierce
hero.add_armour(class_=4, amount=6)  # Melee

# Cost
hero.cost.food = 100
hero.cost.gold = 120

# Training
hero.creatable.train_time = 20
hero.creatable.train_location_id = 82  # Stable

workspace.save("output.dat")
print(f"Created {hero.name} at ID {hero.id}")
```

## Create a Custom Archer

```python
# Create enhanced archer
archer = um.create("Elite Crossbowman", base_unit_id=24)  # Crossbowman

# Range buffs
archer.combat.max_range = 8.0
archer.combat.min_range = 0.0
archer.combat.accuracy_percent = 95

# Attack
archer.set_attack(class_=3, amount=10)  # Pierce damage

# Armor
archer.set_armour(class_=3, amount=2)

# Cost
archer.cost.wood = 35
archer.cost.gold = 50

print(f"Created {archer.name}")
```

## Modify Existing Unit

```python
# Get existing Militia
militia = um.get(74)

# Buff stats
militia.hit_points += 20
militia.speed = 1.1
militia.combat.reload_time = 1.5

# Add bonus vs buildings
militia.add_attack(class_=11, amount=5)

print(f"Modified {militia.name}")
```

## Create Unit Series

```python
base_hp = 100

for i in range(3):
    unit = um.create(
        name=f"Soldier {i+1}",
        base_unit_id=74,  # Militia
        on_conflict="overwrite",
    )
    unit.hit_points = base_hp + (i * 30)
    unit.cost.food = 50 + (i * 10)
    print(f"Created {unit.name} with {unit.hit_points} HP")
```

## Clone and Modify

```python
# Clone Knight to new ID
clone = um.clone_into(
    dest_unit_id=2500,
    base_unit_id=38,
    name="Knight Elite",
)

# Enhance
clone.hit_points = int(clone.hit_points * 1.5)
clone.speed *= 1.1

print(f"Cloned to {clone.name} at ID {clone.id}")
```

## Create Gatherer Unit

```python
from Datasets import Task, Resource

# Create villager variant
gatherer = um.create("Super Villager", base_unit_id=83)

# Faster work
gatherer.bird.work_rate = 0.6
gatherer.bird.search_radius = 10

# Add gather task
gatherer.tasks.add_task(
    task_type=Task.GATHER,
    resource_in=Resource.FOOD,
    resource_out=Resource.FOOD,
    work_value_1=0.5,
    work_range=0.5,
)

# Drop sites
gatherer.bird.drop_sites = [109, 68, 562]  # TC, Mill, Folwark
```

## Building with Garrison

```python
# Create custom barracks
barracks = um.create("Fortress Barracks", base_unit_id=12)

# Garrison settings
barracks.building.garrison_type = 15
barracks.garrison_capacity = 15
barracks.building.garrison_heal_rate = 0.5

# HP
barracks.hit_points = 2500
```
