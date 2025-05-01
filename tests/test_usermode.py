import os
import subprocess

from pandare import Panda

import exert.utilities.command as cmd
from exert.utilities.debug import RUN_PLUGIN_TESTS
from exert.usermode import plugin
from exert.utilities.types.multi_arch import CPUState, ExertCallable

CALLED_BACK: bool = False
def set_called_back(called_back: bool) -> None:
    global CALLED_BACK
    CALLED_BACK = called_back

TEST_PREFIX = """
import tests.test_usermode as ttu
ttu.run_test('{}', {}, '{}', ttu.{})
"""

def do_test(test: ExertCallable, arch:str, generic: bool = True, kernel: (str | None) = None) -> None:
    if not RUN_PLUGIN_TESTS:
        return
    formatted = TEST_PREFIX.format(arch, generic, kernel, test.__name__)
    print(formatted)
    subprocess.run(['python'], input = formatted, check = True, text = True)

def run_test(arch: str, generic: bool, kernel: str, test: ExertCallable) -> None:
    set_called_back(False)

    def callback(panda: Panda, cpu: CPUState) -> None:
        return

    def hypervisor_callback(panda: Panda, cpu: CPUState) -> None:
        set_called_back(True)
        test(panda, cpu)

    plugin.run(arch = arch, callback = callback, generic = generic,
               kernel = kernel, usermode = 'file_reader-' + arch,
               command = './user_prog /init', hypercall_callback = hypervisor_callback)
    assert CALLED_BACK

def file_reader_callback(panda:Panda, cpu: CPUState) -> None:
    magic = panda.arch.get_arg(cpu, 0, convention='syscall')
    typ = panda.arch.get_arg(cpu, 1, convention='syscall')
    assert magic == 0
    assert typ == 3

def test_i386_file_reader() -> None:
    do_test(file_reader_callback, 'i386',
            generic=False, kernel='./kernels/vmlinuz-i386-4.4.100')

def test_x86_file_reader() -> None:
    do_test(file_reader_callback, 'x86_64',
            generic=False, kernel='./kernels/vmlinuz-x86_64-4.4.100')

def test_armv5l_file_reader() -> None:
    do_test(file_reader_callback, 'armv5l',
            generic=False, kernel='./kernels/vmlinuz-arm-3.2.51-1')

def test_aarch64_file_reader() -> None:
    do_test(file_reader_callback, 'aarch64',
            generic=False, kernel='./kernels/vmlinuz-aarch64-4.4.100')

def _test_compile() -> None:
    cmd.run_command('pushd usermode')
    cmd.run_command('make clean')
    cmd.run_command('make all ARCH=arm LIBC=musleabi')
    cmd.run_command('popd')
    assert os.path.isfile("usermode/build/helloworld")
    assert cmd.get_stdout(cmd.run_command("usermode/build/helloworld", True)).strip() \
        == "hello world"
    assert cmd.get_stderr(cmd.run_command("ldd usermode/build/helloworld", True)) \
        .strip() == "not a dynamic executable"
    print("Task successful!")
