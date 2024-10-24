"""The core file for the plugin component of the EXERT system"""

import os
import IPython
from pandare import PyPlugin, Panda
from exert.usermode.filesystem_convert import filesystem_convert

class Exert(PyPlugin):
    """The Exert plugin"""
    # pylint: disable=attribute-defined-outside-init
    def __preinit__(self, pypluginmgr, args):
        self.pypluginmgr = pypluginmgr
        self.args = args
        self.callback = args['callback'] if 'callback' in args else None
        print(self.callback)

    def __init__(self, panda):
        @panda.hook_symbol(None, 'getpid')
        def getpid_hook(cpu, tb, hook):
            print(f"Hooking into {panda.ffi.string(hook.sym.name).decode()}...")
            print(self.callback)
            if self.callback:
                self.callback(panda, cpu, tb, hook)
            else:
                IPython.embed()

def run(arch = 'i386', callback = None):
    filesystem_convert(f'{os.path.dirname(os.path.abspath(__file__))}/filesystem')
    # args="--nographic \
    #     --machine virt-2.6 \
    #     -kernel ./vmlinuz \
    #     -initrd ramdisk.img.gz \
    #     -append 'console=ttyS0 earlyprintk=serial nokaslr init=/linuxrc root=/dev/ram0'"
    # panda = Panda(arch='arm', mem="1G", extra_args=args)
    # panda.set_os_name("linux_32_ubuntu:4.4.0-98-generic")
    panda = Panda(generic=arch)
    # panda = Panda(generic='i386', extra_args = \
    #   '-initrd filesystem.cpio -kernel ./vmlinuz init=/helloworld root=/dev/ram1')

    panda.pyplugins.load(Exert, args={
        'callback': callback
    })

    @panda.queue_blocking
    def drive():
        panda.revert_sync("root")
        print(panda.run_serial_cmd('uname -r'))
        panda.end_analysis()

    panda.run()
