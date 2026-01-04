from enum import IntEnum


class TargetDiplomacy(IntEnum):
    """
    Target Diplomacy values for Tasks/Effects.
<<<<<<< HEAD

=======
    
>>>>>>> origin/refactor-port-managers-to-gdp-783808832176151754
    Source: https://ageofempires.fandom.com/wiki/Genie_Editor#Task_attributes
    """
    ALL_OBJECTS = 0
    OWN = 1
    NEUTRAL_AND_ENEMY = 2
    GAIA = 3
    GAIA_AND_TEAM = 4
    GAIA_NEUTRAL_AND_ENEMY = 5
    ALL_BUT_OWN = 6
    ALL_OBJECTS_ALT = 7  # 7+ is all objects


class UnusedFlag(IntEnum):
    """
    Unused Flag (Task Attribute) Bitmask.
    Used in Influence Ability (Task 155).
    """
    MULTIPLY_INSTEAD_OF_ADD = 1
    CIRCULAR_RADIUS = 2
    SHOW_RANGE_INDICATOR = 4
    TRANSLUCENT = 32
    HIDE_ICON = 128
