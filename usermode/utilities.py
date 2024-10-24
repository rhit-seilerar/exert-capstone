"""Some useful utilities for the pyton scripts"""

import subprocess
import re

def run_command(command, capture_output=False):
    """Run a command in a forked child and return the stdout"""
    pattern = re.compile('("[^"]+"|[^\\s"]+)')
    args = [arg.replace('"', '') for arg in re.findall(pattern, command)]
    return subprocess.run(args, capture_output = capture_output, check = False)

def get_stdout(result):
    return result.stdout.decode()

def get_stderr(result):
    return result.stderr.decode()
