# import subprocess
# from exert.usermode import plugin
# import exert.usermode.task_struct_stack as tss
# from exert.utilities.debug import RUN_PLUGIN_TESTS
# 
# CALLED_BACK = False
# def set_called_back(called_back):
#     global CALLED_BACK
#     CALLED_BACK = called_back
# 
# TEST_PREFIX = """
# import tests.test_task_struct
# import exert.usermode.task_struct_stack as tss
# tests.test_task_struct.run_test('{}', {}, '{}', tss.{})
# """
# 
# def do_test(test, arch, generic = True, kernel = None):
#     if not RUN_PLUGIN_TESTS:
#         return
#     formatted = TEST_PREFIX.format(arch, generic, kernel, test.__name__)
#     print(formatted)
#     subprocess.run(['python'], input = formatted, check = True, text = True)
# 
# def run_test(arch, generic, kernel, test):
#     set_called_back(False)
#     def callback(panda, cpu):
#         set_called_back(True)
#         test(panda, cpu)
#     plugin.run(arch = arch, generic = generic, kernel = kernel, callback = callback)
#     assert CALLED_BACK
# 
# def test_task_struct_arm_generic():
#     do_test(tss.task_address_arm_callback, 'arm')
# 
# def test_task_struct_arm_nongeneric():
#     do_test(tss.task_address_arm_callback, 'armv5l',
#             generic=False, kernel='./kernels/vmlinuz-arm-3.2.51-1')
# 
# def test_task_struct_i386_nongeneric():
#     do_test(tss.task_address_i386_callback, 'i386',
#             generic=False, kernel='./kernels/vmlinuz-i386-4.4.100')
# 
# def test_task_struct_x86_64_nongeneric():
#     do_test(tss.task_address_x86_64_callback, 'x86_64',
#             generic=False, kernel='./kernels/vmlinuz-x86_64-4.4.100')
#     
# def test_task_struct_aarch_nongeneric():
#     do_test(tss.task_address_aarch_callback, 'aarch64',
#             generic=False, kernel='./kernels/vmlinuz-aarch64-4.4.100')
#     return
