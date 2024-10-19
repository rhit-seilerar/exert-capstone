import subprocess
import os
import platform
import argparse


def main(cmd):
    print("test")
    commands = [cmd]
    docker = subprocess.getoutput('docker ps').splitlines()
    if(len(docker) > 1):
        print("Success! Docker is up; no further actions needed.")
    else:
        print("Docker needs to be started.")
        commands_linux = [
            'docker run --rm -dit --name pandare -v "$(realpath $(dirname $0)):/mount" pandare/panda',
        ];
        commands_windows = [
            'docker run --rm -dit --name pandare -v "%~dp0:/mount" pandare/pandadev',
        ];
        commands_common = [
            'docker exec -it pandare apt-get install -y vim gdb',
            'docker exec -it pandare bash'
         ];
    
        plat = platform.uname()
        if(plat.system == 'Linux'):
            commands = commands_linux + commands_common + commands
        elif(plat.system == 'Windowns'):
            commands = commands_windows + commands_common + commands
        else:
            print("Error: OS not supported.")
            return
        print("Docker container now online.")

    for x in commands:
        subprocess.Popen(x, shell=True)#, executable='/bin/bash')
    return

parser = argparse.ArgumentParser()
parser.add_argument("command",help="Command to execute in the Docker container")
args = parser.parse_args()
if(len(args.command) > 0):
    print("yay!")
    main(args.command)
