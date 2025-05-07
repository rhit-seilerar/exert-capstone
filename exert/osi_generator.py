import sys
import subprocess
import os
import pickle
from typing import cast
from pandare import Panda
from exert.utilities import version as ver
from exert.usermode import osi, rules, context
from exert.usermode import task_struct_stack as tss
from exert.utilities.types.multi_arch import CPUState, ExertCallable
from exert.utilities.types.x86_64_types import CPUState as X86_64CPUState

PANDA_PLUGIN_PREFIX: str = """
from exert.usermode import plugin
from exert import osi_generator as osi
from exert.usermode import task_struct_stack as tss
plugin.run(arch='{}', generic={}, kernel='{}',
           usermode='{}', command='{}',
           callback={}, hypercall_callback={})
"""

def empty_callback(panda:Panda, cpu: CPUState) -> None: # pragma: no cover
    return

def get_data_addresses(panda:Panda, cpu: CPUState) -> None: # pragma: no cover
    magic = panda.arch.get_arg(cpu, 0, convention='syscall')
    string_address = panda.arch.get_arg(cpu, 1, convention='syscall')
    assert magic == 204
    address_string = panda.read_str(cpu, string_address)

    address_parts = address_string.split()

    address = []
    for part in address_parts:
        if part.find('x') != -1:
            address.append(part)

    assert len(address) == 2
    address_bytes = pickle.dumps(address)
    with open("tmp_data", "wb") as data:
        data.write(address_bytes)

def get_task_struct_size(panda:Panda, cpu: CPUState) -> bytes: # pragma: no cover
    magic = panda.arch.get_arg(cpu, 0, convention='syscall')
    string_address = panda.arch.get_arg(cpu, 1, convention='syscall')
    assert magic == 204
    slab_info = panda.read_str(cpu, string_address)

    data_parts = slab_info.split()

    size_bytes = pickle.dumps(data_parts[3])
    with open("tmp_data", "wb") as data:
        data.write(size_bytes)

    return size_bytes

def get_tasks_offset(panda: Panda, cpu: CPUState) -> None:
    task_address = None
    if panda.arch_name == 'arm':
        task_address = tss.task_address_arm_callback(panda, cpu)
    elif panda.arch_name == 'aarch64':
        task_address = tss.task_address_aarch_callback(panda, cpu)
    elif panda.arch_name == 'i386':
        task_address = tss.task_address_i386_callback(panda, cpu)
    elif panda.arch_name == 'x86_64':
        cpu = cast(X86_64CPUState, cpu)
        task_address = tss.task_address_x86_64_callback(panda, cpu)
    else:
        assert False

    tasks_context = context.Context(panda)

    fields_addresses = rules.TASK_STRUCT.get_field_addresses(tasks_context, task_address)

    fields_offsets: set[int] = set()
    fields_offset: (int | None) = None
    for field in fields_addresses["Field('tasks', _ListHead)"]:
        field_context = context.Context(panda)
        offset = field - task_address
        if rules.test_list_head(field_context, field, offset):
            fields_offsets.add(offset)

    if len(fields_offsets) == 1:
        fields_offset = fields_offsets.pop()

    if fields_offset is not None:
        valid_offsets = pickle.dumps(fields_offset)
    else:
        valid_offsets = pickle.dumps(fields_offsets)

    with open("tmp_data", "wb") as data:
        data.write(valid_offsets)

def get_osi_info(kernel: str, arch: str, version: str) -> None:
    version_supported = False

    ver_entry = ver.version_from_string(version)

    min_ver = ver.Version(4,4,99)
    max_ver = ver.Version(4,4,101)
    if (arch in ['armv4l', 'armv5l', 'armv6l', 'armv7l', 'x86_64', 'i386', 'aarch64']):
        if(ver.compare_version(ver_entry, min_ver) and ver.compare_version(max_ver, ver_entry)):
            version_supported = True

            osi_prog = ''
            task_struct_callback: ExertCallable = tss.task_address_arm_callback

            if (arch in ['armv4l', 'armv5l', 'armv6l', 'armv7l']):
                osi_prog = 'osi-armv5l'
            else:
                osi_prog = 'osi-' + arch

                if arch == 'aarch64':
                    task_struct_callback = tss.task_address_aarch_callback
                elif arch == 'x86_64':
                    task_struct_callback = cast(ExertCallable, tss.task_address_x86_64_callback)
                elif arch == 'i386':
                    task_struct_callback = tss.task_address_i386_callback

            bits = ''
            if (arch in ['armv4l', 'armv5l', 'armv6l', 'armv7l', 'i386']):
                bits = '32'
            else:
                bits = '64'

            # data_address_prefix = PANDA_PLUGIN_PREFIX.format(arch, False, kernel, osi_prog,
            #                                                  './user_prog data_address',
            #                                                  'osi.' + empty_callback.__name__,
            #                                                  'osi.' + get_data_addresses.__name__)
            # subprocess.run(['python'], input = data_address_prefix, check = True, text = True)
            # data = open("tmp_data", "rb")
            # data_addresses = pickle.load(data)
            # data.close()

            task_struct_prefix = PANDA_PLUGIN_PREFIX.format(arch, False, kernel, osi_prog,
                                                            './user_prog data_address',
                                                            'tss.' + task_struct_callback.__name__,
                                                            'osi.' + empty_callback.__name__)

            subprocess.run(['python'], input = task_struct_prefix, check = True, text = True)

            with open("tmp_data", "rb") as data:
                init_task_struct_addr = pickle.load(data)

            first_callback_name = 'osi.' + empty_callback.__name__
            second_callback_name = 'osi.' + get_task_struct_size.__name__
            task_struct_size_prefix = PANDA_PLUGIN_PREFIX.format(arch, False, kernel, osi_prog,
                                                                 './user_prog task_struct_size',
                                                                 first_callback_name,
                                                                 second_callback_name)
            subprocess.run(['python'], input = task_struct_size_prefix, check = True, text = True)
            with open("tmp_data", "rb") as data:
                task_struct_size = int(pickle.load(data))

            tasks_addresses_prefix = PANDA_PLUGIN_PREFIX.format(arch, False, kernel, osi_prog,
                                                                './user_prog data_address',
                                                                'osi.' + get_tasks_offset.__name__,
                                                                'osi.' + empty_callback.__name__)

            subprocess.run(['python'], input = tasks_addresses_prefix, check = True, text = True)

            tasks_offsets: set[int] | int
            with open("tmp_data", "rb") as data:
                tasks_offsets = pickle.load(data)

            if isinstance(tasks_offsets, set):
                real_offsets: set[int] = set()

                for tasks_offset in tasks_offsets:
                    if tasks_offset < task_struct_size:
                        real_offsets.add(tasks_offset)

                tasks_offsets = real_offsets

                if len(tasks_offsets) == 1:
                    tasks_offsets = tasks_offsets.pop()

            print(tasks_offsets)

            os.remove("tmp_data")

            header_line = osi.HeaderLine("[linux:" + version + ":" + bits + "]")
            osi_name = osi.Name(version + "|linux|" + arch)
            osi_version = osi.Version(ver_entry.x, ver_entry.y, ver_entry.z)
            task = osi.Task(init_addr = init_task_struct_addr,
                            size = task_struct_size,
                            tasks_offset = tasks_offsets,
                            comm_size = 16) # This is hardcoded in the kernel
            cred = osi.Cred()
            mm = osi.MM()
            vma = osi.VMA()
            fs = osi.FS()
            qstr = osi.QSTR()
            osi_path = osi.Path()
            demo_path = "./Linux-" + version + "-" + arch + ".osi"
            osi.main(header_line=header_line,
                    osi_name=osi_name,
                    osi_version=osi_version,
                    task=task,
                    cred=cred,
                    mm=mm,
                    vma=vma,
                    fs=fs,
                    qstr=qstr,
                    osi_path=osi_path,
                    demo_path=demo_path,
                    demo_mode=True)

    if not version_supported:
        print("Version not supported")

if __name__ == '__main__':
    get_osi_info(sys.argv[1], sys.argv[2], sys.argv[3])
