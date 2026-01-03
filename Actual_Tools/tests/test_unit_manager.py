"""
Tests for GenieUnitManager create/clone_into/move operations.
"""
import pytest
from copy import deepcopy

from Actual_Tools.Units.unit_manager import GenieUnitManager
from Actual_Tools.exceptions import (
    GapNotAllowedError,
    InvalidIdError,
    UnitIdConflictError,
)
from Actual_Tools.tests.conftest import FakeDatFile, FakeCiv, FakeUnit


class TestCreate:
    """Tests for create() method."""

    def test_create_appends_to_end(self, fake_dat_file: FakeDatFile):
        """Create without unit_id should append to end."""
        manager = GenieUnitManager(fake_dat_file)
        
        handle = manager.create("New Unit", base_unit_id=0)
        
        assert handle.unit_id == 10  # Original had 10 units (0-9)
        assert fake_dat_file.civs[0].units[10].name == "New Unit"
        assert fake_dat_file.civs[1].units[10].name == "New Unit"

    def test_create_at_specific_id(self, fake_dat_file: FakeDatFile):
        """Create at specific ID should place unit there."""
        manager = GenieUnitManager(fake_dat_file)
        
        handle = manager.create("Custom Unit", base_unit_id=0, unit_id=15)
        
        assert handle.unit_id == 15
        assert fake_dat_file.civs[0].units[15].name == "Custom Unit"

    def test_create_fills_gaps_with_placeholders(self, fake_dat_file: FakeDatFile):
        """Create beyond max should fill gaps with placeholders."""
        manager = GenieUnitManager(fake_dat_file)
        
        handle = manager.create("Far Unit", base_unit_id=0, unit_id=20)
        
        # Check gaps are filled (indices 10-19 should be placeholders)
        for i in range(10, 20):
            unit = fake_dat_file.civs[0].units[i]
            assert unit is not None, f"Gap at index {i}"
            # Placeholders have enabled=0, name="", hit_points=1
            assert unit.enabled == 0
            assert unit.name == ""
            assert unit.hit_points == 1

    def test_create_conflict_error(self, fake_dat_file: FakeDatFile):
        """Create at existing ID should raise UnitIdConflictError."""
        manager = GenieUnitManager(fake_dat_file)
        
        with pytest.raises(UnitIdConflictError):
            manager.create("Conflict Unit", base_unit_id=0, unit_id=5)

    def test_create_conflict_overwrite(self, fake_dat_file: FakeDatFile):
        """Create with on_conflict='overwrite' should replace existing."""
        manager = GenieUnitManager(fake_dat_file)
        
        handle = manager.create(
            "Overwrite Unit",
            base_unit_id=0,
            unit_id=5,
            on_conflict="overwrite"
        )
        
        assert handle.unit_id == 5
        assert fake_dat_file.civs[0].units[5].name == "Overwrite Unit"

    def test_create_fill_gaps_error(self, fake_dat_file: FakeDatFile):
        """Create with fill_gaps='error' should raise when gaps needed."""
        manager = GenieUnitManager(fake_dat_file)
        
        with pytest.raises(GapNotAllowedError):
            manager.create(
                "Far Unit",
                base_unit_id=0,
                unit_id=20,
                fill_gaps="error"
            )

    def test_create_enable_for_specific_civs(self, fake_dat_file: FakeDatFile):
        """Create with enable_for_civs should only affect those civs."""
        manager = GenieUnitManager(fake_dat_file)
        
        handle = manager.create(
            "Civ 0 Only",
            base_unit_id=0,
            unit_id=10,
            enable_for_civs=[0]
        )
        
        assert fake_dat_file.civs[0].units[10].name == "Civ 0 Only"
        # Civ 1 should have placeholder (from capacity extension)
        assert fake_dat_file.civs[1].units[10].enabled == 0


class TestCloneInto:
    """Tests for clone_into() method."""

    def test_clone_into_specific_id(self, fake_dat_file: FakeDatFile):
        """clone_into should place clone at exact destination."""
        manager = GenieUnitManager(fake_dat_file)
        
        handle = manager.clone_into(dest_unit_id=15, base_unit_id=5, name="Clone")
        
        assert handle.unit_id == 15
        assert fake_dat_file.civs[0].units[15].name == "Clone"
        assert fake_dat_file.civs[0].units[15].id == 15

    def test_clone_into_preserves_source(self, fake_dat_file: FakeDatFile):
        """clone_into should not modify source unit."""
        manager = GenieUnitManager(fake_dat_file)
        original_name = fake_dat_file.civs[0].units[5].name
        
        manager.clone_into(dest_unit_id=15, base_unit_id=5, name="Clone")
        
        assert fake_dat_file.civs[0].units[5].name == original_name

    def test_clone_into_keeps_original_name(self, fake_dat_file: FakeDatFile):
        """clone_into with name=None should keep original name."""
        manager = GenieUnitManager(fake_dat_file)
        original_name = fake_dat_file.civs[0].units[3].name
        
        handle = manager.clone_into(dest_unit_id=15, base_unit_id=3)
        
        assert fake_dat_file.civs[0].units[15].name == original_name


class TestMove:
    """Tests for move() method."""

    def test_move_updates_destination(self, fake_dat_file: FakeDatFile):
        """Move should place unit at destination."""
        manager = GenieUnitManager(fake_dat_file)
        original_name = fake_dat_file.civs[0].units[5].name
        
        manager.move(src_unit_id=5, dst_unit_id=15)
        
        assert fake_dat_file.civs[0].units[15].name == original_name
        assert fake_dat_file.civs[0].units[15].id == 15

    def test_move_leaves_placeholder_at_source(self, fake_dat_file: FakeDatFile):
        """Move should leave placeholder at source (not None)."""
        manager = GenieUnitManager(fake_dat_file)
        
        manager.move(src_unit_id=5, dst_unit_id=15)
        
        # Source should NOT be None
        source = fake_dat_file.civs[0].units[5]
        assert source is not None
        # Should be a placeholder
        assert source.enabled == 0
        assert source.name == ""
        assert source.hit_points == 1

    def test_move_conflict_error(self, fake_dat_file: FakeDatFile):
        """Move to existing ID should raise by default."""
        manager = GenieUnitManager(fake_dat_file)
        
        with pytest.raises(UnitIdConflictError):
            manager.move(src_unit_id=5, dst_unit_id=3)

    def test_move_conflict_overwrite(self, fake_dat_file: FakeDatFile):
        """Move with on_conflict='overwrite' should replace destination."""
        manager = GenieUnitManager(fake_dat_file)
        src_name = fake_dat_file.civs[0].units[5].name
        
        manager.move(src_unit_id=5, dst_unit_id=3, on_conflict="overwrite")
        
        assert fake_dat_file.civs[0].units[3].name == src_name

    def test_move_conflict_swap(self, fake_dat_file: FakeDatFile):
        """Move with on_conflict='swap' should exchange units."""
        manager = GenieUnitManager(fake_dat_file)
        src_name = fake_dat_file.civs[0].units[5].name
        dst_name = fake_dat_file.civs[0].units[3].name
        
        manager.move(src_unit_id=5, dst_unit_id=3, on_conflict="swap")
        
        assert fake_dat_file.civs[0].units[3].name == src_name
        assert fake_dat_file.civs[0].units[5].name == dst_name

    def test_move_invalid_source(self, fake_dat_file: FakeDatFile):
        """Move from non-existent source should raise."""
        manager = GenieUnitManager(fake_dat_file)
        
        with pytest.raises(InvalidIdError):
            manager.move(src_unit_id=999, dst_unit_id=15)


class TestExistsAndGet:
    """Tests for exists() and get() methods."""

    def test_exists_returns_true_for_real_unit(self, fake_dat_file: FakeDatFile):
        """exists() should return True for real units."""
        manager = GenieUnitManager(fake_dat_file)
        
        assert manager.exists(5) is True

    def test_exists_returns_false_for_placeholder(self, fake_dat_file: FakeDatFile):
        """exists() should return False for placeholder units."""
        manager = GenieUnitManager(fake_dat_file)
        
        # Create placeholder by extending
        manager.create("Test", base_unit_id=0, unit_id=20)
        
        # Index 15 should be a placeholder
        assert manager.exists(15) is False

    def test_exists_raw_returns_true_for_placeholder(self, fake_dat_file: FakeDatFile):
        """exists_raw() should return True for placeholder units."""
        manager = GenieUnitManager(fake_dat_file)
        
        manager.create("Test", base_unit_id=0, unit_id=20)
        
        # Index 15 should exist (as placeholder)
        assert manager.exists_raw(15) is True

    def test_get_returns_handle(self, fake_dat_file: FakeDatFile):
        """get() should return a UnitHandle."""
        manager = GenieUnitManager(fake_dat_file)
        
        handle = manager.get(5)
        
        assert handle.unit_id == 5
        assert handle.name == "Unit 5"

    def test_get_invalid_id_raises(self, fake_dat_file: FakeDatFile):
        """get() with invalid ID should raise."""
        manager = GenieUnitManager(fake_dat_file)
        
        with pytest.raises(InvalidIdError):
            manager.get(999)
