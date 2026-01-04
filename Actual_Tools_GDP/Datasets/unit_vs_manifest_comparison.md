# GenieUnit Attributes vs Manifest Comparison

## Summary

| Category | Count |
|----------|-------|
| Total unique genieutils attributes | 199 |
| In Attribute Enum (manifest) | 49 |
| NOT in Attribute Enum | 150 |

## Understanding the Discrepancy

The 150 "missing" attributes are **normal and correct**. The Attribute enum represents **modifiable game attributes** (used by triggers, technologies, effects), while genieutils contains **all internal data fields**.

### Categories of "Missing" Attributes:

**1. Structural/Pointer Fields (not modifiable)**
- `bird`, `dead_fish`, `type_50`, `projectile`, `creatable`, `building` (component pointers)
- `id`, `type`, `copy_id`, `base_id`, `name` (identity fields)

**2. Internal Lists/Collections**
- `attacks`, `armours`, `tasks`, `annexes`, `drop_sites`, `train_locations`
- `resource_storages`, `damage_graphics`, `looting_table`

**3. Editor/Display Only**
- `hide_in_editor`, `editor_selection_colour`, `sort_number`
- `language_dll_*` (string IDs)

**4. Legacy/Obsolete Fields**
- `old_move_algorithm`, `old_size_class`, `old_overlap_id`, `old_attack_reaction`

**5. WWise Sound IDs (modern replacements)**
- `wwise_*` fields (WWise audio engine IDs)

---

## Attributes IN BOTH (need manifest entry)

These are the 49 attributes that appear in both genieutils AND Attribute enum:

| Field Name | Attribute Enum Name | Component |
|------------|---------------------|-----------|
| hit_points | HIT_POINTS | Unit |
| line_of_sight | LINE_OF_SIGHT | Unit |
| garrison_capacity | GARRISON_CAPACITY | Unit |
| standing_graphic | STANDING_GRAPHIC | Unit |
| dying_graphic | DYING_GRAPHIC | Unit |
| undead_graphic | UNDEAD_GRAPHIC | Unit |
| dead_unit_id | DEAD_UNIT_ID | Unit |
| blood_unit_id | BLOOD_UNIT_ID | Unit |
| can_be_built_on | CAN_BE_BUILT_ON | Unit |
| icon_id | ICON_ID | Unit |
| fog_visibility | FOG_VISIBILITY | Unit |
| terrain_restriction | TERRAIN_RESTRICTION | Unit |
| blast_defense_level | BLAST_DEFENSE_LEVEL | Unit |
| combat_level | COMBAT_LEVEL | Unit |
| interaction_mode | INTERACTION_MODE | Unit |
| minimap_mode | MINIMAP_MODE | Unit |
| interface_kind | INTERFACE_KIND | Unit |
| occlusion_mode | OCCLUSION_MODE | Unit |
| obstruction_type | OBSTRUCTION_TYPE | Unit |
| trait | UNIT_TRAIT | Unit |
| search_radius | SEARCH_RADIUS | Bird |
| work_rate | WORK_RATE | Bird |
| rotation_speed | ROTATION_SPEED | DeadFish |
| walking_graphic | WALKING_GRAPHIC | DeadFish |
| running_graphic | RUNNING_GRAPHIC | DeadFish |
| accuracy_percent | ACCURACY_PERCENT | Type50 |
| base_armor | BASE_ARMOR | Type50 |
| blast_attack_level | BLAST_ATTACK_LEVEL | Type50 |
| blast_width | BLAST_WIDTH | Type50 |
| frame_delay | FRAME_DELAY | Type50 |
| max_range | MAXIMUM_RANGE | Type50 |
| min_range | MINIMUM_RANGE | Type50 |
| attack_graphic | ATTACK_GRAPHIC | Type50 |
| projectile_arc | PROJECTILE_ARC | Projectile |
| attack_priority | ATTACK_PRIORITY | Creatable |
| charge_event | CHARGE_EVENT | Creatable |
| charge_type | CHARGE_TYPE | Creatable |
| hero_mode | HERO_STATUS | Creatable |
| invulnerability_level | INVULNERABILITY_LEVEL | Creatable |
| max_charge | MAXIMUM_CHARGE | Creatable |
| recharge_rate | RECHARGE_RATE | Creatable |
| secondary_projectile_unit | SECONDARY_PROJECTILE_UNIT | Creatable |
| special_ability | SPECIAL_ABILITY | Creatable |
| special_graphic | SPECIAL_GRAPHIC | Creatable |
| foundation_terrain_id | FOUNDATION_TERRAIN | Building |
| garrison_heal_rate | GARRISON_HEAL_RATE | Building |
| garrison_type | GARRISON_TYPE | Building |
| researching_graphic | RESEARCHING_GRAPHIC | Building |
| research_completed_graphic | RESEARCH_COMPLETED_GRAPHIC | Building |

---

## User's Corrections Applied

### TerrainTable vs TerrainType:
- ID 18 (TERRAIN_DEFENSE_BONUS) → `Enum:TerrainTable`
- ID 34 (FOUNDATION_TERRAIN) → `Enum:TerrainType`
- ID 53 (TERRAIN_RESTRICTION) → `Enum:TerrainTable`

### New Enum Values to Add:
- `FogVisibility` (ID 28)
- `OcclusionMode` (ID 29)
- `BlastAttackLevel` (ID 44)
- `ProjectileVanishMode` (ID 68)
- `SelectionEffect` (ID for selection_effect)
- `DisabledFlag` (ID 127)
