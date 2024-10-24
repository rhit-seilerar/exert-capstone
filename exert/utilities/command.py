"""Some useful command utilities for the pyton scripts"""

import subprocess
import re

def run_command(command, capture_output=False, check=True):
    """Run a command in a forked child and return the stdout"""
    pattern = re.compile('("[^"]+"|[^\\s"]+)')
    args = [arg.replace('"', '') for arg in re.findall(pattern, command)]
    return subprocess.run(args, capture_output = capture_output, check = check)

def get_stdout(result):
    return result.stdout.decode()

def get_stderr(result):
    return result.stderr.decode()
