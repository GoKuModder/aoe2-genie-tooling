"""
Terrain types dataset.

Contains terrain IDs used for foundation_terrain, placement_terrain, etc.
"""
from enum import IntEnum

__all__ = ["TerrainType"]


class TerrainType(IntEnum):
    """
    Terrain type IDs for foundation_terrain, placement_terrain, terrain_restriction.

    Note: Full terrain list can have 100+ terrains depending on the dataset.
    These are common base game terrains.
    """
    GRASS = 0
    WATER_SHALLOW = 1
    BEACH = 2
    DIRT = 3
    WATER_MEDIUM = 4
    LEAVES = 5
    DIRT_3 = 6
    FARM = 7
    DEAD_FARM = 8
    GRASS_2 = 9
    FOREST_LEAVES = 10
    DIRT_4 = 11
    GRASS_3 = 12
    FOREST_SNOW = 13
    DESERT = 14
    WATER_DEEP = 15
    GRASS_4 = 16
    JUNGLE_LEAVES = 17
    BAMBOO = 18
    GRASS_5 = 19
    BAMBOO_2 = 20
    PALM_DESERT = 21
    WATER_SHALLOW_2 = 22
    MANGROVE_FOREST = 23
    ROAD = 24
    ROAD_2 = 25
    WATER_BRIDGE = 26
    FARM_CONSTRUCT = 27
    FARM_2 = 28
    FOUNDATION = 29  # Building foundation terrain
    GRASS_6 = 30
    WATER_SHALLOW_3 = 31
    SNOW = 32
    SNOW_FOREST = 33
    SNOW_2 = 34
    SNOW_3 = 35
    ICE = 36
    SNOW_ROAD = 37
    FUNGUS_ROAD = 38
    KOH = 39  # King of the Hill
    WATER_FORD = 40
    FARM_DEAD = 41
    # ... additional terrains 42+ in newer datasets
