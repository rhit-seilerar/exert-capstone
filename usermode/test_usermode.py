import os.path
import utilities as util

def _test_compile_i386():
    util.run_command('pushd usermode')
    util.run_command('make clean')
    util.run_command('make all ARCH=arm LIBC=musleabi')
    util.run_command('popd')
    assert os.path.isfile("usermode/build/helloworld")
    assert util.get_stdout(util.run_command("usermode/build/helloworld", True)).strip() \
        == "hello world"
    assert util.get_stderr(util.run_command("ldd usermode/build/helloworld", True)) \
        .strip() == "not a dynamic executable"
    print("Task successful!")
