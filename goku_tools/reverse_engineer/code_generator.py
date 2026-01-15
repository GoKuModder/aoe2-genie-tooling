"""
RECodeGenerator V2 - Modularized Version

Generates Python code from units, graphics, and sounds in a .dat file.
This file is now a facade that delegates logic to the .generator subpackage.
"""
from __future__ import annotations
from pathlib import Path
from typing import TYPE_CHECKING, List, Dict, Optional, Tuple

# Import from our new modular structure
from .generator.models import UnitGroup, IndependentObjects
from .generator.discovery import discover_groups_and_independent, export_validation_json
from .generator.orchestrator import (
    create_folder_structure, 
    generate_group_code, 
    generate_master_module,
    generate_independent_code,
)

if TYPE_CHECKING:
    from Actual_Tools_GDP.Base.workspace import GenieWorkspace
    from goku_tools.reverse_engineer.link_finder import LinkFinder, UnitLinks

__all__ = ["RECodeGenerator", "UnitGroup", "IndependentObjects", "generate_from_dat"]


def generate_from_dat(
    dat_path: str,
    output_folder: str,
    min_unit_id: int = 0,
    min_graphic_id: int = 0,
    min_sound_id: int = 0,
    min_unit_ref_id: Optional[int] = None,
    export_json: bool = False,
) -> Tuple[List[UnitGroup], IndependentObjects]:
    """
    Convenience wrapper to load a DAT file, discover links, and emit Python code.

    Args:
        dat_path: Path to the DAT file to read.
        output_folder: Destination folder for generated Python modules.
        min_unit_id: Only scan units with IDs at or above this value.
        min_graphic_id: Treat graphics with IDs >= this value as linkable.
        min_sound_id: Treat sounds with IDs >= this value as linkable.
        min_unit_ref_id: Optional override for unit reference linking (defaults to min_unit_id).
        export_json: If True, export validation JSONs (relationship_graph.json, independent_objects.json).
    
    Returns:
        Tuple of (groups, independent_objects)
    """
    from Actual_Tools_GDP.Base.workspace import GenieWorkspace
    from goku_tools.reverse_engineer.link_finder import LinkFinder

    dat_path = Path(dat_path)
    output_folder = Path(output_folder)

    print(f"Loading workspace from {dat_path}...")
    ws = GenieWorkspace.load(str(dat_path))

    finder = LinkFinder(
        workspace=ws,
        min_unit_id=min_unit_id,
        min_graphic_id=min_graphic_id,
        min_sound_id=min_sound_id,
        min_unit_ref_id=min_unit_ref_id if min_unit_ref_id is not None else min_unit_id,
    )

    generator = RECodeGenerator(
        workspace=ws,
        folder_location=str(output_folder),
        link_finder=finder,
    )

    return generator.generate(export_json=export_json)


class RECodeGenerator:
    """
    Reverse Engineer Code Generator V2.
    
    Generates Python code for units, graphics, and sounds.
    Modularized to improve maintainability.
    """
    
    def __init__(
        self,
        workspace: "GenieWorkspace",
        folder_location: str,
        link_finder: "LinkFinder"
    ):
        self.ws = workspace
        self.folder_location = Path(folder_location)
        self.link_finder = link_finder
        
        self.link_results: Dict[int, "UnitLinks"] = {}
        self.groups: List[UnitGroup] = []
        self.independent: IndependentObjects = IndependentObjects()

    def generate(self, export_json: bool = False) -> Tuple[List[UnitGroup], IndependentObjects]:
        """
        Run the full generation pipeline.
        
        Args:
            export_json: If True, export validation JSONs.
        
        Returns:
            Tuple of (groups, independent_objects)
        """
        print(f"\n=== RECodeGenerator V2 (Modular) ===")
        print(f"Output folder: {self.folder_location}")
        
        # Step 1: Get link results
        print("\n[1] Finding links...")
        self.link_results = self.link_finder.find_links()
        print(f"    Found {len(self.link_results)} units with links")
        
        # Step 2: Discover groups and independent objects
        print("\n[2] Discovering groups and independent objects...")
        self.groups, self.independent = discover_groups_and_independent(
            self.ws, self.link_finder, self.link_results
        )
        print(f"    Found {len(self.groups)} groups")
        print(f"    Found {len(self.independent.unit_ids)} independent units")
        print(f"    Found {len(self.independent.graphic_ids)} independent graphics")
        print(f"    Found {len(self.independent.sound_ids)} independent sounds")
        
        # Step 3: Create folder structure
        print("\n[3] Creating folder structure...")
        create_folder_structure(self.folder_location, self.groups, self.independent)
        
        # Step 4: Generate code for each group
        print("\n[4] Generating code for groups...")
        for group in self.groups:
            generate_group_code(self.ws, group, self.folder_location, self.link_finder.config)
        
        # Step 5: Generate code for independent objects
        print("\n[5] Generating code for independent objects...")
        generate_independent_code(self.ws, self.independent, self.folder_location, self.link_finder.config)
        
        # Step 6: Generate master module
        print("\n[6] Generating master module...")
        generate_master_module(self.folder_location, self.groups, self.independent)
        
        # Step 7: Export validation JSONs (optional)
        if export_json:
            print("\n[7] Exporting validation JSONs...")
            export_validation_json(self.folder_location, self.groups, self.independent, self.ws)
        
        print(f"\n=== Done! Generated {len(self.groups)} groups + independent objects ===")
        return self.groups, self.independent


# Quick test runner
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate Python reconstruction code from an AoE2 DAT file."
    )
    parser.add_argument(
        "--dat",
        "-d",
        default="empires2_x2_p1.dat",
        help="Path to the DAT file to read",
    )
    parser.add_argument(
        "--output",
        "-o",
        default="output/goku_generated_v2refactored",
        help="Folder where generated modules will be written",
    )
    parser.add_argument(
        "--min-unit-id",
        type=int,
        default=0,
        help="Only scan units with IDs at/above this value",
    )
    parser.add_argument(
        "--min-graphic-id",
        type=int,
        default=0,
        help="Only link graphics with IDs at/above this value",
    )
    parser.add_argument(
        "--min-sound-id",
        type=int,
        default=0,
        help="Only link sounds with IDs at/above this value",
    )
    parser.add_argument(
        "--min-unit-ref-id",
        type=int,
        default=None,
        help="Optional override for unit ref linking (defaults to --min-unit-id)",
    )
    parser.add_argument(
        "--export-json",
        action="store_true",
        help="Export validation JSONs (relationship_graph.json, independent_objects.json)",
    )

    args = parser.parse_args()

    groups, independent = generate_from_dat(
        dat_path=args.dat,
        output_folder=args.output,
        min_unit_id=args.min_unit_id,
        min_graphic_id=args.min_graphic_id,
        min_sound_id=args.min_sound_id,
        min_unit_ref_id=args.min_unit_ref_id,
        export_json=args.export_json,
    )

    print(f"\n=== Summary ===")
    print(f"Generated {len(groups)} groups into {args.output}")
    print(f"Independent: {len(independent.unit_ids)} units, {len(independent.graphic_ids)} graphics, {len(independent.sound_ids)} sounds")
    for g in groups[:10]:
        print(
            f"- Group: {g.name} (Units: {len(g.unit_ids)}, Graphics: {len(g.graphic_ids)}, Sounds: {len(g.sound_ids)})"
        )
