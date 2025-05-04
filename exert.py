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
def command_dict(command: str, capture_output: bool = False, check: bool = True):
    cd: dict[str, (str | bool)] = {'comm' : command, 'cap': capture_output, 'chk' : check}
    return cd

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
    osi_parser.add_argument('image_path')
    osi_parser.add_argument('image_arch')
    osi_parser.add_argument('image_version')
    osi_parser.set_defaults(func = osi)

    task_addr_parser = subparsers.add_parser('task_address',
        help='Get the task address for a given kernel')
    task_addr_parser.add_argument('kernel_path')
    task_addr_parser.add_argument('kernel_arch')
    task_addr_parser.add_argument('kernel_version')
    task_addr_parser.set_defaults(func = lambda parsed:
        get_task_address(parsed.kernel_path,
                         parsed.kernel_arch,
                         parsed.kernel_version,
                         parsed.docker))

    dev_parser = subparsers.add_parser('dev', help = 'Development tools')
    dev_subparsers = dev_parser.add_subparsers()

    dev_attach_parser = dev_subparsers.add_parser('attach',
        help='Attach a shell to the panda container')
    dev_attach_parser.add_argument('-r', '--reset', action='store_true',
        help='Reset the container first')
    dev_attach_parser.add_argument('-c', '--container', default='PANDA',
        help='Specify which Docker container to attach into')
    dev_attach_parser.set_defaults(func = lambda parsed:
            dev_rta(in_docker=parsed.docker, reset=parsed.reset,
                container=parsed.container, rta_mode=2))

    dev_test_parser = dev_subparsers.add_parser('test',
        help='Run the unit tests for the EXERT system')
    dev_test_parser.add_argument('-r', '--reset', action='store_true',
        help='Reset the container first')
    dev_test_parser.set_defaults(func = lambda parsed:
            dev_rta(in_docker=parsed.docker, reset=parsed.reset, rta_mode=1)
            )

    compile_parser = dev_subparsers.add_parser('compile',
        help='Compile the usermode program')
    compile_parser.set_defaults(func = lambda args:
        make_usermode())

    dev_rules_parser = dev_subparsers.add_parser('rules',
        help='Generate a ruleset from a specified linux version')
    dev_rules_parser.add_argument('version', type=str,
        help='The version to generate the ruleset for. Format like 4.4.100.')
    dev_rules_parser.add_argument('arch', type=str,
        help='The architecture to generate the ruleset for. Use names like x86, arm64, etc.')
    dev_rules_parser.add_argument('-r', '--reset', action='store_true',
        help='Reset the container first')
    dev_rules_parser.set_defaults(func = lambda parsed:
            dev_rta(in_docker=parsed.docker, reset=parsed.reset, version=parsed.version,
                arch=parsed.arch, rta_mode=0))

    parsed = parser.parse_args()
    parsed.func(parsed)

def dev_reset():
    run_command('docker stop pandare', True, False)
    run_command('docker stop pandare-init', True, False)
    volume_srd(2)

# Rules, Tests, Attach. 0,1,2 to determine if its a rules, tests, or attach.
# true if test, false if rules
def dev_rta(in_docker: bool, reset: bool, version: str=None,
            arch: str=None, container:str = None, rta_mode: int = 1):
    command = ''
    name = 'pandare'

    container = container or PANDA_CONTAINER
    if reset:
        if in_docker:
            print("Cannot reset from within a container. Command cancelled.")
            return
        dev_reset()
        time.sleep(1)
    if not in_docker:
        volume_srd(0)

    interactive = False
    if rta_mode == 1:
        make_usermode()
        command = 'pytest --cov-config=.coveragerc --cov=exert tests/'
    elif rta_mode == 0:
        command = f'python -u -m exert.parser.parser {version} {arch}'
    else:
        interactive = True
        if container == 'PANDA':
            print('Container is panda')
            container = PANDA_CONTAINER
        elif container == 'XMAKE':
            print('Container is xmake')
            name = 'XMAKE'
            container = XMAKE_CONTAINER
        else:
            print('Container not recognized, defaulting')
    run_docker(interactive = interactive, command = command, in_docker = in_docker,
        name = name, container=container)

    volume_srd(1)

# pylint: disable=unused-argument
def init(parsed:argparse.ArgumentParser):
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
    volume_srd(0)
    run_command('docker stop pandare-init')

    print('EXERT successfully initialized!')

# srd = Sync Reverse Delete. 0 = sync, 1 = reverse, 2 = delete
def volume_srd(srd: int =0):
    local_mount = f'-v "{os.path.dirname(os.path.realpath(__file__))}:/local"'
    exclude = '--exclude .git --exclude .venv'

    ls_out = run_command('docker volume ls -q -f "name=pandare"', True, True)
    if 'pandare' not in get_stdout(ls_out).splitlines():
        run_command('docker volume create pandare', True, True)
    else:
        if srd == 2:
            run_command('docker volume rm pandare', True, True)
            return
        exclude += ' --exclude cache'

    command = ''
    extra_args = ''
    if not container_is_running('pandare-init'):
        command = 'apt-get update && apt-get install -y rsync &&'
        extra_args = local_mount
    if srd == 1:
        command += f'rsync -auv --progress {exclude} /mount/ /local'
    else:
        command += f'rm -rf /mount/exert/ && rm -rf /mount/tests && rm -rf /mount/kernels/ \
            && rsync -auv --progress {exclude} /local/ /mount'
    run_docker(name = 'pandare-init', command = command,
               capture_output=False, extra_args=extra_args)

def osi(parsed:argparse.ArgumentParser):
    """Validate the provided image, and then generate its OSI information"""
    # init(parsed)
    path:str = parsed.image_path
    arch:str = parsed.image_arch
    version:str = parsed.image_version
    volume_srd(0)
    run_docker(command=f'python -m exert.osi_generator {path} {arch} {version}')

def run_docker(container:str = PANDA_CONTAINER, *, name: str = 'pandare', command: str = '',
    interactive: bool = False, in_docker: bool = False, extra_args: str = '',
    capture_output: bool = False):
    commands = []
    try:
        validate_initialized()
        if in_docker:
            if command.startswith('docker'):
                print('This is only applicable without the -d argument.')
                return
            run_command(command)
            return

        mount = '-v "pandare:/mount"'
        name_arg = '' if name is None else f'--name {name}'
        args = f'--rm -it {name_arg} {mount} {extra_args} {container}'

        env = ''

        if container == PANDA_CONTAINER:
            env = 'source /mount/.venv/bin/activate && '

        if name is None:
            commands.append(command_dict(f'docker run {args} bash -c "cd /mount; {command}"',
                capture_output, False))
        else:
            if not container_is_running(name):
                commands.append(command_dict(f'docker run -d {args}'))
                if name == 'pandare':
                    commands.append(command_dict(f'docker exec -t {name} bash -c '
                        '"cd /mount; chmod +x ./setup.sh; ./setup.sh"'))
            commands.append(
                command_dict(f'docker exec -t {name} bash -c "{env}cd /mount; {command}"',
                capture_output)
            )

            if interactive:
                commands.append(command_dict(f'docker exec -it {name} bash"'))
        for c in commands:
            run_command(c['comm'], capture_output=c['cap'], check=c['chk'])
    except CalledProcessError:
        print("Commands failed! Exiting.")
        sys.exit(-1)

def container_is_running(name: str):
    names = get_stdout(run_command('docker ps --format {{.Names}}', True)).splitlines()
    try:
        names.index(name)
        return True
    except ValueError:
        return False

def validate_initialized():
    # TODO: Test if initialized
    pass

def make_usermode():
    # TODO: Compile usermode for specific version
    run_docker(XMAKE_CONTAINER, name = None, command='make -C /mount/exert/usermode')

def validate_iso(image: str):
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
                if header_identifier != 'CD001' or header_version != 1:
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

def get_task_address(kernel_path: str, kernel_arch: str, kernel_version: str, in_docker: bool):
    command = f'python -u -m exert.usermode.plugin {kernel_path} {kernel_arch} {kernel_version}'
    #file needs to initiate a hypercall, but before that, plugin needs to intercept a hypercall
    if in_docker:
        run_command(command, True)
        return

    run_docker(command = command, in_docker = in_docker)

main()
