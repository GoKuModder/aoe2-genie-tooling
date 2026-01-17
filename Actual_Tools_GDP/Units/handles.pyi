"""Type stubs for Unit handles - enables IDE autocomplete"""
from typing import Any, Optional


class TaskHandle:
    """Wrapper for a UnitTask with its index."""
    
    @property
    def task_id(self) -> int:
        """Index of this task in the parent's list."""
        ...
    
    # Core properties
    task_type: int
    id: int
    is_default: int
    action_type: int
    class_id: int
    unit_id: int
    terrain_id: int
    resource_in: int
    resource_out: int
    work_value_1: float
    work_value_2: float
    work_range: float
    target_diplomacy: int
    working_graphic_id: int
    carrying_graphic_id: int
    enabled: int
    
    # Additional task properties
    search_wait_time: float
    work_flag_2: int  # Alias for work_mode. MUST be 2001 for speed_charge.
    work_mode: int
    combat_level: int  # Used in combat tasks
    unused_flag: int  # Alias for combat_level (Genie Editor naming)
    
    # Build task properties
    building_pick: bool  # Alias for build_task_flag
    build_task_flag: bool
    auto_search_targets: bool
    
    # Other task properties
    productivity_resource: int
    unused_resource: int
    proceeding_graphic_id: int
    resource_gather_sound_id: int
    resource_deposit_sound_id: int
    gather_type: int
    enable_targeting: int
    target_resource_flag: bool
    move_sprite_id: int
    proceed_sprite_id: int
    work_sprite_id: int
    carry_sprite_id: int
    wwise_resource_gather_sound_id: int
    wwise_resource_deposit_sound_id: int
    resource_which_enables_task: int


class AttackHandle:
    """Wrapper for an attack damage class entry."""
    
    @property
    def attack_id(self) -> int:
        """Index of this attack in the parent's list."""
        ...
    
    class_: int
    amount: int


class ArmourHandle:
    """Wrapper for an armour damage class entry."""
    
    @property
    def armour_id(self) -> int:
        """Index of this armour in the parent's list."""
        ...
    
    class_: int
    amount: int


class DamageGraphicHandle:
    """Wrapper for a damage graphic entry."""
    
    @property
    def damage_graphic_id(self) -> int:
        """Index of this damage graphic in the parent's list."""
        ...
    
    graphic_id: int
    damage_percent: int
    apply_mode: int
    old_apply_mode: int


class TrainLocationHandle:
    """Wrapper for a train location entry."""
    
    @property
    def train_location_id(self) -> int:
        """Index of this train location in the parent's list."""
        ...
    
    unit_id: int
    train_time: int
    button_id: int
    hot_key_id: int


class DropSiteHandle:
    """Wrapper for a drop site entry."""
    
    @property
    def drop_site_id(self) -> int:
        """Index of this drop site in the parent's list."""
        ...
    
    unit_id: int


class BuildingAnnexHandle:
    """Wrapper for a building annex entry."""
    
    @property
    def annex_id(self) -> int:
        """Index of this annex in the parent's list."""
        ...
    
    unit_id: int
    x_offset: float
    y_offset: float


class CostHandle:
    """Wrapper for a resource cost entry."""
    
    @property
    def cost_id(self) -> int:
        """Index of this cost in the parent's list (0-2)."""
        ...
    
    resource_type: int
    amount: int
    is_paid: int


class ResourceHandle:
    """Wrapper for a resource storage entry."""
    
    @property
    def resource_id(self) -> int:
        """Index of this resource in the parent's list (0-2)."""
        ...
    
    resource_type: int
    amount: float
    flag: int
