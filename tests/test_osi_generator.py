import subprocess
from exert.utilities.debug import RUN_PLUGIN_TESTS

def test_osi_generator_arm():
    if not RUN_PLUGIN_TESTS:
        return
    subprocess.run(['python', '-u', '-m', 'exert.osi_generator', './kernels/vmlinuz-arm-4.4.100',
                    'armv5l', '4.4.100'], check = True)
    
def test_osi_generator_aarch():
    if not RUN_PLUGIN_TESTS:
        return
    subprocess.run(['python', '-u', '-m', 'exert.osi_generator', './kernels/vmlinuz-aarch64-4.4.100',
                    'aarch64', '4.4.100'], check = True)
    
def test_osi_generator_i386():
    if not RUN_PLUGIN_TESTS:
        return
    subprocess.run(['python', '-u', '-m', 'exert.osi_generator', './kernels/vmlinuz-i386-4.4.100',
                    'i386', '4.4.100'], check = True)

def test_osi_generator_unsupported_version():
    if not RUN_PLUGIN_TESTS:
        return
    subprocess.run(['python', '-u', '-m', 'exert.osi_generator', './kernels/vmlinuz-aarch64-4.4.100',
                    'aarch64', '6.12.1'], check = True) 

def test_osi_generator_unsupported_arch():
    if not RUN_PLUGIN_TESTS:
        return
    subprocess.run(['python', '-u', '-m', 'exert.osi_generator', './kernels/vmlinuz-aarch64-4.4.100',
                    'ia64', '6.12.1'], check = True)

def test_osi_generator_nonexistent_kernel():
    if not RUN_PLUGIN_TESTS:
        return
    subprocess.run(['python', '-u', '-m', 'exert.osi_generator', './kernels/vmlinuz-idontexist-4.5.1',
                    'aarch64', '4.4.100'], check = True) 