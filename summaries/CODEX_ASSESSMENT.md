# CODEX_ASSESSMENT

## Scope and method
- Summaries reviewed:
  - `summaries/sections/civilization/A01-Civ_Core.md`
  - `summaries/sections/civilization/A02-Civ_Unit.md`
  - `summaries/sections/civilization/A03-Civ_TypeA.md`
  - `summaries/sections/civilization/A04-Civ_TypeB.md`
  - `summaries/sections/color_data/A05-Color.md`
  - `summaries/sections/map_data/A06-Map_1.md`
  - `summaries/sections/map_data/A07-Map_2.md`
  - `summaries/sections/sounds/A08-Snd_Swgb.md`
  - `summaries/sections/sprite_data/A09-Sprite.md`
  - `summaries/sections/tech/A10-Tech.md`
  - `summaries/sections/tech_tree/A11-Tree_1.md`
  - `summaries/sections/tech_tree/A12-Tree_2.md`
  - `summaries/sections/terrain_data/A13-Terrain_1.md`
  - `summaries/sections/terrain_data/A14-Terrain_2.md`
  - `summaries/sections/unit_data/A15-Tab_Unit.md`
- Code compared against the referenced modules under `GenieDatParser/src/sections/`, with integration order confirmed in `GenieDatParser/src/sections/datfile_sections.py`.
- Focus: structural alignment (fields, version gates, repeats), with gaps and mismatches called out explicitly.

## Cross-cutting patterns seen in code
- `bfp_rs` defines layouts with `BaseStruct` + `Retriever`, heavy `Version` gating, and `RetrieverCombiner` for unified fields across versions.
- Dynamic list sizing uses `set_repeat` on read and occasional write-time sync; some counts must be kept in sync manually.
- Many pointer-like fields are stored as raw `Bytes` and are not dereferenced; they preserve file fidelity rather than drive logic.

## Section-by-section comparison

### A01 - Civilization Core
Alignment:
- `Civilization.name` combines `str16` (DE) and `NtStr[20]` (older versions) with DE string signatures (`_str_sign_de1`, `_str_sign_de2`) in `GenieDatParser/src/sections/civilization/civilization.py`.
- `num_resources` drives repeat count for `resources` via `resources_repeat`.
- `units` is `StackedAttrArray16[Option32[Unit]]`.
- `UnitResource`, `UnitDamageSprite`, and `DamageClass` layouts match the summary in `GenieDatParser/src/sections/civilization/unit_resource.py`, `GenieDatParser/src/sections/civilization/unit_damage_sprite.py`, `GenieDatParser/src/sections/civilization/type_info/damage_class.py`.
Notes and gaps:
- `num_resources` has no on_write sync, so list length and count must be kept consistent manually.
- `name2` and `unique_unit_effect_ids` only exist for Version(5,9); `name2` defaults to `0` despite being a string type.

### A02 - Civilization Unit
Alignment:
- Versioned fields and `RetrieverCombiner` patterns match; AoE1/AoE2 names use length fields with on_read/on_write hooks in `GenieDatParser/src/sections/civilization/unit.py`.
- `disable_types` gates nested `*Info` blocks based on `UnitType`.
- `resources` is `Array[3][UnitResource]`; `damage_sprites` is `Array8[UnitDamageSprite]`.
- Wwise IDs and `scx_trigger_data*` TODO comments match.
Notes and gaps:
- `copy_id` and `base_id` are synced to `id` via `sync_ids` on write.
- The summary does not mention `name_str_id`, `creation_str_id`, `help_str_id`, or `hotkey_str_id` fields.
- SWGB-specific fields (`name2`, `unit_line_id`, `min_tech_level`) are present for Version(5,9).

### A03 - Civilization TypeA (Building/Combat/Creation)
Alignment:
- `BuildingInfo`, `CombatInfo`, and `CreationInfo` structures match the summary in `GenieDatParser/src/sections/civilization/type_info/building_info.py`, `GenieDatParser/src/sections/civilization/type_info/combat_info.py`, `GenieDatParser/src/sections/civilization/type_info/creation_info.py`.
- `TrainLocation` exists and is versioned (old vs new layout).
- `CombatInfo` uses `RetrieverCombiner` for `base_armor` and `Array16[DamageClass]` for `attacks` and `armors`.
Notes and gaps:
- The parent container is the `Unit` class in `GenieDatParser/src/sections/civilization/unit.py`.
- `CreationInfo` includes charge and UI fields (`charge_*`, `button_*`, `invulnerability_level`, conversion modifiers) not covered in the summary.
- `CombatInfo` contains later-version fields such as `bonus_damage_resistance`, `blast_damage`, `damage_reflection`, `friendly_fire_damage`, `interrupt_frame`, `garrison_firepower`, and `attack_graphic2`.

### A04 - Civilization TypeB (Task/Movement/Projectile)
Alignment:
- `TaskInfo` fields and versioned `drop_site_unit_ids` are accurate in `GenieDatParser/src/sections/civilization/type_info/task_info.py`.
- `MovementInfo` core fields match in `GenieDatParser/src/sections/civilization/type_info/movement_info.py`.
- `ProjectileInfo` layout matches in `GenieDatParser/src/sections/civilization/type_info/projectile_info.py`.
Notes and gaps:
- `MovementInfo` includes `trail_mode`, `trail_spacing`, `old_move_algorithm`, `standing_yaw_revolution_time`, and `min_collision_size_multiplier`, which are not mentioned in the summary.
- `TaskInfo.tasks` only exists for Versions 3.7-4.5 and 7.2+; 5.7-5.9 tasks are represented under `UnitData` instead.

### A05 - Color Data
Alignment:
- `PlayerColorData1` and `PlayerColorData2` field layouts match the summary in `GenieDatParser/src/sections/color_data/player_color_data1.py` and `GenieDatParser/src/sections/color_data/player_color_data2.py`.
- `ColorData` holds 16 entries per version in `GenieDatParser/src/sections/color_data/color_data.py`.
Notes and gaps:
- There is no unified `player_colors` combiner; the active field is `player_color_data_age1` or `player_color_data_age2` based on version.

### A06 - Map Data (Container and Info)
Alignment:
- `MapData.num_maps` sets repeats for `map_info1` and `map_info2` in `GenieDatParser/src/sections/map_data/map_data.py`.
- `MapInfo1` is duplicate metadata; `MapInfo2` uses its own counts for lands/terrains/units/elevations in `GenieDatParser/src/sections/map_data/map_info1.py` and `GenieDatParser/src/sections/map_data/map_info2.py`.
Notes and gaps:
- `MapInfo2` includes `elevations` of type `MapElevation` with its own structure in `GenieDatParser/src/sections/map_data/map_elevation.py`.

### A07 - Map Data (Land/Terrain/Unit)
Alignment:
- Roles of `MapLand`, `MapTerrain`, and `MapUnit` match the summary in `GenieDatParser/src/sections/map_data/map_land.py`, `GenieDatParser/src/sections/map_data/map_terrain.py`, and `GenieDatParser/src/sections/map_data/map_unit.py`.
Notes and gaps:
- `MapLand` includes additional fields: `land_avoidance_distance`, `zone`, `land_usage_percent`, `by_player_mode`, `start_area_radius`, `terrain_edge_fade`, `clumpiness_factor`.
- `MapTerrain` includes `edge_spacing`, `placement_zone`, and `clumpiness_factor`.
- `MapUnit` includes grouping fields: `group_mode`, `scale_mode`, `group_size`, `group_size_delta`, `num_groups`, `group_radius`, `set_place_for_all_players`.

### A08 - Sounds and SWGB
Alignment:
- `Sound` and `SoundFile` roles match in `GenieDatParser/src/sections/sounds/sound.py` and `GenieDatParser/src/sections/sounds/sound_file.py`.
- `SwgbData` exists with SWGB-only counts in `GenieDatParser/src/sections/swgb_data/swgb_data.py`.
Notes and gaps:
- `Sound.total_probability` is versioned (`_total_probability_de1`, `_total_probability_de2`) and combined with `RetrieverCombiner`.
- `SoundFile` uses DE string signatures with `str16` and fixed-length `Str` for AoE1/AoE2/SWGB filenames.
- `SwgbData` includes `unknown1` and `unknown2` fields not mentioned in the summary.

### A09 - Sprite Data
Alignment:
- `FacetAttackSound`, `SpriteDelta`, and `Sprite` core layouts match in `GenieDatParser/src/sections/sprite_data/facet_attack_sound.py`, `GenieDatParser/src/sections/sprite_data/sprite_delta.py`, and `GenieDatParser/src/sections/sprite_data/sprite.py`.
- Dynamic repeats for deltas and facet attack sounds are consistent with the summary.
Notes and gaps:
- `Sprite` includes `particle_effect_name`, `wwise_sound_id`, `facets_have_attack_sounds`, `speed_mult`, `replay_delay`, `sequence_type`, `mirroring_mode`, and `editor_mode`.
- `SpriteDelta` includes `_parent_sprite_ptr` and padding fields.

### A10 - Tech and Tech Effect
Alignment:
- `Tech`, `TechCost`, `EffectCommand`, and `TechEffect` roles match in `GenieDatParser/src/sections/tech/tech.py`, `GenieDatParser/src/sections/tech/tech_cost.py`, `GenieDatParser/src/sections/tech_effect/effect_command.py`, and `GenieDatParser/src/sections/tech_effect/tech_effect.py`.
- `ResearchLocation` exists and is used in newer versions.
Notes and gaps:
- `Tech` includes `min_required_techs`, `full_tech_tree_mode`, `effect_id`, `type`, `help_str_id`, `tech_tree_str_id`, `repeatable`, `name2`, and `research_locations` (min_ver 8.8).
- `TechEffect` names are versioned and combined with `RetrieverCombiner`.

### A11 - Tech Tree (Root/Age/Building)
Alignment:
- `TechTree` container counts and versioned `num_units` handling match in `GenieDatParser/src/sections/tech_tree/tech_tree.py`.
- `TechTreeAge` and `TechTreeBuilding` structures align in `GenieDatParser/src/sections/tech_tree/tech_tree_age.py` and `GenieDatParser/src/sections/tech_tree/tech_tree_building.py`.
Notes and gaps:
- `TechTree` includes telemetry-like fields (`_time_slice`, `_unit_kill_rate`, etc.) and `num_groups`.
- `TechTreeAge` includes `buildings_per_zone`, `group_length_per_zone`, `max_age_length`, and `node_type`.
- `TechTreeBuilding` includes `total_children_by_age` and `initial_children_by_age` arrays.

### A12 - Tech Tree (Tech/Unit/Dependency)
Alignment:
- `TechTreeDependency` type mapping matches in `GenieDatParser/src/sections/tech_tree/tech_tree_dependency.py`.
- `TechTreeTech` and `TechTreeUnit` layouts match the summary in `GenieDatParser/src/sections/tech_tree/tech_tree_tech.py` and `GenieDatParser/src/sections/tech_tree/tech_tree_unit.py`.
Notes and gaps:
- `num_used_dependencies` fields exist across the tech tree structs and are not emphasized in the summaries.

### A13 - Terrain Data (TerrainData/Terrain)
Alignment:
- Versioned terrain counts, borders, tile sizes, elevation sprites, and audio fields align in `GenieDatParser/src/sections/terrain_data/terrain_data.py` and `GenieDatParser/src/sections/terrain_data/terrain.py`.
Notes and gaps:
- `TerrainData` includes several map and pointer fields (`_map_width`, `_map_height`, `_world_width`, `_world_height`, `_search_map_ptr`, etc.) that are not covered in the summary.
- `Terrain` includes `phantom` and SWGB/AoE blobs that remain unexplained.

### A14 - Terrain Support Structures
Alignment:
- `TerrainBorder`, `TerrainUnit`, and `TerrainAnimation` match in `GenieDatParser/src/sections/terrain_data/terrain_border.py`, `GenieDatParser/src/sections/terrain_data/terrain_unit.py`, and `GenieDatParser/src/sections/terrain_data/terrain_animation.py`.
Notes and gaps:
- None beyond the fixed-length `Str[13]` names on borders.

### A15 - Terrain Tables and Unit Data
Alignment:
- `TerrainTableData` repeat logic and `TerrainTable` layout match in `GenieDatParser/src/sections/terrain_table_data/terrain_table_data.py` and `GenieDatParser/src/sections/terrain_table_data/terrain_table.py`.
- `TerrainPassGraphic`, `UnitData`, `UnitLine`, and `UnitTask` structures align in `GenieDatParser/src/sections/terrain_table_data/terrain_pass_graphic.py`, `GenieDatParser/src/sections/unit_data/unit_data.py`, `GenieDatParser/src/sections/unit_data/unit_line.py`, and `GenieDatParser/src/sections/unit_data/unit_task.py`.
Notes and gaps:
- `num_used_terrains` is passed via `set_key` and is not auto-synced on write; list lengths must be managed manually.
- `UnitData.unit_lines` is only present for Version(5,9); `UnitData.tasks` exists for Version(5,7)+ with nested `Option8[Array16[UnitTask]]`.

## Overall assessment
- The 15 summaries are structurally accurate and consistent with the codebase, especially around `bfp_rs` patterns and version gating.
- Most differences are omissions of additional fields, pointer values, or later-version flags rather than contradictions.
- Open questions in the summaries are usually answered by nearby code (for example, `Unit` aggregates the type info classes).
- The main operational risks are write-time count sync for sections that only set repeats on read.
