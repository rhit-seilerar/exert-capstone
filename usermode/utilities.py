"""Some useful utilities for the pyton scripts"""

import subprocess
import sys

def run_command(command, capture_output=False):
    """Run a command in a forked child and return the stdout"""
    return subprocess.run(command, capture_output=capture_output, shell=True)
    
def run_commands(commands, capture_output=False):
    """Run a series of commands"""
    if capture_output:
        return run_command(';'.join(commands), True)
    for command in commands:
        run_command(command, False)

def get_stdout(result):
    return result.stdout.decode()

def get_stderr(result):
    return result.stderr.decode()
