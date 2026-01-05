#!/usr/bin/env python3
"""
Actual_Tools Demo with Colored Logging and JSON Registry

This script demonstrates:
1. Colored logging output showing what the library is doing
2. JSON registry export for communication with AoE2ScenarioParser
3. FLat attribute access on UnitHandle
4. Modular wrapper access (tasks, resource_storages)

Run with: python run_tools.py
"""
from __future__ import annotations

import sys
import zlib
from pathlib import Path

# Add paths for development
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
sys.path.insert(0, str(Path(__file__).parent.parent))

from Actual_Tools_GDP.Shared.dat_adapter import DatFile


# --- Monkeypatch DatFile.save to fix zlib issue ---
def patched_save(self, target_file: str) -> None:
    """Patched save method to fix zlib wbits issue."""
    uncompressed = self.to_bytes()
    compressobj = zlib.compressobj(level=-1, wbits=-15)
    compressed = compressobj.compress(uncompressed) + compressobj.flush()
    Path(target_file).write_bytes(compressed)

DatFile.save = patched_save
# --------------------------------------------------------


def main() -> int:
    """Run the demo."""
    from Actual_Tools import GenieWorkspace, registry
    
    # Paths
    script_dir = Path(__file__).parent
    input_dat = script_dir / "empires2_x2_p1.dat"
    output_dat = script_dir / "empires2_x2_p1_output.dat"
    registry_json = script_dir / "genie_edits.json"
    
    if not input_dat.exists():
        print(f"ERROR: Input DAT file not found: {input_dat}")
        return 1
    
    # ============================
    # Load
    # ============================
    workspace = GenieWorkspace.load(input_dat)
    
    # ============================
    # Create units with FLAT attribute access
    # ============================
    unit1 = workspace.units.create(
        name="Hero1",
        base_unit_id=4,
        unit_id=2900,
        on_conflict="overwrite",
    )
    # FLAT access - no nested .stats or .cost!
    unit1.hit_points = 500
    unit1.gold = 100
    
    # NEW: Resource Storages API
    unit1.resource_storages.RESOURCE_1(resource_type=0, amount=200.0, flag=1)
    unit1.resource_storages.set_storage(1, resource_type=1, amount=150.0, flag=1)
    
    # NEW: Damage Graphics API
    unit1.damage_graphics.add_damage_graphic(graphic_id=450, damage_percent=50)
    
    unit2 = workspace.units.create(
        name="Hero2",
        base_unit_id=83, # Villager (has tasks)
        unit_id=2901,
        on_conflict="overwrite",
    )
    
    # NEW: Tasks API (direct delegation)
    unit2.tasks.add_task(
        task_type=7,
        id=5,
        work_value_1=1.0, 
        enabled=1
    )
    
    # ============================
    # Create graphics (from scratch, no template)
    # ============================
    gfx1 = workspace.graphics.add_graphic("hero1_attack.slp")
    gfx2 = workspace.graphics.add_graphic("hero2_attack.slp")
    
    snd1 = workspace.sounds.add_sound("hero1_voice.wav")
    snd2 = workspace.sounds.add_sound("hero2_voice.wav")
    
    # Assign graphic to unit (flat access)
    unit1.attack_graphic = gfx1
    
    # ============================
    # Save DAT
    # ============================
    workspace.save(output_dat)
    
    # ============================
    # Save registry for ASP
    # ============================
    workspace.save_registry(registry_json)
    
    # ============================
    # Print timing summary
    # ============================
    workspace.print_summary()
    
    # ============================
    # Show registry contents
    # ============================
    print("\nRegistry JSON preview:")
    print(f"  {registry.summary()}")
    
    # Show a few entries
    if registry.units:
        print("\n  Units:")
        for u in registry.units[:3]:
            print(f"    {u['name']} → ID {u['id']}")
    
    print(f"\n✓ Registry saved to: {registry_json.name}")
    print(f"✓ Use this JSON file in AoE2ScenarioParser to reference created IDs")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
