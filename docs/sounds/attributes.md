# Sound Attributes

Complete reference of all attributes available on `SoundHandle` and `SoundFileHandle`.

## SoundHandle Attributes

The `SoundHandle` represents a sound group that can contain multiple audio files.

| Attribute | Type | R/W | Description |
|-----------|------|-----|-------------|
| `id` | `int` | R | Sound ID (read-only) |
| `files` | `List[SoundFileHandle]` | R | List of audio files |
| `sounds` | `List[SoundFileHandle]` | R | Alias for `files` |

### Usage

```python
sound_manager = workspace.sound_manager
sound = sound_manager.get(50)

print(f"Sound ID: {sound.id}")
print(f"Number of files: {len(sound.files)}")
```

---

## SoundFileHandle Attributes

Each audio file in a sound group has these properties:

| Attribute | Type | R/W | Description |
|-----------|------|-----|-------------|
| `filename` | `str` | RW | Physical audio filename |
| `sound_name` | `str` | RW | Internal name (DE only) |
| `resource_id` | `int` | RW | Resource ID |
| `probability` | `int` | RW | Play probability (0-100) |
| `civilization_id` | `int` | RW | Civ filter (-1 = all) |
| `icon_set` | `int` | RW | Icon set filter |

### Usage

```python
# Get first file
file = sound.get_file(0)

# Read
print(f"Filename: {file.filename}")
print(f"Probability: {file.probability}%")
print(f"Civ: {file.civilization_id}")

# Write
file.filename = "new_attack.wav"
file.probability = 75
file.civilization_id = 1  # Britons only
```

---

## Probability System

When a sound group has multiple files, the game randomly selects one based on probability:

```python
# Equal chance for all
sound.new_sound(filename="hit_01.wav", probability=33)
sound.new_sound(filename="hit_02.wav", probability=33)
sound.new_sound(filename="hit_03.wav", probability=34)

# Weighted selection
sound.new_sound(filename="common.wav", probability=70)
sound.new_sound(filename="rare.wav", probability=30)
```

**Note:** Probabilities don't need to sum to 100 - they're relative weights.

---

## Civilization Filtering

Use `civilization_id` to play different sounds for different civs:

```python
# Different attack sounds per civ
sound.new_sound(filename="briton_attack.wav", civilization_id=1)
sound.new_sound(filename="frank_attack.wav", civilization_id=2)
sound.new_sound(filename="generic_attack.wav", civilization_id=-1)  # Fallback
```

When `civilization_id = -1`, the sound plays for all civs.

---

## Version-Specific Attributes

| Attribute | Availability | Notes |
|-----------|--------------|-------|
| `filename` | All versions | Physical file path |
| `sound_name` | DE only | Internal string name |
| `wwise_sound_id` | DE only | Wwise audio ID |

```python
# For DE
file.sound_name = "attack_sound"

# For older versions, use filename only
file.filename = "attack.wav"
```

---

## Example: Configure Sound Group

```python
# Create a new sound group
sound_manager = workspace.sound_manager
attack = sound_manager.add_new("HeroAttack")

# Add variations with different probabilities
attack.new_sound(filename="hero_attack_01.wav", probability=40)
attack.new_sound(filename="hero_attack_02.wav", probability=30)
attack.new_sound(filename="hero_attack_03.wav", probability=30)

# Verify
for file in attack.files:
    print(f"{file.filename}: {file.probability}%")
```

---

## Example: Civ-Specific Sounds

```python
# Create sound with per-civ variations
sound_manager = workspace.sound_manager
war_cry = sound_manager.add_new("WarCry")

# Britons
war_cry.new_sound(
    filename="briton_warcry.wav",
    civilization_id=1,
    probability=100,
)

# Franks
war_cry.new_sound(
    filename="frank_warcry.wav",
    civilization_id=2,
    probability=100,
)

# Generic fallback
war_cry.new_sound(
    filename="generic_warcry.wav",
    civilization_id=-1,
    probability=100,
)
```
