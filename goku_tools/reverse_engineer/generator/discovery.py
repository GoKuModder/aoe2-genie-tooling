"""
Group discovery logic for RECodeGenerator.
"""
from __future__ import annotations
import json
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple
from .models import UnitGroup, IndependentObjects


def discover_groups_and_independent(
    ws: Any, link_finder: Any, link_results: Dict[int, Any]
) -> Tuple[List[UnitGroup], IndependentObjects]:
    """
    Discover groups of connected units, graphics, and sounds.
    Also identifies independent objects with no links to other above-threshold objects.
    
    Returns:
        Tuple of (groups, independent_objects)
    """
    adjacency: Dict[int, Set[int]] = defaultdict(set)
    min_unit_id = link_finder.config.min_unit_id
    
    # Build unit adjacency graph
    for unit_id, links in link_results.items():
        for ref_id in links.unit_refs:
            if ref_id >= min_unit_id:
                adjacency[unit_id].add(ref_id)
                adjacency[ref_id].add(unit_id)
    
    visited: Set[int] = set()
    groups: List[UnitGroup] = []
    independent = IndependentObjects()
    
    # Step 1: Discover unit-based groups (connected components)
    for unit_id in link_results.keys():
        if unit_id in visited:
            continue
        
        component: Set[int] = set()
        stack = [unit_id]
        
        while stack:
            current = stack.pop()
            if current in visited:
                continue
            visited.add(current)
            component.add(current)
            
            for neighbor in adjacency.get(current, []):
                if neighbor not in visited and neighbor in link_results:
                    stack.append(neighbor)
        
        if not component:
            continue
            
        first_id = min(component)
        first_links = link_results.get(first_id)
        name = first_links.name if first_links else f"Unit_{first_id}"
        
        # Collect graphics and sounds
        all_graphics: Set[int] = set()
        all_sounds: Set[int] = set()
        for uid in component:
            if uid in link_results:
                all_graphics.update(link_results[uid].graphics)
                all_sounds.update(link_results[uid].sounds)
        
        # Expand graphics via deltas
        expanded_graphics: Set[int] = set()
        for gid in all_graphics:
            expanded_graphics.update(
                link_finder._discover_graphic_deltas(gid)
            )
        # Filter to only graphics at or above threshold
        min_graphic_id = link_finder.config.min_graphic_id
        all_graphics = {gid for gid in expanded_graphics if gid >= min_graphic_id}
        
        # Check if this is a true group (has connections) or a single independent unit
        if len(component) == 1 and not all_graphics and not all_sounds:
            # Single unit with no graphics/sounds - independent
            independent.unit_ids.add(first_id)
        else:
            group = UnitGroup(
                name=name,
                unit_ids=component,
                graphic_ids=all_graphics,
                sound_ids=all_sounds
            )
            groups.append(group)
    
    # Step 2: Find standalone graphics and sounds
    all_discovered_graphics: Set[int] = set()
    all_discovered_sounds: Set[int] = set()
    for g in groups:
        all_discovered_graphics.update(g.graphic_ids)
        all_discovered_sounds.update(g.sound_ids)
    
    all_workspace_graphics = link_finder.discover_all_graphics()
    all_workspace_sounds = link_finder.discover_all_sounds()
    
    orphan_graphics = all_workspace_graphics - all_discovered_graphics
    orphan_sounds = all_workspace_sounds - all_discovered_sounds
    
    # Expand orphan graphics via deltas
    expanded_orphan_graphics: Set[int] = set()
    for gid in orphan_graphics:
        expanded_orphan_graphics.update(
            link_finder._discover_graphic_deltas(gid)
        )
    # Filter to only graphics at or above threshold
    min_graphic_id = link_finder.config.min_graphic_id
    orphan_graphics = {gid for gid in expanded_orphan_graphics if gid >= min_graphic_id}
    
    # Step 3: Classify orphan graphics - connected clusters = groups, singles = independent
    orphan_graphics_remaining = orphan_graphics.copy()
    while orphan_graphics_remaining:
        start_gid = min(orphan_graphics_remaining)
        connected = link_finder._discover_graphic_deltas(start_gid)
        connected_in_orphans = connected & orphan_graphics_remaining
        
        if len(connected_in_orphans) > 1:
            # Multiple connected graphics = group
            try:
                graphic = ws.graphic_manager.get(start_gid)
                name = getattr(graphic, "name", None)
                if not name or not name.strip():
                    name = f"Graphic_{start_gid}"
            except Exception:
                name = f"Graphic_{start_gid}"
            
            group = UnitGroup(
                name=name,
                unit_ids=set(),
                graphic_ids=connected_in_orphans,
                sound_ids=set()
            )
            groups.append(group)
        else:
            # Single graphic = independent
            independent.graphic_ids.update(connected_in_orphans)
        
        orphan_graphics_remaining -= connected_in_orphans
    
    # Step 4: All orphan sounds go to independent
    independent.sound_ids.update(orphan_sounds)
    
    # Sort groups
    def sort_key(g):
        if g.unit_ids:
            return (0, min(g.unit_ids))
        elif g.graphic_ids:
            return (1, min(g.graphic_ids))
        else:
            return (2, min(g.sound_ids) if g.sound_ids else 0)
    
    groups.sort(key=sort_key)
    return groups, independent


def discover_groups(ws: Any, link_finder: Any, link_results: Dict[int, Any]) -> List[UnitGroup]:
    """
    Legacy wrapper - returns only groups for backward compatibility.
    """
    groups, _ = discover_groups_and_independent(ws, link_finder, link_results)
    return groups


def export_validation_json(
    folder: Path, 
    groups: List[UnitGroup], 
    independent: IndependentObjects,
    ws: Any
) -> None:
    """
    Export validation JSONs for debugging.
    
    Creates:
        - relationship_graph.json: All groups with their objects and links
        - independent_objects.json: All standalone object IDs
    """
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    
    # Relationship graph
    relationship_graph = {
        "groups": []
    }
    for group in groups:
        group_data = {
            "group_id": group.folder_name,
            "name": group.name,
            "units": sorted(group.unit_ids),
            "graphics": sorted(group.graphic_ids),
            "sounds": sorted(group.sound_ids),
        }
        relationship_graph["groups"].append(group_data)
    
    (folder / "relationship_graph.json").write_text(
        json.dumps(relationship_graph, indent=2)
    )
    
    # Independent objects
    independent_data = {
        "units": sorted(independent.unit_ids),
        "graphics": sorted(independent.graphic_ids),
        "sounds": sorted(independent.sound_ids)
    }
    
    (folder / "independent_objects.json").write_text(
        json.dumps(independent_data, indent=2)
    )
