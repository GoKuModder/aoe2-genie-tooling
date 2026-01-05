# Tech Tree Data Structures

This document outlines the structure of the technology tree data as defined in the `GenieDatParser` library. The tech tree is composed of three main components: technologies, units, and their dependencies.

## `TechTreeDependency`

This is the most fundamental class, representing a single prerequisite for a technology or unit.

-   **File:** `tech_tree_dependency.py`
-   **Class:** `TechTreeDependency`

**Attributes:**

-   `id` (int): The ID of the required age, building, unit, or technology.
-   `type` (int): An enum-like integer that specifies the type of dependency:
    -   `0`: Age
    -   `1`: Building
    -   `2`: Unit
    -   `3`: Technology

## `TechTreeTech`

This class defines the structure for a single technology within the tech tree. It includes its own attributes and a list of dependencies.

-   **File:** `tech_tree_tech.py`
-   **Class:** `TechTreeTech`

**Key Attributes:**

-   `id` (int): The unique identifier for the technology.
-   `status` (int): Indicates the availability of the technology (e.g., available, researched, disabled).
-   `building_id` (int): The ID of the building where this technology is researched.
-   `dependencies` (list[`TechTreeDependency`]): A list of prerequisites that must be met to unlock this technology. This list is dynamically sized and version-aware, handling different array sizes for different game versions (Age of Empires, Age of Kings, Star Wars: Galactic Battlegrounds, Definitive Edition).
-   `building_ids`, `unit_ids`, `tech_ids`: Lists of other game objects that are directly tied to this technology. These are also version-aware.
-   `group_id` (int): Used for grouping related technologies in the UI (often represented as a vertical line).
-   `location_in_age` (int): The position of the technology within its age.
-   `node_type` (int): Defines the visual representation or line style in the tech tree UI.

## `TechTreeUnit`

This class defines the structure for a single unit within the tech tree, including its dependencies and prerequisites.

-   **File:** `tech_tree_unit.py`
-   **Class:** `TechTreeUnit`

**Key Attributes:**

-   `id` (int): The unique identifier for the unit.
-   `status` (int): Indicates the availability of the unit.
-   `building_id` (int): The ID of the building where this unit is trained or built.
-   `dependencies` (list[`TechTreeDependency`]): A version-aware list of prerequisites for the unit.
-   `group_id` (int): The UI grouping ID.
-   `unit_ids` (list[int]): A version-aware list of related unit IDs.
-   `location_in_age` (int): The position of the unit within its age.
-   `prerequisite_tech_id` (int): The ID of a technology that is a hard prerequisite for this unit.
-   `enabling_tech_id` (int): The ID of the technology that enables this unit.
-   `node_type` (int): Defines the visual representation in the tech tree UI.

## Common Design Patterns

-   **Declarative Parsing:** All classes inherit from `bfp_rs.BaseStruct` and use the `Retriever` and `RetrieverCombiner` fields to define the binary layout of the data declaratively.
-   **Version Handling:** The structures are designed to handle multiple versions of the Genie Engine data format. The `Retriever` fields often specify `min_ver` and `max_ver` to parse data correctly depending on the game version.
-   **Dynamic Sizing:** Version differences in array sizes (e.g., the number of dependencies) are handled by defining separate private attributes for each version (`_dependencies_age1`, `_dependencies_aoe2`, etc.) and then using `RetrieverCombiner` to expose a single, unified list to the end-user.
