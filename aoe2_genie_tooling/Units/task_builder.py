"""
TaskBuilder - Fluent API for creating unit tasks.

Provides named methods matching AGE (Advanced Genie Editor) task types.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from aoe2_genie_tooling.Units.unit_handle import UnitHandle
    from aoe2_genie_tooling.Units.handles import TaskHandle

__all__ = ["TaskBuilder"]


class TaskBuilder:
    """
    Fluent builder for adding typed tasks to units.
    
    Usage:
        unit.add_task.combat(class_id=0)
        unit.add_task.garrison(class_id=11)
        unit.add_task.resource_generation(amount_received=10, type_resource_received=1)
    """
    
    def __init__(self, unit_handle: UnitHandle) -> None:
        self._unit_handle = unit_handle
    
    def _add(self, action_type: int, **kwargs) -> Optional["TaskHandle"]:
        """Internal helper to add a task with given action_type."""
        return self._unit_handle.create_task(action_type=action_type, **kwargs)
    
    # =========================================================================
    # Basic Tasks (0-14, 20-21, 101-106)
    # =========================================================================
    
    def none(self, **kwargs) -> Optional["TaskHandle"]:
        """Action Type 0 - None"""
        return self._add(0, **kwargs)
    
    def move_to(self, **kwargs) -> Optional["TaskHandle"]:
        """Action Type 1 - Move To"""
        return self._add(1, **kwargs)
    
    def follow(self, **kwargs) -> Optional["TaskHandle"]:
        """Action Type 2 - Follow"""
        return self._add(2, **kwargs)
    
    def garrison(self, class_id: int = -1, **kwargs) -> Optional["TaskHandle"]:
        """Action Type 3 - Garrison"""
        return self._add(3, class_id=class_id, **kwargs)
    
    def explore(self, **kwargs) -> Optional["TaskHandle"]:
        """Action Type 4 - Explore"""
        return self._add(4, **kwargs)
    
    def gather(self, resource_in: int = -1, resource_out: int = -1, **kwargs) -> Optional["TaskHandle"]:
        """Action Type 5 - Gather/Rebuild"""
        return self._add(5, resource_in=resource_in, resource_out=resource_out, **kwargs)
    
    def graze(self, **kwargs) -> Optional["TaskHandle"]:
        """Action Type 6 - Graze"""
        return self._add(6, **kwargs)
    
    def combat(
        self, 
        class_id: int = -1, 
        target_diplomacy: int = 5,  # Gaia + Neutral + Enemy
        search_wait_time: float = 3.0,
        combat_level: int = 1,  # unused_flag
        enable_targeting: int = 1,
        auto_search_targets: bool = True,
        **kwargs
    ) -> Optional["TaskHandle"]:
        """
        Action Type 7 - Combat
        
        Args:
            class_id: Target unit class ID (-1 for any).
            target_diplomacy: Target diplomacy (5=Gaia+Neutral+Enemy).
            search_wait_time: Time to wait between searches.
            combat_level: Combat level flag (1 for combat units).
            enable_targeting: Enable targeting (1 to enable).
            auto_search_targets: Auto search for targets.
        """
        return self._add(
            7, 
            class_id=class_id, 
            target_diplomacy=target_diplomacy,
            search_wait_time=search_wait_time,
            combat_level=combat_level,
            enable_targeting=enable_targeting,
            auto_search_targets=auto_search_targets,
            **kwargs
        )
    
    def shoot(self, **kwargs) -> Optional["TaskHandle"]:
        """Action Type 8 - Shoot"""
        return self._add(8, **kwargs)
    
    def attack(self, **kwargs) -> Optional["TaskHandle"]:
        """Action Type 9 - Attack"""
        return self._add(9, **kwargs)
    
    def fly(self, **kwargs) -> Optional["TaskHandle"]:
        """Action Type 10 - Fly"""
        return self._add(10, **kwargs)
    
    def scare_hunt(self, **kwargs) -> Optional["TaskHandle"]:
        """Action Type 11 - Scare/Hunt"""
        return self._add(11, **kwargs)
    
    def unload_boat(self, **kwargs) -> Optional["TaskHandle"]:
        """Action Type 12 - Unload (boat-like)"""
        return self._add(12, **kwargs)
    
    def guard(self, **kwargs) -> Optional["TaskHandle"]:
        """Action Type 13 - Guard"""
        return self._add(13, **kwargs)
    
    def siege_tower_ability(self, **kwargs) -> Optional["TaskHandle"]:
        """Action Type 14 - Siege Tower Ability"""
        return self._add(14, **kwargs)
        
    def escape(self, **kwargs) -> Optional["TaskHandle"]:
        """Action Type 20 - Escape"""
        return self._add(20, **kwargs)
    
    def make(self, **kwargs) -> Optional["TaskHandle"]:
        """Action Type 21 - Make"""
        return self._add(21, **kwargs)

    def build(self, **kwargs) -> Optional["TaskHandle"]:
        """Action Type 101 - Build"""
        return self._add(101, **kwargs)
    
    def make_unit(self, **kwargs) -> Optional["TaskHandle"]:
        """Action Type 102 - Make a Unit"""
        return self._add(102, **kwargs)
    
    def make_technology(self, **kwargs) -> Optional["TaskHandle"]:
        """Action Type 103 - Make a Technology"""
        return self._add(103, **kwargs)
    
    def convert(self, work_value_1: float = 0.0, work_value_2: float = 0.0, **kwargs) -> Optional["TaskHandle"]:
        """Action Type 104 - Convert"""
        return self._add(104, work_value_1=work_value_1, work_value_2=work_value_2, **kwargs)
    
    def heal(self, work_value_1: float = 0.0, work_range: float = 0.0, **kwargs) -> Optional["TaskHandle"]:
        """Action Type 105 - Heal"""
        return self._add(105, work_value_1=work_value_1, work_range=work_range, **kwargs)
    
    def repair(self, **kwargs) -> Optional["TaskHandle"]:
        """Action Type 106 - Repair"""
        return self._add(106, **kwargs)

    # =========================================================================
    # Updated/New Tasks
    # =========================================================================

    def auto_convert(self, capture_text_id: float = 0.0, **kwargs) -> Optional["TaskHandle"]:
        """
        Action Type 107 - Get Auto-Converted (Tasks 107)
        
        Args:
            capture_text_id: String ID to display when capturing (maps to search_wait_time)
        """
        return self._add(107, search_wait_time=capture_text_id, **kwargs)

    def discovery_artifact(self, **kwargs) -> Optional["TaskHandle"]:
        """Action Type 108 - Discovery Artifact"""
        return self._add(108, **kwargs)

    def hunt(
        self, 
        resource_in: int = -1, 
        resource_out: int = -1, 
        decay_prevent_resource: int = -1,
        **kwargs
    ) -> Optional["TaskHandle"]:
        """
        Action Type 110 - Hunt (Tasks 111?)
        
        Args:
            resource_in: Resource gathered
            resource_out: Resource returned
            decay_prevent_resource: If "Unused Resource" set and corresponding val is 1, prevents decay (maps to unused_resource)
        """
        return self._add(110, resource_in=resource_in, resource_out=resource_out, 
                        unused_resource=decay_prevent_resource, **kwargs)

    def trade(self, unit_id: int = -1, **kwargs) -> Optional["TaskHandle"]:
        """Action Type 111 - Trade"""
        return self._add(111, unit_id=unit_id, **kwargs)

    def generate_wonder_victory(self, **kwargs) -> Optional["TaskHandle"]:
        """Action Type 120 - Generate Wonder Victory"""
        return self._add(120, **kwargs)
    
    def deselect_when_tasked_farm(self, **kwargs) -> Optional["TaskHandle"]:
        """Action Type 121 - Deselect When Tasked (Farm)"""
        return self._add(121, **kwargs)
    
    def loot_gather(self, **kwargs) -> Optional["TaskHandle"]:
        """Action Type 122 - Loot (Gather)"""
        return self._add(122, **kwargs)
    
    def housing(self, **kwargs) -> Optional["TaskHandle"]:
        """Action Type 123 - Housing"""
        return self._add(123, **kwargs)
    
    def pack(self, **kwargs) -> Optional["TaskHandle"]:
        """Action Type 124 - Pack"""
        return self._add(124, **kwargs)
    
    def unpack_and_attack(self, **kwargs) -> Optional["TaskHandle"]:
        """Action Type 125 - Unpack and Attack"""
        return self._add(125, **kwargs)
    
    def off_map_trade(self, **kwargs) -> Optional["TaskHandle"]:
        """Action Type 131 - Off-map Trade"""
        return self._add(131, **kwargs)

    def pickup_unit(self, transform_unit_id: float = 0.0, **kwargs) -> Optional["TaskHandle"]:
        """
        Action Type 132 - Pickup Unit
        
        Args:
            transform_unit_id: Unit ID to transform into (maps to work_value_1)
        """
        return self._add(132, work_value_1=transform_unit_id, **kwargs)
    
    def speed_charge(
        self, 
        work_value_1: float = 0.0, 
        work_value_2: float = 0.0,
        work_range: float = 0.0,
        work_flag_2: int = 2001,
        **kwargs
    ) -> Optional["TaskHandle"]:
        """
        Action Type 133 - Speed Charge (Charge Attack in Editor)
        
        Requires "Special Ability" attribute to be 3.
        
        Args:
            work_value_1: Minimum distance from target for speed up to start
            work_value_2: Maximum distance from target for speed up to start
            work_range: Multiplier on the unit speed while charging
            work_flag_2: MUST be 2001 for the task to work (default: 2001)
        """
        return self._add(
            133, 
            work_value_1=work_value_1, 
            work_value_2=work_value_2,
            work_range=work_range,
            work_flag_2=work_flag_2,
            **kwargs
        )
    
    def transform_unit(self, **kwargs) -> Optional["TaskHandle"]:
        """Action Type 134 - Transform Unit"""
        return self._add(134, **kwargs)
    
    def kidnap_unit(self, **kwargs) -> Optional["TaskHandle"]:
        """Action Type 135 - Kidnap Unit"""
        return self._add(135, **kwargs)

    def deposit_unit(self, transform_unit_id: float = 0.0, **kwargs) -> Optional["TaskHandle"]:
        """
        Action Type 136 - Deposit Unit
        
        Args:
            transform_unit_id: Unit ID to transform into (maps to work_value_1)
        """
        return self._add(136, work_value_1=transform_unit_id, **kwargs)

    def shear(self, **kwargs) -> Optional["TaskHandle"]:
        """Action Type 149 - Shear"""
        return self._add(149, **kwargs)
    
    def regeneration(self, **kwargs) -> Optional["TaskHandle"]:
        """Action Type 150 - Regeneration"""
        return self._add(150, **kwargs)

    def resource_generation(
        self,
        amount_received: float = 0.0,
        type_resource_received: int = -1,
        productivity_resource: int = -1,
        target_unit_id: int = -1,
        target_class_id: int = -1,
        units_require_flag_2: int = 0,
        **kwargs
    ) -> Optional["TaskHandle"]:
        """
        Action Type 151 - Resource Generation
        
        Args:
            amount_received: Work Value 1 - Amount
            type_resource_received: Resource Out - Type
            productivity_resource: Multiplier resource
            target_unit_id: Unit ID target (maps to unit_id)
            target_class_id: Class ID target (maps to class_id)
            units_require_flag_2: Work Mode - For passive gen (maps to work_mode)
        """
        return self._add(151, work_value_1=amount_received, resource_out=type_resource_received,
                        productivity_resource=productivity_resource, unit_id=target_unit_id,
                        class_id=target_class_id, work_mode=units_require_flag_2, **kwargs)

    def movement_damage(self, **kwargs) -> Optional["TaskHandle"]:
        """Action Type 152 - Movement Damage"""
        return self._add(152, **kwargs)
    
    def moveable_drop_site(self, **kwargs) -> Optional["TaskHandle"]:
        """Action Type 153 - Moveable Drop Site"""
        return self._add(153, **kwargs)

    def pillage(
        self,
        amount_received: float = 0.0,
        type_resource_received: int = -1,
        productivity_resource: int = -1,
        tech_effect_id: int = -1,
        unused_4th_resource: int = -1,
        owner_vs_target_range: float = 0.0,
        proceeding_graphic: int = -1,
        resource_gathering_sound: int = -1,
        carry_check_id: int = -1,
        work_flag: int = 0,
        veterancy_effect_attr: float = 0.0,
        veterancy_effect_val: int = 0,
        **kwargs
    ) -> Optional["TaskHandle"]:
        """
        Action Type 154 - Loot/Pillage
        
        Args:
            amount_received: Work Value 1
            type_resource_received: Resource Out
            productivity_resource: Productivity/Multiplier
            tech_effect_id: Resource In (tech effect ID)
            unused_4th_resource: Unused Resource
            owner_vs_target_range: Work Range (0=owner, !=0=target)
            proceeding_graphic: Proceed Sprite ID
            resource_gathering_sound: Gather Sound ID
            carry_check_id: Carry Sprite ID
            work_flag: Work Mode (max triggers)
            veterancy_effect_attr: Search Wait Time (if Unused Flag=1)
            veterancy_effect_val: Gather Type (if Unused Flag=1)
        """
        return self._add(154, work_value_1=amount_received, resource_out=type_resource_received,
                        productivity_resource=productivity_resource, resource_in=tech_effect_id,
                        unused_resource=unused_4th_resource, work_range=owner_vs_target_range,
                        proceeding_graphic_id=proceeding_graphic, resource_gather_sound_id=resource_gathering_sound,
                        carry_sprite_id=carry_check_id, work_mode=work_flag,
                        search_wait_time=veterancy_effect_attr, gather_type=veterancy_effect_val,
                        **kwargs)

    def aura(
        self,
        attribute_id: float = 0.0,
        max_increase: float = 0.0,
        required_units: float = 0.0,
        radius: float = 0.0,
        affected_players: int = 0,
        proceeding_graphic: int = -1,
        icon_id: int = 0,
        tooltip_short: int = -1,
        tooltip_long: int = -1,
        flags: int = 0,
        **kwargs
    ) -> Optional["TaskHandle"]:
        """
        Action Type 155 - Aura
        
        Args:
            attribute_id: Search Wait Time
            max_increase: Work Value 1
            required_units: Work Value 2
            radius: Work Range
            affected_players: Target Diplomacy
            proceeding_graphic: Proceed Sprite ID
            icon_id: Gather Type
            tooltip_short: Resource Gather Sound ID
            tooltip_long: Resource Deposit Sound ID
            flags: Enable Targeting (Unused Flag)
        """
        return self._add(155, search_wait_time=attribute_id, work_value_1=max_increase,
                        work_value_2=required_units, work_range=radius, target_diplomacy=affected_players,
                        proceeding_graphic_id=proceeding_graphic, gather_type=icon_id,
                        resource_gather_sound_id=tooltip_short, resource_deposit_sound_id=tooltip_long,
                        enable_targeting=flags, **kwargs)

    def additional_spawn(
        self,
        spawn_unit_id: float = 0.0,
        spawn_count: float = 0.0,
        additional_spawn_count: int = -1,
        **kwargs
    ) -> Optional["TaskHandle"]:
        """
        Action Type 156 - Additional Spawn
        
        Args:
            spawn_unit_id: Work Value 1
            spawn_count: Work Value 2
            additional_spawn_count: Productivity Resource (alias as requested)
        """
        return self._add(156, work_value_1=spawn_unit_id, work_value_2=spawn_count,
                        productivity_resource=additional_spawn_count, **kwargs)

    def stingers(
        self,
        value_add: float = 0.0,
        duration: float = 0.0,
        apply_to_target: float = 0.0,
        attribute_id: float = 0.0,
        productivity_resource: int = -1,
        flags: int = 0,
        **kwargs
    ) -> Optional["TaskHandle"]:
        """
        Action Type 157 - Stingers
        
        Args:
            value_add: Work Value 1
            duration: Work Value 2
            apply_to_target: Work Range (0 or 1)
            attribute_id: Search Wait Time
            productivity_resource: Productivity Resource
            flags: Enable Targeting/Unused Flag
        """
        return self._add(157, work_value_1=value_add, work_value_2=duration, work_range=apply_to_target,
                        search_wait_time=attribute_id, productivity_resource=productivity_resource,
                        enable_targeting=flags, **kwargs)

    def hp_transformation(
        self,
        transform_unit_id: float = 0.0,
        threshold_hp: float = 0.0,
        productivity_resource: int = -1,
        multiplier_resource: int = -1,
        flags: int = 0,
        **kwargs
    ) -> Optional["TaskHandle"]:
        """
        Action Type 158 - HP Transformation
        
        Args:
            transform_unit_id: Work Value 1
            threshold_hp: Work Value 2
            productivity_resource: Productivity Resource
            multiplier_resource: Resource Out
            flags: Enable Targeting/Unused Flag
        """
        return self._add(158, work_value_1=transform_unit_id, work_value_2=threshold_hp,
                        productivity_resource=productivity_resource, resource_out=multiplier_resource,
                        enable_targeting=flags, **kwargs)
