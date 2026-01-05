# Tech Tree Module Analysis (A11-Tree_1)

This document summarizes the structure and functionality of the base, age, and building-related modules within the `tech_tree` section of the GenieDatParser.

## 1. `tech_tree.py` - The Root Container

The `tech_tree.py` module defines the `TechTree` class, which serves as the top-level container for the entire technology tree structure in a Genie Engine `.dat` file.

### Key Attributes:

- **`num_ages`, `num_buildings`, `num_units`, `num_techs`**: These fields specify the number of corresponding sub-structures to read from the data file.
- **`ages`, `buildings`, `units`, `techs`**: These are lists that hold the actual `TechTreeAge`, `TechTreeBuilding`, `TechTreeUnit`, and `TechTreeTech` objects, respectively.
- **Version Handling**: The class uses version-specific retrievers (e.g., `_num_units_age1_aoe2_swgb`, `_num_units_de2`) to handle variations in the data format across different game versions (like Age of Empires, Age of Empires II, and Star Wars: Galactic Battlegrounds). The `RetrieverCombiner` is used to present a unified `num_units` attribute to the user, abstracting away the version differences.
- **Callbacks**: The `on_read` and `on_write` callbacks are used to dynamically set the repeat counts for the lists, ensuring that the correct number of objects are parsed or written.

### Purpose:

The `TechTree` class acts as the entry point for parsing the technology tree. It reads the counts of each sub-structure and then proceeds to parse those structures into organized lists.

## 2. `tech_tree_age.py` - Age-Specific Data

The `tech_tree_age.py` module defines the `TechTreeAge` class, which encapsulates all the data related to a single age within the game (e.g., Dark Age, Feudal Age).

### Key Attributes:

- **`id`**: The unique identifier for the age.
- **`status`**: A flag indicating the state of the age (e.g., enabled, disabled).
- **`building_ids`, `unit_ids`, `tech_ids`**: Lists of IDs for buildings, units, and technologies that are available or affected by this age.
- **`dependencies`**: A list of `TechTreeDependency` objects, defining the prerequisites for this age or the items it unlocks.
- **Version Handling**: Similar to `TechTree`, this class uses versioned attributes (e.g., `_buildings_age1`, `_buildings_age2`) and `RetrieverCombiner` to handle different data layouts between game versions. The arrays for dependencies and other lists have different fixed sizes depending on the game (e.g., 5 for Age of Empires, 10 for Age of Empires II DE).

### Purpose:

The `TechTreeAge` class models the progression through the game's ages, detailing what becomes available and what requirements must be met to advance.

## 3. `tech_tree_building.py` - Building-Specific Data

The `tech_tree_building.py` module defines the `TechTreeBuilding` class, which is structured very similarly to `TechTreeAge` but focuses on a single building.

### Key Attributes:

- **`id`**: The unique identifier for the building.
- **`status`**: A flag indicating the state of the building.
- **`building_ids`, `unit_ids`, `tech_ids`**: Lists of IDs that this building enables or interacts with. For example, the `unit_ids` would specify which units can be trained at this building.
- **`dependencies`**: A list of `TechTreeDependency` objects that must be satisfied for this building to be available.
- **`location_in_age`**: Specifies the age level at which this building appears in the tech tree UI.
- **`enabling_tech_id`**: The ID of the technology that enables this building.
- **Version Handling**: This class also follows the same version-aware pattern, using different fixed-size arrays and `RetrieverCombiner` to adapt to the data format of the specific game version being parsed.

### Purpose:

The `TechTreeBuilding` class defines a building's position and function within the technology tree, including its prerequisites and what it unlocks.

## Overall Structure and Design

The `tech_tree` modules are designed with a clear hierarchical and compositional structure:

- A single `TechTree` object contains lists of `TechTreeAge`, `TechTreeBuilding`, `TechTreeUnit`, and `TechTreeTech` objects.
- The use of `bfp-rs` with its `Retriever`, `RetrieverCombiner`, and version-aware selectors (`min_ver`, `max_ver`) is central to the design. This allows the parser to be flexible and robust, capable of handling multiple versions of the Genie Engine data format within a single, unified codebase.
- The code is declarative, describing the structure of the data rather than the imperative steps to parse it. This makes it easier to read and maintain.
