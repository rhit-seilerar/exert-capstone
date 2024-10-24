from exert.usermode import plugin

# Kernel info taken from https://panda.re/kernelinfos/ubuntu:4.4.0-170-generic:32.conf

CALLBACK_WAS_CALLED = False
def test_ground_truth_tasklist():
    # pylint: disable=unused-argument
    global CALLBACK_WAS_CALLED
    CALLBACK_WAS_CALLED = False
    def callback(panda, cpu, tb, hook):
        global CALLBACK_WAS_CALLED
        CALLBACK_WAS_CALLED = True
        init_addr = 0xc1b1da80
        parent_offset = 804
        mem = panda.virtual_memory_read(cpu, init_addr + parent_offset, 4)
        parent_addr = int.from_bytes(mem, 'little')
        print(f'{parent_addr:02X}')
        assert parent_addr == init_addr
    plugin.run(callback = callback)
    assert CALLBACK_WAS_CALLED

def test_get_current_tasklist():
    # pylint: disable=unused-argument
    def callback(panda, cpu, tb, hook):
        # We're going to keep using the ground-truth offset for now
        parent_offset = 804
        # In linux kernel 2.6.26 and up, per-cpu info (such as the current task) was moved to
        # a static pointer stored in the .data or .data..percpu section.
        # We can stil test earlier versions though. Previously, a the current task pointer was
        # stored at the base of the stack, e.g. masking off either 12 or 13 bits.
        stack_pointer_name = list(panda.arch.registers.keys())[panda.arch.reg_sp]
        stack_pointer = panda.arch.get_reg(cpu, stack_pointer_name)
        current_task_4k = stack_pointer & 0xfffff000
        current_task_8k = stack_pointer & 0xffffe000
        mem_8k = panda.virtual_memory_read(cpu, current_task_8k + parent_offset, 4)
        mem_4k = panda.virtual_memory_read(cpu, current_task_4k + parent_offset, 4)
        parent_addr_4k = int.from_bytes(mem_4k, 'little')
        parent_addr_8k = int.from_bytes(mem_8k, 'little')
        assert parent_addr_4k == current_task_4k or parent_addr_8k == current_task_8k
    plugin.run(callback = callback)
