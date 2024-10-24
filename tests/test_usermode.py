import os
import exert.utilities.command as cmd

def _test_compile_i386():
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
