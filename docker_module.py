import subprocess
import os
import platform
import argparse
import utilities
panda_container_name = "pandare/panda"

def main(cmd):
    commands = ['docker exec -it pandare ' + cmd]
    docker = subprocess.getoutput('docker ps --format "{{.Image}}"')
    if(docker.find(panda_container_name) != -1):
        print("Docker container already running.")
    else:
        print("Docker needs to be started.")
        commands_linux = [
            'docker run --rm -dit --name pandare -v "$(realpath $(dirname $0)):/mount" pandare/panda',
        ];
        commands_windows = [
            'docker run --rm -dit --name pandare -v "%~dp0:/mount" pandare/pandadev',
        ];
        commands_common = [
            'docker exec -it pandare /mount/setup.sh',
            """'docker exec -it pandare apt-get install -y vim gdb cpio',
            'docker exec -it pandare pip install ipython',
            'docker exec -it pandare pip install pytest',
            
            #'docker exec -it pandare if [[ ! -d /mount/.panda ]]; then mkdir /mount/.panda; fi',
            #'docker exec -it pandare if [[ -L /root/.panda ]]; then rm /root/.panda; fi',
            #'docker exec -it pandare ln -sf /mount/.panda /root/.panda',
            #'docker exec -it pandare cd /mount',
            'docker exec -it pandare bash'"""
         ];
    
        plat = platform.uname()
        if(plat.system == 'Linux'):
            commands = commands_linux + commands_common + commands
        elif(plat.system == 'Windows'):
            commands = commands_windows + commands_common + commands
        else:
            print("Error: OS not supported.")
            return
    x = utilities.run_commands(commands)
    print(utilities.get_stdout(x))

    print("Command execution complete.")
    

parser = argparse.ArgumentParser()
parser.add_argument("command",help="Command to execute in the Docker container")
args = parser.parse_args()
if(len(args.command) > 0):
    main(args.command)
