"""The core file for the plugin component of the EXERT system"""

import IPython
from pandare import PyPlugin, Panda
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
            args = '--nographic \
                -kernel ./vmlinuz \
                -initrd ./cache/customfs.cpio \
                -machine versatilepb \
                -append "console=ttyAMA0 earlyprintk=serial nokaslr init=/bin/sh root=/dev/ram0"'
            panda = Panda(
                arch='arm', mem='256M', extra_args=args,
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
