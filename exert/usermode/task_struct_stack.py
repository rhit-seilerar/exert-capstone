TASK_ADDRESS = None

def read_mem(panda, cpu, addr, size):
    return panda.virtual_memory_read(cpu, addr, size)

def read_word(mem, offset):
    return int.from_bytes(mem[offset:offset+4], byteorder='little', signed=False)

def read_long(mem, offset):
    return int.from_bytes(mem[offset:offset+8], byteorder='little', signed=False)

def task_address_arm_callback(panda, cpu):
    sp = panda.arch.get_reg(cpu, 'SP')

    thread_info_addr = sp & ~(8192 - 1)
    thread_info = read_mem(panda, cpu, thread_info_addr, 80)

    task_addr = read_word(thread_info, 12)
    task = read_mem(panda, cpu, task_addr, 400)

    task_stack = read_word(task, 4)
    assert task_stack == thread_info_addr

    global TASK_ADDRESS
    TASK_ADDRESS = task_addr

    return task_addr

def task_address_i386_callback(panda, cpu):
    assert panda.in_kernel(cpu)
    sp = panda.current_sp(cpu)

    thread_info_addr = sp & ~(8192 - 1)
    thread_info = read_mem(panda, cpu, thread_info_addr, 4)

    task_addr = read_word(thread_info, 0)
    task = read_mem(panda, cpu, task_addr, 8)

    task_stack = read_word(task, 4)
    assert task_stack == thread_info_addr

def task_address_x86_64_callback(panda, cpu):
    sp0_offset = 4
    esp0_ptr = cpu.env_ptr.tr.base + sp0_offset
    esp0_bytes = read_mem(panda, cpu, esp0_ptr, 8)
    esp0 = read_long(esp0_bytes, 0)

    thread_info_addr = esp0 - 16384
    thread_info = read_mem(panda, cpu, thread_info_addr, 36)
    task_addr = read_long(thread_info, 0)
    task = read_mem(panda, cpu, task_addr, 16)

    task_stack = read_long(task, 8)
    assert task_stack == thread_info_addr
    return task_addr
