# Sounds Module - Complete Documentation

## Overview
The Sounds module provides access to sound data in the DAT file through `SoundManager` and `SoundHandle`.

## Usage

```python
from aoe2_genie_tooling.Base.workspace import GenieWorkspace

# Load workspace
workspace = GenieWorkspace.load("empires2_x2_p1.dat")

# Access sounds
sound = workspace.sound_manager.get(5)
print(f"Total sounds: {workspace.sound_manager.count()}")  # 769

# Read attributes
print(sound.id)                  # Sound ID
print(sound.play_delay)          # Play delay in ms
print(sound.cache_time)          # Cache time (default 300000ms)
print(sound.num_sound_files)     # Number of sound file variants
print(sound.total_probability)   # Total probability

# Access sound files (variants)
for sound_file in sound.sound_files:
    print(sound_file.sound_name)      # WAV filename
    print(sound_file.probability)     # Play probability %
    print(sound_file.resource_id)     # Resource ID

# Modify attributes
sound.play_delay = 100
sound.cache_time = 500000

# Save changes
workspace.save("output.dat", validate=False)
```

## Available Sound Attributes

### Identity
- `id` - Sound ID (int)

### Timing
- `play_delay` - Play delay in milliseconds (int)
- `cache_time` - Cache time in milliseconds (int, default 300000)

### Sound Files
- `num_sound_files` - Number of sound file variants (int)
- `total_probability` - Total probability for all variants (int, default 100)
- `sound_files` - List of SoundFile objects

## SoundFile Attributes (variants)

Each sound can have multiple file variants (different WAV files played randomly):

- `sound_name` - WAV filename (str)
- `filename` - Alternative filename field (str)
- `resource_id` - Resource ID (int)
- `probability` - Probability this variant plays (int, 0-100)
- `civilization_id` - Civilization-specific sound (int, -1 = all)
- `icon_set` - Icon set ID (int)

## Implementation Files

- `Sounds/sound_manager.py` - Manager class
- `Sounds/sound_handle.py` - Handle wrapper class
- `Sounds/__init__.py` - Module exports

## Architecture

```
GenieWorkspace
  └─ sound_manager: SoundManager
       └─ get(id) -> SoundHandle
            └─ _sound: Sound (from GenieDatParser)
                 └─ sound_files: list[SoundFile]
```

**Pattern**: Top-to-bottom dependency injection
- Manager receives `workspace` reference
- Handle accesses data via `workspace.dat.sounds[id]`
- Direct attribute access through `__getattr__`/`__setattr__`

## Test Results

✅ Load DAT file (769 sounds)
✅ Get sound by ID
✅ Read all sound attributes
✅ Access sound file variants
✅ Modify sound attributes
✅ Save changes to DAT file

**Status**: COMPLETE AND VERIFIED
