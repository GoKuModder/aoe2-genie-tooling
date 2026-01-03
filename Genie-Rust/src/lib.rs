pub mod generated_structs;
pub mod manual_structs;
pub mod datfile;

use pyo3::prelude::*;
use generated_structs::*;
use manual_structs::*;
use datfile::DatFile;

#[pymodule]
fn genie_rust(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<DatFile>()?;
    
    // Core Manual Structs
    m.add_class::<Unit>()?;
    m.add_class::<Civ>()?;
    m.add_class::<Graphic>()?;
    m.add_class::<Tech>()?;
    m.add_class::<Effect>()?;
    m.add_class::<TerrainRestriction>()?;
    m.add_class::<PlayerColour>()?;
    m.add_class::<Sound>()?;
    m.add_class::<UnitHeaders>()?;
    m.add_class::<TechTree>()?;
    
    // Sub-structs (Manual)
    m.add_class::<SoundItem>()?;
    m.add_class::<GraphicDelta>()?;
    m.add_class::<GraphicAngleSound>()?;
    m.add_class::<Type50>()?;
    m.add_class::<Projectile>()?;
    m.add_class::<Creatable>()?;
    m.add_class::<Building>()?;
    m.add_class::<DeadFish>()?;
    m.add_class::<Bird>()?;
    
    // Sub-structs (Generated)
    m.add_class::<AttackOrArmor>()?;
    m.add_class::<ResourceStorage>()?;
    m.add_class::<TrainLocation>()?;
    m.add_class::<ResourceCost>()?;
    m.add_class::<BuildingAnnex>()?;
    
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::path::Path;

    #[test]
    fn test_parse_file() {
        let path = Path::new("../empires2_x2_p1_RUST_TEST.dat");
        if !path.exists() {
            println!("Test file not found at {:?}, skipping test.", path);
            return;
        }

        println!("Parsing {:?}", path);
        // We can call DatFile::from_file via PyO3 wrapper, or better, access the rust method if exposed.
        // DatFile::from_file returns PyResult<Self>.
        // Since we are in rust test, we can just unwrap/expect.
        
        let result = DatFile::from_file(path.to_str().unwrap());
        match result {
            Ok(dat) => {
                println!("Version: {}", dat.version);
                println!("Civs: {}", dat.civs.len());
                assert_eq!(dat.version.trim(), "VER 8.8");
                assert_eq!(dat.civs.len(), 2);
                
                if let Some(Some(unit)) = dat.civs[0].units.first() {
                    println!("First Unit: {}", unit.name);
                }
            },
            Err(e) => {
                panic!("Failed to parse: {:?}", e);
            }
        }
    }
}
