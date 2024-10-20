from utilities import *
import os.path

def _test_compile_i386():
    run_commands([
        "pushd usermode",
        "make clean",
        "make all ARCH=arm LIBC=musleabi",
        "popd"])
    assert os.path.isfile("usermode/build/helloworld")
    assert get_stdout(run_command("usermode/build/helloworld")) == "hello world\n"
    assert get_stderr(run_command("ldd usermode/build/helloworld")).strip() == "not a dynamic executable"
    print("Task successful!")
