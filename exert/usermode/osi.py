# Created a boilerplate for the OSI files.
# This isn't very optimized but hopefully this should give a good idea of what to expect?
# First line thing
class HeaderLine():
    def __init__(self, header_line = '[ubuntu:4.4.0-98-generic:64]'):
        self.header_line = header_line

    def to_string(self):
        return f'{self.header_line}\n'

#name
class Name():
    def __init__(self,
                 name = '4.4.0-98-generic|#121-Ubuntu SMP Tue Oct 10 14:24:03 UTC 2017|x86_64'):
        self.name = name

    def to_string(self):
        return f'name = {self.name}\n'

#version
class Version():
    def __init__(self, a = 4, b = 4, c = 0):
        self.a = a
        self.b = b
        self.c = c

    def to_string(self):
        return f'version.a = {self.a}\nversion.b = {self.b}\nversion.c = {self.c}\n'

#task
class Task():
    def __init__(self,
                 per_cpu_offsets_addr = 18446744071594801600,
                 per_cpu_offset_0_addr = 18446744071594856448,
                 current_task_addr = 54272,
                 init_addr = 18446744071593596160,
                 size = 6848,
                 tasks_offset = 848,
                 pid_offset = 1096,
                 tgid_offset = 1100,
                 group_leader_offset = 1160,
                 thread_group_offset = 1272,
                 real_parent_offset = 1112,
                 parent_offset = 1120,
                 mm_offset = 928,
                 stack_offset = 8,
                 real_cred_offset = 1520,
                 cred_offset = 1528,
                 comm_offset = 1536,
                 comm_size = 16,
                 files_offset = 1600,
                 start_time_offset = 1408):
        self.per_cpu_offsets_addr = per_cpu_offsets_addr
        self.per_cpu_offset_0_addr = per_cpu_offset_0_addr
        self.current_task_addr = current_task_addr
        self.init_addr = init_addr
        self.size = size
        self.tasks_offset = tasks_offset
        self.pid_offset = pid_offset
        self.tgid_offset = tgid_offset
        self.group_leader_offset = group_leader_offset
        self.thread_group_offset = thread_group_offset
        self.real_parent_offset = real_parent_offset
        self.parent_offset = parent_offset
        self.mm_offset = mm_offset
        self.stack_offset = stack_offset
        self.real_cred_offset = real_cred_offset
        self.cred_offset = cred_offset
        self.comm_offset = comm_offset
        self.comm_size = comm_size
        self.files_offset = files_offset
        self.start_time_offset = start_time_offset

    def to_string(self):
        return f'''task.per_cpu_offsets_addr = {self.per_cpu_offsets_addr}
        task.per_cpu_offset_0_addr = {self.per_cpu_offset_0_addr}
        task.current_task_addr = {self.current_task_addr}
        task.init_addr = {self.init_addr}
        task.size = {self.size}\ntask.tasks_offset = {self.tasks_offset}
        task.pid_offset = {self.pid_offset}task.tgid_offset = {self.tgid_offset}
        task.group_leader_offset = {self.group_leader_offset}
        task.thread_group_offset = {self.thread_group_offset}
        task.real_parent_offset = {self.real_parent_offset}
        task.parent_offset = {self.parent_offset}
        task.mm_offset = {self.mm_offset}
        task.stack_offset = {self.stack_offset}
        task.real_cred_offset = {self.real_cred_offset}
        task.cred_offset = {self.cred_offset}
        task.comm_offset = {self.comm_offset}
        task.comm_size = {self.comm_size}
        task.files_offset = {self.files_offset}
        task.start_time_offset = {self.start_time_offset}\n'''

#cred
class Cred():
    def __init__(self, uid_offset = 4, gid_offset = 8, euid_offset = 20, egid_offset = 24):
        self.uid_offset = uid_offset
        self.gid_offset = gid_offset
        self.euid_offset = euid_offset
        self.egid_offset =egid_offset

    def to_string(self):
        return f'''cred.uid_offset = {self.uid_offset}
        cred.gid_offset = {self.gid_offset}
        cred.euid_offset = {self.euid_offset}
        cred.egid_offset = {self.egid_offset}\n'''

#mm
class MM():
    def __init__(self,
                 size = 460,
                 mmap_offset = 0,
                 pgd_offset = 32,
                 arg_start_offset = 156,
                 start_brk_offset = 144,
                 brk_offset = 148,
                 start_stack_offset = 152):
        self.size = size
        self.mmap_offset = mmap_offset
        self.pgd_offset = pgd_offset
        self.arg_start_offset = arg_start_offset
        self.start_brk_offset = start_brk_offset
        self.brk_offset = brk_offset
        self.start_stack_offset = start_stack_offset

    def to_string(self):
        return f'''mm.size = {self.size}
        mm.mmap_offset = {self.mmap_offset}
        mm.pgd_offset = {self.pgd_offset}
        mm.arg_start_offset = {self.arg_start_offset}
        mm.start_brk_offset = {self.start_brk_offset}
        mm.brk_offset = {self.brk_offset}
        mm.start_stack_offset = {self.start_stack_offset}\n'''

#vma
class VMA():
    def __init__(self,
                 size = 100,
                 vm_mm_offset = 32,
                 vm_start_offset = 0,
                 vm_end_offset = 4,
                 vm_next_offset = 8,
                 vm_flags_offset = 44,
                 vm_file_offset = 84):
        self.size = size
        self.vm_mm_offset = vm_mm_offset
        self.vm_start_offset = vm_start_offset
        self.vm_end_offset = vm_end_offset
        self.vm_next_offset = vm_next_offset
        self.vm_flags_offset = vm_flags_offset
        self.vm_file_offset = vm_file_offset

    def to_string(self):
        return f'''vma.size = {self.size}
        vma.vm_mm_offset = {self.vm_mm_offset}
        vma.vm_start_offset = {self.vm_start_offset}
        vma.vm_end_offset = {self.vm_end_offset}
        vma.vm_next_offset = {self.vm_next_offset}
        vma.vm_flags_offset = {self.vm_flags_offset}
        vma.vm_file_offset = {self.vm_file_offset}\n'''

#fs
class FS():
    def __init__(self,
    f_path_dentry_offset = 12,
    f_path_mnt_offset = 8,
    f_pos_offset = 64,
    fdt_offset = 20,
    fdtab_offset = 24,
    fd_offset = 4):
        self.f_path_dentry_offset = f_path_dentry_offset
        self.f_path_mnt_offset = f_path_mnt_offset
        self.f_pos_offset = f_pos_offset
        self.fdt_offset = fdt_offset
        self.fdtab_offset = fdtab_offset
        self.fd_offset = fd_offset

    def to_string(self):
        return f'''fs.f_path_dentry_offset = {self.f_path_dentry_offset}
        fs.f_path_mnt_offset = {self.f_path_mnt_offset}
        fs.f_pos_offset = {self.f_pos_offset}
        fs.fdt_offset = {self.fdt_offset}
        fs.fdtab_offset = {self.fdtab_offset}
        fs.fdtab_offset = {self.fdtab_offset}
        fs.fd_offset = {self.fd_offset}\n'''

#qstr
class QSTR():
    def __init__(self, size = 12, name_offset = 8):
        self.size = size
        self.name_offset = name_offset

    def to_string(self):
        return f'qstr.size = {self.size}\nqstr.name_offset = {self.name_offset}\n'

#path
class Path():
    def __init__(self,
                 d_name_offset = 20,
                 d_iname_offset = 36,
                 d_parent_offset = 16,
                 d_op_offset = 80,
                 d_dname_offset = 32,
                 mnt_root_offset = 0,
                 mnt_parent_offset = -8,
                 mnt_mountpoint_offset = -4):
        self.d_name_offset = d_name_offset
        self.d_iname_offset = d_iname_offset
        self.d_parent_offset = d_parent_offset
        self.d_op_offset = d_op_offset
        self.d_dname_offset = d_dname_offset
        self.mnt_root_offset =mnt_root_offset
        self.mnt_parent_offset = mnt_parent_offset
        self.mnt_mountpoint_offset = mnt_mountpoint_offset

    def to_string(self):
        return f'''path.d_name_offset = {self.d_name_offset}
        path.d_iname_offset = {self.d_iname_offset}
        path.d_parent_offset = {self.d_parent_offset}
        path.d_op_offset = {self.d_op_offset}
        path.d_dname_offset = {self.d_dname_offset}
        path.mnt_root_offset = {self.mnt_root_offset}
        path.mnt_parent_offset = {self.mnt_parent_offset}
        path.mnt_mountpoint_offset = {self.mnt_mountpoint_offset}\n'''

def main():
    header_line = HeaderLine()
    osi_name = Name()
    osi_version = Version()
    task = Task()
    cred = Cred()
    mm = MM()
    vma = VMA()
    fs = FS()
    qstr = QSTR()
    osi_path = Path()

    with open("demo_osi.osi", "w", encoding='utf-8') as f:
        f.write(header_line.to_string())
        f.write(osi_name.to_string())
        f.write(osi_version.to_string())
        f.write(task.to_string())
        f.write(cred.to_string())
        f.write(mm.to_string())
        f.write(vma.to_string())
        f.write(fs.to_string())
        f.write(qstr.to_string())
        f.write(osi_path.to_string())
        f.close()

main()
