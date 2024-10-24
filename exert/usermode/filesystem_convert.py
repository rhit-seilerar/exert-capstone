import subprocess

def filesystem_convert(path):
    cmd = f'ls {path} | cpio -o -D {path} -F {path}.cpio'
    print('Attempting to create CPIO using command: ' + cmd)
    subprocess.run(cmd, check = True, capture_output = False, shell = True)
