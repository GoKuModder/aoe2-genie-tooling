# Attacks & Armours

Units have attack and armour entries organized by damage class. This page covers how to view, add, modify, and remove them.

## Overview

The AoE2 damage system uses **damage classes**:
- Each attack has a class and damage amount
- Each armour has a class and armor amount
- When attacking, damage is calculated by matching attack classes to armour classes

Common damage classes:
| Class | Name | Description |
|-------|------|-------------|
| 1 | Infantry | Bonus vs infantry |
| 2 | Turtle Ship | Specific unit bonus |
| 3 | Pierce | Base ranged damage |
| 4 | Melee | Base melee damage |
| 5 | War Elephant | Bonus vs elephants |
| 8 | Cavalry | Bonus vs cavalry |
| 11 | Building | Bonus vs buildings |
| 15 | Archer | Bonus vs archers |
| 16 | Ship | Bonus vs ships |
| 17 | Ram | Bonus vs rams |
| 19 | Unique Unit | Civ-specific bonus |
| 21 | Building (base) | Standard building damage |

---

## Adding Attacks

### `add_attack(class_, amount)`

Add a new attack entry.

| Parameter | Type | Description |
|-----------|------|-------------|
| `class_` | `int` | Damage class |
| `amount` | `int` | Damage amount |

**Returns:** `AttackHandle`

```python
unit_manager = workspace.unit_manager
unit = unit_manager.get(4)

# Add melee attack
unit.add_attack(class_=4, amount=10)

# Add pierce attack
unit.add_attack(class_=3, amount=6)

# Add bonus vs cavalry
unit.add_attack(class_=8, amount=5)
```

---

### `set_attack(class_, amount)`

Update an existing attack by class, or add if not present.

| Parameter | Type | Description |
|-----------|------|-------------|
| `class_` | `int` | Damage class |
| `amount` | `int` | Damage amount |

**Returns:** `AttackHandle`

```python
# Update melee to 15, or add if missing
unit.set_attack(class_=4, amount=15)
```

This is safer than `add_attack` when you're not sure if an attack already exists.

---

## Getting Attacks

### `get_attack_by_class(class_)`

Get attack entry by damage class.

**Returns:** `AttackHandle` or `None`

```python
melee = unit.get_attack_by_class(4)
if melee:
    print(f"Melee damage: {melee.amount}")
```

---

### `get_attack_by_id(attack_id)`

Get attack entry by index position.

**Returns:** `AttackHandle` or `None`

```python
first = unit.get_attack_by_id(0)  # First attack
```

---

### `attacks` Property

Access the raw attacks list.

```python
for attack in unit.attacks:
    print(f"Class {attack.class_}: {attack.amount} damage")
```

---

## Modifying Attacks

Use the returned `AttackHandle` to modify:

```python
attack = unit.get_attack_by_class(4)
attack.amount = 20  # Change damage

attack.class_ = 8   # Change class (careful - may create duplicates)
```

---

## Removing Attacks

### `remove_attack(attack_id)`

Remove attack by index position.

| Parameter | Type | Description |
|-----------|------|-------------|
| `attack_id` | `int` | Index of attack to remove |

**Returns:** `bool`

```python
unit.remove_attack(0)  # Remove first attack
```

---

## AttackHandle Properties

| Property | Type | R/W | Description |
|----------|------|-----|-------------|
| `class_` | `int` | RW | Damage class |
| `amount` | `int` | RW | Damage amount |

---

## Adding Armours

### `add_armour(class_, amount)`

Add a new armour entry.

| Parameter | Type | Description |
|-----------|------|-------------|
| `class_` | `int` | Armor class |
| `amount` | `int` | Armor amount |

**Returns:** `ArmourHandle`

```python
# Add melee armor
unit.add_armour(class_=4, amount=2)

# Add pierce armor
unit.add_armour(class_=3, amount=5)

# Add cavalry armor (for cavalry units)
unit.add_armour(class_=8, amount=0)
```

---

### `set_armour(class_, amount)`

Update an existing armour by class, or add if not present.

**Returns:** `ArmourHandle`

```python
unit.set_armour(class_=3, amount=7)  # Set pierce armor to 7
```

---

## Getting Armours

### `get_armour_by_class(class_)`

Get armour entry by damage class.

**Returns:** `ArmourHandle` or `None`

```python
pierce = unit.get_armour_by_class(3)
if pierce:
    print(f"Pierce armor: {pierce.amount}")
```

---

### `get_armour_by_id(armour_id)`

Get armour entry by index position.

**Returns:** `ArmourHandle` or `None`

```python
first = unit.get_armour_by_id(0)
```

---

### `armours` Property

Access the raw armours list.

```python
for armour in unit.armours:
    print(f"Class {armour.class_}: {armour.amount} armor")
```

---

## Modifying Armours

```python
armour = unit.get_armour_by_class(3)
armour.amount = 10  # Change armor value
```

---

## Removing Armours

### `remove_armour(armour_id)`

Remove armour by index position.

**Returns:** `bool`

```python
unit.remove_armour(0)  # Remove first armour
```

---

## ArmourHandle Properties

| Property | Type | R/W | Description |
|----------|------|-----|-------------|
| `class_` | `int` | RW | Armor class |
| `amount` | `int` | RW | Armor amount |

---

## Example: Create a Tanky Unit

```python
unit_manager = workspace.unit_manager
unit = unit_manager.create("Tank", base_unit_id=38)

# Strong attacks
unit.set_attack(class_=4, amount=20)   # 20 melee
unit.set_attack(class_=8, amount=10)   # +10 vs cavalry

# High armor
unit.set_armour(class_=4, amount=5)    # 5 melee armor
unit.set_armour(class_=3, amount=8)    # 8 pierce armor

# Print final stats
print("Attacks:")
for a in unit.attacks:
    print(f"  Class {a.class_}: {a.amount}")

print("Armours:")
for a in unit.armours:
    print(f"  Class {a.class_}: {a.amount}")
```

---

## Example: Copy Attacks from Another Unit

```python
unit_manager = workspace.unit_manager
source = unit_manager.get(38)  # Knight
target = unit_manager.get(100)  # New unit

# Copy all attacks
for attack in source.attacks:
    target.set_attack(class_=attack.class_, amount=attack.amount)

# Copy all armours
for armour in source.armours:
    target.set_armour(class_=armour.class_, amount=armour.amount)
```
