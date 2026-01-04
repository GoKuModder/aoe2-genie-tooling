import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from ..base_manager import GenieWorkspace
from ..Terrains.terrain_manager import TerrainManager

class TestTerrainManager(unittest.TestCase):

    def setUp(self):
        # Create a mock DatFile object
        self.mock_dat = MagicMock()
        self.mock_dat.terrains = [MagicMock(), MagicMock()]

        # Patch the DatFile loader to return the mock object
        self.patcher = patch('Actual_Tools_GDP.base_manager.DatFile')
        self.mock_dat_class = self.patcher.start()
        self.mock_dat_class.parse.return_value = self.mock_dat
        self.mock_dat_class.from_file.return_value = self.mock_dat

    def tearDown(self):
        self.patcher.stop()

    def test_workspace_creation(self):
        """Test if the GenieWorkspace is created and loads the mock dat file."""
        workspace = GenieWorkspace.load("dummy.dat")
        self.assertIsNotNone(workspace)
        self.assertIsInstance(workspace.terrains, TerrainManager)

    def test_get_terrains(self):
        """Test getting all terrains from the TerrainManager."""
        workspace = GenieWorkspace.load("dummy.dat")
        terrains = workspace.terrain_manager().get_terrains()
        self.assertEqual(len(terrains), 2)

    def test_get_terrain(self):
        """Test getting a single terrain by ID."""
        workspace = GenieWorkspace.load("dummy.dat")
        terrain = workspace.terrain_manager().get_terrain(0)
        self.assertIsNotNone(terrain)
        terrain = workspace.terrain_manager().get_terrain(1)
        self.assertIsNotNone(terrain)

    def test_count_terrains(self):
        """Test counting the number of terrains."""
        workspace = GenieWorkspace.load("dummy.dat")
        count = workspace.terrain_manager().count()
        self.assertEqual(count, 2)

    def test_get_terrain_out_of_bounds(self):
        """Test that getting a terrain with an out-of-bounds ID raises an IndexError."""
        workspace = GenieWorkspace.load("dummy.dat")
        with self.assertRaises(IndexError):
            workspace.terrain_manager().get_terrain(2)

if __name__ == '__main__':
    unittest.main()
