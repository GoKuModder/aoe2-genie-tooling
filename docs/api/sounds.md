# Sounds Manager

The `SoundManager` handles the creation and management of audio assets.

## Mental Model

*   **Sound Holder (Sound ID)**: A "Sound" in the DAT file (e.g., ID 500) is a container. It can hold multiple variations of a sound (e.g., 5 different sword swing samples) which the engine plays randomly.
*   **Sound File**: The actual reference to a `.wav` or `.wem` file. A Sound Holder contains a list of Sound Files.
*   **File References**: Like graphics, the DAT file doesn't store the audio. It stores the filename (e.g., `attack01.wav`) which must exist in the `drs` or `sound` folder.

## Public API

### SoundManager (`Actual_Tools_GDP.Sounds.sound_manager`)

Access via `workspace.sound_manager`.

*   `add_sound(filename: str) -> SoundHandle`: Quick helper to create a Sound Holder with one file.
*   `add_new() -> SoundHandle`: Creates an empty Sound Holder.
*   `get(sound_id) -> SoundHandle`: Gets a handle.
*   `find_by_file_name(name) -> SoundHandle`: Searches for a sound that contains a specific filename.

### SoundHandle (`Actual_Tools_GDP.Sounds.sound_handle`)

*   `id`: The Sound ID.
*   `new_sound(filename, probability, ...)`: Adds a new file variation to this holder.
*   `sounds` / `files`: List of `SoundFileHandle` objects.

### SoundFileHandle (`Actual_Tools_GDP.Sounds.sound_file_handle`)

*   `filename`: The name of the audio file.
*   `probability`: Chance (0-100) for this specific variation to play.
*   `civilization_id`: If set, only plays for that civ.

## Workflows

### creating a Simple Sound

```python
# Create a new sound ID pointing to "boom.wav"
sound = workspace.sound_manager.add_sound("boom.wav")
print(f"Created Sound ID {sound.id}")
```

### Creating a Random Variation Sound

```python
# Create empty holder
sound = workspace.sound_manager.add_new()

# Add 3 variations, equal probability
sound.new_sound("sword1.wav", probability=100)
sound.new_sound("sword2.wav", probability=100)
sound.new_sound("sword3.wav", probability=100)
```

## Gotchas & Invariants

*   **Missing Files**: If the filename doesn't match an actual file in your mods folder or game data, the sound will be silent.
*   **Wwise IDs**: Definitive Edition uses Wwise (`.wem` files). Sometimes the engine uses `resource_id` or `icon_set` to map to Wwise sound banks instead of using the filename.
*   **Probabilities**: If multiple files have 100 probability, the engine picks one randomly.

## Cross-Links

*   [Graphics](../graphics.md)
