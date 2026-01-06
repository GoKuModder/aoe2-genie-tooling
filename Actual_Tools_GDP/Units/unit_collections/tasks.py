"""
TasksManager - Collection manager for unit tasks.

Ported from tasks_OLD.py and logic formerly in UnitHandle.
Manages the `task_info.tasks` collection across multiple units.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, List, Optional, Iterator

from Actual_Tools_GDP.Units.handles import TaskHandle
from sections.unit_data.unit_task import UnitTask

if TYPE_CHECKING:
    from sections.civilization.unit import Unit

__all__ = ["TasksManager"]


class TasksManager:
    """
    Manager for the tasks collection of a unit bundle.
    
    Provides list-like access to TaskHandle objects and collective 
    modification methods (add, remove, clear).
    """

    __slots__ = ("_units",)

    def __init__(self, units: List[Unit]) -> None:
        """
        Initialize with a list of units to manage.
        
        Args:
            units: List of Unit objects.
        """
        object.__setattr__(self, "_units", units)

    def _get_task_info(self) -> Optional[Any]:
        """Get task_info from the primary unit."""
        if self._units and hasattr(self._units[0], "task_info"):
            return self._units[0].task_info
        return None

    def __len__(self) -> int:
        """Number of tasks in the primary unit."""
        ti = self._get_task_info()
        return len(ti.tasks) if ti and ti.tasks else 0

    def __getitem__(self, index: int) -> TaskHandle:
        """Get TaskHandle by index."""
        ti = self._get_task_info()
        if ti and 0 <= index < len(ti.tasks):
            return TaskHandle(ti.tasks[index], index)
        raise IndexError(f"Task index {index} out of range (0-{len(self)-1})")

    def __iter__(self) -> Iterator[TaskHandle]:
        """Iterate over TaskHandles for all tasks."""
        for i in range(len(self)):
            yield self[i]

    def __repr__(self) -> str:
        return f"TasksManager(tasks={len(self)}, units={len(self._units)})"

    def add(
        self,
        task_type: int = 1,
        id: int = -1,
        is_default: bool = False,
        action_type: int = 0,
        unit_class_id: int = -1,
        unit_type: int = -1,
        terrain_type: int = -1,
        resource_in: int = -1,
        resource_out: int = -1,
        work_value1: float = 0.0,
        work_value2: float = 0.0,
        work_range: float = 0.0,
        **kwargs
    ) -> TaskHandle:
        """
        Add a new task to all units in the bundle.
        
        Args:
            task_type: Type of task.
            id: Task ID (-1 to auto-assign based on index).
            is_default: Whether this is the default task.
            action_type: Type of action.
            unit_class_id: Target class ID.
            unit_type: Target unit ID.
            terrain_type: Target terrain ID.
            resource_in: Input resource ID.
            resource_out: Output resource ID.
            work_value1: Primary work value (e.g. rate).
            work_value2: Secondary work value.
            work_range: Work range.
            **kwargs: Any other UnitTask attributes (class_id handles unit_class_id).

        Returns:
            TaskHandle for the new task in the primary unit.
        """
        # Alias handling for backward compatibility in kwargs
        if 'class_id' in kwargs:
            unit_class_id = kwargs.pop('class_id')
        if 'unit_id' in kwargs:
            unit_type = kwargs.pop('unit_id')
        if 'terrain_id' in kwargs:
            terrain_type = kwargs.pop('terrain_id')
        if 'work_value_1' in kwargs:
            work_value1 = kwargs.pop('work_value_1')
        if 'work_value_2' in kwargs:
            work_value2 = kwargs.pop('work_value_2')

        task_idx = -1
        for u in self._units:
            if hasattr(u, "task_info") and u.task_info:
                # Create with version from unit
                new_task = UnitTask(ver=u.ver)
                new_task.task_type = task_type
                new_task.id = id if id != -1 else len(u.task_info.tasks)
                new_task.is_default = is_default
                new_task.action_type = action_type
                new_task.unit_class_id = unit_class_id
                new_task.unit_type = unit_type
                new_task.terrain_type = terrain_type
                new_task.resource_in = resource_in
                new_task.resource_out = resource_out
                new_task.work_value1 = work_value1
                new_task.work_value2 = work_value2
                new_task.work_range = work_range
                
                # Apply extra attributes
                for key, val in kwargs.items():
                    if hasattr(new_task, key):
                        setattr(new_task, key, val)
                
                u.task_info.tasks.append(new_task)
                if task_idx == -1:
                    task_idx = len(u.task_info.tasks) - 1

        return self[task_idx]

    def remove(self, index: int) -> bool:
        """
        Remove task at specified index from all units.
        
        Args:
            index: Index of the task to remove.
            
        Returns:
            True if removed, False otherwise.
        """
        removed = False
        for u in self._units:
            if hasattr(u, "task_info") and u.task_info:
                if 0 <= index < len(u.task_info.tasks):
                    u.task_info.tasks.pop(index)
                    removed = True
        return removed

    def clear(self) -> None:
        """Remove all tasks from all units."""
        for u in self._units:
            if hasattr(u, "task_info") and u.task_info:
                u.task_info.tasks.clear()

    def get_by_type(self, task_type: int) -> Optional[TaskHandle]:
        """Find the first task with the specified type in the primary unit."""
        for i, handle in enumerate(self):
            if handle.task_type == task_type:
                return handle
        return None
