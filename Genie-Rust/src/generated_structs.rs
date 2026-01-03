use pyo3::prelude::*;
use serde::{Serialize, Deserialize};
use byteorder::{ReadBytesExt, LittleEndian};
use std::io::{Read, Seek};

#[pyclass]
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct AttackOrArmor {
    #[pyo3(get, set)] pub class_: i16,
    #[pyo3(get, set)] pub amount: i16,
}

impl AttackOrArmor {
    pub fn read_from<R: Read + Seek>(reader: &mut R) -> std::io::Result<Self> {
        Ok(Self {
            class_: reader.read_i16::<LittleEndian>()?,
            amount: reader.read_i16::<LittleEndian>()?,
        })
    }
}

#[pyclass]
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct BuildingAnnex {
    #[pyo3(get, set)] pub unit_id: i16,
    #[pyo3(get, set)] pub misplacement_x: f32,
    #[pyo3(get, set)] pub misplacement_y: f32,
}

impl BuildingAnnex {
    pub fn read_from<R: Read + Seek>(reader: &mut R) -> std::io::Result<Self> {
        Ok(Self {
            unit_id: reader.read_i16::<LittleEndian>()?,
            misplacement_x: reader.read_f32::<LittleEndian>()?,
            misplacement_y: reader.read_f32::<LittleEndian>()?,
        })
    }
}

#[pyclass]
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct ResourceCost {
    #[pyo3(get, set)] pub type_: i16,
    #[pyo3(get, set)] pub amount: i16,
    #[pyo3(get, set)] pub flag: i16,
}

impl ResourceCost {
    pub fn read_from<R: Read + Seek>(reader: &mut R) -> std::io::Result<Self> {
        Ok(Self {
            type_: reader.read_i16::<LittleEndian>()?,
            amount: reader.read_i16::<LittleEndian>()?,
            flag: reader.read_i16::<LittleEndian>()?,
        })
    }
}

#[pyclass]
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct ResourceStorage {
    #[pyo3(get, set)] pub type_: i16,
    #[pyo3(get, set)] pub amount: f32,
    #[pyo3(get, set)] pub flag: i8,
}

impl ResourceStorage {
    pub fn read_from<R: Read + Seek>(reader: &mut R) -> std::io::Result<Self> {
        Ok(Self {
            type_: reader.read_i16::<LittleEndian>()?,
            amount: reader.read_f32::<LittleEndian>()?,
            flag: reader.read_i8()?,
        })
    }
}

#[pyclass]
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct TrainLocation {
    #[pyo3(get, set)] pub train_time: i16,
    #[pyo3(get, set)] pub unit_id: i16,
    #[pyo3(get, set)] pub button_id: i8,
    #[pyo3(get, set)] pub hot_key_id: i32,
}

impl TrainLocation {
    pub fn read_from<R: Read + Seek>(reader: &mut R, version: &str) -> std::io::Result<Self> {
        let train_time = reader.read_i16::<LittleEndian>()?;
        let unit_id = reader.read_i16::<LittleEndian>()?;
        let button_id = reader.read_i8()?;
        let hot_key_id = if version >= "VER 8.8" {
            reader.read_i32::<LittleEndian>()?
        } else {
            16000
        };
        Ok(Self {
            train_time,
            unit_id,
            button_id,
            hot_key_id,
        })
    }
}
