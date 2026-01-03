import sys
import os
import inspect
import re
from dataclasses import fields

# Add parent dir to path to find genieutils
sys.path.append(os.path.abspath(".."))

from genieutils import unit, tech, graphic, civ, effect, terrainrestriction, playercolour, sound, terrainblock, randommaps, unitheaders, techtree

MODULES_TO_PROCESS = [
    unit, tech, graphic, civ, effect, terrainrestriction, playercolour, sound, terrainblock, randommaps, unitheaders, techtree
]

RUST_MAP = {
    'b': 'i8', 'B': 'u8',
    'h': 'i16', 'H': 'u16',
    'i': 'i32', 'I': 'u32',
    'l': 'i32', 'L': 'u32',
    'q': 'i64', 'Q': 'u64',
    'f': 'f32', 'd': 'f64',
    '?': 'bool',
    's': 'String',
    'x': None,
}

def parse_format(fmt):
    fmt = fmt.replace('<', '').replace('>', '').replace('!', '').replace('@', '').replace('=', '')
    types = []
    i = 0
    while i < len(fmt):
        c = fmt[i]
        count_str = ''
        while i < len(fmt) and fmt[i].isdigit():
            count_str += fmt[i]
            i += 1
        
        if c == 's':
            types.append(('s', int(count_str) if count_str else 1))
        elif c == 'x':
             pass 
        else:
            count = int(count_str) if count_str else 1
            for _ in range(count):
                types.append((c, 1))
        i += 1
    return types

if __name__ == "__main__":
    with open("src/generated_structs.rs", "w", encoding="utf-8") as f:
        print(f"use pyo3.prelude::*;", file=f)
        print(f"use serde::{{Serialize, Deserialize}};", file=f)
        print(f"use byteorder::{{ReadBytesExt, LittleEndian}};", file=f)
        print(f"use std::io::{{Read, Seek}};", file=f)
        
        def analyze_module_file(module, out_file):
            if module.__name__ == 'genieutils.sound':
                sys.stderr.write(f"DEBUG: sound dir: {dir(module)}\n")
                
            print(f"// ========================================================================", file=out_file)
            print(f"// Generated from {module.__name__}", file=out_file)
            print(f"// ========================================================================", file=out_file)
            
            for name, obj in inspect.getmembers(module, inspect.isclass):
                if obj.__module__ != module.__name__:
                   continue 

                # Skip manual structs
                if name in ["Unit", "Civ", "Graphic"]:
                    continue
                
                # Try various format naming conventions
                candidates = []
                
                # 1. Stripped name upper (e.g. SOUNDITEM_FORMAT)
                upper_name_stripped = ''.join(['_'+c if c.isupper() else c.upper() for c in name]).lstrip('_').replace('_', '')
                candidates.append(f"{upper_name_stripped}_FORMAT")

                # 2. Original snake upper (e.g. SOUND_ITEM_FORMAT if class is SoundItem)
                # CamelCase to snake_case regex
                s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
                snake_name = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).upper()
                candidates.append(f"{snake_name}_FORMAT")
                
                # 3. Direct name upper (e.g. SOUND_FORMAT for Sound)
                candidates.append(f"{name.upper()}_FORMAT")
                
                fmt_name = None
                found_fmt = False
                for c in candidates:
                    if hasattr(module, c):
                        fmt_name = c
                        found_fmt = True
                        break
                
                if not found_fmt:
                    sys.stderr.write(f"DEBUG: {name} - Candidates checked: {candidates}. Found nothing.\n")
                    continue
                else:
                    sys.stderr.write(f"DEBUG: {name} - Found format: {fmt_name}\n")
                
                fmt = getattr(module, fmt_name)
                
                try:
                    type_definitions = parse_format(fmt)
                except Exception:
                    continue

                try:
                    cls_fields = fields(obj)
                except Exception:
                    continue
                    
                print(f"#[pyclass]", file=out_file)
                print(f"#[derive(Clone, Debug, Serialize, Deserialize)]", file=out_file)
                print(f"pub struct {name} {{", file=out_file)
                
                # Injected Fields Logic
                EXTRA_FIELDS = {
                    'Creatable': [
                        ('pub resource_costs: Vec<ResourceCost>', 'ResourceCost'),
                        ('pub train_locations: Vec<TrainLocation>', 'TrainLocation'),
                    ],
                    'Building': [
                        ('pub annexes: Vec<BuildingAnnex>', 'BuildingAnnex'),
                    ],
                    'Sound': [
                        ('pub items: Vec<SoundItem>', 'SoundItem'),
                    ]
                }

                for i, (t_code, t_len) in enumerate(type_definitions):
                    r_type = RUST_MAP.get(t_code, 'UNKNOWN')
                    f_name = f"_unknown_{i}"
                    if i < len(cls_fields):
                        f = cls_fields[i]
                        f_name = f.name
                        if f_name == 'type': f_name = 'type_'
                    
                    print(f"    #[pyo3(get, set)]", file=out_file)
                    print(f"    pub {f_name}: {r_type},", file=out_file)
                
                if name in EXTRA_FIELDS:
                    for field_def, _ in EXTRA_FIELDS[name]:
                        print(f"    #[pyo3(get, set)]", file=out_file)
                        print(f"    {field_def},", file=out_file)

                print("}\n", file=out_file)
                
                print(f"impl {name} {{", file=out_file)
                print(f"    pub fn read_from<R: Read + Seek>(reader: &mut R) -> std::io::Result<Self> {{", file=out_file)
                
                lines = []
                field_names = []
                
                for i, (t_code, t_len) in enumerate(type_definitions):
                    f_name = f"_unknown_{i}"
                    if i < len(cls_fields):
                        f = cls_fields[i]
                        f_name = f.name
                        if f_name == 'type': f_name = 'type_'
                    field_names.append(f_name)
                    
                    if t_code == 'b': 
                        lines.append(f"        let {f_name} = reader.read_i8()?;")
                    elif t_code == 'B': 
                        lines.append(f"        let {f_name} = reader.read_u8()?;")
                    elif t_code == 'h': 
                        lines.append(f"        let {f_name} = reader.read_i16::<LittleEndian>()?;")
                    elif t_code == 'H': 
                        lines.append(f"        let {f_name} = reader.read_u16::<LittleEndian>()?;")
                    elif t_code == 'i' or t_code == 'l': 
                        lines.append(f"        let {f_name} = reader.read_i32::<LittleEndian>()?;")
                    elif t_code == 'I' or t_code == 'L': 
                        lines.append(f"        let {f_name} = reader.read_u32::<LittleEndian>()?;")
                    elif t_code == 'f': 
                        lines.append(f"        let {f_name} = reader.read_f32::<LittleEndian>()?;")
                    elif t_code == 'd': 
                        lines.append(f"        let {f_name} = reader.read_f64::<LittleEndian>()?;")
                    elif t_code == 's': 
                        lines.append(f"        let mut {f_name}_buf = vec![0u8; {t_len}];")
                        lines.append(f"        reader.read_exact(&mut {f_name}_buf)?;")
                        lines.append(f"        let {f_name} = String::from_utf8_lossy(&{f_name}_buf).trim_matches(char::from(0)).to_string();")
                    
                for line in lines:
                    print(line, file=out_file)

                if name in EXTRA_FIELDS:
                    for field_def, type_name in EXTRA_FIELDS[name]:
                         fname = field_def.split(':')[0].replace('pub ', '').strip()
                         field_names.append(fname)
                         if "Vec" in field_def:
                            print(f"        let {fname} = Vec::new();", file=out_file) 
                         else:
                            print(f"        let {fname} = None;", file=out_file)
                    
                print(f"        Ok(Self {{", file=out_file)
                for fnm in field_names:
                    print(f"            {fnm},", file=out_file)
                print(f"        }})", file=out_file)
                
                print(f"    }}", file=out_file)
                print(f"}}", file=out_file)
                print("", file=out_file)

        for mod in MODULES_TO_PROCESS:
            analyze_module_file(mod, f)
