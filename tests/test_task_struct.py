import subprocess
from typing import cast
from pandare.panda import Panda
from exert.usermode import plugin
import exert.usermode.task_struct_stack as tss
from exert.utilities.debug import RUN_PLUGIN_TESTS
from exert.utilities.types.multi_arch import ExertCallable, CPUState

CALLED_BACK: bool = False
def set_called_back(called_back: bool) -> None:
    global CALLED_BACK
    CALLED_BACK = called_back

TEST_PREFIX: str = """
import tests.test_task_struct
import exert.usermode.task_struct_stack as tss
tests.test_task_struct.run_test('{}', {}, '{}', tss.{})
"""

def do_test(test: ExertCallable, arch: str, generic: bool = True,
            kernel: (str | None) = None) -> None:
    if not RUN_PLUGIN_TESTS:
        return
    formatted = TEST_PREFIX.format(arch, generic, kernel, test.__name__)
    print(formatted)
    subprocess.run(['python'], input = formatted, check = True, text = True)

def run_test(arch: str, generic: bool, kernel: str, test: ExertCallable) -> None:
    set_called_back(False)
    def callback(panda: Panda, cpu: CPUState) -> None:
        set_called_back(True)
        test(panda, cpu)
    plugin.run(arch = arch, generic = generic, kernel = kernel, callback = callback)
    assert CALLED_BACK

def test_task_struct_arm_generic() -> None:
    do_test(tss.task_address_arm_callback, 'arm')

def test_task_struct_arm_nongeneric() -> None:
    do_test(tss.task_address_arm_callback, 'armv5l',
            generic=False, kernel='./kernels/vmlinuz-arm-3.2.51-1')

def test_task_struct_i386_nongeneric() -> None:
    do_test(tss.task_address_i386_callback, 'i386',
            generic=False, kernel='./kernels/vmlinuz-i386-4.4.100')

def test_task_struct_x86_64_nongeneric() -> None:
    do_test(cast(ExertCallable, tss.task_address_x86_64_callback), 'x86_64',
            generic=False, kernel='./kernels/vmlinuz-x86_64-4.4.100')

def test_task_struct_aarch_nongeneric() -> None:
    do_test(tss.task_address_aarch_callback, 'aarch64',
            generic=False, kernel='./kernels/vmlinuz-aarch64-4.4.100')
