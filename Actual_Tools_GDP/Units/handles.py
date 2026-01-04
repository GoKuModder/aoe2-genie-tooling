"""
Handle wrapper classes for Unit collection items.

Provides index-aware wrappers:
- TaskHandle: For Bird.tasks
- AttackHandle: For Type50.attacks
- ArmourHandle: For Type50.armours
- DamageGraphicHandle: For Unit.damage_graphics
- TrainLocationHandle: For Creatable.train_locations
- DropSiteHandle: For Bird.drop_sites
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional

if TYPE_CHECKING:
    from Actual_Tools_GDP.Shared.dat_adapter import Task
    from Actual_Tools_GDP.Shared.dat_adapter import AttackOrArmor, DamageGraphic, TrainLocation

__all__ = [
    "TaskHandle",
    "AttackHandle",
    "ArmourHandle",
    "DamageGraphicHandle",
    "TrainLocationHandle",
    "DropSiteHandle",
]


class TaskHandle:
    """
    Wrapper for a Task with its index.
    
    Attributes:
        task_id: Index of this task in the parent's tasks list.
        All Task properties are accessible directly.
    """
    
    __slots__ = ("_task", "_task_id")
    
    def __init__(self, task: Task, task_id: int) -> None:
        object.__setattr__(self, "_task", task)
        object.__setattr__(self, "_task_id", task_id)
    
    def __repr__(self) -> str:
        return f"TaskHandle(task_id={self._task_id}, task_type={self._task.task_type})"
    
    @property
    def task_id(self) -> int:
        """Index of this task in the parent's list."""
        return self._task_id
    
    # Forward all Task attributes
    @property
    def task_type(self) -> int:
        return self._task.task_type
    
    @task_type.setter
    def task_type(self, value: int) -> None:
        self._task.task_type = value
    
    @property
    def id(self) -> int:
        """Task's internal ID."""
        return self._task.id
    
    @id.setter
    def id(self, value: int) -> None:
        self._task.id = value
    
    @property
    def is_default(self) -> int:
        return self._task.is_default
    
    @is_default.setter
    def is_default(self, value: int) -> None:
        self._task.is_default = value
    
    @property
    def action_type(self) -> int:
        return self._task.action_type
    
    @action_type.setter
    def action_type(self, value: int) -> None:
        self._task.action_type = value
    
    @property
    def class_id(self) -> int:
        return self._task.class_id
    
    @class_id.setter
    def class_id(self, value: int) -> None:
        self._task.class_id = value
    
    @property
    def unit_id(self) -> int:
        return self._task.unit_id
    
    @unit_id.setter
    def unit_id(self, value: int) -> None:
        self._task.unit_id = value
    
    @property
    def terrain_id(self) -> int:
        return self._task.terrain_id
    
    @terrain_id.setter
    def terrain_id(self, value: int) -> None:
        self._task.terrain_id = value
    
    @property
    def resource_in(self) -> int:
        return self._task.resource_in
    
    @resource_in.setter
    def resource_in(self, value: int) -> None:
        self._task.resource_in = value
    
    @property
    def resource_out(self) -> int:
        return self._task.resource_out
    
    @resource_out.setter
    def resource_out(self, value: int) -> None:
        self._task.resource_out = value
    
    @property
    def work_value_1(self) -> float:
        return self._task.work_value_1
    
    @work_value_1.setter
    def work_value_1(self, value: float) -> None:
        self._task.work_value_1 = value
    
    @property
    def work_value_2(self) -> float:
        return self._task.work_value_2
    
    @work_value_2.setter
    def work_value_2(self, value: float) -> None:
        self._task.work_value_2 = value
    
    @property
    def work_range(self) -> float:
        return self._task.work_range
    
    @work_range.setter
    def work_range(self, value: float) -> None:
        self._task.work_range = value
    
    @property
    def target_diplomacy(self) -> int:
        return self._task.target_diplomacy
    
    @target_diplomacy.setter
    def target_diplomacy(self, value: int) -> None:
        self._task.target_diplomacy = value
    
    @property
    def working_graphic_id(self) -> int:
        return self._task.working_graphic_id
    
    @working_graphic_id.setter
    def working_graphic_id(self, value: int) -> None:
        self._task.working_graphic_id = value
    
    @property
    def carrying_graphic_id(self) -> int:
        return self._task.carrying_graphic_id
    
    @carrying_graphic_id.setter
    def carrying_graphic_id(self, value: int) -> None:
        self._task.carrying_graphic_id = value
    
    @property
    def enabled(self) -> int:
        return self._task.enabled
    
    @enabled.setter
    def enabled(self, value: int) -> None:
        self._task.enabled = value
    
    # Dynamic access for remaining attributes
    def __getattr__(self, name: str) -> Any:
        if hasattr(self._task, name):
            return getattr(self._task, name)
        raise AttributeError(f"'{type(self).__name__}' has no attribute '{name}'")
    
    def __setattr__(self, name: str, value: Any) -> None:
        if name in self.__slots__:
            object.__setattr__(self, name, value)
        elif hasattr(self._task, name):
            setattr(self._task, name, value)
        else:
            raise AttributeError(f"'{type(self).__name__}' has no attribute '{name}'")


class AttackHandle:
    """
    Wrapper for an AttackOrArmor (attack) with its index.
    """
    
    __slots__ = ("_attack", "_attack_id")
    
    def __init__(self, attack: AttackOrArmor, attack_id: int) -> None:
        object.__setattr__(self, "_attack", attack)
        object.__setattr__(self, "_attack_id", attack_id)
    
    def __repr__(self) -> str:
        return f"AttackHandle(attack_id={self._attack_id}, class_={self._attack.class_}, amount={self._attack.amount})"
    
    @property
    def attack_id(self) -> int:
        """Index of this attack in the parent's list."""
        return self._attack_id
    
    @property
    def class_(self) -> int:
        """Attack class (damage type)."""
        return self._attack.class_
    
    @class_.setter
    def class_(self, value: int) -> None:
        self._attack.class_ = value
    
    @property
    def amount(self) -> int:
        """Attack amount (damage)."""
        return self._attack.amount
    
    @amount.setter
    def amount(self, value: int) -> None:
        self._attack.amount = value


class ArmourHandle:
    """
    Wrapper for an AttackOrArmor (armour) with its index.
    """
    
    __slots__ = ("_armour", "_armour_id")
    
    def __init__(self, armour: AttackOrArmor, armour_id: int) -> None:
        object.__setattr__(self, "_armour", armour)
        object.__setattr__(self, "_armour_id", armour_id)
    
    def __repr__(self) -> str:
        return f"ArmourHandle(armour_id={self._armour_id}, class_={self._armour.class_}, amount={self._armour.amount})"
    
    @property
    def armour_id(self) -> int:
        """Index of this armour in the parent's list."""
        return self._armour_id
    
    @property
    def class_(self) -> int:
        """Armour class (defense type)."""
        return self._armour.class_
    
    @class_.setter
    def class_(self, value: int) -> None:
        self._armour.class_ = value
    
    @property
    def amount(self) -> int:
        """Armour amount (defense)."""
        return self._armour.amount
    
    @amount.setter
    def amount(self, value: int) -> None:
        self._armour.amount = value


class DamageGraphicHandle:
    """
    Wrapper for a DamageGraphic with its index.
    """
    
    __slots__ = ("_damage_graphic", "_damage_graphic_id")
    
    def __init__(self, damage_graphic: DamageGraphic, damage_graphic_id: int) -> None:
        object.__setattr__(self, "_damage_graphic", damage_graphic)
        object.__setattr__(self, "_damage_graphic_id", damage_graphic_id)
    
    def __repr__(self) -> str:
        return f"DamageGraphicHandle(id={self._damage_graphic_id}, graphic_id={self._damage_graphic.graphic_id})"
    
    @property
    def damage_graphic_id(self) -> int:
        """Index of this damage graphic in the parent's list."""
        return self._damage_graphic_id
    
    @property
    def graphic_id(self) -> int:
        """Graphic ID to display."""
        return self._damage_graphic.graphic_id
    
    @graphic_id.setter
    def graphic_id(self, value: int) -> None:
        self._damage_graphic.graphic_id = value
    
    @property
    def damage_percent(self) -> int:
        """Damage percentage threshold (0-100)."""
        return self._damage_graphic.damage_percent
    
    @damage_percent.setter
    def damage_percent(self, value: int) -> None:
        self._damage_graphic.damage_percent = value
    
    @property
    def apply_mode(self) -> int:
        """Apply mode."""
        return self._damage_graphic.apply_mode
    
    @apply_mode.setter
    def apply_mode(self, value: int) -> None:
        self._damage_graphic.apply_mode = value


class TrainLocationHandle:
    """
    Wrapper for a TrainLocation with its index.
    """
    
    __slots__ = ("_train_location", "_train_location_id")
    
    def __init__(self, train_location: TrainLocation, train_location_id: int) -> None:
        object.__setattr__(self, "_train_location", train_location)
        object.__setattr__(self, "_train_location_id", train_location_id)
    
    def __repr__(self) -> str:
        return f"TrainLocationHandle(id={self._train_location_id}, unit_id={self._train_location.unit_id})"
    
    @property
    def train_location_id(self) -> int:
        """Index of this train location in the parent's list."""
        return self._train_location_id
    
    @property
    def train_time(self) -> int:
        """Training time."""
        return self._train_location.train_time
    
    @train_time.setter
    def train_time(self, value: int) -> None:
        self._train_location.train_time = value
    
    @property
    def unit_id(self) -> int:
        """Building unit ID where trained."""
        return self._train_location.unit_id
    
    @unit_id.setter
    def unit_id(self, value: int) -> None:
        self._train_location.unit_id = value
    
    @property
    def button_id(self) -> int:
        """Button position ID."""
        return self._train_location.button_id
    
    @button_id.setter
    def button_id(self, value: int) -> None:
        self._train_location.button_id = value
    
    @property
    def hot_key_id(self) -> int:
        """Hotkey ID."""
        return self._train_location.hot_key_id
    
    @hot_key_id.setter
    def hot_key_id(self, value: int) -> None:
        self._train_location.hot_key_id = value


class DropSiteHandle:
    """
    Wrapper for a drop site (just an int) with its index.
    """
    
    __slots__ = ("_drop_sites_list", "_drop_site_id")
    
    def __init__(self, drop_sites_list: list, drop_site_id: int) -> None:
        object.__setattr__(self, "_drop_sites_list", drop_sites_list)
        object.__setattr__(self, "_drop_site_id", drop_site_id)
    
    def __repr__(self) -> str:
        return f"DropSiteHandle(id={self._drop_site_id}, unit_id={self.unit_id})"
    
    @property
    def drop_site_id(self) -> int:
        """Index of this drop site in the parent's list."""
        return self._drop_site_id
    
    @property
    def unit_id(self) -> int:
        """Drop site unit ID."""
        if 0 <= self._drop_site_id < len(self._drop_sites_list):
            return self._drop_sites_list[self._drop_site_id]
        return -1
    
    @unit_id.setter
    def unit_id(self, value: int) -> None:
        if 0 <= self._drop_site_id < len(self._drop_sites_list):
            self._drop_sites_list[self._drop_site_id] = value
