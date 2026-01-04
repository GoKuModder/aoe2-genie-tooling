"""
Tests for UnitHandle multi-civ property propagation using the Genie-Rust backend.
"""
import pytest
from Actual_Tools import GenieWorkspace
from Actual_Tools.Units.unit_handle import UnitHandle

# ID of a known unit that exists in the test DAT file (Archer)
ARCHER_ID = 4
VILLAGER_ID = 21 # Villager (Female) - using a different unit for variety

class TestUnitHandle:
    """Tests for UnitHandle basic functionality against a real DAT file."""

    def test_handle_references_correct_unit(self, dat_file: GenieWorkspace):
        """Handle should reference the correct unit by ID."""
        um = dat_file.genie_unit_manager()
        handle = um.get(ARCHER_ID)

        # In the test DAT, the Archer's name is "ARCHR" (padded with nulls)
        assert handle.name == "ARCHR"
        assert handle.id == ARCHER_ID

    def test_name_propagates_to_all_civs(self, dat_file: GenieWorkspace):
        """Setting name should update all enabled civs."""
        um = dat_file.genie_unit_manager()
        handle = um.get(ARCHER_ID)

        original_name = handle.name
        new_name = "Test Archer"

        handle.name = new_name

        # Verify the change was propagated to the underlying objects
        for civ in dat_file.dat.civs:
            if civ.units[ARCHER_ID] is not None:
                assert civ.units[ARCHER_ID].name == new_name

        # Cleanup: revert the name change
        handle.name = original_name

class TestUnitStats:
    """Tests for UnitHandle stats against a real DAT file."""

    def test_hit_points_get(self, dat_file: GenieWorkspace):
        """Should get hit_points from the real unit data."""
        um = dat_file.genie_unit_manager()
        handle = um.get(ARCHER_ID)

        # The Archer unit in the base game has 30 HP.
        assert handle.hit_points == 30

    def test_hit_points_set_propagates(self, dat_file: GenieWorkspace):
        """Setting hit_points should update all civs."""
        um = dat_file.genie_unit_manager()
        handle = um.get(ARCHER_ID)

        original_hp = handle.hit_points

        handle.hit_points = 999

        assert handle.hit_points == 999
        for civ in dat_file.dat.civs:
             if civ.units[ARCHER_ID] is not None:
                assert civ.units[ARCHER_ID].hit_points == 999

        # Cleanup
        handle.hit_points = original_hp

    def test_speed_get_and_set(self, dat_file: GenieWorkspace):
        """Speed should get/set correctly."""
        um = dat_file.genie_unit_manager()
        handle = um.get(VILLAGER_ID)

        original_speed = handle.speed

        handle.speed = 1.5
        assert handle.speed == 1.5

        # Cleanup
        handle.speed = original_speed
