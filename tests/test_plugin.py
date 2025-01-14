import subprocess
from exert.usermode import plugin

# Kernel info taken from https://panda.re/kernelinfos/ubuntu:4.4.0-170-generic:32.conf

def read_mem(panda, cpu, addr, size):
    return panda.virtual_memory_read(cpu, addr, size)

def read_word(mem, offset):
    return int.from_bytes(mem[offset:offset+4], byteorder='little', signed=False)

CALLED_BACK = False
def set_called_back(called_back):
    global CALLED_BACK
    CALLED_BACK = called_back

TEST_PREFIX = """
import tests.test_plugin
tests.test_plugin.run_test('{}', {}, '{}', tests.test_plugin.{})
"""
def do_test(test, arch, generic = True, kernel = None):
    formatted = TEST_PREFIX.format(arch, generic, kernel, test.__name__)
    print(formatted)
    subprocess.run(['python'], input = formatted, check = True, text = True)

def run_test(arch, generic, kernel, test):
    set_called_back(False)
    def callback(panda, cpu):
        set_called_back(True)
        test(panda, cpu)
    plugin.run(arch = arch, generic = generic, kernel = kernel, callback = callback)
    assert CALLED_BACK

def callback_test_ground_truth_tasklist(panda, cpu):
    init_addr = 0xc1b1da80
    parent_offset = 804

    init_task = read_mem(panda, cpu, init_addr, parent_offset + 4)

    parent_addr = read_word(init_task, parent_offset)
    assert parent_addr == init_addr
def test_ground_truth_tasklist():
    do_test(callback_test_ground_truth_tasklist, 'i386')

def callback_test_get_current_from_stack(panda, cpu):
    sp = panda.arch.get_reg(cpu, 'SP')

    thread_info_addr = sp & ~(8192 - 1)
    thread_info = read_mem(panda, cpu, thread_info_addr, 80)

    task_addr = read_word(thread_info, 12)
    task = read_mem(panda, cpu, task_addr, 400)

    task_stack = read_word(task, 4)
    assert task_stack == thread_info_addr
def test_get_current_from_stack():
    do_test(callback_test_get_current_from_stack, 'arm')

def callback_test_nongeneric_kernel(panda, cpu):
    pass
def test_nongeneric_kernel_armv5l():
    do_test(callback_test_nongeneric_kernel, 'armv5l', generic=False, kernel='./vmlinuz')

def test_nongeneric_kernel_aarch64():
    do_test(callback_test_nongeneric_kernel, 'aarch64', generic=False, kernel='./vmlinuz-aarch64')

def test_nongeneric_kernel_x86_64():
    do_test(callback_test_nongeneric_kernel, 'x86_64', generic=False, kernel='./vmlinuz-x86_64')