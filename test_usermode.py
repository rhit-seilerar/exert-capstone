from utilities import *
import os.path
#test 1
def compile_i386():
    run_commands([
        "pushd usermode",
        "make clean",
        "make all",
        "popd"])
    if not os.path.isfile("usermode/build/helloworld"):
        raise Exception(f"{compile_i386.__name__} failed: No output was produced")

    if get_stdout(run_command("usermode/build/helloworld")) != "hello world\n":
        raise Exception(f"{compile_i386.__name__} failed: The output was not 'hello world'")

    if get_stderr(run_command("ldd usermode/build/helloworld")).strip() != "not a dynamic executable":
        raise Exception(f"{compile_i386.__name__} failed: The output was not statically linked")
    
    print("Task successful!")

def run_tests():
    compile_i386()
