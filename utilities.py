"""Some useful utilities for the pyton scripts"""

import subprocess

def run_command(command):
    """Run a command in a forked child and return the stdout"""
    return subprocess.check_output(command, shell=True).decode()
