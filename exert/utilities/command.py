"""Some useful command utilities for the pyton scripts"""
from typing import Any
import subprocess
import re

def run_command(command: str, capture_output: bool=False,
                check: bool=True, cwd=None):
    """Run a command in a forked child and return the stdout"""
    pattern = re.compile('("[^"]+"|[^\\s"]+)')
    args = [arg.replace('"', '') for arg in re.findall(pattern, command)]
    return subprocess.run(args, capture_output = capture_output, check = check, cwd = cwd)

def get_stdout(result:Any):
    return result.stdout.decode()

def get_stderr(result:Any):
    return result.stderr.decode()
