from utilities import *
import os.path
#test 1
def compile_i386():
    run_commands([
        "pushd usermode",
        "make clean",
        "make i386",
        "popd"])
    if not os.path.isfile("usermode/helloworld"):
        raise Exception(f"{compile_i386.__name__} failed")

    if get_stdout(run_command("usermode/helloworld")) != "hello world\n":
        raise Exception(f"{compile_i386.__name__} failed")

    #print("Not an octopus\n")
    if get_stderr(run_command("ldd usermode/helloworld")).strip() != "not a dynamic executable":
        raise Exception(f"{compile_i386.__name__} failed")
    
    print("Task successful!")

def run_tests():
    compile_i386()
