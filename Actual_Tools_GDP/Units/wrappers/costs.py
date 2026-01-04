"""
CostWrapper - Resource cost wrapper for UnitHandle.

Provides flat property access to resource costs (food, wood, stone, gold).
Maps to Creatable.resource_costs structure.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, List, Optional

if TYPE_CHECKING:
    from genie_rust import Unit

__all__ = ["CostWrapper"]
from Actual_Tools_GDP.Datasets.resources import Resource

# Resource type IDs from AoE2
RESOURCE_FOOD = Resource.FOOD_STORAGE
RESOURCE_WOOD = Resource.WOOD_STORAGE
RESOURCE_STONE = Resource.STONE_STORAGE
RESOURCE_GOLD = Resource.GOLD_STORAGE


class CostWrapper:
    """
    Wrapper for unit resource costs.

    Provides flat property access:
    - unit.cost.food = 100
    - unit.cost.gold = 50

    Maps to Creatable.resource_costs[].amount based on type.
    """

    __slots__ = ("_units",)

    def __init__(self, units: List[Unit]) -> None:
        """
        Initialize with list of units to modify.

        Args:
            units: List of Unit objects to proxy
        """
        object.__setattr__(self, "_units", units)

    def _get_creatable(self) -> Optional[Any]:
        """Get Creatable from first unit."""
        if self._units and self._units[0].creatable:
            return self._units[0].creatable
        return None

    def _get_cost_by_type(self, resource_type: int | Resource) -> int:
        """Get cost amount for a resource type."""
        creatable = self._get_creatable()
        if creatable:
            for cost in creatable.resource_costs:
                if cost.type == resource_type:
                    return cost.amount
        return 0

    def _set_cost_by_type(self, resource_type: int | Resource, amount: int) -> None:
        """Set cost amount for a resource type across all units."""
        for unit in self._units:
            if unit.creatable:
                for cost in unit.creatable.resource_costs:
                    if cost.type == resource_type:
                        cost.amount = amount
                        break

    # -------------------------
    # Resource Properties
    # -------------------------

    @property
    def food(self) -> int:
        """Food cost."""
        return self._get_cost_by_type(RESOURCE_FOOD)

    @food.setter
    def food(self, value: int) -> None:
        self._set_cost_by_type(RESOURCE_FOOD, value)

    @property
    def wood(self) -> int:
        """Wood cost."""
        return self._get_cost_by_type(RESOURCE_WOOD)

    @wood.setter
    def wood(self, value: int) -> None:
        self._set_cost_by_type(RESOURCE_WOOD, value)

    @property
    def stone(self) -> int:
        """Stone cost."""
        return self._get_cost_by_type(RESOURCE_STONE)

    @stone.setter
    def stone(self, value: int) -> None:
        self._set_cost_by_type(RESOURCE_STONE, value)

    @property
    def gold(self) -> int:
        """Gold cost."""
        return self._get_cost_by_type(RESOURCE_GOLD)

    @gold.setter
    def gold(self, value: int) -> None:
        self._set_cost_by_type(RESOURCE_GOLD, value)
