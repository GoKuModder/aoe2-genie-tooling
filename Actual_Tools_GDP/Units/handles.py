"""
Handle wrapper classes for Unit collection items.

Ported from handles_OLD.py to work with GenieDatParser.

Provides index-aware wrappers:
- TaskHandle: For task_info.tasks
- AttackHandle: For combat_info.attacks
- ArmourHandle: For combat_info.armors
- DamageGraphicHandle: For unit.damage_sprites
- TrainLocationHandle: For creation_info.train_locations_new
- DropSiteHandle: For task_info.drop_site_unit_ids
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, List, Optional

if TYPE_CHECKING:
    from sections.unit_data.unit_task import UnitTask
    from sections.civilization.type_info.damage_class import DamageClass
    from sections.civilization.unit_damage_sprite import UnitDamageSprite
    from sections.civilization.type_info.train_location import TrainLocation


__all__ = [
    "TaskHandle",
    "AttackHandle",
    "ArmourHandle",
    "DamageGraphicHandle",
    "TrainLocationHandle",
    "DropSiteHandle",
    "BuildingAnnexHandle",
    "CostHandle",
    "ResourceHandle",
]


class TaskHandle:
    """
    Wrapper for a UnitTask with its index.

    Attributes:
        task_id: Index of this task in the parent's tasks list.
        All Task properties are accessible directly.
    """

    __slots__ = ("_task", "_task_id")

    def __init__(self, task: "UnitTask", task_id: int) -> None:
        object.__setattr__(self, "_task", task)
        object.__setattr__(self, "_task_id", task_id)

    def __repr__(self) -> str:
        task_type = getattr(self._task, 'task_type', 0)
        return f"TaskHandle(task_id={self._task_id}, task_type={task_type})"

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
        self._task.is_default = bool(value)

    @property
    def action_type(self) -> int:
        return self._task.action_type

    @action_type.setter
    def action_type(self, value: int) -> None:
        self._task.action_type = value

    @property
    def class_id(self) -> int:
        return self._task.unit_class_id

    @class_id.setter
    def class_id(self, value: int) -> None:
        self._task.unit_class_id = value

    @property
    def unit_id(self) -> int:
        return self._task.unit_type

    @unit_id.setter
    def unit_id(self, value: int) -> None:
        self._task.unit_type = value

    @property
    def terrain_id(self) -> int:
        return self._task.terrain_type

    @terrain_id.setter
    def terrain_id(self, value: int) -> None:
        self._task.terrain_type = value

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
        return self._task.work_value1

    @work_value_1.setter
    def work_value_1(self, value: float) -> None:
        self._task.work_value1 = value

    @property
    def work_value_2(self) -> float:
        return self._task.work_value2

    @work_value_2.setter
    def work_value_2(self, value: float) -> None:
        self._task.work_value2 = value

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

    # Core graphic mapping fixes (UnitTask struct uses these names)
    @property
    def working_graphic_id(self) -> int:
        return self._task.work_sprite_id

    @working_graphic_id.setter
    def working_graphic_id(self, value: int) -> None:
        self._task.work_sprite_id = value

    @property
    def carrying_graphic_id(self) -> int:
        return self._task.carry_sprite_id

    @carrying_graphic_id.setter
    def carrying_graphic_id(self, value: int) -> None:
        self._task.carry_sprite_id = value

    # New Property aliases for TaskBuilder
    @property
    def work_sprite_id(self) -> int:
        return self._task.work_sprite_id

    @work_sprite_id.setter
    def work_sprite_id(self, value: int) -> None:
        self._task.work_sprite_id = value

    @property
    def carry_sprite_id(self) -> int:
        return self._task.carry_sprite_id

    @carry_sprite_id.setter
    def carry_sprite_id(self, value: int) -> None:
        self._task.carry_sprite_id = value
        
    @property
    def productivity_resource(self) -> int:
        return self._task.productivity_resource
        
    @productivity_resource.setter
    def productivity_resource(self, value: int) -> None:
        self._task.productivity_resource = value
        
    @property
    def unused_resource(self) -> int:
        return self._task.unused_resource
        
    @unused_resource.setter
    def unused_resource(self, value: int) -> None:
        self._task.unused_resource = value
        
    @property
    def search_wait_time(self) -> float:
        return self._task.search_wait_time
        
    @search_wait_time.setter
    def search_wait_time(self, value: float) -> None:
        self._task.search_wait_time = value
        
    @property
    def proceeding_graphic_id(self) -> int:
        return self._task.proceed_sprite_id
        
    @proceeding_graphic_id.setter
    def proceeding_graphic_id(self, value: int) -> None:
        self._task.proceed_sprite_id = value
        
    @property
    def resource_gather_sound_id(self) -> int:
        return self._task.resource_gather_sound_id
        
    @resource_gather_sound_id.setter
    def resource_gather_sound_id(self, value: int) -> None:
        self._task.resource_gather_sound_id = value
        
    @property
    def resource_deposit_sound_id(self) -> int:
        return self._task.resource_deposit_sound_id
        
    @resource_deposit_sound_id.setter
    def resource_deposit_sound_id(self, value: int) -> None:
        self._task.resource_deposit_sound_id = value
    
    @property
    def gather_type(self) -> int:
        return self._task.gather_type
        
    @gather_type.setter
    def gather_type(self, value: int) -> None:
        self._task.gather_type = value
        
    @property
    def work_mode(self) -> int:
        return self._task.work_mode
        
    @work_mode.setter
    def work_mode(self, value: int) -> None:
        self._task.work_mode = value
    
    @property
    def enable_targeting(self) -> int:
        return self._task.enable_targeting
        
    @enable_targeting.setter
    def enable_targeting(self, value: int) -> None:
        self._task.enable_targeting = value

    @property
    def enabled(self) -> int:
        return 1

    @enabled.setter
    def enabled(self, value: int) -> None:
        pass

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
    Wrapper for a DamageClass (attack) with its index.
    """

    __slots__ = ("_attack", "_attack_id")

    def __init__(self, attack: "DamageClass", attack_id: int) -> None:
        object.__setattr__(self, "_attack", attack)
        object.__setattr__(self, "_attack_id", attack_id)

    def __repr__(self) -> str:
        cls = getattr(self._attack, 'id', -1)
        amount = getattr(self._attack, 'amount', 0)
        return f"AttackHandle(attack_id={self._attack_id}, class_={cls}, amount={amount})"

    @property
    def attack_id(self) -> int:
        """Index of this attack in the parent's list."""
        return self._attack_id

    @property
    def class_(self) -> int:
        """Attack class (damage type)."""
        return self._attack.id

    @class_.setter
    def class_(self, value: int) -> None:
        self._attack.id = value

    @property
    def id(self) -> int:
        """Attack class (damage type) - same as class_."""
        return self._attack.id

    @id.setter
    def id(self, value: int) -> None:
        self._attack.id = value

    @property
    def amount(self) -> int:
        """Attack amount (damage)."""
        return self._attack.amount

    @amount.setter
    def amount(self, value: int) -> None:
        self._attack.amount = value


class ArmourHandle:
    """
    Wrapper for a DamageClass (armour) with its index.
    """

    __slots__ = ("_armour", "_armour_id")

    def __init__(self, armour: "DamageClass", armour_id: int) -> None:
        object.__setattr__(self, "_armour", armour)
        object.__setattr__(self, "_armour_id", armour_id)

    def __repr__(self) -> str:
        cls = getattr(self._armour, 'id', -1)
        amount = getattr(self._armour, 'amount', 0)
        return f"ArmourHandle(armour_id={self._armour_id}, class_={cls}, amount={amount})"

    @property
    def armour_id(self) -> int:
        """Index of this armour in the parent's list."""
        return self._armour_id

    @property
    def class_(self) -> int:
        """Armour class (defense type)."""
        return self._armour.id

    @class_.setter
    def class_(self, value: int) -> None:
        self._armour.id = value

    @property
    def id(self) -> int:
        """Armour class (defense type) - same as class_."""
        return self._armour.id

    @id.setter
    def id(self, value: int) -> None:
        self._armour.id = value

    @property
    def amount(self) -> int:
        """Armour amount (defense)."""
        return self._armour.amount

    @amount.setter
    def amount(self, value: int) -> None:
        self._armour.amount = value


class DamageGraphicHandle:
    """
    Wrapper for a UnitDamageSprite with its index.
    """

    __slots__ = ("_damage_graphic", "_damage_graphic_id")

    def __init__(self, damage_graphic: "UnitDamageSprite", damage_graphic_id: int) -> None:
        object.__setattr__(self, "_damage_graphic", damage_graphic)
        object.__setattr__(self, "_damage_graphic_id", damage_graphic_id)

    def __repr__(self) -> str:
        gfx_id = getattr(self._damage_graphic, 'sprite_id', -1)
        return f"DamageGraphicHandle(id={self._damage_graphic_id}, sprite_id={gfx_id})"

    @property
    def damage_graphic_id(self) -> int:
        """Index of this damage graphic in the parent's list."""
        return self._damage_graphic_id

    @property
    def sprite_id(self) -> int:
        """Sprite ID to display."""
        return self._damage_graphic.sprite_id

    @sprite_id.setter
    def sprite_id(self, value: int) -> None:
        self._damage_graphic.sprite_id = value

    @property
    def graphic_id(self) -> int:
        """Alias for sprite_id."""
        return self.sprite_id

    @graphic_id.setter
    def graphic_id(self, value: int) -> None:
        self.sprite_id = value

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

    def __init__(self, train_location: "TrainLocation", train_location_id: int) -> None:
        object.__setattr__(self, "_train_location", train_location)
        object.__setattr__(self, "_train_location_id", train_location_id)

    def __repr__(self) -> str:
        uid = getattr(self._train_location, 'unit_id', -1)
        return f"TrainLocationHandle(id={self._train_location_id}, unit_id={uid})"

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
        return self._train_location.location_unit_id

    @unit_id.setter
    def unit_id(self, value: int) -> None:
        self._train_location.location_unit_id = value

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
        return self._train_location.hotkey_id

    @hot_key_id.setter
    def hot_key_id(self, value: int) -> None:
        self._train_location.hotkey_id = value


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


class BuildingAnnexHandle:
    """
    Wrapper for a BuildingAnnex with its index.
    """

    __slots__ = ("_annex", "_annex_id")

    def __init__(self, annex: Any, annex_id: int) -> None:
        object.__setattr__(self, "_annex", annex)
        object.__setattr__(self, "_annex_id", annex_id)

    def __repr__(self) -> str:
        uid = getattr(self._annex, 'unit_id', -1)
        return f"BuildingAnnexHandle(id={self._annex_id}, unit_id={uid})"

    @property
    def index(self) -> int:
        """Index of this annex (0-3)."""
        return self._annex_id

    @property
    def unit_id(self) -> int:
        """Annex unit ID."""
        return self._annex.unit_id

    @unit_id.setter
    def unit_id(self, value: int) -> None:
        self._annex.unit_id = value

    @property
    def displacement_x(self) -> float:
        """X offset."""
        return self._annex.displacement_x

    @displacement_x.setter
    def displacement_x(self, value: float) -> None:
        self._annex.displacement_x = value

    @property
    def displacement_y(self) -> float:
        """Y offset."""
        return self._annex.displacement_y

    @displacement_y.setter
    def displacement_y(self, value: float) -> None:
        self._annex.displacement_y = value

    @property
    def misplacement_x(self) -> float:
        """Alias for displacement_x."""
        return self.displacement_x

    @misplacement_x.setter
    def misplacement_x(self, value: float) -> None:
        self.displacement_x = value

    @property
    def misplacement_y(self) -> float:
        """Alias for displacement_y."""
        return self.displacement_y

    @misplacement_y.setter
    def misplacement_y(self, value: float) -> None:
        self.displacement_y = value


class CostHandle:
    """
    Wrapper for a UnitCost with its index.
    """

    __slots__ = ("_cost", "_cost_id")

    def __init__(self, cost: Any, cost_id: int) -> None:
        object.__setattr__(self, "_cost", cost)
        object.__setattr__(self, "_cost_id", cost_id)

    def __repr__(self) -> str:
        rid = getattr(self._cost, 'resource_id', -1)
        qty = getattr(self._cost, 'quantity', 0)
        return f"CostHandle(id={self._cost_id}, resource_id={rid}, quantity={qty})"

    @property
    def index(self) -> int:
        return self._cost_id

    @property
    def resource_id(self) -> int:
        return self._cost.resource_id

    @resource_id.setter
    def resource_id(self, value: int) -> None:
        self._cost.resource_id = value

    @property
    def quantity(self) -> int:
        return self._cost.quantity

    @quantity.setter
    def quantity(self, value: int) -> None:
        self._cost.quantity = value

    @property
    def deduct_flag(self) -> int:
        return self._cost.deduct_flag

    @deduct_flag.setter
    def deduct_flag(self, value: int) -> None:
        self._cost.deduct_flag = value


class ResourceHandle:
    """
    Wrapper for a UnitResource with its index.
    """

    __slots__ = ("_resource", "_resource_id")

    def __init__(self, resource: Any, resource_id: int) -> None:
        object.__setattr__(self, "_resource", resource)
        object.__setattr__(self, "_resource_id", resource_id)

    def __repr__(self) -> str:
        rtype = getattr(self._resource, 'type', -1)
        qty = getattr(self._resource, 'quantity', 0.0)
        return f"ResourceHandle(id={self._resource_id}, type={rtype}, quantity={qty})"

    @property
    def index(self) -> int:
        return self._resource_id

    @property
    def type(self) -> int:
        return self._resource.type

    @type.setter
    def type(self, value: int) -> None:
        self._resource.type = value

    @property
    def quantity(self) -> float:
        return self._resource.quantity

    @quantity.setter
    def quantity(self, value: float) -> None:
        self._resource.quantity = value

    @property
    def store_mode(self) -> int:
        return self._resource.store_mode

    @store_mode.setter
    def store_mode(self, value: int) -> None:
        self._resource.store_mode = value

    @property
    def flag(self) -> int:
        """Alias for store_mode."""
        return self.store_mode

    @flag.setter
    def flag(self, value: int) -> None:
        self.store_mode = value
