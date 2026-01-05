from __future__ import annotations
from typing import TYPE_CHECKING, List

from ..Shared.tool_base import ToolBase
from ..backend import DatFile

if TYPE_CHECKING:
    from ..backend import Terrain

class TerrainManager(ToolBase):
    """
    Manager for accessing terrain data in a DAT file.
    """

    def __init__(self, dat_file: DatFile) -> None:
        super().__init__(dat_file)
        self._terrains = self.dat_file.terrains

    def get_terrains(self) -> List[Terrain]:
        """
        Get a list of all terrains.

        Returns:
            A list of terrain objects.
        """
        return self._terrains

    def get_terrain(self, terrain_id: int) -> Terrain:
        """
        Get a single terrain by its ID.

        Args:
            terrain_id: The ID of the terrain to retrieve.

        Returns:
            The terrain object.

        Raises:
            IndexError: If the terrain_id is out of bounds.
        """
        return self._terrains[terrain_id]

    def count(self) -> int:
        """
        Return the total number of terrains.
        """
        return len(self._terrains)
