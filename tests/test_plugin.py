import subprocess
from pandare import Panda
import exert.usermode.task_struct_stack as tss
from exert.usermode import plugin
from exert.usermode.context import Context
from exert.usermode.rules import TASK_STRUCT
from exert.utilities.debug import RUN_PLUGIN_TESTS
from exert.utilities.types.multi_arch import CPUState, ExertCallable

# Kernel info taken from https://panda.re/kernelinfos/ubuntu:4.4.0-170-generic:32.conf

CALLED_BACK: bool = False
def set_called_back(called_back: bool) -> None:
    global CALLED_BACK
    CALLED_BACK = called_back

TEST_PREFIX: str = """
import tests.test_plugin
tests.test_plugin.run_test('{}', {}, '{}', tests.test_plugin.{})
"""
def do_test(test: ExertCallable, arch: str, generic: bool = True,
    kernel: (str | None) = None) -> None:

    if not RUN_PLUGIN_TESTS:
        return
    formatted = TEST_PREFIX.format(arch, generic, kernel, test.__name__)
    subprocess.run(['python'], input = formatted, check = True, text = True)

def run_test(arch: str, generic: bool, kernel: str, test: ExertCallable) -> None:
    set_called_back(False)
    def callback(panda: Panda, cpu: CPUState) -> None:
        set_called_back(True)
        test(panda, cpu)
    plugin.run(arch = arch, generic = generic, kernel = kernel, callback = callback)
    assert CALLED_BACK

def callback_test_ground_truth_tasklist(panda: Panda, cpu: CPUState) -> None:
    init_addr = 0xc1b1da80
    parent_offset = 804

    init_task = tss.read_mem(panda, cpu, init_addr, parent_offset + 4)

    parent_addr = tss.read_word(init_task, parent_offset)
    assert parent_addr == init_addr

def test_ground_truth_tasklist() -> None:
    do_test(callback_test_ground_truth_tasklist, 'i386')

def callback_test_get_task_from_current(panda: Panda, cpu: CPUState) -> None:
    task_addr = tss.task_address_arm_callback(panda, cpu)
    context = Context(panda)
    results = TASK_STRUCT.test(context, task_addr)
    assert results

def test_get_task_from_current() -> None:
    do_test(callback_test_get_task_from_current, 'arm')

def callback_test_nongeneric_kernel(panda: Panda, cpu: CPUState) -> None:
    pass

    # assert context.read(0x4, 4) is None
    # assert context.read(0x0, 1) == b'\x05'

def test_nongeneric_kernel_armv5l() -> None:
    do_test(callback_test_nongeneric_kernel, 'armv5l', generic=False,
            kernel='./kernels/vmlinuz-arm-3.2.51-1')

def test_nongeneric_kernel_aarch64() -> None:
    do_test(callback_test_nongeneric_kernel, 'aarch64',
            generic=False, kernel='./kernels/vmlinuz-aarch64-4.4.100')

def test_nongeneric_kernel_x86_64() -> None:
    do_test(callback_test_nongeneric_kernel, 'x86_64',
            generic=False, kernel='./kernels/vmlinuz-x86_64-4.4.100')

def test_plugin_kernel_supported() -> None:
    if not RUN_PLUGIN_TESTS:
        return
    subprocess.run(['python', '-u', '-m', 'exert.usermode.plugin', './kernels/vmlinuz-arm-3.2.51-1',
                    'armv5l', '3.2.51-1-versatile'], check = True)

def test_plugin_kernel_unsupported() -> None:
    if not RUN_PLUGIN_TESTS:
        return
    subprocess.run(['python', '-u', '-m', 'exert.usermode.plugin', './kernels/vmlinuz-arm-3.2.51-1',
                    'armv5l', '6.12.9'], check = True)
