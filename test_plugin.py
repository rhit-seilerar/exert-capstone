import plugin

def run_tests():
    def callback(panda, cpu, tb, hook):
        mem = panda.virtual_memory_read(cpu, panda.arch.get_pc(cpu), 64)
        print (' '.join([f"{byte:02X}" for byte in mem]))
    
    plugin.main(callback)