import sys
import subprocess
import os
import pickle
from exert.utilities import version as ver
from exert.usermode import plugin, osi
from exert.usermode import task_struct_stack as tss

PANDA_PLUGIN_PREFIX = """
from exert.usermode import plugin
from exert import osi_generator as osi
from exert.usermode import task_struct_stack as tss
plugin.run(arch='{}', generic={}, kernel='{}',
           usermode='{}', command='{}',
           callback={}, hypercall_callback={})
"""

def empty_callback(panda, cpu): # pragma: no cover
    return

def get_data_addresses(panda, cpu): # pragma: no cover
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
    data = open("tmp_data", "wb")
    data.write(address_bytes)
    data.close()

def get_task_struct_size(panda, cpu): # pragma: no cover
    magic = panda.arch.get_arg(cpu, 0, convention='syscall')
    string_address = panda.arch.get_arg(cpu, 1, convention='syscall')
    assert magic == 204
    slab_info = panda.read_str(cpu, string_address)

    data_parts = slab_info.split()

    size_bytes = pickle.dumps(data_parts[3])
    data = open("tmp_data", "wb")
    data.write(size_bytes)
    data.close()

def get_osi_info(kernel, arch, version):
    version_supported = False

    ver_entry = ver.version_from_string(version)

    min_ver = ver.Version(4,4,99)
    max_ver = ver.Version(4,4,101)
    if (arch in ['armv4l', 'armv5l', 'armv6l', 'armv7l', 'x86_64', 'i386', 'aarch64']):
        if(ver.compare_version(ver_entry, min_ver) and ver.compare_version(max_ver, ver_entry)):
            version_supported = True

            osi_prog = ''
            task_struct_callback = None

            if (arch in ['armv4l', 'armv5l', 'armv6l', 'armv7l']):
                osi_prog = 'osi-armv5l'
                task_struct_callback = tss.task_address_arm_callback
            else:
                osi_prog = 'osi-' + arch

                if (arch == 'aarch64'):
                    task_struct_callback = tss.task_address_aarch_callback
                elif (arch == 'x86_64'):
                    task_struct_callback = tss.task_address_x86_64_callback
                elif (arch == 'i386'):
                    task_struct_callback = tss.task_address_i386_callback

            bits = ''
            if (arch in ['armv4l', 'armv5l', 'armv6l', 'armv7l', 'i386']):
                bits = '32'
            else:
                bits = '64'

            data_address_prefix = PANDA_PLUGIN_PREFIX.format(arch, False, kernel, osi_prog,
                                                             './user_prog data_address',
                                                             'osi.' + empty_callback.__name__,
                                                             'osi.' + get_data_addresses.__name__)
            subprocess.run(['python'], input = data_address_prefix, check = True, text = True)
            data = open("tmp_data", "rb")
            data_addresses = pickle.load(data)
            data.close()
            
            task_struct_prefix = PANDA_PLUGIN_PREFIX.format(arch, False, kernel, osi_prog,
                                                            './user_prog data_address',
                                                            'tss.' + task_struct_callback.__name__,
                                                            'osi.' + empty_callback.__name__)

            subprocess.run(['python'], input = task_struct_prefix, check = True, text = True)

            data = open("tmp_data", "rb")
            init_task_struct_addr = pickle.load(data)
            data.close()

            task_struct_size_prefix = PANDA_PLUGIN_PREFIX.format(arch, False, kernel, osi_prog,
                                                                 './user_prog task_struct_size',
                                                                 'osi.' + empty_callback.__name__,
                                                                 'osi.' + get_task_struct_size.__name__)
            subprocess.run(['python'], input = task_struct_size_prefix, check = True, text = True)
            data = open("tmp_data", "rb")
            task_struct_size = pickle.load(data)
            data.close()

            os.remove("tmp_data")
            
            header_line = osi.HeaderLine("[linux:" + version + ":" + bits + "]")
            osi_name = osi.Name(version + "|linux|" + arch)
            osi_version = osi.Version(ver_entry.x, ver_entry.y, ver_entry.z)
            task = osi.Task(per_cpu_offsets_addr = -1,
                            per_cpu_offset_0_addr = -1,
                            current_task_addr = -1,
                            init_addr = init_task_struct_addr,
                            size = task_struct_size,
                            tasks_offset = -1,
                            pid_offset = -1,
                            tgid_offset = -1,
                            group_leader_offset = -1,
                            thread_group_offset = -1,
                            real_parent_offset = -1,
                            parent_offset = -1,
                            mm_offset = -1,
                            stack_offset = -1,
                            real_cred_offset = -1,
                            cred_offset = -1,
                            comm_offset = -1,
                            comm_size = -1,
                            files_offset = -1,
                            start_time_offset = -1)
            cred = osi.Cred(uid_offset = -1,
                            gid_offset = -1,
                            euid_offset = -1,
                            egid_offset = -1)
            mm = osi.MM(size = -1,
                        mmap_offset = -1,
                        pgd_offset = -1,
                        arg_start_offset = -1,
                        start_brk_offset = -1,
                        brk_offset = -1,
                        start_stack_offset = -1)
            vma = osi.VMA(size = -1,
                          vm_mm_offset = -1,
                          vm_start_offset = -1,
                          vm_end_offset = -1,
                          vm_next_offset = -1,
                          vm_flags_offset = -1,
                          vm_file_offset = -1)
            fs = osi.FS(f_path_dentry_offset = -1,
                        f_path_mnt_offset = -1,
                        f_pos_offset = -1,
                        fdt_offset = -1,
                        fdtab_offset = -1,
                        fd_offset = -1)
            qstr = osi.QSTR(size = -1,
                            name_offset = -1)
            osi_path = osi.Path(d_name_offset = -1,
                                d_iname_offset = -1,
                                d_parent_offset = -1,
                                d_op_offset = -1,
                                d_dname_offset = -1,
                                mnt_root_offset = -1,
                                mnt_parent_offset = -1,
                                mnt_mountpoint_offset = -1)
            demo_path = "./result_osi.osi"
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
                    demo_path=demo_path)

    if not version_supported:
        print("Version not supported")

if __name__ == '__main__':
    get_osi_info(sys.argv[1], sys.argv[2], sys.argv[3])
