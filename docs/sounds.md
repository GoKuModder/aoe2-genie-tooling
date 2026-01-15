# Sounds

The Sounds module manages audio files and sound groups used throughout the game.

## Quick Example

```python
from Actual_Tools_GDP import GenieWorkspace

workspace = GenieWorkspace.load("empires2_x2_p1.dat")

# Get the sound manager
sound_manager = workspace.sound_manager

# Get an existing sound
sound = sound_manager.get(50)
print(f"Sound has {len(sound.files)} audio files")

# Create a new sound
attack_sound = sound_manager.add_new("HeroAttack")
attack_sound.new_sound(filename="hero_attack.wav", probability=100)
```

---

## Sub-Pages

| Page | Description |
|------|-------------|
| [Methods](sounds/methods.md) | All SoundManager and SoundHandle methods |
| [Attributes](sounds/attributes.md) | SoundHandle and SoundFileHandle properties |

---

## Overview

### SoundManager (`workspace.sound_manager`)

The manager handles sound CRUD operations:

| Method | Description |
|--------|-------------|
| `get(sound_id)` | Get a SoundHandle |
| `add_new(name)` | Create a new sound group |
| `copy(source_id)` | Copy a sound |
| `delete(sound_id)` | Delete a sound |
| `exists(sound_id)` | Check if sound exists |
| `find_by_name(name)` | Find by name |
| `find_by_file_name(file_name)` | Find by audio filename |

### SoundHandle

The handle provides access to a sound group:

**Properties:**
- `id` - Sound ID
- `files` / `sounds` - List of audio files

**Methods:**
- `new_sound(filename, ...)` - Add audio file
- `get_file(index)` - Get file by index
- `remove_file(index)` - Remove file

---

## Sound Structure

Sounds follow a two-tier structure:

1. **Sound Holder** - A group/container (identified by ID)
2. **Sound Files** - Actual audio files inside

```
Sound (ID: 50)
├── attack_01.wav (probability: 40%)
├── attack_02.wav (probability: 30%)
└── attack_03.wav (probability: 30%)
```

---

## Creating Sounds

```python
sound_manager = workspace.sound_manager

# Create a new sound group
sound = sound_manager.add_new("AttackSound")

# Add audio files
sound.new_sound(filename="attack_01.wav", probability=50)
sound.new_sound(filename="attack_02.wav", probability=50)
```

---

## Probability-Based Selection

When multiple files exist, the game randomly selects based on probability:

```python
# 70% chance for main, 30% for alternate
sound.new_sound(filename="main.wav", probability=70)
sound.new_sound(filename="alt.wav", probability=30)
```

---

## Assigning to Units

Sounds are assigned to units via their IDs:

```python
unit = workspace.unit_manager.get(4)

# Movement sounds
unit.move_sound = sound.id
unit.attack_sound = attack_sound.id
unit.damage_sound = damage_sound.id
```

---

## Managing Files

```python
# List all files
for file in sound.files:
    print(f"{file.filename}: {file.probability}%")

# Modify file
file = sound.get_file(0)
file.probability = 80

# Remove file
sound.remove_file(0)

# Clear all
sound.clear_files()
```

See [Attributes](sounds/attributes.md) for file properties.
