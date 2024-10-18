import subprocess
import os

def main():
    print("test")
    
    commands = [
            'docker run --rm -dit --name pandare -v "$(realpath $(dirname $0)):/mount" pandare/panda',
            'docker exec -it pandare apt-get install -y vim gdb',
            'docker exec -it pandare bash'
        ];
    for x in commands:
        res = subprocess.run(x, shell=True, executable='/bin/bash')
        print(res.stdout)

main()
