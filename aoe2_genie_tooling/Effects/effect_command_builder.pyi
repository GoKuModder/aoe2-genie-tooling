"""Type stubs for EffectCommandBuilder - enables IDE autocomplete"""
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from aoe2_genie_tooling.Effects.command_handle import CommandHandle


class EffectCommandBuilder:
    """
    Fluent builder for adding typed effect commands.
    
    Usage:
        effect.add_command.attribute_modifier_set(a=4, b=-1, c=0, d=100)
        effect.add_command.enable_disable_unit(a=100, b=1)
        effect.add_command.team_upgrade_unit(a=4, b=1000)
    """
    
    # Base Commands (0-8)
    def attribute_modifier_set(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> "CommandHandle":
        """Type 0 - Attribute Modifier (Set)"""
        ...
    
    def resource_modifier(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> "CommandHandle":
        """Type 1 - Resource Modifier (Set/+/-)"""
        ...
    
    def enable_disable_unit(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> "CommandHandle":
        """Type 2 - Enable/Disable Unit"""
        ...
    
    def upgrade_unit(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> "CommandHandle":
        """Type 3 - Upgrade Unit"""
        ...
    
    def attribute_modifier_add(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> "CommandHandle":
        """Type 4 - Attribute Modifier (+/-)"""
        ...
    
    def attribute_modifier_multiply(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> "CommandHandle":
        """Type 5 - Attribute Modifier (Multiply)"""
        ...
    
    def resource_modifier_multiply(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> "CommandHandle":
        """Type 6 - Resource Modifier (Multiply)"""
        ...
    
    def spawn_unit(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> "CommandHandle":
        """Type 7 - Spawn Unit"""
        ...
    
    def modify_tech(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> "CommandHandle":
        """Type 8 - Modify Tech"""
        ...
    
    # Team Commands (10-18)
    def team_attribute_modifier_set(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> "CommandHandle":
        """Type 10 - Team Attribute Modifier (Set)"""
        ...
    
    def team_resource_modifier(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> "CommandHandle":
        """Type 11 - Team Resource Modifier (Set/+/-)"""
        ...
    
    def team_enable_disable_unit(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> "CommandHandle":
        """Type 12 - Team Enable/Disable Unit"""
        ...
    
    def team_upgrade_unit(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> "CommandHandle":
        """Type 13 - Team Upgrade Unit"""
        ...
    
    def team_attribute_modifier_add(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> "CommandHandle":
        """Type 14 - Team Attribute Modifier (+/-)"""
        ...
    
    def team_attribute_modifier_multiply(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> "CommandHandle":
        """Type 15 - Team Attribute Modifier (Multiply)"""
        ...
    
    def team_resource_modifier_multiply(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> "CommandHandle":
        """Type 16 - Team Resource Modifier (Multiply)"""
        ...
    
    def team_spawn_unit(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> "CommandHandle":
        """Type 17 - Team Spawn Unit"""
        ...
    
    def team_modify_tech(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> "CommandHandle":
        """Type 18 - Team Modify Tech"""
        ...
    
    # Enemy Commands (20-28)
    def enemy_attribute_modifier_set(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> "CommandHandle":
        """Type 20 - Enemy Attribute Modifier (Set)"""
        ...
    
    def enemy_resource_modifier(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> "CommandHandle":
        """Type 21 - Enemy Resource Modifier (Set/+/-)"""
        ...
    
    def enemy_enable_disable_unit(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> "CommandHandle":
        """Type 22 - Enemy Enable/Disable Unit"""
        ...
    
    def enemy_upgrade_unit(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> "CommandHandle":
        """Type 23 - Enemy Upgrade Unit"""
        ...
    
    def enemy_attribute_modifier_add(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> "CommandHandle":
        """Type 24 - Enemy Attribute Modifier (+/-)"""
        ...
    
    def enemy_attribute_modifier_multiply(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> "CommandHandle":
        """Type 25 - Enemy Attribute Modifier (Multiply)"""
        ...
    
    def enemy_resource_modifier_multiply(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> "CommandHandle":
        """Type 26 - Enemy Resource Modifier (Multiply)"""
        ...
    
    def enemy_spawn_unit(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> "CommandHandle":
        """Type 27 - Enemy Spawn Unit"""
        ...
    
    def enemy_modify_tech(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> "CommandHandle":
        """Type 28 - Enemy Modify Tech"""
        ...
    
    # Neutral Commands (30-38)
    def neutral_attribute_modifier_set(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> "CommandHandle":
        """Type 30 - Neutral Attribute Modifier (Set)"""
        ...
    
    def neutral_resource_modifier(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> "CommandHandle":
        """Type 31 - Neutral Resource Modifier (Set/+/-)"""
        ...
    
    def neutral_enable_disable_unit(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> "CommandHandle":
        """Type 32 - Neutral Enable/Disable Unit"""
        ...
    
    def neutral_upgrade_unit(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> "CommandHandle":
        """Type 33 - Neutral Upgrade Unit"""
        ...
    
    def neutral_attribute_modifier_add(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> "CommandHandle":
        """Type 34 - Neutral Attribute Modifier (+/-)"""
        ...
    
    def neutral_attribute_modifier_multiply(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> "CommandHandle":
        """Type 35 - Neutral Attribute Modifier (Multiply)"""
        ...
    
    def neutral_resource_modifier_multiply(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> "CommandHandle":
        """Type 36 - Neutral Resource Modifier (Multiply)"""
        ...
    
    def neutral_spawn_unit(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> "CommandHandle":
        """Type 37 - Neutral Spawn Unit"""
        ...
    
    def neutral_modify_tech(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> "CommandHandle":
        """Type 38 - Neutral Modify Tech"""
        ...
    
    # Gaia Commands (40-48)
    def gaia_attribute_modifier_set(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> "CommandHandle":
        """Type 40 - Gaia Attribute Modifier (Set)"""
        ...
    
    def gaia_resource_modifier(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> "CommandHandle":
        """Type 41 - Gaia Resource Modifier (Set/+/-)"""
        ...
    
    def gaia_enable_disable_unit(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> "CommandHandle":
        """Type 42 - Gaia Enable/Disable Unit"""
        ...
    
    def gaia_upgrade_unit(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> "CommandHandle":
        """Type 43 - Gaia Upgrade Unit"""
        ...
    
    def gaia_attribute_modifier_add(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> "CommandHandle":
        """Type 44 - Gaia Attribute Modifier (+/-)"""
        ...
    
    def gaia_attribute_modifier_multiply(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> "CommandHandle":
        """Type 45 - Gaia Attribute Modifier (Multiply)"""
        ...
    
    def gaia_resource_modifier_multiply(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> "CommandHandle":
        """Type 46 - Gaia Resource Modifier (Multiply)"""
        ...
    
    def gaia_spawn_unit(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> "CommandHandle":
        """Type 47 - Gaia Spawn Unit"""
        ...
    
    def gaia_modify_tech(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> "CommandHandle":
        """Type 48 - Gaia Modify Tech"""
        ...
    
    # Tech Commands (101-103)
    def tech_cost_modifier(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> "CommandHandle":
        """Type 101 - Tech Cost Modifier (Set/+/-)"""
        ...
    
    def disable_tech(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> "CommandHandle":
        """Type 102 - Disable Tech"""
        ...
    
    def tech_time_modifier(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> "CommandHandle":
        """Type 103 - Tech Time Modifier (Set/+/-)"""
        ...
    
    # Local/Selected Unit Commands (200-206)
    def own_master_objects_attribute_modifier_set(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> "CommandHandle":
        """Type 200 - Own Master Objects Attribute Modifier (Set)"""
        ...
    
    def own_master_objects_attribute_modifier_add(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> "CommandHandle":
        """Type 201 - Own Master Objects Attribute Modifier (+/-)"""
        ...
    
    def own_master_objects_attribute_modifier_multiply(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> "CommandHandle":
        """Type 202 - Own Master Objects Attribute Modifier (Multiply)"""
        ...
    
    def selected_unit_attribute_modifier_set(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> "CommandHandle":
        """Type 203 - Selected Unit Attribute Modifier (Set)"""
        ...
    
    def selected_unit_attribute_modifier_add(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> "CommandHandle":
        """Type 204 - Selected Unit Attribute Modifier (+/-)"""
        ...
    
    def selected_unit_attribute_modifier_multiply(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> "CommandHandle":
        """Type 205 - Selected Unit Attribute Modifier (Multiply)"""
        ...
    
    def transform_selected_unit(self, a: int = -1, b: int = -1, c: int = -1, d: float = 0.0) -> "CommandHandle":
        """Type 206 - Transform Selected Unit"""
        ...
