"""Quick test to verify GenieDatParser works."""
import sys
sys.path.insert(0, "GenieDatParser/src")

from sections.datfile_sections import DatFile

DAT_FILE = r"F:\Games\AOE II DE Scirpting Python Projects\1 GenieUtils Python Tools  Library\empires2_x2_p1.dat"

def main():
    print("Loading with GenieDatParser...")
    dat = DatFile.from_file(DAT_FILE)
    
    print(f"Version: {dat.file_version}")
    print(f"Civilizations: {len(dat.civilizations)}")
    print(f"Sprites: {len(dat.sprites)}")
    print(f"Sounds: {len(dat.sounds)}")
    print(f"Tech Effects: {len(dat.tech_effects)}")
    print(f"Techs: {len(dat.techs)}")
    
    if len(dat.civilizations) > 0:
        civ = dat.civilizations[0]
        print(f"First Civ Name: {civ.name}")
        if len(civ.units) > 0:
            unit = next((u for u in civ.units if u is not None), None)
            if unit:
                print(f"First Unit Name: {unit.name}")
                print(f"First Unit HP: {unit.hit_points}")

if __name__ == "__main__":
    main()
