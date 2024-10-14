import plugin

# Kernel info taken from https://panda.re/kernelinfos/ubuntu:4.4.0-170-generic:32.conf

def run_tests():
    def callback(panda, cpu, tb, hook):
        init_addr = 0xc1b1da80
        parent_offset = 804
        mem = panda.virtual_memory_read(cpu, init_addr + parent_offset, 4)
        parent_addr = int.from_bytes(mem, 'little')
        print(f'{parent_addr:02X}')
        assert parent_addr == init_addr
    
    plugin.main(callback)
