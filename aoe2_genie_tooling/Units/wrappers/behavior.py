"""
BehaviorWrapper - Unit behavior/action attribute wrapper for UnitHandle.

Ported from bird_OLD.py to work with GenieDatParser.

Provides flat property access to TaskInfo (behavior) attributes:
- default_task_id, search_radius, work_rate
- drop_site_unit_ids, task_swap_group
- attack_sound_id, move_sound_id
- wwise sound IDs, run_mode

Maps to GenieDatParser's TaskInfo structure.
Note: The tasks list itself is managed via collections/tasks.py (TasksManager + TaskHandle).
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, List, Optional

if TYPE_CHECKING:
    from sections.civilization.unit import Unit

__all__ = ["BehaviorWrapper"]


class BehaviorWrapper:
    """
    Wrapper for TaskInfo (unit behavior) attributes.

    Provides flat property access to behavior-related stats.
    Changes propagate to all units in the provided list.

    NOTE: This wrapper handles SCALAR properties of task_info.
    For managing the tasks LIST, use collections/tasks.py.

    Attributes from GenieDatParser TaskInfo:
        default_task_id, search_radius, work_rate,
        drop_site_unit_ids, task_swap_group,
        attack_sound_id, move_sound_id,
        wwise_attack_sound_id, wwise_move_sound_id,
        run_mode
    """

    __slots__ = ("_units",)

    def __init__(self, units: List["Unit"]) -> None:
        """
        Initialize with list of units to modify.

        Args:
            units: List of Unit objects to proxy
        """
        object.__setattr__(self, "_units", units)

    def _get_task_info(self) -> Optional[Any]:
        """Get TaskInfo from first unit."""
        if self._units and hasattr(self._units[0], "task_info") and self._units[0].task_info:
            return self._units[0].task_info
        return None

    def _set_all(self, attr: str, value: Any) -> None:
        """Set attribute on all units' task_info."""
        for unit in self._units:
            if hasattr(unit, "task_info") and unit.task_info:
                setattr(unit.task_info, attr, value)

    # -------------------------
    # Behavior Properties
    # -------------------------

    @property
    def default_task_id(self) -> int:
        """Default task ID."""
        ti = self._get_task_info()
        return ti.default_task_id if ti else -1

    @default_task_id.setter
    def default_task_id(self, value: int) -> None:
        self._set_all("default_task_id", value)

    @property
    def search_radius(self) -> float:
        """Search radius for resources/targets."""
        ti = self._get_task_info()
        return ti.search_radius if ti else 0.0

    @search_radius.setter
    def search_radius(self, value: float) -> None:
        self._set_all("search_radius", value)

    @property
    def work_rate(self) -> float:
        """Work/gathering rate."""
        ti = self._get_task_info()
        return ti.work_rate if ti else 0.0

    @work_rate.setter
    def work_rate(self, value: float) -> None:
        self._set_all("work_rate", value)

    @property
    def task_swap_group(self) -> int:
        """Task swap group."""
        ti = self._get_task_info()
        return ti.task_swap_group if ti else 0

    @task_swap_group.setter
    def task_swap_group(self, value: int) -> None:
        self._set_all("task_swap_group", value)

    @property
    def run_mode(self) -> int:
        """Run mode/pattern."""
        ti = self._get_task_info()
        return ti.run_mode if ti else 0

    @run_mode.setter
    def run_mode(self, value: int) -> None:
        self._set_all("run_mode", value)

    # Alias for backward compatibility
    @property
    def run_pattern(self) -> int:
        """Run pattern mode (alias for run_mode)."""
        return self.run_mode

    @run_pattern.setter
    def run_pattern(self, value: int) -> None:
        self.run_mode = value

    # -------------------------
    # Collections
    # -------------------------

    @property
    def tasks(self) -> "TasksManager":
        """Tasks collection manager."""
        from aoe2_genie_tooling.Units.unit_collections import TasksManager
        return TasksManager(self._units)

    @tasks.setter
    def tasks(self, value: List) -> None:
        """Set the entire tasks list for all units."""
        for u in self._units:
            if u.task_info:
                u.task_info.tasks = value

    @property
    def drop_sites(self) -> "DropSitesManager":
        """Drop sites collection manager."""
        from aoe2_genie_tooling.Units.unit_collections import DropSitesManager
        return DropSitesManager(self._units)

    @drop_sites.setter
    def drop_sites(self, value: List[int]) -> None:
        """Set the entire drop sites list for all units."""
        for u in self._units:
            if u.task_info:
                u.task_info.drop_site_unit_ids = value

    @property
    def drop_site_unit_ids(self) -> "DropSitesManager":
        """Alias for drop_sites."""
        return self.drop_sites

    # -------------------------
    # Sound Properties
    # -------------------------

    @property
    def attack_sound_id(self) -> int:
        """Attack sound ID."""
        ti = self._get_task_info()
        return ti.attack_sound_id if ti else -1

    @attack_sound_id.setter
    def attack_sound_id(self, value: int) -> None:
        self._set_all("attack_sound_id", value)

    # Alias for backward compatibility
    @property
    def attack_sound(self) -> int:
        """Attack sound ID (alias)."""
        return self.attack_sound_id

    @attack_sound.setter
    def attack_sound(self, value: int) -> None:
        self.attack_sound_id = value

    @property
    def move_sound_id(self) -> int:
        """Move sound ID."""
        ti = self._get_task_info()
        return ti.move_sound_id if ti else -1

    @move_sound_id.setter
    def move_sound_id(self, value: int) -> None:
        self._set_all("move_sound_id", value)

    # Alias for backward compatibility
    @property
    def move_sound(self) -> int:
        """Move sound ID (alias)."""
        return self.move_sound_id

    @move_sound.setter
    def move_sound(self, value: int) -> None:
        self.move_sound_id = value

    @property
    def wwise_attack_sound_id(self) -> int:
        """Wwise attack sound ID."""
        ti = self._get_task_info()
        return ti.wwise_attack_sound_id if ti else 0

    @wwise_attack_sound_id.setter
    def wwise_attack_sound_id(self, value: int) -> None:
        self._set_all("wwise_attack_sound_id", value)

    @property
    def wwise_move_sound_id(self) -> int:
        """Wwise move sound ID."""
        ti = self._get_task_info()
        return ti.wwise_move_sound_id if ti else 0

    @wwise_move_sound_id.setter
    def wwise_move_sound_id(self, value: int) -> None:
        self._set_all("wwise_move_sound_id", value)
