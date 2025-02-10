"""The core file for the plugin component of the EXERT system"""

import sys
import IPython
from pandare import PyPlugin, Panda
from exert.utilities.command import run_command

TASK_ADDRESS = None

class Exert(PyPlugin):
    """The Exert plugin"""
    # pylint: disable=attribute-defined-outside-init
    def __preinit__(self, pypluginmgr, args):
        self.pypluginmgr = pypluginmgr
        self.args = args
        self.callback = args['callback'] if 'callback' in args else None

    def __init__(self, panda):
        self.called_back = False

        # TODO: Find a way to cover these
        @panda.ppp('syscalls2', 'on_sys_execve_enter')
        # pragma: no cover
        def hook_syscall(cpu, pc, filename, argv, envp):
            if self.called_back:
                return
            print('Hooking into sys_execve...')
            panda.enable_callback('single_step')

        @panda.cb_start_block_exec
        # pragma: no cover
        def single_step(cpu, tb):
            if panda.in_kernel_mode(cpu):
                panda.disable_callback('single_step')
                self.called_back = True
                if self.callback:
                    self.callback(panda, cpu)
                else:
                    IPython.embed()

        panda.disable_callback('single_step')

def run(arch = 'i386', callback = None, generic = True, kernel = None):
    panda = None
    if generic:
        panda = Panda(generic = arch)
    else:
        run_command(f'./make_initrd.sh {arch}')
        if (arch in ['armv4l', 'armv5l', 'armv6l', 'armv7l']):
            args = f'--nographic \
                -kernel {kernel} \
                -initrd ./cache/customfs.cpio \
                -machine versatilepb \
                -append "console=ttyAMA0 earlyprintk=serial nokaslr init=/bin/sh root=/dev/ram0"'
            panda = Panda(
                arch='arm', mem='256M', extra_args=args,
                expect_prompt='/.*#', os_version='linux-32-generic')
        elif arch in ['aarch64']:
            args = f'--nographic \
                -kernel {kernel} \
                -initrd ./cache/customfs.cpio \
                -machine virt \
                -cpu cortex-a53 \
                -append "console=ttyAMA0 earlyprintk=serial nokaslr init=/bin/sh root=/dev/ram0"'
            panda = Panda(
                arch='aarch64', mem='256M', extra_args=args,
                expect_prompt='~ # ', os_version='linux-64-generic')
        else:
            args = f'--nographic \
                -kernel {kernel} \
                -initrd ./cache/customfs.cpio \
                -append "console=ttyS0 earlyprintk=serial nokaslr init=/bin/sh root=/dev/ram0"'
            panda = Panda(
                arch=arch, mem='256M', extra_args=args,
                expect_prompt='/.*#', os_version='linux-32-generic')

    panda.pyplugins.load(Exert, args={
        'callback': callback
    })

    @panda.queue_blocking
    def drive():
        if generic:
            panda.revert_sync("root")
        print(panda.run_serial_cmd('uname -r'))
        panda.end_analysis()

    panda.run()

def get_task_address(kernel, arch, version):
    version_supported = False

    version = version.split('-')[0]
    version_nums = version.split('.')
    version_nums[0] = int(version_nums[0], 10)
    version_nums[1] = int(version_nums[1], 10)
    version_nums[2] = int(version_nums[2], 10)

    if (arch in ['armv4l', 'armv5l', 'armv6l', 'armv7l']):
        version_greater_than_min = version_nums[0] > 2 or \
            (version_nums[0] == 2 and version_nums[1] > 6) or \
                (version_nums[0] == 2 and version_nums[1] == 6 and version_nums[2] >= 13)
        if version_greater_than_min:
            version_less_than_max = version_nums[0] < 5 or \
                (version_nums[0] == 5 and version_nums[1] < 14) or \
                    (version_nums[0] == 5 and version_nums[1] == 14 and version_nums[2] <= 21)
            if version_less_than_max:
                version_supported = True
                run(arch, task_address_arm_callback, False, kernel)
                print("Task Address: " + hex(TASK_ADDRESS))
    if not version_supported:
        print("Version not supported")

def read_mem(panda, cpu, addr, size):
    return panda.virtual_memory_read(cpu, addr, size)

def read_word(mem, offset):
    return int.from_bytes(mem[offset:offset+4], byteorder='little', signed=False)

def task_address_arm_callback(panda, cpu):
    sp = panda.arch.get_reg(cpu, 'SP')

    thread_info_addr = sp & ~(8192 - 1)
    thread_info = read_mem(panda, cpu, thread_info_addr, 80)

    task_addr = read_word(thread_info, 12)
    task = read_mem(panda, cpu, task_addr, 400)

    task_stack = read_word(task, 4)
    assert task_stack == thread_info_addr

    global TASK_ADDRESS
    TASK_ADDRESS = task_addr

    return task_addr

if __name__ == '__main__':
    get_task_address(sys.argv[1], sys.argv[2], sys.argv[3])
