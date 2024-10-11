from enum import Enum

class data_type(Enum):
    UNKNOWN = 0
    BOOLEAN = 1
    INTEGER8 = 2
    INTEGER16 = 3
    INTEGER32 = 4
    UNSIGNED8 = 5
    UNSIGNED16 = 6
    UNSIGNED32 = 7
    REAL32 = 8
    VISIBLE_STRING = 9
    OCTET_STRING = 0x0A
    UNICODE_STRING = 0x0B
    TIME_OF_DAY = 0x0C
    TIME_DIFFERENCE = 0x0D
    DOMAIN = 0x0F
    INTEGER24 = 0x10
    REAL64 = 0x11
    INTEGER40 = 0x12
    INTEGER48 = 0x13
    INTEGER56 = 0x14
    INTEGER64 = 0x15
    UNSIGNED24 = 0x16
    UNSIGNED40 = 0x18
    UNSIGNED48 = 0x19
    UNSIGNED56 = 0x1A
    UNSIGNED64 = 0x1B
    PDO_COMMUNICATION_PARAMETER = 0x20
    PDO_MAPPING = 0x21
    SDO_PARAMETER = 0x22
    IDENTITY = 0x23

# Mapping of CANopen data types to C strings
canopen_data_type_to_c_string = {
    data_type.UNKNOWN: "void",
    data_type.BOOLEAN: "bool",
    data_type.INTEGER8: "int8_t",
    data_type.INTEGER16: "int16_t",
    data_type.INTEGER32: "int32_t",
    data_type.UNSIGNED8: "uint8_t",
    data_type.UNSIGNED16: "uint16_t",
    data_type.UNSIGNED32: "uint32_t",
    data_type.REAL32: "float",
    data_type.VISIBLE_STRING: "char*",
    data_type.OCTET_STRING: "uint8_t*",
    data_type.UNICODE_STRING: "wchar_t*",
    data_type.TIME_OF_DAY: "time_t",
    data_type.TIME_DIFFERENCE: "time_t",
    data_type.DOMAIN: "void*",
    data_type.INTEGER24: "int24_t",  # Custom type, not standard in C
    data_type.REAL64: "double",
    data_type.INTEGER40: "int40_t",  # Custom type, not standard in C
    data_type.INTEGER48: "int48_t",  # Custom type, not standard in C
    data_type.INTEGER56: "int56_t",  # Custom type, not standard in C
    data_type.INTEGER64: "int64_t",
    data_type.UNSIGNED24: "uint24_t",  # Custom type, not standard in C
    data_type.UNSIGNED40: "uint40_t",  # Custom type, not standard in C
    data_type.UNSIGNED48: "uint48_t",  # Custom type, not standard in C
    data_type.UNSIGNED56: "uint56_t",  # Custom type, not standard in C
    data_type.UNSIGNED64: "uint64_t",
    data_type.PDO_COMMUNICATION_PARAMETER: "pdo_comm_param_t",  # CANopen custom type
    data_type.PDO_MAPPING: "pdo_mapping_t",  # CANopen custom type
    data_type.SDO_PARAMETER: "sdo_param_t",  # CANopen custom type
    data_type.IDENTITY: "identity_t"  # CANopen custom type
}

def c_type(value):
    """Returns the C string representing the CANopen data type for the given integer value."""
    if isinstance(value, str):
        try:
            # Attempt to convert the string to an integer
            value = int(value)
        except ValueError:
            return None
    
    try:
        CO_type = data_type(value)
        return canopen_data_type_to_c_string.get(CO_type, "void")
    except ValueError:
        return "void"

