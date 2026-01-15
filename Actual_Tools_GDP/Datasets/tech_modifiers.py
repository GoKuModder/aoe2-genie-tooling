from enum import IntEnum


class TechModifier(IntEnum):
    """
    Technology Modifier Types.
    
    Source: https://ageofempires.fandom.com/wiki/Genie_Editor#Technology
    """
    # Time Modifiers
    MULTIPLY_TECH_TIME = -3
    ADD_TIME = -2
    SET_TIME = -1
    
    # Basic Cost Modifiers
    SET_FOOD_COST = 0
    SET_WOOD_COST = 1
    SET_STONE_COST = 2
    SET_GOLD_COST = 3
    
    # UI and Metadata
    SET_RESEARCH_LOCATION = 4
    SET_BUTTON_LOCATION = 5
    SET_ICON = 6
    SET_NAME_STRING_ID = 7
    SET_DESCRIPTION_STRING_ID = 8
    
    # Stacking
    ENABLE_STACKING = 9  # Enable 256x tech mod
    SET_STACKING_CAP = 10
    
    # Other
    SET_HOTKEY_ID = 11
    SET_TECH_STATE = 12  # 0: Disabled, 1: Enabled
    
    # Multipliers
    MULTIPLY_FOOD_COST = 13
    MULTIPLY_WOOD_COST = 14
    MULTIPLY_STONE_COST = 15
    MULTIPLY_GOLD_COST = 16
    MULTIPLY_ALL_COSTS = 17
    
    # Effects
    SET_EFFECT_ID = 18
    
    # Add Costs
    ADD_FOOD_COST = 16384
    ADD_WOOD_COST = 16385
    ADD_STONE_COST = 16386
    ADD_GOLD_COST = 16387


class TechCostType(IntEnum):
    """
    Technology Cost Deduction Types.
    """
    UNPAID = 0  # Does not deduct resources
    PAID_GLOBALLY = 1  # Standard behavior
    PAID_FROM_BUILDING = 2  # Deducts from building storage


class TechType(IntEnum):
    """
    Technology Attribute Flags.
    """
    NORMAL = 0
    SHOW_PROGRESS_IN_AGE_BAR = 2
    BUILDING_SPECIFIC = 32
    REPEATABLE = 33
