import unittest
from unittest.mock import MagicMock, Mock
import sys
import os

# Add paths
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from genieutils.datfile import DatFile
from genieutils.unit import Unit
from genieutils.sound import Sound, SoundItem
from genieutils.graphic import Graphic
from genieutils.tech import Tech
from genieutils.civ import Civ

# New Import Paths
from Actual_Tools.Base.base_manager import GenieWorkspace
from Actual_Tools.Units.unit_manager import GenieUnitManager
from Actual_Tools.Graphics.graphic_manager import GraphicManager
from Actual_Tools.Sounds.sound_manager import SoundManager
from Actual_Tools_GDP.Techs.tech_manager import TechManager
from Actual_Tools_GDP.Civilizations.civ_manager import CivilizationsManager

class TestManagers(unittest.TestCase):
    def setUp(self):
        # Mock DatFile structure
        self.dat_file = MagicMock(spec=DatFile)
        self.dat_file.civs = []
        self.dat_file.sounds = []
        self.dat_file.graphics = []
        self.dat_file.techs = []

        # Setup basic Civs (Civ 0, Civ 1)
        civ1 = MagicMock(spec=Civ)
        civ1.name = "Civ1"
        civ1.units = [None] * 10

        civ2 = MagicMock(spec=Civ)
        civ2.name = "Civ2"
        civ2.units = [None] * 10

        self.dat_file.civs = [civ1, civ2]

        # Use GenieWorkspace
        # We Mock the load method OR just modify __init__?
        # Since it's a dataclass, we can just instantiate it with dat
        # But __post_init__ will run and create managers.
        self.workspace = GenieWorkspace(self.dat_file)

    def test_unit_manager_create(self):
        manager = self.workspace.units

        # Mock existing Unit 5
        unit_existing = MagicMock(spec=Unit)
        unit_existing.id = 5
        self.dat_file.civs[0].units[5] = unit_existing

        # Test create new unit
        new_unit = manager.create(name="New Unit", unit_id=6, fill_gaps="empty")

        # Expect Unit Object returned
        self.assertIsInstance(new_unit, Unit)
        self.assertEqual(new_unit.id, 6)
        self.assertEqual(new_unit.name, "New Unit")

        # Verify added to civs
        self.assertEqual(self.dat_file.civs[0].units[6].id, new_unit.id)
        self.assertEqual(self.dat_file.civs[1].units[6].id, new_unit.id)

    def test_sound_manager(self):
        manager = self.workspace.sounds

        # Mock existing sounds
        self.dat_file.sounds = [MagicMock(spec=Sound, id=10)]

        new_sound = manager.add_sound("test.wav", probability=50)

        # Expect Sound Object
        self.assertIsInstance(new_sound, Sound)
        self.assertEqual(new_sound.total_probability, 50)
        self.assertEqual(new_sound.items[0].filename, "test.wav")
        self.assertIn(new_sound, self.dat_file.sounds)

    def test_graphic_manager(self):
        manager = self.workspace.graphics

        # Mock Template Graphic
        g_tpl = MagicMock(spec=Graphic)
        g_tpl.id = 12730
        g_tpl.name = "Template"

        # Fill graphics list so 12730 exists
        self.dat_file.graphics = [None] * 12731
        self.dat_file.graphics[12730] = g_tpl

        new_graphic = manager.add_graphic("new.smx", template_id=12730)

        # Expect Graphic Object
        self.assertIsInstance(new_graphic, Graphic)
        self.assertEqual(new_graphic.file_name, "new.smx")
        self.assertEqual(new_graphic.name, "Template")
        self.assertIn(new_graphic, self.dat_file.graphics)

    def test_tech_manager(self):
        manager = self.workspace.techs

        # Mock Template Tech
        t_tpl = MagicMock(spec=Tech)
        t_tpl.id = 100
        t_tpl.name = "Loom"

        self.dat_file.techs = [None] * 101
        self.dat_file.techs[100] = t_tpl

        new_tech = manager.add_tech("Super Loom", template_id=100)

        self.assertIsInstance(new_tech, Tech)
        self.assertEqual(new_tech.name, "Super Loom")
        self.assertIn(new_tech, self.dat_file.techs)

if __name__ == '__main__':
    unittest.main()
