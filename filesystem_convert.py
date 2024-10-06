from utilities import run_command

def filesystem_convert(path):
    cmd = 'ls ' + path + ' | cpio -o -D ' + path + ' -F ' + path + '.cpio'
    print('Attempting to create CPIO using command: ' + cmd)
    run_command(cmd)