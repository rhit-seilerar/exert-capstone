import utilities
import os.path
#test 1
def compile_i386():
    utilities.run_command("pushd usermode") #temporarily go into usermode
    utilities.run_command("make clean")
    utilities.run_command("make all")
    if not os.path.isfile("test"):
        raise Exception(f"{compile_i386.__name__} failed")
    if (utilities.run_command("helloworld") == "hello world\n"):
        print("Task successful!")
    utilities.run_command("popd") #returns us back

def run_tests():
    compile_i386()
