from enum import IntEnum


class Attribute(IntEnum):
    """
    Genie Editor Attributes.
<<<<<<< HEAD

=======
    
>>>>>>> origin/refactor-port-managers-to-gdp-783808832176151754
    Source: https://ageofempires.fandom.com/wiki/Genie_Editor#Attributes
    """
    HIT_POINTS = 0
    LINE_OF_SIGHT = 1
    GARRISON_CAPACITY = 2
    UNIT_SIZE_X = 3
    UNIT_SIZE_Y = 4
    MOVEMENT_SPEED = 5
    ROTATION_SPEED = 6
    ARMOR = 8
    ATTACK = 9
    ATTACK_RELOAD_TIME = 10
    ACCURACY_PERCENT = 11
    MAXIMUM_RANGE = 12
    WORK_RATE = 13
    CARRY_CAPACITY = 14
    BASE_ARMOR = 15
    PROJECTILE_UNIT = 16
    ICON_GRAPHICS_ANGLE = 17
    TERRAIN_DEFENSE_BONUS = 18
    ENABLE_SMART_PROJECTILE = 19
    MINIMUM_RANGE = 20
    AMOUNT_1ST_RESOURCE_STORAGE = 21
    BLAST_WIDTH = 22
    SEARCH_RADIUS = 23
    HIDDEN_DAMAGE_RESISTANCE = 24
    ICON_ID = 25
    AMOUNT_2ND_RESOURCE_STORAGE = 26
    AMOUNT_3RD_RESOURCE_STORAGE = 27
    FOG_VISIBILITY = 28
    OCCLUSION_MODE = 29
    GARRISON_TYPE = 30
    UNIT_SIZE_Z = 32
    CAN_BE_BUILT_ON = 33
    FOUNDATION_TERRAIN = 34
    HERO_STATUS = 40
    FRAME_DELAY = 41
    TRAIN_LOCATION = 42
    TRAIN_BUTTON = 43
    BLAST_ATTACK_LEVEL = 44
    BLAST_DEFENSE_LEVEL = 45
    SHOWN_ATTACK = 46
    SHOWN_RANGE = 47
    SHOWN_MELEE_ARMOR = 48
    SHOWN_PIERCE_ARMOR = 49
    UNIT_NAME_STRING_ID = 50
    UNIT_SHORT_DESCRIPTION_STRING_ID = 51
    TERRAIN_RESTRICTION = 53
    UNIT_TRAIT = 54
    UNIT_CIVILIZATION = 55  # Unused
    UNIT_TRAIT_PIECE = 56
    DEAD_UNIT_ID = 57
    HOTKEY_ID = 58
    MAXIMUM_CHARGE = 59
    RECHARGE_RATE = 60
    CHARGE_EVENT = 61
    CHARGE_TYPE = 62
    COMBAT_ABILITY = 63
    ATTACK_DISPERSION = 64
    SECONDARY_PROJECTILE_UNIT = 65
    BLOOD_UNIT_ID = 66
    PROJECTILE_HIT_MODE = 67
    PROJECTILE_VANISH_MODE = 68
    PROJECTILE_ARC = 69
    ATTACK_GRAPHIC = 70
    STANDING_GRAPHIC = 71
    STANDING_GRAPHIC_2 = 72
    DYING_GRAPHIC = 73
    UNDEAD_GRAPHIC = 74
    WALKING_GRAPHIC = 75
    RUNNING_GRAPHIC = 76
    SPECIAL_GRAPHIC = 77
    OBSTRUCTION_TYPE = 78  # Also 78 listed twice in wiki?
    SPECIAL_ABILITY = 81
    IDLE_ATTACK_GRAPHIC = 82
    HERO_GLOW_GRAPHIC = 83
    GARRISON_GRAPHIC = 84
    CONSTRUCTION_GRAPHIC = 85
    SNOW_GRAPHIC = 86
    DESTRUCTION_GRAPHIC = 87
    DESTRUCTION_RUBBLE_GRAPHIC = 88
    RESEARCHING_GRAPHIC = 89
    RESEARCH_COMPLETED_GRAPHIC = 90
    DAMAGE_GRAPHIC = 91
    SELECTION_SOUND_ID = 92
    SELECTION_SOUND_EVENT = 93
    DYING_SOUND_ID = 94
    DYING_SOUND_EVENT = 95
    TRAIN_SOUND_ID = 96
    TRAIN_SOUND_EVENT = 97
    DAMAGE_SOUND_ID = 98
    DAMAGE_SOUND_EVENT = 99
    RESOURCE_COSTS = 100
    TRAIN_TIME = 101
    TOTAL_MISSILES = 102
    FOOD_COSTS = 103
    WOOD_COSTS = 104
    GOLD_COSTS = 105
    STONE_COSTS = 106
    MAX_TOTAL_PROJECTILES = 107
    GARRISON_HEAL_RATE = 108
    REGENERATION_RATE = 109
    POPULATION_HEADROOM_STORAGE = 110
    ADDITIONAL_MIN_CONVERSION_TIME = 111
    ADDITIONAL_MAX_CONVERSION_TIME = 112
    ADDITIONAL_CONVERSION_RESISTANCE_LEVEL = 113
    FORMATION_CATEGORY = 114
    AREA_DAMAGE = 115
    MELEE_ARMOR_AURA = 116
    BLOCKAGE_CLASS_PIERCE_ARMOR_AURA = 117
    MELEE_DAMAGE_DEFLECTION = 118
    FRIENDLY_FIRE_MULTIPLIER = 119
    HP_BASED_REGENERATION = 120
    ABILITY_ICON = 121
    SHORT_TOOLTIP = 122
    LONG_TOOLTIP = 123
    ABILITY_HOTKEY = 124
    TRAIN_LIMIT_FOR_DISABLED_UNITS = 126
    DISABLED_FLAG = 127
    ATTACK_PRIORITY = 128
    INVULNERABILITY_LEVEL = 129
    GARRISON_FIREPOWER = 130
    SECONDARY_ATTACK_GRAPHIC = 131
    COMMAND_SOUND_ID = 132
    COMMAND_SOUND_EVENT = 133
    MOVE_SOUND_ID = 134
    MOVE_SOUND_EVENT = 135
    CONSTRUCTION_SOUND_ID = 136
    CONSTRUCTION_SOUND_EVENT = 137
    TRANSFORM_SOUND_ID = 138
    TRANSFORM_SOUND_EVENT = 139
    SHARED_SELECTION = 140
    INTERFACE_KIND = 141
    COMBAT_LEVEL = 142
    INTERACTION_MODE = 143
    MINIMAP_MODE = 144
    TRAILING_UNIT = 145
    TRAIL_MODE = 146
    TRAIL_DENSITY = 147
    PROJECTILE_GRAPHIC_DISPLACEMENT_X = 148
    PROJECTILE_GRAPHIC_DISPLACEMENT_Y = 149
    PROJECTILE_GRAPHIC_DISPLACEMENT_Z = 150
    PROJECTILE_SPAWNING_AREA_WIDTH = 151
    PROJECTILE_SPAWNING_AREA_LENGTH = 152
    PROJECTILE_SPAWNING_AREA_RANDOMNESS = 153
    DAMAGE_GRAPHICS_ENTRY_MOD = 154
    DAMAGE_GRAPHICS_TOTAL_NUM = 155
    DAMAGE_GRAPHIC_PERCENT = 156
    DAMAGE_GRAPHIC_APPLY_MODE = 157


class GarrisonType(IntEnum):
    """Bitmask values for Garrison Type attribute (30)."""
    VILLAGER_AND_KINGS = 1
    INFANTRY_AND_FOOT_ARCHERS = 2
    MOUNTED_UNITS = 4
    FOOT_MONKS = 8
    LIVESTOCK = 16
    SIEGE_UNITS = 32
    SHIPS = 64


class HeroStatus(IntEnum):
    """Bitmask values for Hero Status attribute (40)."""
    FULL_HERO = 1
    CANNOT_BE_CONVERTED = 2
    REGENERATION = 4
    DEFAULT_DEFENSIVE_STANCE = 8
    PROTECTED_FORMATION = 16
    SAFE_DELETE_CONFIRMATION = 32
    GLOW = 64
    INVERT_HERO_PROPERTY = 128


class UnitTrait(IntEnum):
    """Bitmask values for Unit Trait attribute (54)."""
    GARRISON_UNIT = 1
    SHIP_UNIT = 2
    BUILDER_UNIT = 4
    TRANSFORMABLE_UNIT = 8
    SCOUT_UNIT = 16
    BUILDING_TO_TERRAIN_TRANSFORM = 64
    MACEDONIAN_SOLDIER = 128  # "What?" in wiki, implied used by Macedonian human soldiers


class ChargeType(IntEnum):
    """Values for Charge Type attribute (62)."""
    CHARGE_ATTACK = 1
    HIT_POINTS_UNUSED = 2
    CHARGE_AREA_ATTACK = 3
    PROJECTILE_AGILITY = 4
    MELEE_AGILITY = 5
    CHARGED_RANGED_ATTACK_1 = 6
    CHARGED_RANGED_ATTACK_2 = 7
    ACTIVE_TEMPORARY_TRANSFORMATION = -1
    ACTIVE_TARGETED_TRANSFORMATION = -2
    ACTIVE_AURA_ABILITY = -3
    CONVERSION_NON_MONK = -4
    SPAWN_UNIT = -5


class CombatAbility(IntEnum):
    """Bitmask values for Combat Ability attribute (63)."""
    IGNORE_ARMOR = 1
    RESIST_IGNORE_ARMOR = 2
    ARMOR_DAMAGING = 4
    ATTACK_GROUND = 8
    BULK_VOLLEY_RELEASE = 16
    INFLUENCE_ABILITY = 32
    INVERSE_INFLUENCE = 64
    ACTIVATE_STINGERS = 128


class ObstructionType(IntEnum):
    """Values for Obstruction Type attribute (78)."""
    CIRCLE_GROUND_SELECTION_0 = 0
    CIRCLE_GROUND_SELECTION_1 = 1
    SQUARE_GROUND_SELECTION_2 = 2
    SQUARE_GROUND_SELECTION_3 = 3
    SQUARE_GROUND_SELECTION_4 = 4
    CIRCLE_GROUND_SELECTION_5 = 5
    SQUARE_GROUND_SELECTION_10 = 10
    RADIUS_AS_SIZE = 11
    IGNORE_HARD_OBSTRUCTIONS = 12
    RADIUS_SELECTION_ORIGINAL_OBSTRUCTION = 13


class SpecialAbility(IntEnum):
    """Values for Special Ability attribute (81)."""
    NONE = 0
    BLOCK = 1
    COUNTER_CHARGE = 2
    SPEED_CHARGE = 3
    RAM = 4
    GREEK_FIRE = 5
    BOARD = 6
    BUILDING_PLACEMENT = 7


class FormationCategory(IntEnum):
    """Values for Formation Category attribute (114)."""
    NOT_APPLICABLE = 0
    MOBILE = 1
    BODY = 2
    RANGED = 3
    LONG_RANGED = 4
    PROTECTED = 5
    BUILDINGS = 255


class InterfaceKind(IntEnum):
    """Values for Interface Kind attribute (141)."""
    VISIBLE = 0
    RESOURCE = 1
    BUILDING_PAGE_1 = 2
    CIVILIAN = 3
    SOLDIER = 4
    TRADE_UNIT = 5
    PRIEST = 6
    TRANSPORT_SHIP = 7
    RELIC = 8
    FISHING_BOAT = 9
    MILITARY_BUILDING_PAGE_2 = 10
    SHIELD_BUILDING = 11


class SmartProjectileMode(IntEnum):
    """Values for Enable Smart Projectile attribute (19)."""
    DISABLED = 0
    TRACK_MOVING_TARGET = 1
    USE_FRIENDLY_FIRE_MULTIPLIER = 2


class FogVisibility(IntEnum):
    """Values for Fog Visibility attribute (28)."""
    NOT_VISIBLE = 0
    ALWAYS_VISIBLE = 1
    VISIBLE_IF_ALIVE = 2  # Unused
    INVERTED_VISIBILITY = 3  # Used by Doppelganger
    CHECK_DOPPELGANGER = 4  # Unused


class OcclusionMode(IntEnum):
    """Bitmask values for Occlusion Mode attribute (29)."""
    NO_OUTLINE = 0
    OUTLINE_THROUGH_OCCLUSION = 1
    OCCLUDES_OTHERS = 2
    OUTLINE_WHILE_CONSTRUCTING = 4
    UNKNOWN_GATES_FORAGE = 8  # Used by Gates and Forage bushes


class BlastAttackLevel(IntEnum):
    """
    Values for Blast Attack Level attribute (44).
<<<<<<< HEAD

=======
    
>>>>>>> origin/refactor-port-managers-to-gdp-783808832176151754
    Combine one primary (0-3) and one secondary (0/64/128) effect.
    """
    # Primary effects (unique, cannot be combined)
    DAMAGES_RESOURCES = 0
    DAMAGES_TREES = 1
    DAMAGES_NEARBY_UNITS = 2
    DAMAGES_ONLY_TARGET = 3
    # Secondary effects (unique, cannot be combined)
    EQUAL_DAMAGE_IN_RADIUS = 0
    TAPERING_EFFECT_MELEE = 64
    BLAST_ATTACK_DIRECTION = 128


class VanishMode(IntEnum):
    """Bitmask values for Projectile Vanish Mode attribute (68)."""
    NORMAL = 0
    PASS_THROUGH_DAMAGE = 1
    SPAWN_DEAD_UNIT = 2


class DisabledFlag(IntEnum):
    """Bitmask values for Disabled Flag attribute (127)."""
    DISABLED = 1
    LIMITED_NO_RETRAIN = 2
    LIMITED_WITH_RETRAIN = 4
    DISABLED_AFTER_TRAINED = 8  # Hide button after limit reached


class SelectionEffect(IntEnum):
    """Values for Selection Effect attribute."""
    HIT_POINT_BAR = 0
    HIT_POINT_BAR_AND_OUTLINE = 1
    NO_HIT_POINT_BAR_OR_OUTLINE = 2
    NO_HIT_POINT_BAR_WITH_OUTLINE = 3


class ChargeTarget(IntEnum):
    """Bitmask values for Charge Target attribute (Charged Ranged Attack)."""
    ALL_TARGETS = -1
    ALL_EXCEPT_BUILDINGS = 0
    INFANTRY = 1
    CAVALRY = 2
    FOOT_ARCHERS = 4
    MOUNTED_ARCHERS = 8
    MONKS = 16
    VILLAGERS_AND_TRADE_CARTS = 32
    SHIPS = 64
    SIEGE_WEAPONS = 128
    BUILDINGS = 256


class BlockageClass(IntEnum):
    """Values for Blockage Class attribute (117) when used with Aura task."""
    DEFAULT_OBSTRUCTION = 0
    RESOURCE = 1
    UNIT = 2
    BUILDING = 3
    WALL = 4
    GATE = 5  # Allows trespassing
    CLIFF = 6  # Blocks walling


class TrackingUnitMode(IntEnum):
    """Values for Tracking Unit Mode (trailing unit behavior)."""
    NOT_USED = 0
    APPEARS_WHILE_MOVING_AND_START = 1
    APPEARS_WHILE_MOVING_DENSITY = 2  # Based on density
<<<<<<< HEAD
=======


>>>>>>> origin/refactor-port-managers-to-gdp-783808832176151754
