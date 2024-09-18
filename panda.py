#!/usr/bin/python3

from pandare import Panda
panda = Panda(
	generic='i386',
	extra_args = [])

def run_command(cmd):
	print("")
	print(f"Running '{cmd}'...")
	result = panda.run_serial_cmd(cmd, no_timeout = True)
	if result != '':
		print(result)
	return result

@panda.queue_blocking
def primary_callback():
	print("Converting to a snapshot...")
	panda.revert_sync("root")
	print("Copying /panda/panda/plugins/osi_linux/utils/kernelinfo")
	panda.copy_to_guest("/panda/panda/plugins/osi_linux/utils/kernelinfo")
	uname = run_command("uname -r")
	run_command("apt-get update")
	run_command(f"apt-get install -y build-essential linux-headers-{uname}")
	run_command("cd kernelinfo")
	run_command("make")
	run_command("insmod kernelinfo.ko")
	run_command("dmesg")
	panda.end_analysis()

panda.run()
