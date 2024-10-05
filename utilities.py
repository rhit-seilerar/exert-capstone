import subprocess

def run_command(command):
	return subprocess.check_output(command, shell=True).decode()
