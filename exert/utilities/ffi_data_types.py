from cffi.backend_ctypes import CTypesBackend, CTypesType
from pandare import Panda

def get_ffi_datatypes(panda: Panda):
    data_types_tuple: tuple[list[str], list[str], list[str]] = panda.ffi.list_types()
    data_types_tuple[2].append("enum device_endian")
    data_types_tuple[2].append("enum QemuOptType")
    data_types_tuple[2].append("enum kernel_mode")

    python_file_str: str = 'from enum import IntEnum\n'
    python_file_str += "from collections.abc import Callable\n"
    python_file_str += 'import ctypes\n\n'

    for data_types_list in data_types_tuple:

        for data_type in data_types_list:
            try:
                c_data_type: CTypesType = panda.ffi.typeof(panda.ffi.getctype(data_type))
            except Exception as e: # pylint: disable=broad-exception-caught
                # The library throws a generic error, I have to be broad
                error_str = str(e)
                if error_str.find("the type ") != -1:
                    if error_str.find("is a function type"):
                        base_type = error_str.split("'")[1].split("(")[0]
                        ptype = get_python_type(panda.ffi.typeof(base_type))
                        python_file_str += f'{data_type}: {ptype}\n'
                        continue
                elif error_str.find("undefined type name") != -1:
                    c_data_type = panda.ffi.typeof(panda.ffi.getctype("struct " + data_type))
                else:
                    return e

            if c_data_type.kind == 'enum':
                data_name = ''

                if len(data_type.split()) == 1:
                    data_name = data_type
                else:
                    data_name = data_type.split()[1]

                python_file_str += f'class {data_name}(IntEnum):\n'

                for key in c_data_type.elements.keys():
                    python_file_str += f'    {c_data_type.elements[key]}: int = {str(key)}\n'

                python_file_str += '\n'
                continue

            if c_data_type.kind == 'struct':
                python_file_str += get_struct_union_definition(c_data_type, data_type, '')
                python_file_str += '\n'
                continue

            if c_data_type.kind == 'primitive':
                python_file_str += f'{data_type}: {get_primitive_type_name(c_data_type.cname)}\n'
                continue

            if c_data_type.kind == 'array':
                python_file_str += f'{data_type}: {get_python_type(c_data_type)}\n'
                continue

            if c_data_type.kind == 'void':
                python_file_str += f'{data_type}: None\n'
                continue

            if c_data_type.kind == 'function':
                python_file_str += f'{data_type}: {get_python_type(c_data_type)}\n'
                continue

            if c_data_type.kind == 'union':
                python_file_str += get_struct_union_definition(c_data_type, data_type, '')
                python_file_str += '\n'
                continue

            if c_data_type.kind == 'pointer':
                python_file_str += f'{data_type}: {get_python_type(c_data_type)}'
                python_file_str += '\n'
                continue

            assert False, c_data_type.kind

    return python_file_str

def get_struct_union_definition(struct_type: CTypesType, struct_name: str, prefix: str):
    class_str = f'{prefix}class {struct_name}:\n'
    reserved_attributes = []

    if (struct_type.fields is None or len(struct_type.fields) == 0):
        class_str += '    pass\n'
        return class_str

    for field in struct_type.fields:
        field_name = field[0]
        field_type = field[1]

        field_reserved = False

        if field_name in ["as"]:
            field_reserved = True

        field_python_type = get_python_type(field_type.type, struct_name, field_name)

        if field_python_type.find('$') != -1:
            field_python_type = 'internal_' + field_python_type.replace('$', '')
            class_str += get_struct_union_definition(field_type.type, field_python_type, '    ')
            class_str += '\n'

        if field_reserved:
            reserved_str = f'{prefix}setattr'
            reserved_str += f'({struct_name}, "{field_name}", {field_python_type}())\n'
            reserved_attributes.append(reserved_str)
        else:
            class_str += f'    {prefix}{field_name}: {field_python_type}\n'

    for attribute in reserved_attributes:
        class_str += attribute

    return class_str


def get_python_type(c_data_type: CTypesType, struct_type: (str | None) = None,
                    field_name: (str | None) = None):
    c_data_type_kind = c_data_type.kind
    c_data_type_name = c_data_type.cname

    if c_data_type_kind == 'primitive':
        return get_primitive_type_name(c_data_type_name)

    if c_data_type_kind == 'struct':
        return get_struct_type_name(c_data_type_name)

    if c_data_type_kind == 'enum':
        return get_enum_type_name(c_data_type_name)

    if c_data_type_kind == 'array':
        array_type = get_python_type(c_data_type.item, struct_type, field_name)
        return f'ctypes.Array[{array_type}]'

    if c_data_type_kind == 'pointer':
        if c_data_type.item.kind == 'void':
            return 'ctypes.c_void_p'

        pointer_type = get_python_type(c_data_type.item, struct_type, field_name)
        return f'ctypes._Pointer[{pointer_type}]'

    if c_data_type_kind == 'union':
        return get_union_type_name(c_data_type_name)

    if c_data_type_kind == 'function':
        restype = get_python_type(c_data_type.result, struct_type, field_name)

        args = ''
        for index, value in enumerate(c_data_type.args):
            python_arg_type = get_python_type(value)
            if index == (len(c_data_type.args) - 1):
                args += python_arg_type
            else:
                args += python_arg_type + ', '

        return f'Callable[[{args}], {restype}]'

    if c_data_type_kind == 'void':
        return 'None'

    print(struct_type)
    print(field_name)
    assert False, c_data_type_kind

def get_primitive_type_name(prim_name: str):
    for key, value in CTypesBackend.PRIMITIVE_TYPES:
        if key == prim_name:
            return "ctypes." + value.__name__

    assert False, prim_name

def get_struct_type_name(struct_name: str):
    struct_names = struct_name.split()

    if len(struct_names) == 1:
        assert struct_names[0] != 'struct', struct_name
        return struct_names[0]
    if len(struct_names) == 2:
        assert struct_names[0] == 'struct', struct_name
        return struct_names[1]

    assert False, struct_name

def get_union_type_name(union_name: str):
    union_names = union_name.split()

    if len(union_names) == 1:
        assert union_names[0] != 'union', union_name
        return union_names[0]
    if len(union_names) == 2:
        assert union_names[0] == 'union', union_name
        return union_names[1]

    assert False, union_name

def get_enum_type_name(enum_name: str):
    union_names = enum_name.split()

    if len(union_names) == 1:
        assert union_names[0] != 'enum', enum_name
        return union_names[0]
    if len(union_names) == 2:
        assert union_names[0] == 'enum', enum_name
        return union_names[1]

    assert False, enum_name

def write_into_file(python_str: str, path: str):
    with open(path, 'wt', encoding="utf-8") as file:
        file.write(python_str)
