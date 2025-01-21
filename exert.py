"""The black-box component to the EXERT system"""

import argparse
import os
import sys
import shutil
import time
from subprocess import CalledProcessError
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

    osi_parser = subparsers.add_parser('osi',
        help = 'Generate OSI information for the given kernel image')
    osi_parser.add_argument('image', nargs = '+',
        help = 'The kernel image to generate OSI information for.')
    osi_parser.set_defaults(func = osi)

    dev_parser = subparsers.add_parser('dev', help = 'Development tools')
    dev_subparsers = dev_parser.add_subparsers()

    dev_attach_parser = dev_subparsers.add_parser('attach',
        help='Attach a shell to the panda container')
    dev_attach_parser.add_argument('-r', '--reset', action='store_true',
        help='Reset the container first')
    dev_attach_parser.set_defaults(func = lambda parsed:
            dev_attach(parsed.docker, parsed.reset))

    dev_test_parser = dev_subparsers.add_parser('test',
        help='Run the unit tests for the EXERT system')
    dev_test_parser.add_argument('-r', '--reset', action='store_true',
        help='Reset the container first')
    dev_test_parser.set_defaults(func = lambda parsed:
            dev_test(parsed.docker, parsed.reset))

    compile_parser = dev_subparsers.add_parser('compile',
        help='Compile the usermode program')
    compile_parser.add_argument('arch', type=str)
    compile_parser.add_argument('libc', type=str)
    compile_parser.set_defaults(func = lambda args:
        make_usermode(args.arch, args.libc))

    dev_rules_parser = dev_subparsers.add_parser('rules',
        help='Generate a ruleset from a specified linux version')
    dev_rules_parser.add_argument('version', type=str,
        help='The version to generate the ruleset for. Format like 4.4.100.')
    dev_rules_parser.add_argument('-r', '--reset', action='store_true',
        help='Reset the container first')
    dev_rules_parser.set_defaults(func = lambda parsed:
            dev_rules(parsed.docker, parsed.version, parsed.reset))

    parsed = parser.parse_args()
    parsed.func(parsed)

def dev_reset():
    run_command('docker stop pandare', True, False)
    run_command('docker stop pandare-init', True, False)

def dev_attach(in_docker, reset):
    if in_docker:
        print("Cannot execute attach from within a container.")
        return
    if reset:
        dev_reset()
        time.sleep(1)
    sync_volume()
    run_docker(interactive = True, in_docker = in_docker)

def dev_test(in_docker, reset):
    if reset:
        if in_docker:
            print("Cannot reset from within a container. Command cancelled.")
            return
        dev_reset()
        time.sleep(1)
    sync_volume()
    run_docker(command = 'pytest --cov-config=.coveragerc --cov=exert tests/',
        in_docker = in_docker)

def dev_rules(in_docker, version, reset):
    if reset:
        if in_docker:
            print("Cannot reset from within a container. Command cancelled.")
            return
        dev_reset()
        time.sleep(1)
    sync_volume()
    run_docker(command = f'python -m exert.utilities.generator {version}',
        in_docker = in_docker)

# pylint: disable=unused-argument
def init(parsed):
    if parsed.docker:
        run_command('cd /mount; chmod +x ./setup.sh; ./setup.sh')
        return

    # Ensure docker exists
    print('Validating Docker...')
    if shutil.which('docker') is None:
        print('Error: You must have docker installed to run EXERT.')
        return

    # Ensure docker engine is running
    try:
        run_command('docker ps', True, True)
    except ValueError:
        print('Error: Please start the docker engine.')
        return

    print('Pulling containers...')
    run_command(f'docker pull {PANDA_CONTAINER}:latest')
    run_command(f'docker pull {XMAKE_CONTAINER}:latest')

    print('Copying local data to volume...')
    sync_volume()
    run_command('docker stop pandare-init')

    print('EXERT successfully initialized!')

def sync_volume():
    local_mount = f'-v "{os.path.dirname(os.path.realpath(__file__))}:/local"'
    exclude = '--exclude .git'

    ls_out = run_command('docker volume ls -q -f "name=pandare"', True, True)
    if 'pandare' not in get_stdout(ls_out).splitlines():
        run_command('docker volume create pandare', True, True)
    else:
        exclude += ' --exclude cache'

    if not container_is_running('pandare-init'):
        run_docker(name = 'pandare-init',
            command = 'apt-get update && apt-get install -y rsync',
            extra_args = local_mount)
    run_docker(name = 'pandare-init',
        command = f'rsync -av --progress {exclude} /local/ /mount')

def osi(parsed):
    """Validate the provided image, and then generate its OSI information"""
    validate_initialized()
    for image in parsed.image:
        validate_iso(image)
        make_usermode(image, 'musleabi')

    print('OSI not implemented.')

def run_docker(container = PANDA_CONTAINER, name = 'pandare', command = '',
    interactive = False, in_docker = False, extra_args = ''):
    try:
        validate_initialized()
        if in_docker:
            if command.startswith('docker'):
                print('This is only applicable without the -d argument.')
                return

            run_command(command, False, True)
            return

        mount = '-v "pandare:/mount"'
        name_arg = '' if name is None else f'--name {name}'
        args = f'--rm -it {name_arg} {mount} {extra_args} {container}'

        if name is None:
            run_command(f'docker run {args} bash -c "cd /mount; {command}"', False, False)
        else:
            if not container_is_running(name):
                run_command(f'docker run -d {args}')
                if name == 'pandare':
                    run_command(f'docker exec {name} bash -c '
                        '"cd /mount; chmod +x ./setup.sh; ./setup.sh"')
            run_command(f'docker exec {name} bash -c "cd /mount; {command}"', False, True)
            if interactive:
                run_command(f'docker exec -it {name} bash"')
    except CalledProcessError:
        print("Commands failed! Exiting.")
        sys.exit(-1)

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
    run_docker(XMAKE_CONTAINER, name = None,
        command=f'make -C /mount/exert/usermode ARCH={arch} LIBC={libc}')

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
