# Sounds API

Manage sounds using `SoundManager` and `SoundHandle`.

## Mental Model

Sounds in Genie are collections of audio files.
1.  **Sound Group**: The main "Sound" object is actually a group (e.g., "Sword Attack").
2.  **Sound Files**: Inside the group, there are multiple files (e.g., "swing1.wav", "swing2.wav"). The game picks one randomly to play.
3.  **References**: Units reference the Sound Group ID, not the individual file.

## Common Workflows

### Creating a New Sound Group
```python
# Create the container
sword_sound = workspace.sound_manager.add_copy(source_id=0, name="New Sword Sound")

# Clear old files and add new ones
sword_sound.clear_files()
sword_sound.add_file(filename="new_swing1.wav", probability=50)
sword_sound.add_file(filename="new_swing2.wav", probability=50)
```

## Gotchas & Invariants

*   **File Paths**: Filenames are relative to the game's sound folder.
*   **Probabilities**: While there is a probability field, the engine logic for selection can be complex. Usually, ensuring equal probabilities sum to 100 is best practice.

## SoundManager

Access via `workspace.sound_manager`.

### Methods

#### `get(sound_id: int) -> SoundHandle`
Get a handle for an existing sound.

#### `add_copy(source_id: int, name: str) -> SoundHandle`
Create a new sound by copying an existing one.

## SoundHandle

Wrapper for sound data.

### Attributes
- `id` (int)
- `files` (list of sound items)

### Methods

#### `add_file(...)`
Adds a new sound file entry to this group.
