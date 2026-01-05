"""
TasksWrapper - Task collection management wrapper for Bird units.

Provides methods to manage unit tasks (commands):
- add_task: Add a new task with all parameters
- copy_task: Copy an existing task by ID
- get_task: Retrieve a task by ID
- remove_task: Remove a task by ID

Mirrors genieutils.task.Task structure.
"""
from __future__ import annotations

import copy
from typing import TYPE_CHECKING, Any, List, Optional

if TYPE_CHECKING:
    # TODO: Removed genie-rust dependency - needs migration to GenieDatParser
    # from genie_rust import Unit
    # from genie_rust import Task as GenieTask
    pass
    from Datasets.tasks import Task
    from Datasets.task_attributes import TargetDiplomacy
    from Datasets.resources import Resource

__all__ = ["TasksWrapper"]


class TasksWrapper:
    """
    Wrapper for managing Bird.tasks collection.

    Provides methods to add, copy, and manipulate tasks.
    Changes propagate to all units in the provided list.
    """

    __slots__ = ("_units",)

    def __init__(self, units: List[Unit]) -> None:
        object.__setattr__(self, "_units", units)

    def _get_bird(self) -> Optional[Any]:
        """Get Bird from first unit."""
        if self._units and self._units[0].bird:
            return self._units[0].bird
        return None

    def add_task(
        self,
        task_type: int | Task = 0,
        id: int = -1,
        is_default: int = 0,
        action_type: int = 0,
        class_id: int = -1,
        unit_id: int = -1,
        terrain_id: int = -1,
        resource_in: int | Resource = -1,
        resource_multiplier: int = -1,
        resource_out: int | Resource = -1,
        unused_resource: int | Resource = -1,
        work_value_1: float = 0.0,
        work_value_2: float = 0.0,
        work_range: float = 0.0,
        auto_search_targets: int = 0,
        search_wait_time: float = 0.0,
        enable_targeting: int = 0,
        combat_level_flag: int = 0,
        gather_type: int = 0,
        work_flag_2: int = 0,
        target_diplomacy: int | TargetDiplomacy = -1,
        carry_check: int = 0,
        pick_for_construction: int = 0,
        moving_graphic_id: int = -1,
        proceeding_graphic_id: int = -1,
        working_graphic_id: int = -1,
        carrying_graphic_id: int = -1,
        resource_gathering_sound_id: int = -1,
        resource_deposit_sound_id: int = -1,
        wwise_resource_gathering_sound_id: int = 0,
        wwise_resource_deposit_sound_id: int = 0,
        enabled: int = 1,
    ) -> None:
        """
        Add a new task to all units.

        Creates a new Task object with the specified parameters and adds it
        to the Bird.tasks list for all units.

        Args:
            task_type: Task type ID (use Datasets.tasks.Task)
            id: Task ID
            is_default: Whether this is the default task (0 or 1)
            action_type: Action type ID
            class_id: Target class ID
            unit_id: Target unit ID
            terrain_id: Target terrain ID
            resource_in: Input resource type
            resource_multiplier: Resource gather multiplier
            resource_out: Output resource type
            unused_resource: Unused resource field
            work_value_1: Work value 1
            work_value_2: Work value 2
            work_range: Work range
            auto_search_targets: Auto search for targets flag
            search_wait_time: Search wait time
            enable_targeting: Enable targeting flag
            combat_level_flag: Combat level flag
            gather_type: Gather type
            work_flag_2: Work flag 2
            target_diplomacy: Target diplomacy stance (use Datasets.task_attributes.TargetDiplomacy)
            carry_check: Carry check flag
            pick_for_construction: Pick for construction flag
            moving_graphic_id: Moving graphic ID
            proceeding_graphic_id: Proceeding graphic ID
            working_graphic_id: Working graphic ID
            carrying_graphic_id: Carrying graphic ID
            resource_gathering_sound_id: Resource gathering sound ID
            resource_deposit_sound_id: Resource deposit sound ID
            wwise_resource_gathering_sound_id: Wwise resource gathering sound ID
            wwise_resource_deposit_sound_id: Wwise resource deposit sound ID
            enabled: Whether task is enabled
        """
        # TODO: Removed genie-rust dependency - needs migration to GenieDatParser\n        # from genie_rust import Task\n        pass

        new_task = Task(
            task_type=task_type,
            id=id,
            is_default=is_default,
            action_type=action_type,
            class_id=class_id,
            unit_id=unit_id,
            terrain_id=terrain_id,
            resource_in=resource_in,
            resource_multiplier=resource_multiplier,
            resource_out=resource_out,
            unused_resource=unused_resource,
            work_value_1=work_value_1,
            work_value_2=work_value_2,
            work_range=work_range,
            auto_search_targets=auto_search_targets,
            search_wait_time=search_wait_time,
            enable_targeting=enable_targeting,
            combat_level_flag=combat_level_flag,
            gather_type=gather_type,
            work_flag_2=work_flag_2,
            target_diplomacy=target_diplomacy,
            carry_check=carry_check,
            pick_for_construction=pick_for_construction,
            moving_graphic_id=moving_graphic_id,
            proceeding_graphic_id=proceeding_graphic_id,
            working_graphic_id=working_graphic_id,
            carrying_graphic_id=carrying_graphic_id,
            resource_gathering_sound_id=resource_gathering_sound_id,
            resource_deposit_sound_id=resource_deposit_sound_id,
            wwise_resource_gathering_sound_id=wwise_resource_gathering_sound_id,
            wwise_resource_deposit_sound_id=wwise_resource_deposit_sound_id,
            enabled=enabled,
        )

        for unit in self._units:
            if unit.bird:
                unit.bird.tasks.append(copy.deepcopy(new_task))

    def copy_task(self, task_id: int) -> None:
        """
        Copy an existing task by ID and append it.

        Args:
            task_id: ID of the task to copy

        Raises:
            ValueError: If task with specified ID not found
        """
        bird = self._get_bird()
        if not bird:
            raise ValueError("Unit does not have Bird component")

        # Find task to copy
        task_to_copy = None
        for task in bird.tasks:
            if task.id == task_id:
                task_to_copy = task
                break

        if task_to_copy is None:
            raise ValueError(f"Task with ID {task_id} not found")

        # Copy to all units
        for unit in self._units:
            if unit.bird:
                unit.bird.tasks.append(copy.deepcopy(task_to_copy))

    def get_task(self, task_id: int) -> Optional[GenieTask]:
        """
        Get a task by ID from the primary unit.

        Args:
            task_id: ID of the task to retrieve

        Returns:
            Task object if found, None otherwise
        """
        bird = self._get_bird()
        if bird:
            for task in bird.tasks:
                if task.id == task_id:
                    return task
        return None

    def remove_task(self, task_id: int) -> bool:
        """
        Remove a task by ID from all units.

        Args:
            task_id: ID of the task to remove

        Returns:
            True if task was found and removed, False otherwise
        """
        found = False
        for unit in self._units:
            if unit.bird:
                original_len = len(unit.bird.tasks)
                unit.bird.tasks = [t for t in unit.bird.tasks if t.id != task_id]
                if len(unit.bird.tasks) < original_len:
                    found = True
        return found

    def list_tasks(self) -> List[GenieTask]:
        """
        Get all tasks from the primary unit.

        Returns:
            List of Task objects
        """
        bird = self._get_bird()
        return list(bird.tasks) if bird else []

    def clear_tasks(self) -> None:
        """Remove all tasks from all units."""
        for unit in self._units:
            if unit.bird:
                unit.bird.tasks.clear()
