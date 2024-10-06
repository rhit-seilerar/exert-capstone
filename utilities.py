"""Some useful utilities for the pyton scripts"""

import subprocess

def run_command(command):
    """Run a command in a forked child and return the stdout"""
    return subprocess.run(command, shell=True, executable="/bin/bash", capture_output=True)

def run_commands(commands):
    """Run a series of commands"""
    return run_command(";".join(commands))

def get_stdout(result):
    return result.stdout.decode()

def get_stderr(result):
    return result.stderr.decode()
