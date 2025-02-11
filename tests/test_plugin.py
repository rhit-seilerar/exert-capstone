import subprocess
import exert.usermode.task_struct_stack as tss
from exert.usermode import plugin
from exert.usermode.context import Context
from exert.usermode.rules import TASK_STRUCT

# Kernel info taken from https://panda.re/kernelinfos/ubuntu:4.4.0-170-generic:32.conf

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

    init_task = tss.read_mem(panda, cpu, init_addr, parent_offset + 4)

    parent_addr = tss.read_word(init_task, parent_offset)
    assert parent_addr == init_addr
def test_ground_truth_tasklist():
    do_test(callback_test_ground_truth_tasklist, 'i386')

def callback_test_get_current_from_stack(panda, cpu):
    sp = panda.arch.get_reg(cpu, 'SP')

    thread_info_addr = sp & ~(8192 - 1)
    thread_info = tss.read_mem(panda, cpu, thread_info_addr, 80)

    task_addr = tss.read_word(thread_info, 12)
    task = tss.read_mem(panda, cpu, task_addr, 400)

    task_stack = tss.read_word(task, 4)
    assert task_stack == thread_info_addr
    return task_addr

def callback_test_get_current_from_stack_x86_64(panda, cpu): # Tested with 4.4.100
    sp0_offset = 4
    esp0_ptr = cpu.env_ptr.tr.base + sp0_offset
    esp0_bytes = tss.read_mem(panda, cpu, esp0_ptr, 8)
    esp0 = tss.read_long(esp0_bytes, 0)

    thread_info_addr = esp0 - 16384
    thread_info = tss.read_mem(panda, cpu, thread_info_addr, 36)
    task_addr = tss.read_long(thread_info, 0)
    task = tss.read_mem(panda, cpu, task_addr, 16)

    task_stack = tss.read_long(task, 8)
    assert task_stack == thread_info_addr
    return task_addr

def callback_test_get_current_from_stack_i386(panda, cpu):
    assert panda.in_kernel(cpu)
    sp = panda.current_sp(cpu)

    thread_info_addr = sp & ~(8192 - 1)
    thread_info = tss.read_mem(panda, cpu, thread_info_addr, 4)

    task_addr = tss.read_word(thread_info, 0)
    task = tss.read_mem(panda, cpu, task_addr, 8)

    task_stack = tss.read_word(task, 4)
    assert task_stack == thread_info_addr

def test_get_current_from_stack_arm():
    do_test(callback_test_get_current_from_stack, 'arm')

def test_get_current_from_stack_arm_nongeneric():
    do_test(callback_test_get_current_from_stack, 'armv5l',
            generic=False, kernel='./kernels/vmlinuz-arm')

def test_get_current_from_stack_x86_64():
    do_test(callback_test_get_current_from_stack_x86_64, 'x86_64',
            generic=False, kernel='./kernels/vmlinuz-x86_64-2')

def test_get_current_from_stack_i386():
    do_test(callback_test_get_current_from_stack_i386, 'i386',
            generic=False, kernel='./kernels/vmlinuz-i386')

def callback_test_get_task_from_current(panda, cpu):
    task_addr = callback_test_get_current_from_stack(panda, cpu)
    context = Context(panda)
    results = TASK_STRUCT.test(context, task_addr)
    assert results
def test_get_task_from_current():
    do_test(callback_test_get_task_from_current, 'arm')

def callback_test_nongeneric_kernel(panda, cpu):
    pass

    # assert context.read(0x4, 4) is None
    # assert context.read(0x0, 1) == b'\x05'

def test_nongeneric_kernel_armv5l():
    do_test(callback_test_nongeneric_kernel, 'armv5l', generic=False,
            kernel='./kernels/vmlinuz-arm')

def test_nongeneric_kernel_aarch64():
    do_test(callback_test_nongeneric_kernel, 'aarch64',
            generic=False, kernel='./kernels/vmlinuz-aarch64')

def test_nongeneric_kernel_x86_64():
    do_test(callback_test_nongeneric_kernel, 'x86_64',
            generic=False, kernel='./kernels/vmlinuz-x86_64')

def test_nongeneric_kernel_x86_64_2():
    do_test(callback_test_nongeneric_kernel, 'x86_64',
            generic=False, kernel='./kernels/vmlinuz-x86_64-2')

def test_nongeneric_kernel_mips():
    do_test(callback_test_nongeneric_kernel, 'mips',
            generic=False, kernel='./kernels/vmlinux-mips')

KERNEL_SUPPORTED_PREFIX = """
from exert.usermode import plugin
plugin.get_task_address('./kernels/vmlinuz-arm', 'armv5l', '3.2.0-4-versatile')
"""

def test_plugin_kernel_supported():
    subprocess.run(['python'], input = KERNEL_SUPPORTED_PREFIX, check = True, text = True)

KERNEL_UNSUPPORTED_PREFIX = """
from exert.usermode import plugin
plugin.get_task_address('./kernels/vmlinuz-arm', 'armv5l', '6.12.9')
"""

def test_plugin_kernel_unsupported():
    subprocess.run(['python'], input = KERNEL_UNSUPPORTED_PREFIX, check = True, text = True)
