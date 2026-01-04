import unittest
from unittest.mock import MagicMock
import sys
import os

# New Import Paths
from Actual_Tools_GDP.Techs.tech_manager import TechManager
from Actual_Tools_GDP.backend import DatFile, Tech

class TestGDPManagers(unittest.TestCase):
    def setUp(self):
        # Mock DatFile structure
        self.dat_file = MagicMock(spec=DatFile)
        self.dat_file.techs = []

    def test_tech_manager(self):
        manager = TechManager(self.dat_file)

        # Mock Template Tech
        t_tpl = MagicMock(spec=Tech)
        t_tpl.id = 100
        t_tpl.name = "Loom"

        self.dat_file.techs = [None] * 101
        self.dat_file.techs[100] = t_tpl

        new_tech_handle = manager.add_tech("Super Loom", template_id=100)

        self.assertEqual(new_tech_handle.name, "Super Loom")
        self.assertIn(self.dat_file.techs[new_tech_handle.id], self.dat_file.techs)

if __name__ == '__main__':
    unittest.main()
