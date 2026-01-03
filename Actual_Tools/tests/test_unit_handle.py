"""
Tests for UnitHandle multi-civ property propagation.
"""
import pytest
from copy import deepcopy

from Actual_Tools.Units.unit_handle import UnitHandle
from Actual_Tools.tests.conftest import FakeDatFile, FakeCiv, FakeUnit


class TestUnitHandle:
    """Tests for UnitHandle basic functionality."""

    def test_handle_references_correct_unit(self, fake_dat_file: FakeDatFile):
        """Handle should reference the correct unit by ID."""
        handle = UnitHandle(unit_id=5, dat_file=fake_dat_file, civ_ids=[0, 1])
        
        unit = handle.get_unit(civ_id=0)
        assert unit is not None
        assert unit.id == 5
        assert unit.name == "Unit 5"

    def test_name_propagates_to_all_civs(self, fake_dat_file: FakeDatFile):
        """Setting name should update all enabled civs."""
        handle = UnitHandle(unit_id=3, dat_file=fake_dat_file, civ_ids=[0, 1])
        
        handle.name = "New Name"
        
        assert fake_dat_file.civs[0].units[3].name == "New Name"
        assert fake_dat_file.civs[1].units[3].name == "New Name"

    def test_enabled_propagates_to_all_civs(self, fake_dat_file: FakeDatFile):
        """Setting enabled should update all enabled civs."""
        handle = UnitHandle(unit_id=2, dat_file=fake_dat_file, civ_ids=[0, 1])
        
        handle.enabled = 0
        
        assert fake_dat_file.civs[0].units[2].enabled == 0
        assert fake_dat_file.civs[1].units[2].enabled == 0


class TestUnitStatsTab:
    """Tests for UnitHandle.stats tab."""

    def test_hit_points_get(self, fake_dat_file: FakeDatFile):
        """Should get hit_points from first civ."""
        handle = UnitHandle(unit_id=5, dat_file=fake_dat_file, civ_ids=[0, 1])
        
        # FakeUnit sets hit_points = 100 + unit_id
        assert handle.stats.hit_points == 105

    def test_hit_points_set_propagates(self, fake_dat_file: FakeDatFile):
        """Setting hit_points should update all civs."""
        handle = UnitHandle(unit_id=4, dat_file=fake_dat_file, civ_ids=[0, 1])
        
        handle.stats.hit_points = 999
        
        assert fake_dat_file.civs[0].units[4].hit_points == 999
        assert fake_dat_file.civs[1].units[4].hit_points == 999

    def test_speed_get_and_set(self, fake_dat_file: FakeDatFile):
        """Speed should get/set correctly."""
        handle = UnitHandle(unit_id=0, dat_file=fake_dat_file, civ_ids=[0])
        
        handle.stats.speed = 1.5
        assert handle.stats.speed == 1.5
        assert fake_dat_file.civs[0].units[0].speed == 1.5


class TestUnitCostTab:
    """Tests for UnitHandle.cost tab."""

    def test_food_cost_set(self, fake_dat_file: FakeDatFile):
        """Setting food cost should update resource_costs."""
        handle = UnitHandle(unit_id=0, dat_file=fake_dat_file, civ_ids=[0, 1])
        
        handle.cost.food = 50
        
        # Check both civs
        for civ in fake_dat_file.civs:
            unit = civ.units[0]
            found = False
            for rc in unit.creatable.resource_costs:
                if rc.type == 0:  # Food
                    assert rc.amount == 50
                    found = True
            assert found, "Food resource cost not found"

    def test_gold_cost_set(self, fake_dat_file: FakeDatFile):
        """Setting gold cost should update resource_costs."""
        handle = UnitHandle(unit_id=0, dat_file=fake_dat_file, civ_ids=[0])
        
        handle.cost.gold = 75
        
        unit = fake_dat_file.civs[0].units[0]
        for rc in unit.creatable.resource_costs:
            if rc.type == 3:  # Gold
                assert rc.amount == 75
                return
        pytest.fail("Gold resource cost not found")


class TestUnitTrainTab:
    """Tests for UnitHandle.train tab."""

    def test_train_time_set(self, fake_dat_file: FakeDatFile):
        """Setting train time should update train_locations."""
        handle = UnitHandle(unit_id=0, dat_file=fake_dat_file, civ_ids=[0, 1])
        
        handle.train.time_seconds = 45
        
        for civ in fake_dat_file.civs:
            unit = civ.units[0]
            assert unit.creatable.train_locations[0].train_time == 45


class TestForCivOverride:
    """Tests for per-civ overrides via for_civ()."""

    def test_for_civ_returns_scoped_handle(self, fake_dat_file: FakeDatFile):
        """for_civ() should return a handle scoped to single civ."""
        handle = UnitHandle(unit_id=5, dat_file=fake_dat_file, civ_ids=[0, 1])
        
        civ1_handle = handle.for_civ(1)
        
        assert civ1_handle._civ_ids == [1]
        assert civ1_handle.unit_id == 5

    def test_for_civ_changes_only_target_civ(self, fake_dat_file: FakeDatFile):
        """Changes via for_civ() should only affect that civ."""
        handle = UnitHandle(unit_id=3, dat_file=fake_dat_file, civ_ids=[0, 1])
        
        # Set via main handle (affects all)
        handle.stats.hit_points = 200
        
        # Override for civ 1 only
        handle.for_civ(1).stats.hit_points = 300
        
        assert fake_dat_file.civs[0].units[3].hit_points == 200
        assert fake_dat_file.civs[1].units[3].hit_points == 300
