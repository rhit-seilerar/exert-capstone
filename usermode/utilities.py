"""Some useful utilities for the pyton scripts"""

import subprocess
import re

def run_command(command, capture_output=False):
    """Run a command in a forked child and return the stdout"""
    pattern = re.compile('("[^"]+"|[^\\s"]+)')
    args = re.findall(pattern, command)
    print(args)
    return subprocess.run(args, capture_output = capture_output, shell = True, check = False)

def run_commands(commands, capture_output=False):
    """Run a series of commands"""
    if capture_output:
        return run_command(';'.join(commands), True)
    for command in commands:
        run_command(command, False)
    return None

def get_stdout(result):
    return result.stdout.decode()

def get_stderr(result):
    return result.stderr.decode()
