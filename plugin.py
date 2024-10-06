"""The core file for the plugin component of the EXERT system"""

from pandare import PyPlugin
import IPython

class Exert(PyPlugin):
    """The Exert plugin"""
    def __preinit__(self, pypluginmgr, args):
        self.pypluginmgr = pypluginmgr
        self.args = args
        self.callback = args['callback'] if 'callback' in args else None
    
    def __init__(self, panda):
        @panda.hook_symbol(None, 'getpid')
        def getpid_hook(cpu, tb, hook):
            print(f"Hooking into {panda.ffi.string(hook.sym.name).decode()}...")
            if self.callback:
                self.callback(panda, cpu, tb, hook)
            else:
                IPython.embed()

def main(callback):
    from pandare import Panda
    panda = Panda(generic='i386')

    panda.pyplugins.load(Exert, args={
        'callback': callback
    })

    @panda.queue_blocking
    def drive():
        panda.revert_sync("root")
        print(panda.run_serial_cmd('uname -a'))
        panda.end_analysis()

    panda.run()

if __name__ == '__main__':
    main(None)