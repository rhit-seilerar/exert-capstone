"""The black-box component to the EXERT system"""

import argparse
import os
import sys
import shutil
import time
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

    dev_attach_parser = dev_subparsers.add_parser('attach', \
        help='Attach a shell to the panda container')
    dev_attach_parser.add_argument('-r', '--reset', action='store_true', \
        help='Reset the container first')
    dev_attach_parser.set_defaults(func = lambda parsed:
            dev_attach(parsed.docker, parsed.reset))

    dev_test_parser = dev_subparsers.add_parser('test', \
        help='Run the unit tests for the EXERT system')
    dev_test_parser.add_argument('-r', '--reset', action='store_true', \
        help='Reset the container first')
    dev_test_parser.set_defaults(func = lambda parsed:
            dev_test(parsed.docker, parsed.reset))

    compile_parser = dev_subparsers \
        .add_parser('compile', help='Compile the usermode program')
    compile_parser.add_argument('arch', type=str)
    compile_parser.add_argument('libc', type=str)
    compile_parser.set_defaults(func = lambda args:
        make_usermode(args.arch, args.libc))

    parsed = parser.parse_args()
    parsed.func(parsed)

def dev_reset():
    run_command('docker stop pandare', capture_output = True, check = False)

def dev_attach(in_docker, reset):
    if reset:
        dev_reset()
        time.sleep(1)
    run_docker(PANDA_CONTAINER, name = 'pandare', interactive = True, in_docker = in_docker)

def dev_test(in_docker, reset):
    if reset:
        dev_reset()
        time.sleep(1)
    run_docker(PANDA_CONTAINER, name = 'pandare', \
        command = 'pytest --cov-config=.coveragerc --cov=exert tests/', \
        in_docker = in_docker)

# pylint: disable=unused-argument
def init(parsed):
    if(parsed.docker):
        run_command("cd /mount; chmod +x ./setup.sh; ./setup.sh")
        return

    if shutil.which('docker') is None:
        print('Error: You must have docker installed to run EXERT.')
        return

    run_command(f'docker pull {PANDA_CONTAINER}:latest')
    run_command(f'docker pull {XMAKE_CONTAINER}:latest')

    print('EXERT successfully initialized!')

def osi(parsed):
    """Validate the provided image, and then generate its OSI information"""
    validate_initialized()
    for image in parsed.image:
        validate_iso(image)
        make_usermode(image, 'musleabi')

    print('OSI not implemented.')

def run_docker(container, name = None, command = '', interactive = False, in_docker = False):
    validate_initialized()
    if(in_docker):
        if(command.startswith('docker')):
            print('This is only applicable without the -d argument.')
            return

        run_command(command, False, True)
        return

    cwd = os.path.dirname(os.path.realpath(__file__))
    mount = f'-v "{cwd}:/mount"'

    privileged = '--privileged' if name == 'pandare' else ''

    if name is None:
        run_command(f'docker run --rm -it {mount} {container} bash -c'
            f'"cd /mount; {command}"', False, False)
    else:
        if not container_is_running(name):
            run_command(f'docker run --rm -dit {privileged} --name {name} {mount} {container}')
            run_command(f'docker exec {name} bash -c "cd /mount; chmod +x ./setup.sh; ./setup.sh"')
        run_command(f'docker exec {name} bash -c "cd /mount; {command}"', False, True)
        if interactive:
            run_command(f'docker exec -it {name} bash"')

def container_is_running(name):
    names = get_stdout(run_command('docker ps --format {{.Names}}', True)).splitlines()
    try:
        names.index(name)
        return True
    except ValueError:
        return False

def validate_initialized():
    # TODO: Test if initialized
    pass

def make_usermode(arch, libc):
    # TODO: Compile usermode for specific version
    run_docker(XMAKE_CONTAINER, command=f'make -C /mount/exert/usermode ARCH={arch} LIBC={libc}')

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
