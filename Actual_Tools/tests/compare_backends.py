import timeit
import os
import sys

# Ensure the root directory is in the Python path to find the backends
# This allows the script to be run from the 'Actual_Tools/tests' directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# --- Backend Imports ---
try:
    from genie_rust import DatFile as GenieDatParserDatFile
    GENIE_DAT_PARSER_AVAILABLE = True
except ImportError:
    try:
        # Fallback for when the rust module is not installed as genie_rust
        from sections.datfile_sections import DatFile as GenieDatParserDatFile
        GENIE_DAT_PARSER_AVAILABLE = True
    except ImportError:
        GENIE_DAT_PARSER_AVAILABLE = False


try:
    from genieutils.datfile import DatFile as GenieUtilsDatFile
    GENIE_UTILS_AVAILABLE = True
except ImportError:
    GENIE_UTILS_AVAILABLE = False

# --- Constants ---
TEST_DAT_FILE = "empires2_x2_p1_RUST_TEST.dat"
TEMP_SAVE_PATH_GDP = "temp_gdp_save.dat"
TEMP_SAVE_PATH_GU = "temp_gu_save.dat"
NUMBER_OF_RUNS = 10

# --- Benchmark Functions ---

def find_test_file():
    """Find the test DAT file, searching in common locations."""
    if os.path.exists(TEST_DAT_FILE):
        return TEST_DAT_FILE

    # Search in the root directory
    root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', TEST_DAT_FILE))
    if os.path.exists(root_path):
        return root_path

    # Search in the Datasets directory
    datasets_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'Datasets', TEST_DAT_FILE))
    if os.path.exists(datasets_path):
        return datasets_path

    return None

def benchmark_load_gdp(dat_file_path):
    """Benchmarks loading a DAT file with GenieDatParser."""
    if GENIE_DAT_PARSER_AVAILABLE:
        GenieDatParserDatFile.from_file(dat_file_path)

def benchmark_load_gu(dat_file_path):
    """Benchmarks loading a DAT file with genieutils-py."""
    if GENIE_UTILS_AVAILABLE:
        GenieUtilsDatFile(dat_file_path)

def benchmark_access_gdp(datfile):
    """Benchmarks basic data access with GenieDatParser."""
    # Accessing unit names as a simple access test
    for civ in datfile.civs:
        if civ and civ.units:
            for unit in civ.units:
                if unit:
                    _ = unit.name

def benchmark_access_gu(datfile):
    """Benchmarks basic data access with genieutils-py."""
    # Accessing unit names as a simple access test
    for civ in datfile.civs:
        if civ and civ.units:
            for unit in civ.units:
                if unit:
                    _ = unit.name


def benchmark_save_gdp(datfile):
    """Benchmarks saving a DAT file with GenieDatParser."""
    datfile.to_file(TEMP_SAVE_PATH_GDP)
    if os.path.exists(TEMP_SAVE_PATH_GDP):
        os.remove(TEMP_SAVE_PATH_GDP)


def benchmark_save_gu(datfile):
    """Benchmarks saving a DAT file with genieutils-py."""
    datfile.save(TEMP_SAVE_PATH_GU)
    if os.path.exists(TEMP_SAVE_PATH_GU):
        os.remove(TEMP_SAVE_PATH_GU)

# --- Main Execution ---

def run_benchmarks():
    """Runs all benchmarks and prints the results."""
    print("--- GenieDatParser vs. genieutils-py Benchmark ---")

    dat_file_path = find_test_file()

    if not dat_file_path:
        print(f"Error: Test file not found: '{TEST_DAT_FILE}'")
        return

    print(f"Using test file: {dat_file_path}")

    # Initialize times to avoid UnboundLocalError
    time_load_gdp, time_access_gdp, time_save_gdp = 0, 0, 0
    time_load_gu, time_access_gu, time_save_gu = 0, 0, 0

    if GENIE_DAT_PARSER_AVAILABLE:
        print("\n--- GenieDatParser ---")
        gdp_datfile = GenieDatParserDatFile.from_file(dat_file_path)

        time_load_gdp = timeit.timeit(lambda: benchmark_load_gdp(dat_file_path), number=NUMBER_OF_RUNS)
        print(f"Loading:  {time_load_gdp:.6f} seconds for {NUMBER_OF_RUNS} runs")

        time_access_gdp = timeit.timeit(lambda: benchmark_access_gdp(gdp_datfile), number=NUMBER_OF_RUNS)
        print(f"Access:   {time_access_gdp:.6f} seconds for {NUMBER_OF_RUNS} runs")

        time_save_gdp = timeit.timeit(lambda: benchmark_save_gdp(gdp_datfile), number=NUMBER_OF_RUNS)
        print(f"Saving:   {time_save_gdp:.6f} seconds for {NUMBER_OF_RUNS} runs")

    else:
        print("\nGenieDatParser not available. Skipping benchmarks.")

    if GENIE_UTILS_AVAILABLE:
        print("\n--- genieutils-py ---")
        gu_datfile = GenieUtilsDatFile(dat_file_path)

        time_load_gu = timeit.timeit(lambda: benchmark_load_gu(dat_file_path), number=NUMBER_OF_RUNS)
        print(f"Loading:  {time_load_gu:.6f} seconds for {NUMBER_OF_RUNS} runs")

        time_access_gu = timeit.timeit(lambda: benchmark_access_gu(gu_datfile), number=NUMBER_OF_RUNS)
        print(f"Access:   {time_access_gu:.6f} seconds for {NUMBER_OF_RUNS} runs")

        time_save_gu = timeit.timeit(lambda: benchmark_save_gu(gu_datfile), number=NUMBER_OF_RUNS)
        print(f"Saving:   {time_save_gu:.6f} seconds for {NUMBER_OF_RUNS} runs")
    else:
        print("\ngenieutils-py not available. Skipping benchmarks.")

    if GENIE_DAT_PARSER_AVAILABLE and GENIE_UTILS_AVAILABLE:
        print("\n--- Comparison (Factor by which GenieDatParser is faster) ---")
        if time_load_gdp > 0 and time_load_gu > 0:
            print(f"Loading:  {time_load_gu / time_load_gdp:.2f}x faster")
        if time_access_gdp > 0 and time_access_gu > 0:
            print(f"Access:   {time_access_gu / time_access_gdp:.2f}x faster")
        if time_save_gdp > 0 and time_save_gu > 0:
            print(f"Saving:   {time_save_gu / time_save_gdp:.2f}x faster")


if __name__ == "__main__":
    run_benchmarks()
