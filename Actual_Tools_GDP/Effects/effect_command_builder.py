"""
EffectCommandBuilder - Fluent API for creating effect commands.

Provides named methods matching AGE (Advanced Genie Editor) command types.
Parameter names (a, b, c, d) are placeholders - will be renamed once meanings are confirmed.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional

if TYPE_CHECKING:
    from Actual_Tools_GDP.Effects.effect_handle import EffectHandle
    from Actual_Tools_GDP.Effects.command_handle import CommandHandle

__all__ = ["EffectCommandBuilder"]


class EffectCommandBuilder:
    """
    Fluent builder for adding typed effect commands.
    
    Usage:
        effect.add_command.attribute_modifier_set(a=4, b=-1, c=0, d=100)
        effect.add_command.enable_disable_unit(a=100, b=1)
        effect.add_command.team_upgrade_unit(a=4, b=1000)
    """
    
    def __init__(self, effect_handle: EffectHandle) -> None:
        self._effect_handle = effect_handle
    
    def _add(self, type_: int, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> CommandHandle:
        """Internal helper to add a command."""
        return self._effect_handle.new_command(type=type_, a=a, b=b, c=c, d=d)
    
    # =========================================================================
    # Base Commands (0-8)
    # =========================================================================
    
    def attribute_modifier_set(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> CommandHandle:
        """Type 0 - Attribute Modifier (Set)"""
        return self._add(0, a, b, c, d)
    
    def resource_modifier(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> CommandHandle:
        """Type 1 - Resource Modifier (Set/+/-)"""
        return self._add(1, a, b, c, d)
    
    def enable_disable_unit(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> CommandHandle:
        """Type 2 - Enable/Disable Unit"""
        return self._add(2, a, b, c, d)
    
    def upgrade_unit(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> CommandHandle:
        """Type 3 - Upgrade Unit"""
        return self._add(3, a, b, c, d)
    
    def attribute_modifier_add(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> CommandHandle:
        """Type 4 - Attribute Modifier (+/-)"""
        return self._add(4, a, b, c, d)
    
    def attribute_modifier_multiply(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> CommandHandle:
        """Type 5 - Attribute Modifier (Multiply)"""
        return self._add(5, a, b, c, d)
    
    def resource_modifier_multiply(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> CommandHandle:
        """Type 6 - Resource Modifier (Multiply)"""
        return self._add(6, a, b, c, d)
    
    def spawn_unit(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> CommandHandle:
        """Type 7 - Spawn Unit"""
        return self._add(7, a, b, c, d)
    
    def modify_tech(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> CommandHandle:
        """Type 8 - Modify Tech"""
        return self._add(8, a, b, c, d)
    
    # =========================================================================
    # Team Commands (10-18)
    # =========================================================================
    
    def team_attribute_modifier_set(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> CommandHandle:
        """Type 10 - Team Attribute Modifier (Set)"""
        return self._add(10, a, b, c, d)
    
    def team_resource_modifier(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> CommandHandle:
        """Type 11 - Team Resource Modifier (Set/+/-)"""
        return self._add(11, a, b, c, d)
    
    def team_enable_disable_unit(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> CommandHandle:
        """Type 12 - Team Enable/Disable Unit"""
        return self._add(12, a, b, c, d)
    
    def team_upgrade_unit(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> CommandHandle:
        """Type 13 - Team Upgrade Unit"""
        return self._add(13, a, b, c, d)
    
    def team_attribute_modifier_add(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> CommandHandle:
        """Type 14 - Team Attribute Modifier (+/-)"""
        return self._add(14, a, b, c, d)
    
    def team_attribute_modifier_multiply(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> CommandHandle:
        """Type 15 - Team Attribute Modifier (Multiply)"""
        return self._add(15, a, b, c, d)
    
    def team_resource_modifier_multiply(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> CommandHandle:
        """Type 16 - Team Resource Modifier (Multiply)"""
        return self._add(16, a, b, c, d)
    
    def team_spawn_unit(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> CommandHandle:
        """Type 17 - Team Spawn Unit"""
        return self._add(17, a, b, c, d)
    
    def team_modify_tech(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> CommandHandle:
        """Type 18 - Team Modify Tech"""
        return self._add(18, a, b, c, d)
    
    # =========================================================================
    # Enemy Commands (20-28)
    # =========================================================================
    
    def enemy_attribute_modifier_set(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> CommandHandle:
        """Type 20 - Enemy Attribute Modifier (Set)"""
        return self._add(20, a, b, c, d)
    
    def enemy_resource_modifier(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> CommandHandle:
        """Type 21 - Enemy Resource Modifier (Set/+/-)"""
        return self._add(21, a, b, c, d)
    
    def enemy_enable_disable_unit(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> CommandHandle:
        """Type 22 - Enemy Enable/Disable Unit"""
        return self._add(22, a, b, c, d)
    
    def enemy_upgrade_unit(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> CommandHandle:
        """Type 23 - Enemy Upgrade Unit"""
        return self._add(23, a, b, c, d)
    
    def enemy_attribute_modifier_add(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> CommandHandle:
        """Type 24 - Enemy Attribute Modifier (+/-)"""
        return self._add(24, a, b, c, d)
    
    def enemy_attribute_modifier_multiply(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> CommandHandle:
        """Type 25 - Enemy Attribute Modifier (Multiply)"""
        return self._add(25, a, b, c, d)
    
    def enemy_resource_modifier_multiply(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> CommandHandle:
        """Type 26 - Enemy Resource Modifier (Multiply)"""
        return self._add(26, a, b, c, d)
    
    def enemy_spawn_unit(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> CommandHandle:
        """Type 27 - Enemy Spawn Unit"""
        return self._add(27, a, b, c, d)
    
    def enemy_modify_tech(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> CommandHandle:
        """Type 28 - Enemy Modify Tech"""
        return self._add(28, a, b, c, d)
    
    # =========================================================================
    # Neutral Commands (30-38)
    # =========================================================================
    
    def neutral_attribute_modifier_set(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> CommandHandle:
        """Type 30 - Neutral Attribute Modifier (Set)"""
        return self._add(30, a, b, c, d)
    
    def neutral_resource_modifier(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> CommandHandle:
        """Type 31 - Neutral Resource Modifier (Set/+/-)"""
        return self._add(31, a, b, c, d)
    
    def neutral_enable_disable_unit(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> CommandHandle:
        """Type 32 - Neutral Enable/Disable Unit"""
        return self._add(32, a, b, c, d)
    
    def neutral_upgrade_unit(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> CommandHandle:
        """Type 33 - Neutral Upgrade Unit"""
        return self._add(33, a, b, c, d)
    
    def neutral_attribute_modifier_add(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> CommandHandle:
        """Type 34 - Neutral Attribute Modifier (+/-)"""
        return self._add(34, a, b, c, d)
    
    def neutral_attribute_modifier_multiply(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> CommandHandle:
        """Type 35 - Neutral Attribute Modifier (Multiply)"""
        return self._add(35, a, b, c, d)
    
    def neutral_resource_modifier_multiply(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> CommandHandle:
        """Type 36 - Neutral Resource Modifier (Multiply)"""
        return self._add(36, a, b, c, d)
    
    def neutral_spawn_unit(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> CommandHandle:
        """Type 37 - Neutral Spawn Unit"""
        return self._add(37, a, b, c, d)
    
    def neutral_modify_tech(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> CommandHandle:
        """Type 38 - Neutral Modify Tech"""
        return self._add(38, a, b, c, d)
    
    # =========================================================================
    # Gaia Commands (40-48)
    # =========================================================================
    
    def gaia_attribute_modifier_set(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> CommandHandle:
        """Type 40 - Gaia Attribute Modifier (Set)"""
        return self._add(40, a, b, c, d)
    
    def gaia_resource_modifier(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> CommandHandle:
        """Type 41 - Gaia Resource Modifier (Set/+/-)"""
        return self._add(41, a, b, c, d)
    
    def gaia_enable_disable_unit(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> CommandHandle:
        """Type 42 - Gaia Enable/Disable Unit"""
        return self._add(42, a, b, c, d)
    
    def gaia_upgrade_unit(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> CommandHandle:
        """Type 43 - Gaia Upgrade Unit"""
        return self._add(43, a, b, c, d)
    
    def gaia_attribute_modifier_add(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> CommandHandle:
        """Type 44 - Gaia Attribute Modifier (+/-)"""
        return self._add(44, a, b, c, d)
    
    def gaia_attribute_modifier_multiply(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> CommandHandle:
        """Type 45 - Gaia Attribute Modifier (Multiply)"""
        return self._add(45, a, b, c, d)
    
    def gaia_resource_modifier_multiply(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> CommandHandle:
        """Type 46 - Gaia Resource Modifier (Multiply)"""
        return self._add(46, a, b, c, d)
    
    def gaia_spawn_unit(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> CommandHandle:
        """Type 47 - Gaia Spawn Unit"""
        return self._add(47, a, b, c, d)
    
    def gaia_modify_tech(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> CommandHandle:
        """Type 48 - Gaia Modify Tech"""
        return self._add(48, a, b, c, d)
    
    # =========================================================================
    # Tech Commands (101-103)
    # =========================================================================
    
    def tech_cost_modifier(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> CommandHandle:
        """Type 101 - Tech Cost Modifier (Set/+/-)"""
        return self._add(101, a, b, c, d)
    
    def disable_tech(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> CommandHandle:
        """Type 102 - Disable Tech"""
        return self._add(102, a, b, c, d)
    
    def tech_time_modifier(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> CommandHandle:
        """Type 103 - Tech Time Modifier (Set/+/-)"""
        return self._add(103, a, b, c, d)
    
    # =========================================================================
    # Local/Selected Unit Commands (200-206)
    # =========================================================================
    
    def own_master_objects_attribute_modifier_set(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> CommandHandle:
        """Type 200 - Own Master Objects Attribute Modifier (Set)"""
        return self._add(200, a, b, c, d)
    
    def own_master_objects_attribute_modifier_add(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> CommandHandle:
        """Type 201 - Own Master Objects Attribute Modifier (+/-)"""
        return self._add(201, a, b, c, d)
    
    def own_master_objects_attribute_modifier_multiply(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> CommandHandle:
        """Type 202 - Own Master Objects Attribute Modifier (Multiply)"""
        return self._add(202, a, b, c, d)
    
    def selected_unit_attribute_modifier_set(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> CommandHandle:
        """Type 203 - Selected Unit Attribute Modifier (Set)"""
        return self._add(203, a, b, c, d)
    
    def selected_unit_attribute_modifier_add(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> CommandHandle:
        """Type 204 - Selected Unit Attribute Modifier (+/-)"""
        return self._add(204, a, b, c, d)
    
    def selected_unit_attribute_modifier_multiply(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> CommandHandle:
        """Type 205 - Selected Unit Attribute Modifier (Multiply)"""
        return self._add(205, a, b, c, d)
    
    def transform_selected_unit(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> CommandHandle:
        """Type 206 - Transform Selected Unit"""
        return self._add(206, a, b, c, d)
