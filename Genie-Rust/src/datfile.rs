use pyo3::prelude::*;
use std::io::{Read, Seek, Cursor};
use std::fs::File;
use flate2::{Decompress, FlushDecompress};
use byteorder::{ReadBytesExt, LittleEndian};

use crate::generated_structs::*;
use crate::manual_structs::*;

#[pyclass]
#[derive(Clone, Debug)]
pub struct DatFile {
    #[pyo3(get, set)] pub version: String,
    #[pyo3(get, set)] pub terrain_restrictions: Vec<TerrainRestriction>,
    #[pyo3(get, set)] pub player_colours: Vec<PlayerColour>,
    #[pyo3(get, set)] pub sounds: Vec<Sound>,
    #[pyo3(get, set)] pub graphics: Vec<Graphic>,
    #[pyo3(get, set)] pub effects: Vec<Effect>,
    #[pyo3(get, set)] pub unit_headers: Vec<UnitHeaders>, 
    #[pyo3(get, set)] pub civs: Vec<Civ>,
    #[pyo3(get, set)] pub techs: Vec<Tech>,
    #[pyo3(get, set)] pub tech_tree: Option<TechTree>,
    #[pyo3(get, set)] pub time_slice: i32,
    #[pyo3(get, set)] pub debug_pos: u64,
}

#[pymethods]
impl DatFile {
    #[staticmethod]
    pub fn from_file(path: &str) -> PyResult<Self> {
        let mut f = File::open(path).map_err(|e| PyErr::new::<pyo3::exceptions::PyOSError, _>(format!("{:?}", e)))?;
        let mut compressed_data = Vec::new();
        f.read_to_end(&mut compressed_data).map_err(|e| PyErr::new::<pyo3::exceptions::PyOSError, _>(format!("{:?}", e)))?;

        let mut decompressor = Decompress::new(false);
        
        let mut uncompressed_data = Vec::with_capacity(compressed_data.len() * 4);
        let mut input_pos = 0;
        let mut chunk = vec![0u8; 65536];
        
        loop {
            let old_total_in = decompressor.total_in();
            let old_total_out = decompressor.total_out();
            let status = decompressor.decompress(
                &compressed_data[input_pos..],
                &mut chunk,
                FlushDecompress::None,
            );
            
            match status {
                Ok(st) => {
                     uncompressed_data.extend_from_slice(&chunk[..(decompressor.total_out() - old_total_out) as usize]);
                     input_pos += (decompressor.total_in() - old_total_in) as usize;
                     if st == flate2::Status::StreamEnd { break; }
                     if input_pos >= compressed_data.len() { break; }
                },
                Err(_) => {
                    break;
                }
            }
        }

        let mut cursor = Cursor::new(uncompressed_data);
        Ok(Self::read_from_soft(&mut cursor))
    }
}

impl DatFile {
    fn read_from_soft<R: Read + Seek>(reader: &mut R) -> Self {
        let mut version = String::new();
        let mut ver_buf = [0u8; 8];
        if reader.read_exact(&mut ver_buf).is_ok() {
            version = String::from_utf8_lossy(&ver_buf).trim_matches(char::from(0)).to_string();
        }
        println!("Version: {}", version);

        let mut terrain_restrictions = Vec::new();
        let mut player_colours = Vec::new();
        let mut sounds = Vec::new();
        let mut graphics = Vec::new();
        let mut effects = Vec::new();
        let mut unit_headers = Vec::new();
        let mut civs = Vec::new();
        let mut techs = Vec::new();
        let mut time_slice = 0;

        let _ = (|| -> std::io::Result<()> {
            let terr_rest_size = reader.read_u16::<LittleEndian>()?;
            let terrains_used = reader.read_u16::<LittleEndian>()? as usize;
            println!("TR size: {}, Used: {}", terr_rest_size, terrains_used);
            // Terrain pointers
            reader.seek(std::io::SeekFrom::Current((terr_rest_size * 4 * 2) as i64))?;
            for _ in 0..terr_rest_size {
                terrain_restrictions.push(TerrainRestriction::read_from(reader, terrains_used)?);
            }
            
            println!("Pos after TR: {}", reader.stream_position()?);
            
            let player_colours_size = reader.read_u16::<LittleEndian>()?;
            println!("Player colors: {}", player_colours_size);
            for _ in 0..player_colours_size { player_colours.push(PlayerColour::read_from(reader)?); }
            
            let sound_count = reader.read_u16::<LittleEndian>()?;
            println!("Sounds: {}", sound_count);
            for _ in 0..sound_count { sounds.push(Sound::read_from(reader)?); }

            let graphic_count = reader.read_u16::<LittleEndian>()?;
            println!("Graphics: {}", graphic_count);
            reader.seek(std::io::SeekFrom::Current((graphic_count as i64) * 4))?; // pointers
            for _ in 0..graphic_count { graphics.push(Graphic::read_from(reader, &version)?); }
            
            println!("Pos before TerrainBlock: {}", reader.stream_position()?);
            let _terrain_block = TerrainBlock::read_from(reader)?;
            println!("Pos after TerrainBlock: {}", reader.stream_position()?);
            
            let _random_maps = RandomMaps::read_from(reader)?;
            println!("Pos after RandomMaps: {}", reader.stream_position()?);
            
            let effects_count = reader.read_u32::<LittleEndian>()?;
            println!("Effects: {}", effects_count);
            for _ in 0..effects_count { effects.push(Effect::read_from(reader)?); }
            
            println!("Pos before UnitHeaders: {}", reader.stream_position()?);
            let unit_headers_count = reader.read_u32::<LittleEndian>()?;
            println!("Unit Headers: {}", unit_headers_count);
            for _ in 0..unit_headers_count { unit_headers.push(UnitHeaders::read_from(reader, &version)?); }
            
            let civs_count = reader.read_u16::<LittleEndian>()?;
            println!("Civs: {}", civs_count);
            for _ in 0..civs_count { civs.push(Civ::read_from(reader, &version)?); }
            
            let techs_count = reader.read_u16::<LittleEndian>()?;
            for _ in 0..techs_count { techs.push(Tech::read_from(reader, &version)?); }
            
            time_slice = reader.read_i32::<LittleEndian>()?;
            Ok(())
        })();

        DatFile {
            version, terrain_restrictions, player_colours, sounds, graphics,
            effects, unit_headers, civs, techs, tech_tree: None,
            time_slice, debug_pos: reader.stream_position().unwrap_or(0),
        }
    }
}
