import os
import sys
import glob
from pyclibrary import CParser
from exert.utilities.command import run_command

REPO_URL = 'git://git.kernel.org/pub/scm/linux/kernel/git/stable/linux-stable.git'
SOURCE_PATH = './cache/linux'
PARSE_CACHE = './cache/parsed'

def generate(version):
    switch_to_version(version)
    print(get_files())
    print('Parsing files...')
    if not os.path.exists(PARSE_CACHE):
        os.mkdir(PARSE_CACHE)
    parser = CParser(get_files(), cache = f'{PARSE_CACHE}/v{version}')
    parser.print_all()

def get_files():
    return glob.glob(f'{SOURCE_PATH}/include/linux/**/*.h', recursive = True)

def switch_to_version(version):
    if not os.path.exists(SOURCE_PATH):
        print('Cloning Linux...')
        run_command(f'git clone {REPO_URL} {SOURCE_PATH}', True, True)
    print(f'Checking out version {version}...')
    run_command(f'git checkout v{version}', True, True, './cache/linux')

if __name__ == '__main__':
    generate(sys.argv[1])
