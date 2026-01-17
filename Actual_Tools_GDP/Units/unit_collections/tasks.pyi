"""
Type stubs for TasksManager - Provides IDE autocomplete.
"""
from typing import Iterator, Optional, List, Any
from Actual_Tools_GDP.Units.handles import TaskHandle


class TasksManager:
    """Manager for unit tasks across all civilizations."""
    
    def __init__(self, units: List[Any]) -> None: ...
    
    def __len__(self) -> int:
        """Number of tasks in the primary unit."""
        ...
    
    def __getitem__(self, index: int) -> TaskHandle:
        """Get TaskHandle by index (wrapping tasks from all civs at that index)."""
        ...
    
    def __iter__(self) -> Iterator[TaskHandle]:
        """Iterate over TaskHandles for all tasks."""
        ...
    
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
        """Add a new task to all units in the bundle."""
        ...
    
    def remove(self, index: int) -> bool:
        """Remove task at specified index from all units."""
        ...
    
    def clear(self) -> None:
        """Remove all tasks from all units."""
        ...
    
    def get_by_type(self, task_type: int) -> Optional[TaskHandle]:
        """Find the first task with the specified type in the primary unit."""
        ...
    
    def remove_by_action_type(self, action_type: int) -> int:
        """
        Remove all tasks with the specified action_type from all units.
        
        Args:
            action_type: The action type to filter tasks by (e.g., 101 for Build, 133 for Speed Charge).
            
        Returns:
            Number of tasks removed.
        """
        ...
