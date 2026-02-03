"""
Link Finder - Find connections between units above specified thresholds.

This module scans units and finds links (graphics, sounds, unit references)
that are above specified minimum IDs. Only connections above thresholds are reported.

Usage:
    from goku_tools.reverse_engineer.link_finder import LinkFinder
    
    finder = LinkFinder(
        workspace=ws,
        min_unit_id=2300,
        min_graphic_id=2500,
        min_sound_id=700
    )
    
    links = finder.find_links()
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Dict, List, Optional, Set, Tuple
from collections import defaultdict

if TYPE_CHECKING:
    from aoe2_genie_tooling.Base.workspace import GenieWorkspace

__all__ = ["LinkFinder", "UnitLinks", "LinkFinderConfig"]


@dataclass
class LinkFinderConfig:
    """Configuration for link finding thresholds."""
    min_unit_id: int = 0        # Only scan units >= this ID
    min_graphic_id: int = 0     # Only report graphic links >= this ID
    min_sound_id: int = 0       # Only report sound links >= this ID
    min_unit_ref_id: int = 0    # Only report unit ref links >= this ID (defaults to min_unit_id)
    
    def __post_init__(self):
        # If min_unit_ref_id not set, default to min_unit_id
        if self.min_unit_ref_id == 0 and self.min_unit_id > 0:
            self.min_unit_ref_id = self.min_unit_id


@dataclass
class UnitLinks:
    """Links found for a single unit."""
    unit_id: int
    name: str
    
    # Filtered links (only those above thresholds)
    graphics: List[int] = field(default_factory=list)
    sounds: List[int] = field(default_factory=list)
    unit_refs: List[int] = field(default_factory=list)
    
    @property
    def has_links(self) -> bool:
        """Check if this unit has any links above thresholds."""
        return bool(self.graphics or self.sounds or self.unit_refs)
    
    @property
    def total_links(self) -> int:
        """Total number of links found."""
        return len(self.graphics) + len(self.sounds) + len(self.unit_refs)


class LinkFinder:
    """
    Find connections/links between units above specified thresholds.
    
    Only reports links where the target ID is >= the corresponding threshold.
    E.g., if min_graphic_id=2500, a unit with standing_graphic=100 will NOT
    be reported, but a unit with standing_graphic=3000 WILL be reported.
    """
    
    def __init__(
        self,
        workspace: "GenieWorkspace",
        min_unit_id: int = 0,
        min_graphic_id: int = 0,
        min_sound_id: int = 0,
        min_unit_ref_id: Optional[int] = None
    ):
        """
        Initialize the link finder.
        
        Args:
            workspace: GenieWorkspace to scan
            min_unit_id: Only scan units with ID >= this value
            min_graphic_id: Only report graphic links >= this value
            min_sound_id: Only report sound links >= this value
            min_unit_ref_id: Only report unit ref links >= this value (defaults to min_unit_id)
        """
        self.ws = workspace
        self.config = LinkFinderConfig(
            min_unit_id=min_unit_id,
            min_graphic_id=min_graphic_id,
            min_sound_id=min_sound_id,
            min_unit_ref_id=min_unit_ref_id if min_unit_ref_id is not None else min_unit_id
        )
        
        # Load field metadata
        from aoe2_genie_tooling.Base.core.field_metadata import get_flat_fields
        self.unit_fields = get_flat_fields("units")
        
        # Categorize fields
        self.graphic_fields = [f for f, ref in self.unit_fields.items() if ref.target_type == "GraphicHandle"]
        self.sound_fields = [f for f, ref in self.unit_fields.items() if ref.target_type == "SoundHandle"]
        self.unit_ref_fields = [f for f, ref in self.unit_fields.items() if ref.target_type == "UnitHandle"]
    
    def _get_field_value(self, obj, field_name: str):
        """Get value from object, traversing dotted paths."""
        if "." in field_name:
            parts = field_name.split(".")
            current = obj
            for part in parts:
                try:
                    current = getattr(current, part, None)
                except Exception:
                    return None
                if current is None:
                    return None
            return current
        return getattr(obj, field_name, None)
    
    def _extract_scalar_ids(self, unit, field_names: List[str]) -> List[int]:
        """Extract scalar IDs from field list."""
        ids = []
        for field in field_names:
            val = self._get_field_value(unit, field)
            if isinstance(val, int) and val >= 0:
                ids.append(val)
        return ids
    
    def _extract_collection_ids(self, unit) -> Tuple[List[int], List[int], List[int]]:
        """Extract IDs from collection fields (tasks, damage_graphics, etc.)."""
        g_ids = []
        s_ids = []
        u_ids = []
        
        # Damage Graphics
        try:
            if unit.damage_graphics:
                for dg in unit.damage_graphics:
                    if hasattr(dg, 'graphic_id') and dg.graphic_id >= 0:
                        g_ids.append(dg.graphic_id)
        except Exception:
            pass
        
        # Tasks
        try:
            if unit.tasks:
                for t in unit.tasks:
                    # Graphics
                    for attr in ['proceeding_graphic_id', 'working_graphic_id', 'carrying_graphic_id']:
                        if hasattr(t, attr):
                            val = getattr(t, attr, -1)
                            if val >= 0:
                                g_ids.append(val)
                    # Sounds
                    for attr in ['resource_gather_sound_id', 'resource_deposit_sound_id']:
                        if hasattr(t, attr):
                            val = getattr(t, attr, -1)
                            if val >= 0:
                                s_ids.append(val)
        except Exception:
            pass
        
        # Train Locations
        try:
            if unit.train_locations:
                for tl in unit.train_locations:
                    if hasattr(tl, 'unit_id') and tl.unit_id >= 0:
                        u_ids.append(tl.unit_id)
        except Exception:
            pass
        
        # Annexes
        try:
            if unit.annexes:
                for a in unit.annexes:
                    if hasattr(a, 'unit_id') and a.unit_id >= 0:
                        u_ids.append(a.unit_id)
        except Exception:
            pass
        
        # Drop Sites
        try:
            if unit.drop_sites:
                for ds in unit.drop_sites:
                    if hasattr(ds, 'unit_id') and ds.unit_id >= 0:
                        u_ids.append(ds.unit_id)
        except Exception:
            pass
        
        return g_ids, s_ids, u_ids
    
    def _discover_graphic_deltas(self, graphic_id: int, visited: Set[int] = None) -> Set[int]:
        """
        Recursively discover all graphics linked via deltas.
        
        Args:
            graphic_id: Starting graphic ID
            visited: Set of already visited graphic IDs (to prevent cycles)
            
        Returns:
            Set of all graphic IDs reachable via delta links
        """
        if visited is None:
            visited = set()
        
        if graphic_id in visited or graphic_id < 0:
            return set()
        
        visited.add(graphic_id)
        result = {graphic_id}
        
        try:
            graphic = self.ws.graphic_manager.get(graphic_id)
            if graphic and hasattr(graphic, 'deltas'):
                for delta in graphic.deltas:
                    delta_gid = int(delta.graphic_id) if delta.graphic_id is not None else -1
                    if delta_gid >= 0 and delta_gid not in visited:
                        # Recursively discover delta-referenced graphics
                        result.update(self._discover_graphic_deltas(delta_gid, visited))
        except Exception:
            pass
        
        return result
    
    def discover_all_graphics(self) -> Set[int]:
        """
        Discover ALL graphics >= min_graphic_id in the workspace.
        Returns set of all graphic IDs above threshold.
        """
        result = set()
        min_gid = self.config.min_graphic_id
        
        try:
            sprites = self.ws.dat.sprites
            for i, sprite in enumerate(sprites):
                if sprite is not None and i >= min_gid:
                    result.add(i)
        except Exception:
            pass
        
        return result
    
    def discover_all_sounds(self) -> Set[int]:
        """
        Discover ALL sounds >= min_sound_id in the workspace.
        Returns set of all sound IDs above threshold.
        """
        result = set()
        min_sid = self.config.min_sound_id
        
        try:
            sounds = self.ws.dat.sounds
            for i, sound in enumerate(sounds):
                if sound is not None and i >= min_sid:
                    result.add(i)
        except Exception:
            pass
        
        return result
    
    def find_links_for_unit(self, unit_id: int) -> Optional[UnitLinks]:
        """
        Find all links for a single unit that are above thresholds.
        
        Returns None if unit doesn't exist or has no links above thresholds.
        """
        try:
            unit = self.ws.unit_manager.get(unit_id)
        except Exception:
            return None
            
        if unit is None or unit._primary_unit is None:
            return None
        
        name = getattr(unit, "name", f"Unit_{unit_id}")
        
        # Extract all IDs
        graphics = self._extract_scalar_ids(unit, self.graphic_fields)
        sounds = self._extract_scalar_ids(unit, self.sound_fields)
        unit_refs = self._extract_scalar_ids(unit, self.unit_ref_fields)
        
        # Add collection IDs
        col_g, col_s, col_u = self._extract_collection_ids(unit)
        graphics.extend(col_g)
        sounds.extend(col_s)
        unit_refs.extend(col_u)
        
        # Filter by thresholds - THIS IS THE KEY LOGIC
        filtered_graphics = [g for g in set(graphics) if g >= self.config.min_graphic_id]
        filtered_sounds = [s for s in set(sounds) if s >= self.config.min_sound_id]
        filtered_unit_refs = [u for u in set(unit_refs) if u >= self.config.min_unit_ref_id]
        
        links = UnitLinks(
            unit_id=unit_id,
            name=name,
            graphics=sorted(filtered_graphics),
            sounds=sorted(filtered_sounds),
            unit_refs=sorted(filtered_unit_refs)
        )
        
        return links if links.has_links else None
    
    def find_links(self) -> Dict[int, UnitLinks]:
        """
        Find all links for units above min_unit_id threshold.
        
        Returns dict of unit_id -> UnitLinks for units that have links above thresholds.
        """
        results = {}
        
        civ = self.ws.dat.civilizations[0]
        total_units = len(civ.units)
        
        for unit_id in range(self.config.min_unit_id, total_units):
            links = self.find_links_for_unit(unit_id)
            if links is not None:
                results[unit_id] = links
        
        return results
    
    def print_summary(self, results: Optional[Dict[int, UnitLinks]] = None):
        """Print a summary of found links."""
        if results is None:
            results = self.find_links()
        
        print(f"\n=== Link Finder Results ===")
        print(f"Config:")
        print(f"  min_unit_id:     {self.config.min_unit_id}")
        print(f"  min_graphic_id:  {self.config.min_graphic_id}")
        print(f"  min_sound_id:    {self.config.min_sound_id}")
        print(f"  min_unit_ref_id: {self.config.min_unit_ref_id}")
        print()
        
        print(f"Units with links above thresholds: {len(results)}")
        print()
        
        # Group by link type
        with_graphics = [u for u in results.values() if u.graphics]
        with_sounds = [u for u in results.values() if u.sounds]
        with_unit_refs = [u for u in results.values() if u.unit_refs]
        
        print(f"  With graphics links: {len(with_graphics)}")
        print(f"  With sound links:    {len(with_sounds)}")
        print(f"  With unit refs:      {len(with_unit_refs)}")
        print()
        
        # Show first 10 units with their links
        print("=== Sample Links (first 10) ===")
        for unit_id, links in list(results.items())[:10]:
            print(f"\n  {unit_id}: {links.name}")
            if links.graphics:
                print(f"    Graphics: {links.graphics}")
            if links.sounds:
                print(f"    Sounds: {links.sounds}")
            if links.unit_refs:
                print(f"    Unit Refs: {links.unit_refs}")


# Quick test runner
if __name__ == "__main__":
    import sys
    sys.path.insert(0, ".")
    from aoe2_genie_tooling.Base.workspace import GenieWorkspace
    
    # Example usage
    print("Loading workspace...")
    ws = GenieWorkspace.load("Testing/GoKu_RPG.dat")
    
    finder = LinkFinder(
        workspace=ws,
        min_unit_id=2300,
        min_graphic_id=15000,
        min_sound_id=700
    )
    
    results = finder.find_links()
    finder.print_summary(results)
