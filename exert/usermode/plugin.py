"""The core file for the plugin component of the EXERT system"""

import sys
import IPython
from pandare import PyPlugin, Panda
from exert.usermode import task_struct_stack
from exert.utilities.command import run_command

class Exert(PyPlugin):
    """The Exert plugin"""
    # pylint: disable=attribute-defined-outside-init
    def __preinit__(self, pypluginmgr, args):
        self.pypluginmgr = pypluginmgr
        self.args = args
        self.callback = args['callback'] if 'callback' in args else None
        self.hypercall_callback = args['hypercall_callback'] if 'hypercall_callback' in args else None

    def __init__(self, panda):
        self.called_back = False

        # TODO: Find a way to cover these
        @panda.ppp('syscalls2', 'on_sys_execve_enter')
        def hook_syscall(cpu, pc, filename, argv, envp): # pragma: no cover
            if self.called_back:
                return
            print('Hooking into sys_execve...')
            panda.enable_callback('single_step')
            panda.enable_callback('hypercall')

        @panda.cb_guest_hypercall
        def hypercall(cpu):
            panda.disable_callback('hypercall') # pragma: no cover
            self.called_back = True
            if self.hypercall_callback:
                self.hypercall_callback(panda, cpu)
            else:
                IPython.embed()

        @panda.cb_start_block_exec
        def single_step(cpu, tb): # pragma: no cover
            if panda.in_kernel_mode(cpu):
                panda.disable_callback('single_step')
                self.called_back = True
                if self.callback:
                    self.callback(panda, cpu)
                else:
                    IPython.embed()

        panda.disable_callback('single_step')
        panda.disable_callback('hypercall')

def create_panda(arch, mem, extra_args, prompt, os_version):
    return Panda(arch, mem, extra_args, prompt, os_version)

def run(arch = 'i386', callback = None, generic = True, kernel = None,
    usermode = None, command = None, hypercall_callback = None):
    panda = None
    arch_type = arch
    mem_use = '256M'
    my_prompt = '/.*#'
    my_os_version = 'linux-32-generic'
    extra_args_part = ''
    my_console = 'ttyAMA0'
    if generic:
        panda = Panda(generic = arch)
    else:
        if usermode:
            if command:
                run_command(f'./make_initrd.sh {arch} {usermode} "{command}"')
            else:
                run_command(f'./make_initrd.sh {arch} {usermode}')
        else:
            run_command(f'./make_initrd.sh {arch}')
        if (arch in ['armv4l', 'armv5l', 'armv6l', 'armv7l']):
            extra_args_part = '-machine versatilepb'
            arch_type = 'arm'
        elif arch in ['aarch64']:
            extra_args_part = '-machine virt \
                -cpu cortex-a53'
            my_prompt = '~ #'
            my_os_version = 'linux-64-generic'
        else:
            my_console = 'ttyS0'
        args = f'--nographic \
            -kernel {kernel} \
            -initrd ./cache/customfs.cpio \
            {extra_args_part}\
            -append "console={my_console} earlyprintk=serial nokaslr init=/bin/sh root=/dev/ram0"'
        panda = create_panda(
            arch=arch_type, mem=mem_use, extra_args=args,
            prompt=my_prompt, os_version=my_os_version)

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
                run(arch, task_struct_stack.task_address_arm_callback, False, kernel)
                print("Task Address: " + hex(task_struct_stack.TASK_ADDRESS))
    if not version_supported:
        print("Version not supported")

if __name__ == '__main__':
    get_task_address(sys.argv[1], sys.argv[2], sys.argv[3])
