import utilities
import os.path
#test 1
def compile_i386():
    utilities.run_commands([
        "pushd usermode",
        "make clean",
        "make all",
        "popd"])
    if not os.path.isfile("usermode/helloworld"):
        raise Exception(f"{compile_i386.__name__} failed")

    if not utilities.run_command("usermode/helloworld") == "hello world\n":
        raise Exception(f"{compile_i386.__name__} failed")
    
    print("Task successful!")

def run_tests():
    compile_i386()
