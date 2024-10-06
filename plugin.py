"""The core file for the plugin component of the EXERT system"""

from pandare import PyPlugin

class Exert(PyPlugin):
    """The Exert plugin"""
    def __init__(self, panda):
        @panda.hook_symbol('', 'getpid')
        def on_hook(cpu, tb, hook):
            name = panda.ffi.string(hook.sym.name).decode()
            print(name)
            panda.interact()

if __name__ == '__main__':
    from pandare import Panda
    panda = Panda(generic='i386')

    panda.pyplugins.load(Exert)

    @panda.queue_blocking
    def drive():
        panda.revert_sync("root")
        print(panda.run_serial_cmd('bash -c "whoami"'))
        panda.end_analysis()

    panda.run()
