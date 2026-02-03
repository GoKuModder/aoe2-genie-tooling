"""
DropSitesManager - Collection manager for unit drop sites.

Manages the `task_info.drop_site_unit_ids` collection across multiple units.
Since drop sites are just unit IDs (integers), this wraps the integer list.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, List, Optional, Iterator

from aoe2_genie_tooling.Units.handles import DropSiteHandle

if TYPE_CHECKING:
    from sections.civilization.unit import Unit

__all__ = ["DropSitesManager"]


class DropSitesManager:
    """
    Manager for the drop sites collection (task_info.drop_site_unit_ids) of a unit bundle.
    """

    __slots__ = ("_units",)

    def __init__(self, units: List[Unit]) -> None:
        object.__setattr__(self, "_units", units)

    def _get_task_info(self) -> Optional[Any]:
        if self._units and hasattr(self._units[0], "task_info"):
            return self._units[0].task_info
        return None

    def __len__(self) -> int:
        ti = self._get_task_info()
        return len(ti.drop_site_unit_ids) if ti and ti.drop_site_unit_ids else 0

    def __getitem__(self, index: int) -> DropSiteHandle:
        ti = self._get_task_info()
        if ti and 0 <= index < len(ti.drop_site_unit_ids):
            return DropSiteHandle(ti.drop_site_unit_ids, index)
        raise IndexError(f"Drop site index {index} out of range (0-{len(self)-1})")

    def __iter__(self) -> Iterator[DropSiteHandle]:
        for i in range(len(self)):
            yield self[i]

    def add(self, unit_id: int) -> DropSiteHandle:
        """Add a drop site unit ID to all units.
        
        IMPORTANT: Uses setattr with a new list instead of append() because
        bfp_rs Retriever lists share internal storage across clones.
        """
        site_idx = -1
        for u in self._units:
            if hasattr(u, "task_info") and u.task_info:
                # CRITICAL: Don't use append()! bfp_rs lists share internal storage.
                current_sites = list(u.task_info.drop_site_unit_ids)
                current_sites.append(unit_id)
                u.task_info.drop_site_unit_ids = current_sites  # setattr triggers bfp_rs copy
                
                if site_idx == -1:
                    site_idx = len(u.task_info.drop_site_unit_ids) - 1
        
        return self[site_idx]

    def remove(self, index: int) -> bool:
        """Remove drop site at index from all units.
        
        IMPORTANT: Uses setattr with a new list instead of pop() because
        bfp_rs Retriever lists share internal storage across clones.
        """
        removed = False
        for u in self._units:
            if hasattr(u, "task_info") and u.task_info:
                current_sites = list(u.task_info.drop_site_unit_ids)
                if 0 <= index < len(current_sites):
                    current_sites.pop(index)
                    u.task_info.drop_site_unit_ids = current_sites  # setattr triggers bfp_rs copy
                    removed = True
        return removed

    def clear(self) -> None:
        """Clear all drop sites from all units.
        
        IMPORTANT: Uses setattr with empty list instead of clear() because
        bfp_rs Retriever lists share internal storage across clones.
        """
        for u in self._units:
            if hasattr(u, "task_info") and u.task_info:
                u.task_info.drop_site_unit_ids = []  # setattr triggers bfp_rs copy
