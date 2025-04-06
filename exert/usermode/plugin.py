"""The core file for the plugin component of the EXERT system"""

import sys
from typing import Any
import IPython
from pandare import PyPlugin, Panda
from exert.usermode import task_struct_stack
from exert.utilities.command import run_command
from exert.utilities import version as ver


class Exert(PyPlugin):
    """The Exert plugin"""
    # pylint: disable=attribute-defined-outside-init
    def __preinit__(self, pypluginmgr: Any, args: list[str]):
        self.pypluginmgr = pypluginmgr
        self.args = args
        self.callback = args['callback'] if 'callback' in args else None
        self.hypercall_callback = args['hypercall_callback'] \
            if 'hypercall_callback' in args else None

    def __init__(self, panda: Panda):
        self.called_back = False

        @panda.ppp('syscalls2', 'on_sys_execve_enter')
        def hook_syscall(cpu, pc, filename: str, argv: list, envp):
            if self.called_back:
                return
            print('Hooking into sys_execve...')
            panda.enable_callback('single_step')
            panda.enable_callback('hypercall')

        @panda.cb_guest_hypercall
        def hypercall(cpu):
            panda.disable_callback('hypercall')
            self.called_back = True
            if self.hypercall_callback:
                self.hypercall_callback(panda, cpu)
            else:
                IPython.embed()

        @panda.cb_start_block_exec
        def single_step(cpu, tb):
            if panda.in_kernel_mode(cpu):
                panda.disable_callback('single_step')
                self.called_back = True
                if self.callback:
                    self.callback(panda, cpu)
                else:
                    IPython.embed()

        panda.disable_callback('single_step')
        panda.disable_callback('hypercall')

def run(arch: str = 'i386', callback: str = None, generic: bool = True, kernel: str = None,
    usermode: bool = None, command: str = None, hypercall_callback: Any|None = None):
    panda = None
    if generic:
        panda = Panda(generic = arch)
    else:
        if not usermode:
            usermode = ""
        if not command:
            command = ""
        run_command(f'./make_initrd.sh {arch} {usermode} "{command}"')

        arch_type = arch
        mem_use = "256M"
        hardware_args = ''
        console_ver = "ttyAMA0"
        expect_prompt_entry = '\/ # '
        os_ver_entry = 'linux-32-generic'
        if (arch in ['armv4l', 'armv5l', 'armv6l', 'armv7l']):
            hardware_args = '-machine versatilepb'
            arch_type = 'arm'
        elif arch in ['aarch64']:
            hardware_args = "-machine virt -cpu cortex-a53"
            expect_prompt_entry = '~ # '
            arch_type = 'aarch64'
            os_ver_entry = 'linux-64-generic'
        else:
            console_ver = 'ttyS0'

        args = f'--nographic \
            -kernel {kernel} \
            -initrd ./cache/customfs.cpio \
            {hardware_args} \
            -append "console={console_ver} earlyprintk=serial nokaslr init=/bin/sh root=/dev/ram0"'
        panda = Panda(
            arch=arch_type, mem=mem_use, extra_args=args,
            expect_prompt=expect_prompt_entry, os_version=os_ver_entry)


    panda.pyplugins.load(Exert, args={
        'callback': callback,
        'hypercall_callback': hypercall_callback
    })

    @panda.queue_blocking
    def drive():
        if generic:
            panda.revert_sync("root")
        print(panda.run_serial_cmd('uname -r'))
        panda.end_analysis()

    panda.run()

def get_task_address(kernel: str, arch: str, version: str):
    version_supported = False

    ver_entry = ver.version_from_string(version)

    print("LOCATING TASK ADDRESS")
    min_ver = ver.Version(2,6,13)
    max_ver = ver.Version(5,14,21)
    if (arch in ['armv4l', 'armv5l', 'armv6l', 'armv7l']):
        if(ver.compare_version(ver_entry, min_ver) and ver.compare_version(max_ver, ver_entry)):
            version_supported = True
            run(arch, task_struct_stack.task_address_arm_callback, False, kernel)
            print("Task Address: " + hex(task_struct_stack.TASK_ADDRESS))
    if not version_supported:
        print("Version not supported")

if __name__ == '__main__':
    get_task_address(sys.argv[1], sys.argv[2], sys.argv[3])
