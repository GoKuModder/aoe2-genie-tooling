# Tech and Tech Effect Sections Analysis

## Directory: `src/sections/tech/`

### `tech.py`

- **`ResearchLocation` class**: This class defines the structure for a research location, including the unit ID where the research can be performed, the research time, and UI-related button and hotkey IDs.
- **`Tech` class**: This is the main data structure for a technology. It contains a comprehensive set of attributes, such as:
  - Required technologies (`required_tech_ids`)
  - Resource costs (`costs`), which is a list of `TechCost` objects.
  - Civilization-specific information (`civilization_id`).
  - UI elements like name, description, icon, and hotkey string IDs.
  - A list of `ResearchLocation` objects for DE versions of the game.

### `tech_cost.py`

- **`TechCost` class**: A simple class that defines the cost of a technology. It includes the resource ID, the quantity of the resource, and a flag to indicate if the resource is deducted.

## Directory: `src/sections/tech_effect/`

### `effect_command.py`

- **`EffectCommand` class**: This class represents a single effect of a technology. It has a `type` and four generic parameters (`a`, `b`, `c`, `d`) that are interpreted based on the `type` of the effect.

### `tech_effect.py`

- **`TechEffect` class**: This class ties a name to a list of `EffectCommand` objects. It defines the collection of effects that a technology applies.
