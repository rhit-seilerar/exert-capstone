# Day 1 (Introduction to PANDA)
#
# Template for exercise 3, parts 1-3.
#
# Exercise 3: Use an existing plugin to do a little RE
#
# Here, more things happen in the guest, including downloading some
# code and running it. Your job is to begin using PANDA to
# understand what happens.

from pandare import Panda
panda = Panda(generic="x86_64")

# Look how many things we can get the guest driver to do!
@panda.queue_blocking
def guest_driver():
    panda.revert_sync("root")
    cmds = ["rm /usr/bin/apt* /usr/bin/dpkg",
            "dhclient -v",
            "wget http://leet.mit.edu:9000/benew",
            "chmod +x benew",
            "./benew"]
    for cmd in cmds:
        print("cmd=[%s]" % cmd)
        print(panda.run_serial_cmd(cmd, no_timeout=True))

    panda.end_analysis()


# Part 1. Use the @panda.ppp decorator to register this function to run
# on the `on_rec_auxv` callback provided by the plugin `proc_start_linux`
# which corresponds to process start.
#
# Part 2. Read the documentation for `proc_start_linux` at
# https://github.com/panda-re/panda/tree/dev/panda/plugins/proc_start_linux
# to determine what arguments your `on_recv` callback should be called with
# and then fix the method def line.
@panda.ppp('PLUGIN_NAME', 'PLUGIN_CALLBACK_NAME')
def on_recv(cpu, ...):
    
    # Part 3. It's correct to assume that argc is the number of
    # arguments and argv is an array of argument values to the process
    # that just started. Modify the below code to print the value of
    # those arg strings. To convert a guest C-string to a python
    # string, you'll need to use the function
    # `panda.ffi.string(c_string)`
    for idx in range(auxv.argc):
        this_arg_cstring = auxv.argv[idx]
        this_arg = some_fn(this_arg_cstring)
        print(this_arg + " ", end="")
    print()


panda.run()

