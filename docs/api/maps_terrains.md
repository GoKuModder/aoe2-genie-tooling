# Maps & Terrains

*Currently, map and terrain editing features are minimal or placeholders in `Actual_Tools_GDP`.*

The library focuses primarily on the DAT file (Units, Techs, Effects). Map generation and terrain modification are typically handled by `AoE2ScenarioParser` or other tools.

## Future Plans

The `Actual_Tools_GDP.Maps` and `Actual_Tools_GDP.Terrains` modules exist as placeholders for future expansion to cover the `.dat` file sections related to terrain restrictions and random map scripts.

## Current Functionality

*   **Terrain Restrictions**: Exposed via the underlying `workspace.dat.terrain_restrictions` but without high-level wrappers.
*   **Terrains**: Exposed via `workspace.dat.terrains`.
