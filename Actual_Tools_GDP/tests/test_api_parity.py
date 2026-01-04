import pytest
from pathlib import Path

from Actual_Tools import GenieWorkspace
from genieutils.datfile import DatFile as GenieDatFile

DAT_FILE_PATH = Path(__file__).resolve().parent.parent.parent / "empires2_x2_p1_RUST_TEST.dat"

# --- Fixtures ---

@pytest.fixture(scope="module")
def workspace() -> GenieWorkspace:
    """Loads the workspace once per test module using the test DAT file."""
    if not DAT_FILE_PATH.exists():
        pytest.fail(f"Test data file not found at: {DAT_FILE_PATH}")
    return GenieWorkspace.load(str(DAT_FILE_PATH))

@pytest.fixture(scope="module")
def genie_dat() -> GenieDatFile:
    """Loads the raw genieutils DatFile object once per test module."""
    return GenieDatFile.parse(str(DAT_FILE_PATH))

# --- Helper Functions ---

def get_public_attributes_from_object(obj: object) -> set[str]:
    """
    Returns a set of public, non-callable attributes of an object
    to compare the public data API surface.
    """
    return {
        name for name in dir(obj)
        if not name.startswith("_") and not callable(getattr(obj, name))
    }

# --- API Parity Tests ---

def test_unit_api_parity(workspace, genie_dat):
    """
    Verifies UnitHandle has the flattened attributes from genieutils.unit.Unit.
    """
    archer_id = 4  # Archer
    gdp_unit = workspace.genie_unit_manager().get(archer_id)

    gu_unit = next((c.units[archer_id] for c in genie_dat.civs if len(c.units) > archer_id and c.units[archer_id]), None)
    assert gu_unit is not None, f"Unit {archer_id} not found in genieutils test file."

    # These are attributes that are handled by wrappers or are intentionally different
    ignore_list = {
        'type_50', 'creatable', 'bird', 'building', 'dead_fish', 'projectile',
        'cost', 'tasks', 'resource_storages', 'attacks', 'armours',
        'train_locations_wrapper', 'unit_id'
    }

    # Test top-level attributes
    missing_attrs = []
    for attr in get_public_attributes_from_object(gu_unit):
        if attr not in ignore_list and not hasattr(gdp_unit, attr):
            missing_attrs.append(attr)
    assert not missing_attrs, f"UnitHandle is missing core attributes from genieutils.unit.Unit: {sorted(missing_attrs)}"

    # Test flattened attributes
    flattened_sources = {'type_50', 'creatable', 'bird', 'building', 'dead_fish', 'projectile'}
    missing_flattened_attrs = []
    for source_name in flattened_sources:
        source_obj = getattr(gu_unit, source_name)
        if source_obj:
            for attr in get_public_attributes_from_object(source_obj):
                if attr not in ignore_list and not hasattr(gdp_unit, attr):
                    missing_flattened_attrs.append(attr)
    assert not missing_flattened_attrs, f"UnitHandle is missing flattened attributes: {sorted(missing_flattened_attrs)}"

def test_civ_api_parity(workspace, genie_dat):
    """
    Verifies CivHandle has attributes matching genieutils.civ.Civ.
    """
    civ_id = 1  # Britons
    gdp_civ = workspace.civ_manager().get(civ_id)
    gu_civ = genie_dat.civs[civ_id]

    ignore_list = {'units', 'unit_pointers'}
    missing_attrs = []
    for attr in get_public_attributes_from_object(gu_civ):
        if attr not in ignore_list and not hasattr(gdp_civ, attr):
            missing_attrs.append(attr)
    assert not missing_attrs, f"CivHandle is missing attributes from genieutils.civ.Civ: {sorted(missing_attrs)}"

def test_tech_api_parity(workspace, genie_dat):
    """
    Verifies TechHandle has attributes matching genieutils.tech.Tech.
    """
    tech_id = 22  # Loom
    gdp_tech = workspace.tech_manager().get(tech_id)
    gu_tech = genie_dat.techs[tech_id]

    ignore_list = {'resource_costs', 'button_id'}
    missing_attrs = []
    for attr in get_public_attributes_from_object(gu_tech):
        if attr not in ignore_list and not hasattr(gdp_tech, attr):
            missing_attrs.append(attr)
    assert not missing_attrs, f"TechHandle is missing attributes from genieutils.tech.Tech: {sorted(missing_attrs)}"
