# Day 1 (Introduction to PANDA)
#
# Template for exercise 1, parts 1 and 2.
#
# Exercise 1: Control the PANDA guest with a Python script.
#
# This script should run as-is and print out the result of the
# command `whoami` running in the guest.
#
# Part 1. Modify it to run the command `cat /proc/cpuinfo`
# inside the guest instead of `whoami` and print the result.
#
# Part 2. Try changing the string used by `Panda(generic=...)`
# to indicate an `arm` guest. And the re-run the script to see
# the output.

from pandare import Panda


# Create an instance of a panda object using one of our "generic" images.
# By selecting this we don't have to worry about configuring anything else
panda = Panda(generic="arm")


# Queue up a function to interact with the guest while the emulation is
# running. This function runs in a separate thread so it can use synchronous
# panda APIs such as `revert_sync` and `run_serial_cmd`.
@panda.queue_blocking
def guest_driver():
    # Revert the guest to a snapshot called "root" which we've already
    # created in this generic image
    panda.revert_sync("root")

    # Run a command inside the guest, wait for it to finish, then print
    # the output of the command
    print(panda.run_serial_cmd("cat /proc/cpuinfo"))

    # Stop the emulation
    panda.end_analysis()


# Now, after we've registered a blocking function, we start the emulation
panda.run()
