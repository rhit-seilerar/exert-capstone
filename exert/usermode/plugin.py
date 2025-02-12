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

    def __init__(self, panda):
        self.called_back = False

        #What we use to control the filereader.c program?
        #write tests for hypercall, see if it returns correct fd or just True for now.
        # def fd_finder(env):
        #     x = run_command('./file_reader.c demo_osi.osi')
        #     print(f'{x}')
        #     return x
        # @panda.cb_guest_hypercall
        # def fd_reader():
        #     print('Not an octopus.\n')

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
                run(arch, task_struct_stack.task_address_arm_callback, False, kernel)
                print("Task Address: " + hex(task_struct_stack.TASK_ADDRESS))
    if not version_supported:
        print("Version not supported")

if __name__ == '__main__':
    get_task_address(sys.argv[1], sys.argv[2], sys.argv[3])
