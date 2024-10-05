"""Some useful utilities for the pyton scripts"""

import subprocess

def run_command(command):
    """Run a command in a forked child and return the stdout"""
    result = subprocess.run(command, shell=True, executable="/bin/bash", capture_output=True)
    return result.stdout.decode()

def run_commands(commands):
    """Run a series of commands"""
    return run_command(";".join(commands))
