"""Some useful command utilities for the pyton scripts"""
from subprocess import CompletedProcess
from typing import Any
import subprocess
import re

def run_command(command: str, capture_output: bool=False,
                check: bool=True, cwd=None) -> CompletedProcess:
    """Run a command in a forked child and return the stdout"""
    pattern = re.compile('("[^"]+"|[^\\s"]+)')
    args = [arg.replace('"', '') for arg in re.findall(pattern, command)]
    return subprocess.run(args, capture_output = capture_output, check = check, cwd = cwd)

def get_stdout(result:Any)->str:
    return result.stdout.decode()

def get_stderr(result:Any)->str:
    return result.stderr.decode()
