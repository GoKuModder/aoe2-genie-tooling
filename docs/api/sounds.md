# Sounds API

> Coming soon

The Sounds API provides control over sound entries in AoE2 DAT files. 

Sounds follow a two-tier structure:
1. **Sound Holder**: A slot in the "mega-list" (e.g., sound ID 100).
2. **Actual Sounds**: A list of one or more audio files within that holder (e.g., `attack1.wav`, `attack2.wav`).

## Quick Example

```python
sm = workspace.sound_manager

# 1. Create a holder (slot)
holder = sm.add_new(play_delay=50)

# 2. Add actual sounds to the holder
holder.new_sound(file_name="hero_attack_01.wav", probability=50)
holder.new_sound(file_name="hero_attack_02.wav", probability=50)

# 3. Assign the holder ID to a unit
unit.selection_sound = holder.id
```

## SoundManager Methods

| Method | Description |
|--------|-------------|
| `add_new(...)` | Create a new sound holder/slot |
| `get(sound_id)` | Get sound holder by ID |
| `exists(sound_id)` | Check if slot ID is in range |
| `count()` | Total sound slots |
| `find_by_file_name(name)` | Find holder containing a specific filename |
| `copy_to_clipboard(id)` | Copy holder to internal clipboard |
| `paste(target_id)` | Paste from clipboard |

## SoundHolder (`SoundHandle`) Methods

| Method | Description |
|--------|-------------|
| `new_sound(file_name, ...)` | Add an actual audio file to this holder |
| `files` (property) | List of actual sounds in this holder |
| `remove_file(index)` | Remove sound file by index |
| `clear_files()` | Remove all sound files |
| `play_delay` (attr) | Delay before playing |
| `total_probability` (attr) | Total probability sum |
