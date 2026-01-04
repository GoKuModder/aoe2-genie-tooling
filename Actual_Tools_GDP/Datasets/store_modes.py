from enum import IntEnum


class StoreMode(IntEnum):
    """
    Genie Editor Store Modes.

    Source: https://ageofempires.fandom.com/wiki/Genie_Editor#Store_Mode
    """
    KEEP_DECAYABLE = 0  # Resource decays based on decay time
    KEEP_PERMANENT = 1  # Enables instantly, stays after death
    GIVE_AND_TAKE = 2   # Enables instantly, resets on death
    ENABLES_ON_COMPLETION_RESETS = 4
    ENABLES_ON_COMPLETION_STAYS = 8
    LOCAL_STORAGE = 16  # Stores in local repository instead of global
    PREVENT_POPULATION_DROP = 32  # Used by Konnik
