import os.path
import utilities

def _test_compile_i386():
    utilities.run_commands([
        "pushd usermode",
        "make clean",
        "make all ARCH=arm LIBC=musleabi",
        "popd"])
    assert os.path.isfile("usermode/build/helloworld")
    assert utilities.get_stdout(utilities.run_command("usermode/build/helloworld", True)) == "hello world\n"
    assert utilities.get_stderr(utilities.run_command("ldd usermode/build/helloworld", True)).strip() \
        == "not a dynamic executable"
    print("Task successful!")
