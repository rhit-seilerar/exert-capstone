# Day 1 (Introduction to PANDA)
#
# Template for exercise 2, parts 1-4.
#
# Exercise 2: Add some analysis to the script from Exercise 1 with a
# PANDA callback.
#
# Here, you will modify the script from exercise 1 to report whenever
# the guest ASID changes.

from pandare import Panda

panda = Panda(generic="x86_64")

# Control the guest
@panda.queue_blocking
def guest_driver():
    panda.revert_sync("root")
    print(panda.run_serial_cmd("cat /proc/cpuinfo"))
    panda.end_analysis()


# Part 1: Decorate this function so that it will be run whenever the
# guest ASID changes. Look through the callback list in PANDA's
# documentation at https://docs.panda.re/#pandare.Callbacks and find
# the one that will work here.
#
# Part 2: Rename the function and fix up its arguments
@panda.cb_asid_changed(your_fn) # pylint: disable=E1101,E0602
def your_fn(env, old_val, new_val):

    # Part 3: print the old asid and new asid in hexadecimal
    print(f"ASID has changed from {old_val:x} to {new_val:x}")

    # Part 4: Does the return value of this callback get used for something?
    # If so, what value should we return?
    return False


panda.run() # Start emulation
