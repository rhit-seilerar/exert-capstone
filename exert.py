"""The black-box component to the EXERT system"""

import argparse
import os
import shutil
from subprocess import run

PANDA_CONTAINER = 'pandare/panda'
XMAKE_CONTAINER = 'ghcr.io/panda-re/embedded-toolchains'

def main(args = None):
    """Parse and interpret command line arguments"""
    parser = argparse.ArgumentParser(prog = 'EXERT')

    parser.add_argument('-d', '--docker', action = 'store_true',
        help = 'Run this command in the Pandare docker container. '
            'Will initialize the container if it does not exist.')
    subparsers = parser.add_subparsers()
    
    init_parser = subparsers.add_parser('init', help = 'Initialize the required dependencies and docker containers')
    init_parser.set_defaults(func = init)
    
    osi_parser = subparsers.add_parser('osi', help = 'Generate OSI information for the given kernel image')
    osi_parser.add_argument('image', nargs = '+', help = 'The kernel image to generate OSI information for.')
    osi_parser.set_defaults(func = osi)
    
    dev_parser = subparsers.add_parser('dev', help = 'Development tools')
    dev_subparsers = dev_parser.add_subparsers()
    dev_subparsers \
        .add_parser('reset', help = 'Kill all EXERT docker containers') \
        .set_defaults(func = reset)
    dev_subparsers \
        .add_parser('attach', help='Attach a shell to the panda container') \
        .set_defaults(func = lambda parsed : run_docker(PANDA_CONTAINER, name = 'pandare', persist = True))
    dev_subparsers \
        .add_parser('test', help='Run the unit tests for the EXERT system') \
        .set_defaults(func = lambda parsed : run_docker(PANDA_CONTAINER, name = 'pandare', command = 'pytest'))
    
    parsed = parser.parse_args()
    parsed.func(parsed)

def init(parsed):
    if shutil.which('docker') is None:
        print('Error: You must have docker installed to run EXERT.')
        return
    
    run(f'docker pull {PANDA_CONTAINER}:latest', check = True)
    run(f'docker pull {XMAKE_CONTAINER}:latest', check = True)
    
    print('EXERT successfully initialized!')

def reset(parsed):
    run('docker stop pandare', capture_output = True)

def osi(parsed):
    """Validate the provided image, and then generate its OSI information"""
    validate_initialized()
    for image in parsed.image:
        validate_iso(image)
        make_usermode(image)
    
    print('OSI not implemented.')

def run_docker(container, name = None, command = '', persist = False):
    validate_initialized()
    cwd = os.path.dirname(os.path.realpath(__file__))
    mount = f'-v "{cwd}/usermode:/mount"'
    if name is None:
        run(f'docker run --rm -it {mount} {container} bash -c "cd /mount; ./setup.sh; {command}"')
    else:
        if not container_is_running(name):
            run(f'docker run --rm -dit --name {name} {mount} {container}')
            run(f'docker exec -it {name} bash -c "cd /mount; ./setup.sh"')
        run(f'docker exec -it {name} bash -c "cd /mount; {command}"')
        if persist:
            run(f'docker exec -it {name} bash"')

def container_is_running(name):
    names = run('docker ps --format {{.Names}}', capture_output = True).stdout.decode().splitlines()
    try:
        names.index(name)
        return True
    except ValueError:
        return False

def validate_initialized():
    #TODO: Test if initialized
    pass

def make_usermode(image):
    #TODO: Compile usermode for specific version
    pass

def validate_iso(image):
    try:
        fo = open(image,'rb')
        cursor = 0x8000
        size = os.stat(image).st_size
        valid = cursor + 5 < size
        while cursor + 7 < size and valid:
            fo.seek(cursor)
            header_type = int.from_bytes(fo.read(1))
            header_identifier = fo.read(5).decode('ascii')
            header_version = int.from_bytes(fo.read(1))
            if header_identifier != 'CD001':
                valid = False
            if header_version != 1:
                valid = False
            if header_type == 255:
                break
            if header_type < 0 or header_type > 3:
                valid = False
            cursor += 0x800
        if not valid:
            print(f'The file {image} is not a valid kernel image.')
            exit(1)
    except FileNotFoundError:
        print(f'Could not find {image}.')
        exit(1)
    except UnicodeDecodeError:
        print(f'The file {image} is not a valid kernel image.')
        exit(1)

main()
