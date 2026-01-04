"""
Tests for the UnitManager using the Genie-Rust backend and a real DAT file.
"""
import pytest
from Actual_Tools import GenieWorkspace
from Actual_Tools.exceptions import UnitIdConflictError, InvalidIdError

# A high unit ID that is guaranteed not to exist in the test file
TEST_UNIT_ID = 1699 # Last unit is 1600, leave buffer

class TestUnitManager:
    """Tests for creating, getting, and cloning units."""

    def test_get_unit_by_id(self, dat_file: GenieWorkspace):
        """Should return a valid UnitHandle for an existing unit."""
        um = dat_file.genie_unit_manager()
        archer = um.get(4)
        assert archer is not None
        assert archer.id == 4
        # The name is read as a padded string from the DAT file
        assert archer.name == "ARCHR"

    def test_get_unit_by_name(self, dat_file: GenieWorkspace):
        """Should return a valid UnitHandle for an existing unit by name."""
        um = dat_file.genie_unit_manager()
        archer = um.get("ARCHR")
        assert archer is not None
        assert archer.id == 4

    def test_get_non_existent_unit_raises_error(self, dat_file: GenieWorkspace):
        """Should raise InvalidIdError for a non-existent unit ID."""
        um = dat_file.genie_unit_manager()
        with pytest.raises(InvalidIdError):
            um.get(9999)

    def test_create_unit(self, dat_file: GenieWorkspace):
        """Should create a new unit, clone from base, and return a handle."""
        um = dat_file.genie_unit_manager()

        new_unit = um.create(
            name="Test Unit",
            src_unit_id=4,  # Clone from Archer
            unit_id=TEST_UNIT_ID,
        )

        assert new_unit is not None
        assert new_unit.id == TEST_UNIT_ID
        assert new_unit.name == "Test Unit"

        # Verify it was actually added to the manager
        retrieved_unit = um.get(TEST_UNIT_ID)
        assert retrieved_unit.id == new_unit.id

    def test_create_unit_with_conflicting_id_raises_error(self, dat_file: GenieWorkspace):
        """Should raise UnitIdConflictError if the target ID already exists."""
        um = dat_file.genie_unit_manager()
        with pytest.raises(UnitIdConflictError):
            um.create("Conflict Unit", src_unit_id=4, unit_id=4) # ID 4 (Archer) exists

    def test_clone_into(self, dat_file: GenieWorkspace):
        """Should clone an existing unit to a new ID."""
        um = dat_file.genie_unit_manager()

        clone = um.clone_into(
            4, # src_unit_id
            TEST_UNIT_ID, # dst_unit_id
            name="Archer Clone",
        )

        assert clone.id == TEST_UNIT_ID
        assert clone.name == "Archer Clone"

        # Original archer should have 30 HP
        assert clone.hit_points == 30

    def test_clone_with_overwrite(self, dat_file: GenieWorkspace):
        """Should overwrite an existing unit when on_conflict is 'overwrite'."""
        um = dat_file.genie_unit_manager()

        # We will overwrite unit 21 (Villager) with a clone of unit 4 (Archer)
        original_villager_name = um.get(21).name

        clone = um.clone_into(
            4, # src_unit_id
            21, # dst_unit_id
            name="Archer Overwrite",
            on_conflict="overwrite",
        )

        assert clone.id == 21
        assert clone.name == "Archer Overwrite"
        assert clone.hit_points == 30 # Archer's HP, not Villager's

        # Cleanup: restore the original name
        # This doesn't restore all stats, but it's better than nothing
        um.get(21).name = original_villager_name
