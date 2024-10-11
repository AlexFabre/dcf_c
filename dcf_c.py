import argparse
import canopen
from datetime import datetime
import re
import os
import CIA_301.data_type as co_type

canopener_MAJOR = 0
canopener_MINOR = 0
canopener_FIX = 1

def str_version() -> str:
    return f'Generated with CANopener v{canopener_MAJOR}.{canopener_MINOR}.{canopener_FIX}'

def str_low(input_string: str) -> str:
    # Replace all non-alphanumeric characters with '_'
    return re.sub(r'[^a-zA-Z0-9]', '_', input_string).lower()

def str_to_define(input_string: str) -> str:
    # Replace all non-alphanumeric characters with '_'
    return re.sub(r'[^a-zA-Z0-9]', '_', input_string).upper()

def format_value(value) -> str:
    # Format unsigned integers in hex format
    if (value == None):
        return f'0'
    
    if isinstance(value, int):
        if value < 0:
            return str(value)
        
        try:
            return f"0x{value:02X}"
        except ValueError:
            return str(value)
    else:
        return f"\"{value}\""
    
def str_size(obj: canopen.ObjectDictionary) -> str:
    # output the object size depending on it's type and value.
    obj_type = co_type.data_type(obj.data_type)
    if (obj_type == co_type.data_type.VISIBLE_STRING):
        return f'sizeof(\"{obj.value}\")'
    else:
        return f'sizeof({co_type.c_type(obj.data_type)})'

def get_dictionary(device_node_ID: int, eds_file_path: str):
    try:
        node = canopen.RemoteNode(device_node_ID, eds_file_path)
        return node.object_dictionary
    except Exception as e:
        print(f"Error reading EDS file: {e}")
        return None

def generate_c_header(eds_file_path: str, device_name: str, dictionary: canopen.ObjectDictionary, output_file: str):

    eds_file_path = os.path.basename(eds_file_path)
    header_guard = str_to_define(device_name) + '_' + str_to_define(eds_file_path) + '_H_'
    
    try:
        with open(output_file, 'w') as header_file:

            header_file.write(f'/* clang-format off */\n\n')

            header_file.write(f'/**\n * {str_version()}\n * Base file: {eds_file_path}\n * Date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n */\n\n')

            # Write header guard
            header_file.write(f"#ifndef {header_guard}\n")
            header_file.write(f"#define {header_guard}\n\n")

            header_file.write(f'#include <stdlib.h>\n\n')
            header_file.write(f'#include <stdint.h>\n\n')

            # Iterate over objects in the dictionary
            for obj in dictionary.values():
                write_object_to_header(header_file, device_name, obj)

            # End of header guard
            header_file.write(f"#endif /* {header_guard} */\n")
            header_file.write(f'\n/* clang-format on */\n')

    except IOError as e:
        print(f"Error writing to file: {e}")

def write_object_to_header(header_file, device_name, obj):
    if isinstance(obj, canopen.objectdictionary.ODRecord):
        # Definitions (Record)
        header_file.write(f'/* Object 0x{obj.index:04X} (Record): {obj.name} */\n')
        header_file.write(f"#define {str_to_define(device_name)}_{str_to_define(obj.name)}_INDEX  {format_value(obj.index)}\n")
        header_file.write(f"#define {str_to_define(device_name)}_{obj.index:04X}_DESCRIPTION      \"{obj.name}\"\n")
        for idx, subobj in enumerate(obj.values()):
            if idx == 0:
                continue
            write_subobject_to_header(header_file, device_name, obj.index, subobj)
        
        # Structure (Records)
        header_file.write(f'\n/* Represents record at index 0x{obj.index:04X} */\n')
        header_file.write(f'struct {str_low(device_name)}_{obj.index:04X}_{str_low(obj.name)} {{\n')
        for idx, subobj in enumerate(obj.values()):
            if idx == 0:
                continue
            write_subobject_structure(header_file, obj.index, subobj)
        header_file.write(f'}};\n')

        # Fill function (Records)
        header_file.write(f'\n/* Inline function to fill the structure {str_low(device_name)}_{obj.index:04X}_{str_low(obj.name)}\n * with the default writeable values from the DCF file. */\n')
        header_file.write(f'static inline void {str_low(device_name)}_{obj.index:04X}_fill_with_default(struct {str_low(device_name)}_{obj.index:04X}_{str_low(obj.name)}* p) {{\n')
        for idx, subobj in enumerate(obj.values()):
            if idx == 0:
                continue
            write_subobject_fill_function_assignations(header_file, device_name, obj.index, subobj)
        header_file.write(f'}}\n')
    elif isinstance(obj, canopen.objectdictionary.ODArray):
        # Definitions (Array)
        header_file.write(f'/* Object 0x{obj.index:04X} (Array): {obj.name} */\n')
        header_file.write(f"#define {str_to_define(device_name)}_{str_to_define(obj.name)}_INDEX   {format_value(obj.index)}\n")
        header_file.write(f"#define {str_to_define(device_name)}_{obj.index:04X}_DESCRIPTION       \"{obj.name}\"\n")
        for idx, subobj in enumerate(obj.values()):
            if idx == 0:
                continue
            write_subobject_to_header(header_file, device_name, obj.index, subobj)
        
        # Structure (Array)
        header_file.write(f'\n/* Represents array at index 0x{obj.index:04X} */\n')
        header_file.write(f'struct {str_low(device_name)}_{obj.index:04X}_{str_low(obj.name)} {{\n')
        for idx, subobj in enumerate(obj.values()):
            if idx == 0:
                continue
            write_subobject_structure(header_file, obj.index, subobj)
        header_file.write(f'}};\n')

        # Fill function (Array)
        header_file.write(f'\n/* Inline function to fill the structure {str_low(device_name)}_{obj.index:04X}_{str_low(obj.name)}\n * with the default writeable values from the DCF file. */\n')
        header_file.write(f'static inline void {str_low(device_name)}_{obj.index:04X}_fill_with_default(struct {str_low(device_name)}_{obj.index:04X}_{str_low(obj.name)}* p) {{\n')
        for idx, subobj in enumerate(obj.values()):
            if idx == 0:
                continue
            write_subobject_fill_function_assignations(header_file, device_name, obj.index, subobj)
        header_file.write(f'}}\n')
    elif isinstance(obj, canopen.objectdictionary.ODVariable):
        # Definitions
        header_file.write(f'/* Object 0x{obj.index:04X} (Variable): {obj.name} */\n')
        header_file.write(f"#define {str_to_define(device_name)}_{str_to_define(obj.name)}_INDEX    {format_value(obj.index)}\n")
        header_file.write(f"#define {str_to_define(device_name)}_{str_to_define(obj.name)}_SUBINDEX {obj.subindex}\n")
        header_file.write(f"#define {str_to_define(device_name)}_{str_to_define(obj.name)}_SIZE     {str_size(obj)}\n")
        header_file.write(f"#define {str_to_define(device_name)}_{obj.index:04X}_DESCRIPTION        \"{obj.name}\"\n")
        header_file.write(f"#define {str_to_define(device_name)}_{obj.index:04X}_DATA_TYPE          {co_type.c_type(obj.data_type)}\n")
        header_file.write(f"#define {str_to_define(device_name)}_{obj.index:04X}_DATA_VALUE         {format_value(obj.value)}\n")

        # Structure (Variable)
        header_file.write(f'\n/* Represents variable at index 0x{obj.index:04X} */\n')
        header_file.write(f'struct {str_low(device_name)}_{obj.index:04X}_{str_low(obj.name)} {{\n')
        header_file.write(f'    /* {obj.name}: {str_to_define(obj.access_type)} access. */\n')
        header_file.write(f'    {co_type.c_type(obj.data_type)} value;\n')
        header_file.write(f'}};\n')
        
        # Fill function (Variable)
        header_file.write(f'\n/* Inline function to fill the structure {str_low(device_name)}_{obj.index:04X}_{str_low(obj.name)}\n * with the default writeable values from the DCF file. */\n')
        header_file.write(f'static inline void {str_low(device_name)}_{obj.index:04X}_fill_with_default(struct {str_low(device_name)}_{obj.index:04X}_{str_low(obj.name)}* p) {{\n')
        header_file.write(f'    p->value = {str_to_define(device_name)}_{obj.index:04X}_DATA_VALUE;\n')
        header_file.write(f'}}\n')

    header_file.write('\n')

def write_subobject_to_header(header_file, device_name, index, subobj):
    header_file.write(f'/* {subobj.name} */\n')
    header_file.write(f"#define {str_to_define(device_name)}_{index:04X}_{subobj.subindex}_DESCRIPTION  \"{subobj.name}\"\n")
    header_file.write(f"#define {str_to_define(device_name)}_{index:04X}_{subobj.subindex}_SUBINDEX     {subobj.subindex}\n")
    header_file.write(f"#define {str_to_define(device_name)}_{index:04X}_{subobj.subindex}_DATA_TYPE    {co_type.c_type(subobj.data_type)}\n")
    header_file.write(f"#define {str_to_define(device_name)}_{index:04X}_{subobj.subindex}_SIZE         {str_size(subobj)}\n")
    header_file.write(f"#define {str_to_define(device_name)}_{index:04X}_{subobj.subindex}_DATA_VALUE   {format_value(subobj.value)}\n")

def write_subobject_structure(header_file, index, subobj):
    header_file.write(f'    /* {subobj.name}: {str_to_define(subobj.access_type)} access. (Index {index:04X}: subindex {subobj.subindex}) */\n')
    header_file.write(f'    {co_type.c_type(subobj.data_type)} s{subobj.subindex}_{str_low(subobj.name)};\n')

def write_subobject_fill_function_assignations(header_file, device_name, index, subobj):
    if (str_to_define(subobj.access_type) in ("RW","WO")):
        header_file.write(f'    p->s{subobj.subindex}_{str_low(subobj.name)} = {str_to_define(device_name)}_{index:04X}_{subobj.subindex}_DATA_VALUE;\n')
    else:
        header_file.write(f"    /* Nothing to set for s{subobj.subindex}_{str_low(subobj.name)} as it's a {str_to_define(subobj.access_type)} member. */\n")

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Process an EDS file and generate a C header with its object information.')
    parser.add_argument('eds_file_path', type=str, help='Path to the device EDS or DCF')
    parser.add_argument('output_file_path', type=str, help='Path to the output C header file')
    parser.add_argument('--device', type=str, default="OD", help='Name of the CANopen device')
    parser.add_argument('--nodeID', type=int, default=1, help='Node ID of the device')

    # Parse arguments
    args = parser.parse_args()

    # Parse the EDS file
    object_dictionary = get_dictionary(args.nodeID, args.eds_file_path)
    if object_dictionary is None:
        return

    # Generate the C header file
    generate_c_header(args.eds_file_path, args.device, object_dictionary, args.output_file_path)

if __name__ == "__main__":
    main()
