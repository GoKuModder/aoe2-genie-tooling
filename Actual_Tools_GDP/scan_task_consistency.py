"""
Scan for units where task_info exists on Gaia but is missing on Civ 1.
"""
import sys
from pathlib import Path

lib_path = Path(r"c:\AoE2DE Modding\Code\1 GenieUtils Python Tools  Library")
sys.path.insert(0, str(lib_path))
sys.path.insert(0, str(lib_path / "GenieDatParser" / "src"))

from Actual_Tools_GDP.Base.workspace import GenieWorkspace

SOURCE_DAT = Path(r"C:\Program Files (x86)\Steam\steamapps\common\AoE2DE\resources\_common\dat\empires2_x2_p1.dat")
ws = GenieWorkspace.load(str(SOURCE_DAT))

civs = ws.dat.civilizations
gaia = civs[0]
civ1 = civs[1]

print(f"Scanning {len(gaia.units)} units...")

count = 0
for i in range(len(gaia.units)):
    u_gaia = gaia.units[i]
    if not u_gaia: continue
    
    if i < len(civ1.units):
        u_civ1 = civ1.units[i]
        if not u_civ1: continue
        
        has_gaia = hasattr(u_gaia, 'task_info') and bool(u_gaia.task_info)
        has_civ1 = hasattr(u_civ1, 'task_info') and bool(u_civ1.task_info)
        
        if has_gaia and not has_civ1:
            print(f"Unit {i} ({u_gaia.name}): Gaia Has Tasks, Civ1 MISSING Tasks")
            count += 1
            if count > 10: break

print(f"Found {count} inconsistent units.")
