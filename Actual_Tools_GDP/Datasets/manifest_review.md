# Attribute Manifest Review

**Total Attributes:** 147

## Summary by Storage Type

| Storage Type | Count |
|--------------|-------|
| Bitmask | 8 |
| Enum | 10 |
| Reference | 33 |
| Value | 96 |

## Summary by Link Target

| Link Target | Count |
|-------------|-------|
| Enum:BlastAttackLevel | 1 |
| Enum:ChargeType | 1 |
| Enum:CombatAbility | 1 |
| Enum:DisabledFlag | 1 |
| Enum:FogVisibility | 1 |
| Enum:FormationCategory | 1 |
| Enum:GarrisonType | 1 |
| Enum:HeroStatus | 1 |
| Enum:InterfaceKind | 1 |
| Enum:ObstructionType | 1 |
| Enum:OcclusionMode | 1 |
| Enum:SmartProjectileMode | 1 |
| Enum:SpecialAbility | 1 |
| Enum:TerrainTable | 2 |
| Enum:TerrainType | 1 |
| Enum:UnitTrait | 1 |
| Enum:VanishMode | 1 |
| GraphicHandle | 19 |
| SoundHandle | 8 |
| UnitHandle | 6 |

## Full Attribute Table

| ID | Name | Storage | Link Target | Type | Description |
|----|------|---------|-------------|------|-------------|
| 0 | HIT_POINTS | Value | None | int | Unit hit points |
| 1 | LINE_OF_SIGHT | Value | None | float | Vision range |
| 2 | GARRISON_CAPACITY | Value | None | int | Max units that can garrison |
| 3 | UNIT_SIZE_X | Value | None | float | Collision box X |
| 4 | UNIT_SIZE_Y | Value | None | float | Collision box Y |
| 5 | MOVEMENT_SPEED | Value | None | float | Movement speed |
| 6 | ROTATION_SPEED | Value | None | float | Turn rate |
| 8 | ARMOR | Value | None | int | Armor class amount |
| 9 | ATTACK | Value | None | int | Attack class amount |
| 10 | ATTACK_RELOAD_TIME | Value | None | float | Attack cooldown |
| 11 | ACCURACY_PERCENT | Value | None | int | Hit chance percentage |
| 12 | MAXIMUM_RANGE | Value | None | float | Attack range |
| 13 | WORK_RATE | Value | None | float | Gather/build speed |
| 14 | CARRY_CAPACITY | Value | None | int | Resource carry limit |
| 15 | BASE_ARMOR | Value | None | int | Base armor value |
| 16 | PROJECTILE_UNIT | Reference | UnitHandle | int | Projectile unit ID |
| 17 | ICON_GRAPHICS_ANGLE | Value | None | int | Icon display angle |
| 18 | TERRAIN_DEFENSE_BONUS | Enum | Enum:TerrainTable | int | Terrain bonus (TerrainTable class) |
| 19 | ENABLE_SMART_PROJECTILE | Enum | Enum:SmartProjectileMode | int | 1=track target 2=friendly fire mult |
| 20 | MINIMUM_RANGE | Value | None | float | Minimum attack range |
| 21 | AMOUNT_1ST_RESOURCE_STORAGE | Value | None | float | Resource storage 1 |
| 22 | BLAST_WIDTH | Value | None | float | Area damage radius |
| 23 | SEARCH_RADIUS | Value | None | float | Target search radius |
| 24 | HIDDEN_DAMAGE_RESISTANCE | Value | None | float | Hidden damage resist |
| 25 | ICON_ID | Value | None | int | Icon index |
| 26 | AMOUNT_2ND_RESOURCE_STORAGE | Value | None | float | Resource storage 2 |
| 27 | AMOUNT_3RD_RESOURCE_STORAGE | Value | None | float | Resource storage 3 |
| 28 | FOG_VISIBILITY | Enum | Enum:FogVisibility | int | 0=hidden 1=always 2=if alive 3=inverted 4=doppel |
| 29 | OCCLUSION_MODE | Bitmask | Enum:OcclusionMode | int | 0=none 1=outline 2=occlude 4=construct 8=gates |
| 30 | GARRISON_TYPE | Bitmask | Enum:GarrisonType | int | What can garrison |
| 32 | UNIT_SIZE_Z | Value | None | float | Collision box Z |
| 33 | CAN_BE_BUILT_ON | Value | None | int | Foundation flag |
| 34 | FOUNDATION_TERRAIN | Enum | Enum:TerrainType | int | Terrain type under building |
| 40 | HERO_STATUS | Bitmask | Enum:HeroStatus | int | Hero properties |
| 41 | FRAME_DELAY | Value | None | int | Attack frame delay |
| 42 | TRAIN_LOCATION | Reference | UnitHandle | int | Building that trains this |
| 43 | TRAIN_BUTTON | Value | None | int | Button position |
| 44 | BLAST_ATTACK_LEVEL | Bitmask | Enum:BlastAttackLevel | int | Primary 0-3 + Secondary 0/64/128 |
| 45 | BLAST_DEFENSE_LEVEL | Value | None | int | Blast defense type |
| 46 | SHOWN_ATTACK | Value | None | int | Displayed attack |
| 47 | SHOWN_RANGE | Value | None | int | Displayed range |
| 48 | SHOWN_MELEE_ARMOR | Value | None | int | Displayed melee armor |
| 49 | SHOWN_PIERCE_ARMOR | Value | None | int | Displayed pierce armor |
| 50 | UNIT_NAME_STRING_ID | Value | None | int | Name string ID |
| 51 | UNIT_SHORT_DESCRIPTION_STRING_ID | Value | None | int | Description string ID |
| 53 | TERRAIN_RESTRICTION | Enum | Enum:TerrainTable | int | Terrain restriction class |
| 54 | UNIT_TRAIT | Bitmask | Enum:UnitTrait | int | Unit trait flags |
| 55 | UNIT_CIVILIZATION | Value | None | int | Civ restriction (unused) |
| 56 | UNIT_TRAIT_PIECE | Value | None | int | Trait piece value |
| 57 | DEAD_UNIT_ID | Reference | UnitHandle | int | Unit on death |
| 58 | HOTKEY_ID | Value | None | int | Hotkey binding |
| 59 | MAXIMUM_CHARGE | Value | None | float | Max charge amount |
| 60 | RECHARGE_RATE | Value | None | float | Charge regen rate |
| 61 | CHARGE_EVENT | Value | None | int | Charge trigger event |
| 62 | CHARGE_TYPE | Enum | Enum:ChargeType | int | Charge ability type |
| 63 | COMBAT_ABILITY | Bitmask | Enum:CombatAbility | int | Combat ability flags |
| 64 | ATTACK_DISPERSION | Value | None | float | Random aim spread |
| 65 | SECONDARY_PROJECTILE_UNIT | Reference | UnitHandle | int | Secondary projectile |
| 66 | BLOOD_UNIT_ID | Reference | UnitHandle | int | Blood effect unit |
| 67 | PROJECTILE_HIT_MODE | Value | None | int | Hit behavior |
| 68 | PROJECTILE_VANISH_MODE | Bitmask | Enum:VanishMode | int | 1=pass-through 2=spawn dead unit |
| 69 | PROJECTILE_ARC | Value | None | float | Arc trajectory |
| 70 | ATTACK_GRAPHIC | Reference | GraphicHandle | int | Attack animation |
| 71 | STANDING_GRAPHIC | Reference | GraphicHandle | int | Idle animation |
| 72 | STANDING_GRAPHIC_2 | Reference | GraphicHandle | int | Idle animation 2 |
| 73 | DYING_GRAPHIC | Reference | GraphicHandle | int | Death animation |
| 74 | UNDEAD_GRAPHIC | Reference | GraphicHandle | int | Undead animation |
| 75 | WALKING_GRAPHIC | Reference | GraphicHandle | int | Walk animation |
| 76 | RUNNING_GRAPHIC | Reference | GraphicHandle | int | Run animation |
| 77 | SPECIAL_GRAPHIC | Reference | GraphicHandle | int | Special animation |
| 78 | OBSTRUCTION_TYPE | Enum | Enum:ObstructionType | int | Obstruction shape |
| 81 | SPECIAL_ABILITY | Enum | Enum:SpecialAbility | int | Special ability type |
| 82 | IDLE_ATTACK_GRAPHIC | Reference | GraphicHandle | int | Idle attack anim |
| 83 | HERO_GLOW_GRAPHIC | Reference | GraphicHandle | int | Hero glow effect |
| 84 | GARRISON_GRAPHIC | Reference | GraphicHandle | int | Garrison animation |
| 85 | CONSTRUCTION_GRAPHIC | Reference | GraphicHandle | int | Construction anim |
| 86 | SNOW_GRAPHIC | Reference | GraphicHandle | int | Snow variant |
| 87 | DESTRUCTION_GRAPHIC | Reference | GraphicHandle | int | Destruction anim |
| 88 | DESTRUCTION_RUBBLE_GRAPHIC | Reference | GraphicHandle | int | Rubble graphic |
| 89 | RESEARCHING_GRAPHIC | Reference | GraphicHandle | int | Research anim |
| 90 | RESEARCH_COMPLETED_GRAPHIC | Reference | GraphicHandle | int | Research done anim |
| 91 | DAMAGE_GRAPHIC | Reference | GraphicHandle | int | Damage overlay |
| 92 | SELECTION_SOUND_ID | Reference | SoundHandle | int | Selection sound |
| 93 | SELECTION_SOUND_EVENT | Value | None | int | Selection sound event |
| 94 | DYING_SOUND_ID | Reference | SoundHandle | int | Death sound |
| 95 | DYING_SOUND_EVENT | Value | None | int | Death sound event |
| 96 | TRAIN_SOUND_ID | Reference | SoundHandle | int | Train sound |
| 97 | TRAIN_SOUND_EVENT | Value | None | int | Train sound event |
| 98 | DAMAGE_SOUND_ID | Reference | SoundHandle | int | Damage sound |
| 99 | DAMAGE_SOUND_EVENT | Value | None | int | Damage sound event |
| 100 | RESOURCE_COSTS | Value | None | tuple | Resource cost array |
| 101 | TRAIN_TIME | Value | None | int | Training time |
| 102 | TOTAL_MISSILES | Value | None | int | Missiles per attack |
| 103 | FOOD_COSTS | Value | None | int | Food cost |
| 104 | WOOD_COSTS | Value | None | int | Wood cost |
| 105 | GOLD_COSTS | Value | None | int | Gold cost |
| 106 | STONE_COSTS | Value | None | int | Stone cost |
| 107 | MAX_TOTAL_PROJECTILES | Value | None | int | Max projectiles |
| 108 | GARRISON_HEAL_RATE | Value | None | float | Heal rate in garrison |
| 109 | REGENERATION_RATE | Value | None | float | HP regen rate |
| 110 | POPULATION_HEADROOM_STORAGE | Value | None | int | Pop headroom |
| 111 | ADDITIONAL_MIN_CONVERSION_TIME | Value | None | int | Extra min convert time |
| 112 | ADDITIONAL_MAX_CONVERSION_TIME | Value | None | int | Extra max convert time |
| 113 | ADDITIONAL_CONVERSION_RESISTANCE_LEVEL | Value | None | int | Convert resist |
| 114 | FORMATION_CATEGORY | Enum | Enum:FormationCategory | int | Formation type |
| 115 | AREA_DAMAGE | Value | None | float | Area damage amount |
| 116 | MELEE_ARMOR_AURA | Value | None | float | Armor aura amount |
| 117 | BLOCKAGE_CLASS_PIERCE_ARMOR_AURA | Value | None | float | Pierce aura |
| 118 | MELEE_DAMAGE_DEFLECTION | Value | None | float | Damage deflection |
| 119 | FRIENDLY_FIRE_MULTIPLIER | Value | None | float | Friendly fire mult |
| 120 | HP_BASED_REGENERATION | Value | None | float | HP-based regen |
| 121 | ABILITY_ICON | Value | None | int | Ability icon ID |
| 122 | SHORT_TOOLTIP | Value | None | int | Short tooltip ID |
| 123 | LONG_TOOLTIP | Value | None | int | Long tooltip ID |
| 124 | ABILITY_HOTKEY | Value | None | int | Ability hotkey |
| 126 | TRAIN_LIMIT_FOR_DISABLED_UNITS | Value | None | int | Disabled train limit |
| 127 | DISABLED_FLAG | Bitmask | Enum:DisabledFlag | int | 1=disabled 2=limited 4=retrainable 8=hide |
| 128 | ATTACK_PRIORITY | Value | None | int | Attack priority |
| 129 | INVULNERABILITY_LEVEL | Value | None | int | Invulnerability |
| 130 | GARRISON_FIREPOWER | Value | None | float | Garrison attack power |
| 131 | SECONDARY_ATTACK_GRAPHIC | Reference | GraphicHandle | int | Secondary attack anim |
| 132 | COMMAND_SOUND_ID | Reference | SoundHandle | int | Command sound |
| 133 | COMMAND_SOUND_EVENT | Value | None | int | Command sound event |
| 134 | MOVE_SOUND_ID | Reference | SoundHandle | int | Move sound |
| 135 | MOVE_SOUND_EVENT | Value | None | int | Move sound event |
| 136 | CONSTRUCTION_SOUND_ID | Reference | SoundHandle | int | Construction sound |
| 137 | CONSTRUCTION_SOUND_EVENT | Value | None | int | Construction event |
| 138 | TRANSFORM_SOUND_ID | Reference | SoundHandle | int | Transform sound |
| 139 | TRANSFORM_SOUND_EVENT | Value | None | int | Transform event |
| 140 | SHARED_SELECTION | Value | None | int | Shared selection flag |
| 141 | INTERFACE_KIND | Enum | Enum:InterfaceKind | int | UI interface type |
| 142 | COMBAT_LEVEL | Value | None | int | Combat level |
| 143 | INTERACTION_MODE | Value | None | int | Interaction mode |
| 144 | MINIMAP_MODE | Value | None | int | Minimap display mode |
| 145 | TRAILING_UNIT | Reference | UnitHandle | int | Trailing unit ID |
| 146 | TRAIL_MODE | Value | None | int | Trail mode |
| 147 | TRAIL_DENSITY | Value | None | float | Trail density |
| 148 | PROJECTILE_GRAPHIC_DISPLACEMENT_X | Value | None | float | Projectile offset X |
| 149 | PROJECTILE_GRAPHIC_DISPLACEMENT_Y | Value | None | float | Projectile offset Y |
| 150 | PROJECTILE_GRAPHIC_DISPLACEMENT_Z | Value | None | float | Projectile offset Z |
| 151 | PROJECTILE_SPAWNING_AREA_WIDTH | Value | None | float | Spawn area width |
| 152 | PROJECTILE_SPAWNING_AREA_LENGTH | Value | None | float | Spawn area length |
| 153 | PROJECTILE_SPAWNING_AREA_RANDOMNESS | Value | None | float | Spawn randomness |
| 154 | DAMAGE_GRAPHICS_ENTRY_MOD | Value | None | int | Damage graphic mod |
| 155 | DAMAGE_GRAPHICS_TOTAL_NUM | Value | None | int | Total damage graphics |
| 156 | DAMAGE_GRAPHIC_PERCENT | Value | None | int | Damage threshold % |
| 157 | DAMAGE_GRAPHIC_APPLY_MODE | Value | None | int | Damage apply mode |