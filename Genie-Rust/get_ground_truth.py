import sys
import os

# Add the parent directory to path so we can import genieutils
sys.path.append(os.path.dirname(os.getcwd()))

from genieutils.datfile import DatFile

DAT_FILE = r""

def get_truth():
    print(f"Loading {DAT_FILE} with genieutils-py...")
    try:
        df = DatFile.parse(DAT_FILE)
        print("Successfully loaded!")
        print(f"Version: {df.version}")
        print(f"Terrain Restriction Size: {len(df.terrain_restrictions)}")
        if df.terrain_restrictions:
            print(f"Terrains Used: {len(df.terrain_restrictions[0].passable_buildable_dmg_multiplier)}")
        print(f"Player Color Size: {len(df.player_colours)}")
        print(f"Sound Size: {len(df.sounds)}")
        print(f"Graphic Size: {len(df.graphics)}")
        print(f"Effect Size: {len(df.effects)}")
        print(f"Civ Size: {len(df.civs)}")
        print(f"Tech Size: {len(df.techs)}")
    except Exception as e:
        print(f"Failed to load: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    get_truth()
