"""The black-box component to the EXERT system"""

import argparse
import os
import sys
import shutil
from exert.utilities.command import run_command, get_stdout

PANDA_CONTAINER = 'pandare/panda'
XMAKE_CONTAINER = 'ghcr.io/panda-re/embedded-toolchains'

def main():
    """Parse and interpret command line arguments"""
    parser = argparse.ArgumentParser(prog = 'EXERT')

    parser.add_argument('-d', '--docker', action = 'store_true',
        help = 'Run this command in the Pandare docker container. '
            'Will initialize the container if it does not exist.')
    subparsers = parser.add_subparsers()

    init_parser = subparsers.add_parser('init',
        help = 'Initialize the required dependencies and docker containers')
    init_parser.set_defaults(func = init)

    osi_parser = subparsers.add_parser('osi', \
        help = 'Generate OSI information for the given kernel image')
    osi_parser.add_argument('image', nargs = '+', \
        help = 'The kernel image to generate OSI information for.')
    osi_parser.set_defaults(func = osi)

    dev_parser = subparsers.add_parser('dev', help = 'Development tools')
    dev_subparsers = dev_parser.add_subparsers()
    dev_subparsers \
        .add_parser('reset', help = 'Kill all EXERT docker containers') \
        .set_defaults(func = reset)
    dev_subparsers \
        .add_parser('attach', help='Attach a shell to the panda container') \
        .set_defaults(func = lambda parsed:
            run_docker(PANDA_CONTAINER, name = 'pandare', persist = True))
    dev_subparsers \
        .add_parser('test', help='Run the unit tests for the EXERT system') \
        .set_defaults(func = lambda parsed:
            run_docker(PANDA_CONTAINER, name = 'pandare', command = 'pytest --cov=exert tests/'))
    parsed = parser.parse_args()
    parsed.func(parsed)

# pylint: disable=unused-argument
def init(parsed):
    if shutil.which('docker') is None:
        print('Error: You must have docker installed to run EXERT.')
        return

    run_command(f'docker pull {PANDA_CONTAINER}:latest')
    run_command(f'docker pull {XMAKE_CONTAINER}:latest')

    print('EXERT successfully initialized!')

# pylint: disable=unused-argument
def reset(parsed):
    run_and_output('docker stop pandare')

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
    mount = f'-v "{cwd}:/mount"'
    if name is None:
        run_command(f'docker run --rm -it {mount} {container} bash -c'
            f'"cd /mount; ./setup.sh; {command}"', False, False)
    else:
        if not container_is_running(name):
            run_command(f'docker run --rm -dit --name {name} {mount} {container}')
            run_command(f'docker exec -it {name} bash -c "cd /mount; ./setup.sh"')
        run_command(f'docker exec -it {name} bash -c "cd /mount; {command}"', False, False)
        if persist:
            run_command(f'docker exec -it {name} bash"')

def container_is_running(name):
    names = run_and_output('docker ps --format {{.Names}}').splitlines()
    try:
        names.index(name)
        return True
    except ValueError:
        return False

def run_and_output(command):
    return get_stdout(run_command(command, True))

def validate_initialized():
    # TODO: Test if initialized
    pass

# pylint: disable=unused-argument
def make_usermode(image):
    # TODO: Compile usermode for specific version
    pass

def validate_iso(image):
    try:
        with open(image,'rb') as fo:
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
                sys.exit(1)
    except FileNotFoundError:
        print(f'Could not find {image}.')
        sys.exit(1)
    except UnicodeDecodeError:
        print(f'The file {image} is not a valid kernel image.')
        sys.exit(1)

main()
