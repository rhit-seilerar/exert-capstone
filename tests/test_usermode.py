import os
import exert.utilities.command as cmd
import subprocess

from exert.utilities.debug import RUN_PLUGIN_TESTS
from exert.usermode import plugin

CALLED_BACK = False
def set_called_back(called_back):
    global CALLED_BACK
    CALLED_BACK = called_back

TEST_PREFIX = """
import tests.test_usermode as ttu
ttu.run_test('{}', {}, '{}', ttu.{})
"""

def do_test(test, arch, generic = True, kernel = None):
    if not RUN_PLUGIN_TESTS:
        return
    formatted = TEST_PREFIX.format(arch, generic, kernel, test.__name__)
    print(formatted)
    subprocess.run(['python'], input = formatted, check = True, text = True)

def run_test(arch, generic, kernel, test):
    set_called_back(False)

    def callback(panda, cpu):
        return
    
    def hypervisor_callback(panda, cpu):
        set_called_back(True)
        test(panda, cpu)

    plugin.run(arch = arch, callback = callback, generic = generic,
               kernel = kernel, usermode = 'file_reader-' + arch,
               command = './user_prog /init', hypercall_callback = hypervisor_callback)
    assert CALLED_BACK

def file_reader_callback(panda, cpu):
    magic = panda.arch.get_arg(cpu, 0, convention='syscall')
    type = panda.arch.get_arg(cpu, 1, convention='syscall')
    assert magic == 0
    assert type == 3
    return

def test_i386_file_reader():
    do_test(file_reader_callback, 'i386',
            generic=False, kernel='./kernels/vmlinuz-i386-4.4.100')

def test_x86_file_reader():
    do_test(file_reader_callback, 'x86_64',
            generic=False, kernel='./kernels/vmlinuz-x86_64-4.4.100')
    
def test_armv5l_file_reader():
    do_test(file_reader_callback, 'armv5l',
            generic=False, kernel='./kernels/vmlinuz-arm-3.2.51-1')

def test_aarch64_file_reader():
    do_test(file_reader_callback, 'aarch64',
            generic=False, kernel='./kernels/vmlinuz-aarch64-4.4.100')

def _test_compile():
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
