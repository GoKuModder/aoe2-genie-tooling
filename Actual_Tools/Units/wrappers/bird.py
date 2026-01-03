"""
BirdWrapper - Complete Bird/villager movement attribute wrapper for UnitHandle.

Provides flat property access to Bird attributes AND tasks collection management:
- default_task_id, search_radius, work_rate, drop_sites
- task_swap_group, attack_sound, move_sound
- wwise_attack_sound_id, wwise_move_sound_id, run_pattern
- tasks: TasksWrapper for managing task collection

Mirrors genieutils.unit.Bird structure.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, List, Optional

from Actual_Tools.Units.wrappers.tasks import TasksWrapper

if TYPE_CHECKING:
    from genieutils.unit import Unit
    from Datasets.tasks import Task

__all__ = ["BirdWrapper"]


class BirdWrapper:
    """
    Complete wrapper for Bird (bird/villager movement) attributes.
    
    Provides flat property access to bird-specific stats plus task management.
    Changes propagate to all units in the provided list.
    """
    
    __slots__ = ("_units", "_tasks")
    
    def __init__(self, units: List[Unit]) -> None:
        object.__setattr__(self, "_units", units)
        object.__setattr__(self, "_tasks", None)
    
    def _get_bird(self) -> Optional[Any]:
        """Get Bird from first unit."""
        if self._units and self._units[0].bird:
            return self._units[0].bird
        return None
    
    def _set_all(self, attr: str, value: Any) -> None:
        """Set attribute on all units' bird."""
        for unit in self._units:
            if unit.bird:
                setattr(unit.bird, attr, value)
    
    @property
    def tasks(self) -> TasksWrapper:
        """Access tasks collection."""
        if self._tasks is None:
            object.__setattr__(self, "_tasks", TasksWrapper(self._units))
        return self._tasks
    
    @property
    def default_task_id(self) -> int | Task:
        """Default task ID."""
        b = self._get_bird()
        return b.default_task_id if b else -1
    
    @default_task_id.setter
    def default_task_id(self, value: int | Task) -> None:
        self._set_all("default_task_id", value)
    
    @property
    def search_radius(self) -> float:
        """Search radius for resources."""
        b = self._get_bird()
        return b.search_radius if b else 0.0
    
    @search_radius.setter
    def search_radius(self, value: float) -> None:
        self._set_all("search_radius", value)
    
    @property
    def work_rate(self) -> float:
        """Work/gathering rate."""
        b = self._get_bird()
        return b.work_rate if b else 0.0
    
    @work_rate.setter
    def work_rate(self, value: float) -> None:
        self._set_all("work_rate", value)
    
    @property
    def drop_sites(self) -> list:
        """Drop site building IDs."""
        b = self._get_bird()
        return list(b.drop_sites) if b else []
    
    @drop_sites.setter
    def drop_sites(self, value: list) -> None:
        self._set_all("drop_sites", value)
    
    @property
    def task_swap_group(self) -> int:
        """Task swap group ID."""
        b = self._get_bird()
        return b.task_swap_group if b else 0
    
    @task_swap_group.setter
    def task_swap_group(self, value: int) -> None:
        self._set_all("task_swap_group", value)
    
    @property
    def attack_sound(self) -> int:
        """Attack sound ID."""
        b = self._get_bird()
        return b.attack_sound if b else -1
    
    @attack_sound.setter
    def attack_sound(self, value: int) -> None:
        self._set_all("attack_sound", value)
    
    @property
    def move_sound(self) -> int:
        """Move sound ID."""
        b = self._get_bird()
        return b.move_sound if b else -1
    
    @move_sound.setter
    def move_sound(self, value: int) -> None:
        self._set_all("move_sound", value)
    
    @property
    def wwise_attack_sound_id(self) -> int:
        """Wwise attack sound ID."""
        b = self._get_bird()
        return b.wwise_attack_sound_id if b else 0
    
    @wwise_attack_sound_id.setter
    def wwise_attack_sound_id(self, value: int) -> None:
        self._set_all("wwise_attack_sound_id", value)
    
    @property
    def wwise_move_sound_id(self) -> int:
        """Wwise move sound ID."""
        b = self._get_bird()
        return b.wwise_move_sound_id if b else 0
    
    @wwise_move_sound_id.setter
    def wwise_move_sound_id(self, value: int) -> None:
        self._set_all("wwise_move_sound_id", value)
    
    @property
    def run_pattern(self) -> int:
        """Run pattern mode."""
        b = self._get_bird()
        return b.run_pattern if b else 0
    
    @run_pattern.setter
    def run_pattern(self, value: int) -> None:
        self._set_all("run_pattern", value)
