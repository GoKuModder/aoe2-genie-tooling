# A04-Civ_TypeB.md - Analysis Summary

This document summarizes the structures defined in `task_info.py`, `movement_info.py`, and `projectile_info.py` from the `GenieDatParser` library. These files define data structures related to unit behaviors and properties within the Genie Engine.

## `task_info.py`

This file defines the `TaskInfo` class, which outlines the tasks a unit can perform. Key attributes include:

- **`default_task_id`**: The default task assigned to the unit.
- **`search_radius`**: The radius in which a unit will search for tasks.
- **`work_rate`**: The rate at which a unit performs its work.
- **`drop_site_unit_ids`**: A list of unit IDs that can be used as drop sites for resources. This is version-dependent.
- **`task_swap_group`**: A group ID for swapping tasks.
- **`attack_sound_id` and `move_sound_id`**: Sound IDs for attacking and moving. Wwise sound IDs are also included for newer game versions.
- **`run_mode`**: Defines the unit's running behavior.
- **`tasks`**: A list of `UnitTask` objects, defining the specific tasks the unit can perform.

## `movement_info.py`

This file defines the `MovementInfo` class, which contains attributes related to unit movement. Key attributes include:

- **`walking_sprite_id` and `running_sprite_id`**: IDs for the walking and running sprites.
- **`rotation_speed`**: The speed at which the unit can rotate.
- **`old_size_class`**: A legacy attribute for the unit's size class.
- **`trailing_unit_id`**: The ID of a unit that follows this unit.
- **`rotation_radius`**: The radius of the unit's rotation.
- **`max_yaw_per_sec_walking` and `max_yaw_per_sec_standing`**: The maximum yaw per second when walking or standing.

## `projectile_info.py`

This file defines the `ProjectileInfo` class, which describes the behavior of projectiles. Key attributes include:

- **`projectile_type`**: The type of projectile (e.g., arrow, cannonball).
- **`smart_mode`**: A flag for "smart" projectiles that can track targets.
- **`hit_mode`**: How the projectile hits its target.
- **`vanish_mode`**: How the projectile vanishes after impact.
- **`area_effect_specials`**: Defines any area-of-effect specials for the projectile.
- **`projectile_arc`**: The arc of the projectile's trajectory.
