# Complete List of 150 GenieUnit Attributes NOT in Attribute Enum

These are structural/internal fields used by genieutils, not modifiable game attributes.

## Unit (Base Class) - 55 NOT in enum

| Attribute | Type | Purpose |
|-----------|------|---------|
| `id` | int | Unit ID |
| `type` | int | Unit type class |
| `name` | str | Internal name |
| `base_id` | int | Template unit ID |
| `copy_id` | int | Copy source ID |
| `class_` | int | Unit class |
| `civilization` | int | Civ restriction |
| `enabled` | bool | Enabled flag |
| `disabled` | bool | Disabled flag |
| `speed` | float | Movement speed |
| `collision_size_x` | float | Collision X |
| `collision_size_y` | float | Collision Y |
| `collision_size_z` | float | Collision Z |
| `clearance_size` | tuple | Clearance |
| `outline_size_x` | float | Outline X |
| `outline_size_y` | float | Outline Y |
| `outline_size_z` | float | Outline Z |
| `selection_sound` | int | Selection sound ID |
| `dying_sound` | int | Dying sound ID |
| `train_sound` | int | Train sound ID |
| `damage_sound` | int | Damage sound ID |
| `resource_storages` | list | Resource storage slots |
| `damage_graphics` | list | Damage graphics list |
| `language_dll_name` | int | Name string ID |
| `language_dll_creation` | int | Creation string ID |
| `language_dll_help` | int | Help string ID |
| `language_dll_hotkey_text` | int | Hotkey string ID |
| `hot_key` | int | Hotkey ID |
| `hide_in_editor` | bool | Hide in editor |
| `editor_selection_colour` | int | Editor color |
| `sort_number` | int | Sort order |
| `trait` | int | Unit trait |
| `nothing` | int | Unused |
| `selection_effect` | int | Selection effect |
| `placement_terrain` | int | Placement terrain |
| `placement_side_terrain` | int | Side terrain |
| `resource_capacity` | int | Resource capacity |
| `resource_decay` | float | Decay rate |
| `resource_gather_group` | int | Gather group |
| `enable_auto_gather` | bool | Auto gather |
| `create_doppelganger_on_death` | bool | Doppelganger |
| `recyclable` | bool | Recyclable |
| `fly_mode` | int | Fly mode |
| `hill_mode` | int | Hill mode |
| `multiple_attribute_mode` | int | Multi-attr mode |
| `minimap_color` | int | Minimap color |
| `obstruction_class` | int | Obstruction class |
| `convert_terrain` | int | Convert terrain |
| `old_attack_reaction` | int | Legacy field |
| `old_portrait_pict` | int | Legacy field |
| `scenario_triggers_1` | int | Trigger data |
| `scenario_triggers_2` | int | Trigger data |
| `wwise_train_sound_id` | int | WWise sound |
| `wwise_damage_sound_id` | int | WWise sound |
| `wwise_selection_sound_id` | int | WWise sound |
| `wwise_dying_sound_id` | int | WWise sound |

## Component Pointers
| Attribute | Purpose |
|-----------|---------|
| `bird` | Bird component |
| `dead_fish` | DeadFish component |
| `type_50` | Type50 (combat) component |
| `projectile` | Projectile component |
| `creatable` | Creatable component |
| `building` | Building component |

---

## Bird Component - 9 NOT in enum

| Attribute | Purpose |
|-----------|---------|
| `default_task_id` | Default task |
| `drop_sites` | Drop site list |
| `tasks` | Task list |
| `task_swap_group` | Task group |
| `attack_sound` | Attack sound |
| `move_sound` | Move sound |
| `run_pattern` | Run pattern |
| `wwise_attack_sound_id` | WWise sound |
| `wwise_move_sound_id` | WWise sound |

---

## DeadFish Component - 12 NOT in enum

| Attribute | Purpose |
|-----------|---------|
| `tracking_unit` | Tracking unit ID |
| `tracking_unit_mode` | Tracking mode |
| `tracking_unit_density` | Tracking density |
| `turn_radius` | Turn radius |
| `turn_radius_speed` | Turn speed |
| `max_yaw_per_second_moving` | Yaw moving |
| `max_yaw_per_second_stationary` | Yaw stationary |
| `stationary_yaw_revolution_time` | Yaw time |
| `min_collision_size_multiplier` | Collision mult |
| `old_move_algorithm` | Legacy field |
| `old_size_class` | Legacy field |

---

## Type50 Component - 17 NOT in enum

| Attribute | Purpose |
|-----------|---------|
| `attacks` | Attack list |
| `armours` | Armour list |
| `reload_time` | Reload time |
| `projectile_unit_id` | Projectile ID |
| `accuracy_dispersion` | Accuracy |
| `attack_graphic_2` | Attack graphic 2 |
| `graphic_displacement` | Displacement |
| `displayed_attack` | Shown attack |
| `displayed_range` | Shown range |
| `displayed_melee_armour` | Shown melee |
| `displayed_reload_time` | Shown reload |
| `blast_damage` | Blast damage |
| `defense_terrain_bonus` | Defense bonus |
| `bonus_damage_resistance` | Damage resist |
| `break_off_combat` | Combat ability |
| `damage_reflection` | Damage reflect |
| `friendly_fire_damage` | FF damage |
| `interrupt_frame` | Interrupt frame |

---

## Projectile Component - 5 NOT in enum

| Attribute | Purpose |
|-----------|---------|
| `projectile_type` | Type |
| `smart_mode` | Smart mode |
| `hit_mode` | Hit mode |
| `vanish_mode` | Vanish mode |
| `area_effect_specials` | Area effects |

---

## Creatable Component - 22 NOT in enum

| Attribute | Purpose |
|-----------|---------|
| `resource_costs` | Cost tuple |
| `train_locations` | Train locations |
| `total_projectiles` | Missiles |
| `max_total_projectiles` | Max missiles |
| `projectile_spawning_area` | Spawn area |
| `conversion_chance_mod` | Convert chance |
| `min_conversion_time_mod` | Min convert |
| `max_conversion_time_mod` | Max convert |
| `hero_mode` | Hero status |
| `garrison_graphic` | Garrison graphic |
| `hero_glow_graphic` | Glow graphic |
| `idle_attack_graphic` | Idle attack |
| `spawning_graphic` | Spawn graphic |
| `upgrade_graphic` | Upgrade graphic |
| `charge_target` | Charge target |
| `charge_projectile_unit` | Charge projectile |
| `displayed_pierce_armour` | Shown pierce |
| `button_icon_id` | Button icon |
| `button_short_tooltip_id` | Short tooltip |
| `button_extended_tooltip_id` | Long tooltip |
| `button_hotkey_action` | Button hotkey |
| `rear_attack_modifier` | Rear attack |
| `flank_attack_modifier` | Flank attack |
| `creatable_type` | Formation type |

---

## Building Component - 22 NOT in enum

| Attribute | Purpose |
|-----------|---------|
| `construction_graphic_id` | Construction |
| `snow_graphic_id` | Snow graphic |
| `destruction_graphic_id` | Destruction |
| `destruction_rubble_graphic_id` | Rubble |
| `construction_sound` | Construction sound |
| `transform_sound` | Transform sound |
| `wwise_construction_sound_id` | WWise sound |
| `wwise_transform_sound_id` | WWise sound |
| `foundation_terrain_id` | Foundation |
| `garrison_repair_rate` | Repair rate |
| `head_unit` | Head unit |
| `transform_unit` | Transform unit |
| `pile_unit` | Pile unit |
| `adjacent_mode` | Adjacent mode |
| `graphics_angle` | Graphics angle |
| `disappears_when_built` | Disappears |
| `stack_unit_id` | Stack unit |
| `tech_id` | Tech ID |
| `can_burn` | Can burn |
| `annexes` | Annexes tuple |
| `looting_table` | Looting table |
| `old_overlap_id` | Legacy field |
