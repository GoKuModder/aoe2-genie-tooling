# Sounds API

> Coming soon

The Sounds API provides control over sound entries in AoE2 DE DAT files.

## Quick Preview

```python
sm = workspace.sound_manager()

# Create a new sound
sound = sm.add_sound(filename="custom.wav", probability=100)

# Assign to unit
unit.bird.attack_sound = sound.id
```

## SoundManager Methods

| Method | Description |
|--------|-------------|
| `add_sound(filename, ...)` | Create new sound |
| `get(sound_id)` | Get sound by ID |
| `exists(sound_id)` | Check if exists |
| `count()` | Total sound slots |
